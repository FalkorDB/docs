"""Build the JSON payload sent to GraphRAG-UI's /api/admin/update-graph.

Invoked from .github/workflows/update-graph.yml after a push to main:
reads BASE_SHA + HEAD_SHA from env, computes the ingestable diff, reads
file content for added+modified entries, and writes payload.json. Sets the
``skip`` step output to ``true`` when nothing ingestable changed so the
workflow can short-circuit before the network call.

Two extension sets, not one. ``INGEST_SUFFIXES`` is what the graph ingests
today; ``TRACKED_SUFFIXES`` is everything that might already exist in the
graph as a document. The Mintlify migration (#544) moved 151 files from
``.md`` to ``.mdx`` while this script tested a single suffix on both sides
of a rename, so every delete-half silently vanished: the payload read
``+190 ~0 -0`` and the 202 pre-migration documents are still in the live
graph with no way for any future push to evict them. A rename *out of* the
tracked set is a deletion even when the destination is not ingestable.

Nothing here silently drops a file any more. An unreadable blob, an
unreachable base commit, or an oversized payload fails the step with an
actionable message, because a partial payload publishes as a success and
the loss is only visible much later, in retrieval.
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys

# git's well-known empty-tree SHA — used as the "before" when a push
# carries an all-zero ``before`` (i.e., first push to a brand-new branch).
EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

# Suffixes whose *content* the graph ingests. Added/modified files outside
# this set are not sent at all.
INGEST_SUFFIXES = (".mdx",)

# Suffixes that may exist as a :Document in the graph, so a deletion or a
# rename-away has to be reported. Superset of INGEST_SUFFIXES: `.md` files
# were ingested for the three months before the Mintlify migration.
TRACKED_SUFFIXES = (".md", ".mdx")

# The whole payload is one request body with every changed file's content
# inline. 190 files came to 1.1 MB; this cap exists so a pathological diff
# fails here, with a number, instead of as an opaque proxy error after the
# upload has already run for minutes.
MAX_PAYLOAD_BYTES = 25 * 1024 * 1024


def _log(kind: str, message: str) -> None:
    """Emit a GitHub Actions annotation on stderr."""
    print(f"::{kind}::{message}", file=sys.stderr)


def _is_ingestable(path: str) -> bool:
    return path.endswith(INGEST_SUFFIXES)


def _is_tracked(path: str) -> bool:
    return path.endswith(TRACKED_SUFFIXES)


def _commit_exists(sha: str) -> bool:
    """True when ``sha`` names a commit object present in this clone.

    ``github.event.before`` points at whatever main used to be, and after a
    force-push or a history rewrite that commit may not exist any more.
    Without this check ``git diff`` exits non-zero and the step dies on a
    raw CalledProcessError traceback.
    """
    proc = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        capture_output=True, text=True, check=False,
    )
    return proc.returncode == 0


def _git_diff_name_status(base: str, head: str) -> str:
    """Return the raw ``git diff --name-status`` output between two SHAs."""
    return subprocess.run(
        ["git", "diff", "--name-status", base, head],
        capture_output=True, text=True, check=True,
    ).stdout


def _ingestable_paths_at(head: str) -> list[str]:
    """Every ingestable path in the tree at ``head``.

    Sent alongside the diff as a manifest so the server can reconcile the
    graph's document set against what the repo actually contains. A
    diff-only protocol cannot repair a deletion it never heard about — and
    it has already had to.
    """
    out = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", head],
        capture_output=True, text=True, check=True,
    ).stdout
    return sorted(p for p in out.splitlines() if _is_ingestable(p))


def _read_at(head: str, path: str) -> str | None:
    """Read a file's content at a specific commit, regardless of what's
    currently checked out in the working tree.

    Uses ``git show <head>:<path>``, which pulls the blob from the
    object store. Reading from disk via ``pathlib`` would only work if
    the runner had already checked out ``head``; this is more robust
    and lets the script be exercised locally against historical
    commits without checking them out first. Returns None when the blob
    is missing, which the caller treats as fatal.
    """
    proc = subprocess.run(
        ["git", "show", f"{head}:{path}"],
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def _collect_changes(
    diff_output: str, head: str,
) -> tuple[dict[str, str], dict[str, str], list[str], list[str]]:
    """Parse ``git diff --name-status`` and bucket the changes.

    Returns ``(added, modified, deleted, unreadable)``. Renames and copies
    carry two paths; every other status carries one. ``unreadable`` names
    the paths whose blob could not be read — the caller fails on those
    rather than shipping a payload that is quietly missing a document.
    """
    added: dict[str, str] = {}
    modified: dict[str, str] = {}
    deleted: list[str] = []
    unreadable: list[str] = []

    def _take(path: str, bucket: dict[str, str]) -> None:
        content = _read_at(head, path)
        if content is None:
            unreadable.append(path)
            return
        bucket[path] = content

    for line in diff_output.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0][0]  # strip rename/copy similarity score, e.g. R100 → R

        # R (rename) and C (copy) name a source and a destination. A rename
        # moves the document: the old path is gone from the graph and the
        # new one has to be extracted fresh. A copy leaves the source in
        # place, so only the destination is new.
        if status in ("R", "C") and len(parts) >= 3:
            old, new = parts[1], parts[2]
            if status == "R" and _is_tracked(old):
                deleted.append(old)
            if _is_ingestable(new):
                _take(new, added)
            continue

        path = parts[1]
        if status == "D":
            # Deletions use the tracked set, not the ingestable one: a
            # pre-migration .md document still needs evicting.
            if _is_tracked(path):
                deleted.append(path)
        elif status == "A":
            if _is_ingestable(path):
                _take(path, added)
        elif status in ("M", "T"):
            # T is a typechange (symlink ↔ regular file). The content at
            # head is what matters either way.
            if _is_ingestable(path):
                _take(path, modified)
        elif status == "U":
            # Unmerged paths mean the runner is looking at a conflicted
            # tree, which should never reach a push to main.
            _log("warning", f"Ignoring unmerged path: {path}")

    return added, modified, deleted, unreadable


def _set_output(name: str, value: str) -> None:
    """Append to GITHUB_OUTPUT so subsequent steps can branch on it."""
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:  # local dev / standalone run
        return
    with open(out, "a", encoding="utf-8") as f:
        f.write(f"{name}={value}\n")


def main() -> int:
    base = os.environ["BASE_SHA"]
    head = os.environ["HEAD_SHA"]

    if set(base) == {"0"}:
        # First push to a brand-new branch: everything in the tree is new.
        base = EMPTY_TREE_SHA
    elif not _commit_exists(base):
        _log(
            "error",
            f"Base commit {base} is not in this clone — main was probably "
            "force-pushed. Refusing to guess a diff: re-run the workflow "
            "with a base that exists, or reconcile the graph with a full "
            "rebuild.",
        )
        return 1

    diff = _git_diff_name_status(base, head)
    added, modified, deleted, unreadable = _collect_changes(diff, head)

    if unreadable:
        shown = ", ".join(unreadable[:10])
        _log(
            "error",
            f"Could not read {len(unreadable)} file(s) at {head}: {shown}. "
            "Refusing to send a payload that is missing documents — the run "
            "would report success and the graph would silently lack them.",
        )
        return 1

    if not (added or modified or deleted):
        _log("notice", "No ingestable changes — skipping graph update.")
        _set_output("skip", "true")
        return 0

    manifest = _ingestable_paths_at(head)
    payload = {
        "graph_id": os.environ.get("GRAPH_ID", "docs_benchmark"),
        "head_sha": head,
        "files": {"added": added, "modified": modified, "deleted": deleted},
        # Full ingestable inventory at head. Servers that predate manifest
        # support ignore the field; ones that support it reconcile against
        # it, which is what makes a missed deletion recoverable.
        "manifest": manifest,
    }

    body = json.dumps(payload)
    size = len(body.encode("utf-8"))
    if size > MAX_PAYLOAD_BYTES:
        _log(
            "error",
            f"Payload is {size} bytes, over the {MAX_PAYLOAD_BYTES} byte cap. "
            "Split the change across pushes or move to a content-by-reference "
            "payload.",
        )
        return 1

    pathlib.Path("payload.json").write_text(body, encoding="utf-8")
    _log(
        "notice",
        f"Diff: +{len(added)} ~{len(modified)} -{len(deleted)} files; "
        f"manifest {len(manifest)} files; payload {size} bytes",
    )
    _set_output("skip", "false")
    _set_output("added", str(len(added)))
    _set_output("modified", str(len(modified)))
    _set_output("deleted", str(len(deleted)))
    _set_output("manifest", str(len(manifest)))
    _set_output("bytes", str(size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
