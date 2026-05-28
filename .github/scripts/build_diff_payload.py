"""Build the JSON payload sent to GraphRAG-UI's /api/admin/update-graph.

Invoked from .github/workflows/update-graph.yml after a push to main:
reads BASE_SHA + HEAD_SHA from env, computes the .md diff, reads file
content for added+modified entries, and writes payload.json. Sets the
``skip`` step output to ``true`` when nothing ingestable changed so the
workflow can short-circuit before the network call.
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


def _git_diff_name_status(base: str, head: str) -> str:
    """Return the raw ``git diff --name-status`` output between two SHAs."""
    return subprocess.run(
        ["git", "diff", "--name-status", base, head],
        capture_output=True, text=True, check=True,
    ).stdout


def _read_at(head: str, path: str) -> str | None:
    """Read a file's content at a specific commit, regardless of what's
    currently checked out in the working tree.

    Uses ``git show <head>:<path>``, which pulls the blob from the
    object store. Reading from disk via ``pathlib`` would only work if
    the runner had already checked out ``head``; this is more robust
    and lets the script be exercised locally against historical
    commits without checking them out first. Returns None if the path
    doesn't exist at ``head`` (e.g. rare rename edge cases).
    """
    proc = subprocess.run(
        ["git", "show", f"{head}:{path}"],
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout


def _collect_md_changes(
    diff_output: str, head: str,
) -> tuple[dict[str, str], dict[str, str], list[str]]:
    """Parse ``git diff --name-status`` and bucket .md changes.

    Renames (``R``) are split into delete-old + add-new so the SDK
    re-extracts the content under the new path. Non-.md files are
    skipped. File content for added/modified entries is read from
    the git object store at ``head``, not from disk.
    """
    added: dict[str, str] = {}
    modified: dict[str, str] = {}
    deleted: list[str] = []

    for line in diff_output.splitlines():
        parts = line.split("\t")
        if not parts:
            continue
        status = parts[0][0]  # strip rename similarity score, e.g. R100 → R

        if status == "R" and len(parts) >= 3:
            old, new = parts[1], parts[2]
            if old.endswith(".md"):
                deleted.append(old)
            if new.endswith(".md"):
                content = _read_at(head, new)
                if content is not None:
                    added[new] = content
            continue

        if len(parts) < 2 or not parts[1].endswith(".md"):
            continue
        path = parts[1]
        if status == "A":
            content = _read_at(head, path)
            if content is not None:
                added[path] = content
        elif status == "M":
            content = _read_at(head, path)
            if content is not None:
                modified[path] = content
        elif status == "D":
            deleted.append(path)

    return added, modified, deleted


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
        base = EMPTY_TREE_SHA

    diff = _git_diff_name_status(base, head)
    added, modified, deleted = _collect_md_changes(diff, head)

    if not (added or modified or deleted):
        print("::notice::No .md changes — skipping graph update.", file=sys.stderr)
        _set_output("skip", "true")
        return 0

    payload = {
        "graph_id": os.environ.get("GRAPH_ID", "docs_benchmark"),
        "files": {"added": added, "modified": modified, "deleted": deleted},
    }
    pathlib.Path("payload.json").write_text(json.dumps(payload), encoding="utf-8")
    print(f"::notice::Diff: +{len(added)} ~{len(modified)} -{len(deleted)} files")
    _set_output("skip", "false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
