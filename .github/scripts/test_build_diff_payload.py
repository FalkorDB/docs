"""Tests for build_diff_payload.py.

The bug that motivated these: a rename from ``.md`` to ``.mdx`` reported the
addition and dropped the deletion, so 202 pre-migration documents are still
in the live docs graph. ``test_a_rename_out_of_md_reports_both_halves`` is
that exact case and fails against the pre-fix script.

Status parsing is tested against synthetic ``git diff --name-status`` text —
statuses like C (copy) and T (typechange) are impractical to provoke
reliably from a real repo. Everything that involves git itself (base
resolution, the manifest, end-to-end payload shape) runs against a real
temporary repository.

Run: pytest .github/scripts/test_build_diff_payload.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

import build_diff_payload as bdp  # noqa: E402


# ── helpers ─────────────────────────────────────────────────────────────────

def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True,
    ).stdout.strip()


def _commit(repo: Path, message: str) -> str:
    _git(repo, "add", "-A")
    _git(repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-m", message)
    return _git(repo, "rev-parse", "HEAD")


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """A git repo with one committed .md page and one .mdx page."""
    r = tmp_path / "docs"
    r.mkdir()
    _git(r, "init", "-q", "-b", "main")
    (r / "guides").mkdir()
    (r / "guides" / "intro.md").write_text("intro body\n", encoding="utf-8")
    (r / "guides" / "already.mdx").write_text("already mdx\n", encoding="utf-8")
    (r / "logo.png").write_bytes(b"\x89PNG\r\n")
    _commit(r, "initial")
    return r


@pytest.fixture()
def run_main(monkeypatch, tmp_path):
    """Call ``main()`` inside ``repo`` and return (exit_code, payload, outputs)."""
    def _run(repo: Path, base: str, head: str) -> tuple[int, dict | None, dict]:
        out_file = tmp_path / "gh_output"
        out_file.write_text("", encoding="utf-8")
        monkeypatch.chdir(repo)
        monkeypatch.setenv("BASE_SHA", base)
        monkeypatch.setenv("HEAD_SHA", head)
        monkeypatch.setenv("GITHUB_OUTPUT", str(out_file))
        monkeypatch.setenv("GRAPH_ID", "docs_benchmark")

        code = bdp.main()

        outputs = dict(
            line.split("=", 1)
            for line in out_file.read_text(encoding="utf-8").splitlines()
            if "=" in line
        )
        payload_path = repo / "payload.json"
        payload = (
            json.loads(payload_path.read_text(encoding="utf-8"))
            if payload_path.exists()
            else None
        )
        return code, payload, outputs

    return _run


@pytest.fixture()
def parse(monkeypatch):
    """Parse synthetic name-status text with blob reads stubbed out."""
    monkeypatch.setattr(bdp, "_read_at", lambda head, path: f"body of {path}")

    def _parse(*lines: str):
        return bdp._collect_changes("\n".join(lines), "HEAD")

    return _parse


# ── the regression that cost 202 documents ──────────────────────────────────

def test_a_rename_out_of_md_reports_both_halves(parse):
    added, modified, deleted, unreadable = parse("R091\tguides/intro.md\tguides/intro.mdx")

    assert list(added) == ["guides/intro.mdx"], "new path must be ingested"
    assert deleted == ["guides/intro.md"], (
        "the old .md document must be evicted — dropping this half is what "
        "left 202 stale documents in the live graph"
    )
    assert not modified and not unreadable


def test_a_rename_out_of_the_tracked_set_still_deletes(parse):
    """Renamed to something the graph does not ingest: pure eviction."""
    added, _, deleted, _ = parse("R100\tguides/intro.mdx\tsnippets/intro.txt")

    assert deleted == ["guides/intro.mdx"]
    assert added == {}


def test_a_plain_md_deletion_is_reported(parse):
    _, _, deleted, _ = parse("D\tReferences/license.md")

    assert deleted == ["References/license.md"]


def test_an_md_addition_is_not_ingested(parse):
    """`.md` is tracked for deletion but is no longer ingested content."""
    added, modified, deleted, _ = parse("A\tAGENTS.md", "M\tREADME.md")

    assert added == {} and modified == {} and deleted == []


# ── status coverage ─────────────────────────────────────────────────────────

def test_a_copy_adds_the_destination_and_keeps_the_source(parse):
    added, _, deleted, _ = parse("C075\tguides/intro.mdx\tguides/intro-copy.mdx")

    assert list(added) == ["guides/intro-copy.mdx"]
    assert deleted == [], "a copy leaves the source in place"


def test_a_typechange_counts_as_modified(parse):
    _, modified, _, _ = parse("T\tguides/intro.mdx")

    assert list(modified) == ["guides/intro.mdx"]


def test_non_document_files_are_ignored(parse):
    added, modified, deleted, _ = parse(
        "A\tlogo.png", "M\tdocs.json", "D\t_includes/head.html",
    )

    assert added == {} and modified == {} and deleted == []


def test_an_unreadable_blob_is_collected_not_skipped(monkeypatch):
    monkeypatch.setattr(bdp, "_read_at", lambda head, path: None)

    added, _, _, unreadable = bdp._collect_changes("A\tguides/new.mdx", "HEAD")

    assert added == {}, "a file that cannot be read must not look ingested"
    assert unreadable == ["guides/new.mdx"]


# ── main(): base resolution and failure surfaces ────────────────────────────

def test_the_migration_shape_end_to_end(repo, run_main):
    """Rename .md → .mdx plus a fresh page: the #544 diff in miniature."""
    base = _git(repo, "rev-parse", "HEAD")
    _git(repo, "mv", "guides/intro.md", "guides/intro.mdx")
    (repo / "guides" / "new.mdx").write_text("brand new\n", encoding="utf-8")
    head = _commit(repo, "migrate to mdx")

    code, payload, outputs = run_main(repo, base, head)

    assert code == 0
    assert sorted(payload["files"]["added"]) == ["guides/intro.mdx", "guides/new.mdx"]
    assert payload["files"]["deleted"] == ["guides/intro.md"]
    assert payload["files"]["added"]["guides/new.mdx"] == "brand new\n"
    assert outputs["skip"] == "false"
    assert outputs["deleted"] == "1"


def test_the_payload_carries_a_full_manifest(repo, run_main):
    base = _git(repo, "rev-parse", "HEAD")
    (repo / "guides" / "new.mdx").write_text("brand new\n", encoding="utf-8")
    head = _commit(repo, "add a page")

    _, payload, outputs = run_main(repo, base, head)

    assert payload["manifest"] == [
        "guides/already.mdx", "guides/new.mdx",
    ], "every ingestable path at head, not just the changed ones"
    assert payload["head_sha"] == head
    assert outputs["manifest"] == "2"


def test_an_unreachable_base_fails_instead_of_crashing(repo, run_main):
    """Force-push case: the old main tip is no longer in the clone."""
    head = _git(repo, "rev-parse", "HEAD")
    missing = "0" * 39 + "1"  # well-formed, not an object

    code, payload, outputs = run_main(repo, missing, head)

    assert code == 1
    assert payload is None, "no payload may be written from a guessed diff"
    assert outputs == {}


def test_an_all_zero_base_diffs_against_the_empty_tree(repo, run_main):
    head = _git(repo, "rev-parse", "HEAD")

    code, payload, _ = run_main(repo, "0" * 40, head)

    assert code == 0
    assert sorted(payload["files"]["added"]) == ["guides/already.mdx"]


def test_nothing_ingestable_sets_skip(repo, run_main):
    base = _git(repo, "rev-parse", "HEAD")
    (repo / "logo.png").write_bytes(b"\x89PNG\r\n\x00")
    head = _commit(repo, "touch an image")

    code, payload, outputs = run_main(repo, base, head)

    assert code == 0
    assert payload is None
    assert outputs["skip"] == "true"


def test_an_unreadable_file_fails_the_step(repo, run_main, monkeypatch):
    base = _git(repo, "rev-parse", "HEAD")
    (repo / "guides" / "new.mdx").write_text("brand new\n", encoding="utf-8")
    head = _commit(repo, "add a page")
    monkeypatch.setattr(bdp, "_read_at", lambda h, p: None)

    code, payload, outputs = run_main(repo, base, head)

    assert code == 1
    assert payload is None
    assert outputs == {}


def test_an_oversized_payload_fails_the_step(repo, run_main, monkeypatch):
    base = _git(repo, "rev-parse", "HEAD")
    (repo / "guides" / "big.mdx").write_text("x" * 4096, encoding="utf-8")
    head = _commit(repo, "add a big page")
    monkeypatch.setattr(bdp, "MAX_PAYLOAD_BYTES", 512)

    code, payload, _ = run_main(repo, base, head)

    assert code == 1
    assert payload is None, "an oversized payload must not be written"
