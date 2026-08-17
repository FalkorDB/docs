#!/usr/bin/env python3
"""Aggregate the FalkorDB documentation repositories into a single Mintlify site.

Every FalkorDB docs repository declares the same `navigation.products` list and
populates exactly one entry — its own product — while linking to the others with
an `href`. This script uses that convention to build one deployment:

    for each source repo:
        clone it, copy its content under ./<mount>/,
        take its own product entry, prefix every path in it with <mount>/,
        and substitute it for the `href` placeholder in this repo's docs.json

The result is a single Mintlify site, so search and the AI assistant index all
products together instead of one deployment per product.

Usage:
    python3 scripts/aggregate_docs.py --output build
    python3 scripts/aggregate_docs.py --output build --use-local ..
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Files and directories that are tooling rather than documentation.
BASE_EXCLUDES = (
    ".git",
    ".github",
    ".mintignore",
    "node_modules",
    "scripts",
    "AGENTS.md",
    "README.md",
    "CNAME",
    "existing_routes.txt",
)
SOURCE_EXCLUDES = BASE_EXCLUDES + (
    "docs.json",
    "snippets",  # hoisted to the site root instead, see mount_snippets()
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
)

# The canonical URL of this repository's own site. Source repos link to it
# absolutely; once they are part of this deployment those links become internal.
BASE_SITE = "https://docs.falkordb.com"

# Endpoint entries inside an OpenAPI-backed group are operation references, not
# page paths, and must not be prefixed.
HTTP_METHOD = re.compile(r"^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS|TRACE)\s")

# An absolute path used as a link target, image source or import specifier.
ABSOLUTE_PATH = re.compile(r"""(?<=[("'])(/[^\s"'()<>]*)""")


def log(message: str) -> None:
    print(message, flush=True)


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


# --------------------------------------------------------------------------- #
# navigation rewriting
# --------------------------------------------------------------------------- #


def mount_path(path: str, mount: str) -> str:
    return f"{mount}/{path.lstrip('/')}"


def rewrite_openapi(value, mount: str):
    if isinstance(value, str):
        return f"/{mount_path(value, mount)}" if value.startswith("/") else value
    if isinstance(value, dict):
        out = dict(value)
        for key in ("source", "directory"):
            raw = out.get(key)
            if isinstance(raw, str) and not raw.startswith("http"):
                prefixed = mount_path(raw, mount)
                out[key] = f"/{prefixed}" if raw.startswith("/") else prefixed
        return out
    return value


def rewrite_navigation(node, mount: str):
    """Prefix every page, root, openapi and internal href path with the mount."""
    if isinstance(node, list):
        return [rewrite_navigation(item, mount) for item in node]
    if not isinstance(node, dict):
        return node

    out = {}
    for key, value in node.items():
        if key == "pages" and isinstance(value, list):
            out[key] = [
                item
                if isinstance(item, str) and HTTP_METHOD.match(item)
                else mount_path(item, mount)
                if isinstance(item, str)
                else rewrite_navigation(item, mount)
                for item in value
            ]
        elif key == "root" and isinstance(value, str):
            out[key] = mount_path(value, mount)
        elif key == "href" and isinstance(value, str) and value.startswith("/"):
            out[key] = f"/{mount_path(value, mount)}"
        elif key == "openapi":
            out[key] = rewrite_openapi(value, mount)
        else:
            out[key] = rewrite_navigation(value, mount)
    return out


def own_product(config: dict, product: str, label: str) -> dict:
    """Return the product entry a source repo populates for itself."""
    products = config.get("navigation", {}).get("products")
    if not products:
        fail(f"{label}: docs.json has no navigation.products")

    for entry in products:
        if entry.get("product") == product:
            if "href" in entry:
                fail(
                    f"{label}: product {product!r} is still an href placeholder — "
                    "the source repo must populate its own product"
                )
            return entry

    known = ", ".join(repr(e.get("product")) for e in products)
    fail(f"{label}: no product {product!r} in navigation.products (found {known})")


# --------------------------------------------------------------------------- #
# content mounting
# --------------------------------------------------------------------------- #


def copy_tree(src: Path, dest: Path, excludes: tuple[str, ...]) -> None:
    shutil.copytree(
        src,
        dest,
        ignore=shutil.ignore_patterns(*excludes),
        dirs_exist_ok=True,
        symlinks=False,
    )


def addressable_paths(root: Path, extra: set[str]) -> set[str]:
    """Every absolute path a repo can legitimately link to before it is mounted."""
    known = set(extra)
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative.endswith(".mdx"):
            route = "/" + relative[: -len(".mdx")]
            known.add(route)
            if route.endswith("/index"):
                known.add(route[: -len("/index")] or "/")
        else:
            known.add("/" + relative)
    return known


def rewrite_internal_links(root: Path, mount: str, known: set[str]) -> int:
    """Repoint a repo's own absolute links, assets and snippets at the mount.

    Only paths the source repo actually owns are rewritten, so links to other
    products and to external sites are left alone.
    """
    snippets = re.compile(r"""(?<=["'(])/snippets/""")

    def replace(match: re.Match) -> str:
        raw = match.group(1)
        path = raw.split("#")[0].split("?")[0]
        path = path.rstrip("/") or "/"
        if path not in known:
            return raw
        return f"/{mount}" if raw == "/" else f"/{mount}{raw}"

    changed = 0
    for path in root.rglob("*.mdx"):
        text = path.read_text(encoding="utf-8")
        rewritten = ABSOLUTE_PATH.sub(replace, text)
        rewritten = snippets.sub(f"/snippets/{mount}/", rewritten)
        if rewritten != text:
            path.write_text(rewritten, encoding="utf-8")
            changed += 1
    return changed


def mount_snippets(src: Path, output: Path, mount: str) -> None:
    """Mintlify only resolves snippets under the site root, so namespace them there."""
    snippets = src / "snippets"
    if not snippets.is_dir():
        return
    dest = output / "snippets" / mount
    if dest.exists():
        fail(f"snippet namespace {dest} already exists")
    copy_tree(snippets, dest, (".git",))


def mintignore_rules(src: Path, mount: str) -> list[str]:
    """Translate a repo's .mintignore rules so they still apply under its mount."""
    path = src / ".mintignore"
    if not path.is_file():
        return []

    rules = []
    for line in path.read_text(encoding="utf-8").splitlines():
        rule = line.strip()
        if not rule or rule.startswith("#"):
            continue
        if not mount:
            rules.append(rule)
        elif "/" in rule.rstrip("/"):
            rules.append(f"{mount}/{rule.lstrip('/')}")
        else:
            # A bare name matches at any depth, so keep it recursive.
            rules.append(f"{mount}/**/{rule}")
    return rules


def navigation_routes(node, found: set[str]) -> set[str]:
    """Collect declared page routes, including ones generated from an OpenAPI spec."""
    if isinstance(node, list):
        for item in node:
            navigation_routes(item, found)
    elif isinstance(node, dict):
        for key, value in node.items():
            if key == "pages" and isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        if not HTTP_METHOD.match(item):
                            found.add("/" + item.lstrip("/"))
                    else:
                        navigation_routes(item, found)
            elif key == "root" and isinstance(value, str):
                found.add("/" + value.lstrip("/"))
            else:
                navigation_routes(value, found)
    return found


def mount_source(src: Path, output: Path, mount: str, entry: dict) -> None:
    dest = output / mount
    if dest.exists():
        fail(f"mount point {mount!r} collides with existing content in the base repo")
    copy_tree(src, dest, SOURCE_EXCLUDES)
    mount_snippets(src, output, mount)
    known = addressable_paths(dest, navigation_routes(entry, set()))
    changed = rewrite_internal_links(dest, mount, known)
    pages = sum(1 for _ in dest.rglob("*.mdx"))
    log(f"  mounted {pages} pages at /{mount} ({changed} with rewritten links)")


def internalize_site_links(output: Path, sites: dict[str, str]) -> int:
    """Turn absolute links between the product sites into links within this one."""
    pattern = re.compile(
        "(" + "|".join(re.escape(site) for site in sites) + r")(?=[/\s\)\"'#]|$)"
    )
    def replace(match: re.Match) -> str:
        mount = sites[match.group(1)]
        if mount:
            return f"/{mount}"
        # The base site is the root, so let a following path stand on its own.
        return "" if match.string[match.end() : match.end() + 1] == "/" else "/"

    changed = 0
    for path in output.rglob("*.mdx"):
        text = path.read_text(encoding="utf-8")
        rewritten = pattern.sub(replace, text)
        if rewritten != text:
            path.write_text(rewritten, encoding="utf-8")
            changed += 1
    return changed


# --------------------------------------------------------------------------- #
# redirects
# --------------------------------------------------------------------------- #


def internalize_redirects(redirects: list[dict], sites: dict[str, str]) -> list[dict]:
    """Point redirects at the mounted content instead of the standalone sites.

    The base repo keeps absolute URLs so it still validates on its own; once a
    product is part of this deployment those destinations become internal paths.
    Redirects that collapse onto their own source are dropped, since Mintlify
    resolves redirects before pages and a self-redirect would loop.
    """
    out = []
    for entry in redirects:
        destination = entry["destination"]
        for site, mount in sites.items():
            if destination == site or destination.startswith(site + "/"):
                tail = destination[len(site) :].lstrip("/")
                destination = f"/{mount}/{tail}" if tail else f"/{mount}"
                break
        if destination == entry["source"]:
            continue
        out.append({**entry, "destination": destination})
    return out


# --------------------------------------------------------------------------- #
# sources
# --------------------------------------------------------------------------- #


def resolve_source(source: dict, workdir: Path, use_local: Path | None) -> Path:
    owner, repo = source["owner"], source["repo"]
    subdirectory = source.get("subdirectory", ".")

    if use_local:
        checkout = use_local / repo
        if not checkout.is_dir():
            fail(f"{owner}/{repo}: no local checkout at {checkout}")
        log(f"  using local checkout {checkout}")
    else:
        checkout = workdir / repo
        token = os.environ.get("DOCS_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
        credentials = f"x-access-token:{token}@" if token else ""
        url = f"https://{credentials}github.com/{owner}/{repo}.git"
        log(f"  cloning {owner}/{repo}@{source.get('ref', 'main')}")
        subprocess.run(
            ["git", "clone", "--depth", "1", "--branch", source.get("ref", "main"),
             url, str(checkout)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=None,
        )

    docs = (checkout / subdirectory).resolve()
    if not (docs / "docs.json").is_file():
        fail(f"{owner}/{repo}: no docs.json at {subdirectory}")
    return docs


# --------------------------------------------------------------------------- #


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="build", help="directory to build the site into")
    parser.add_argument("--sources", default=str(REPO_ROOT / "scripts" / "sources.json"))
    parser.add_argument(
        "--use-local",
        metavar="DIR",
        help="use sibling checkouts in DIR instead of cloning (for local testing)",
    )
    args = parser.parse_args()

    output = Path(args.output).resolve()
    if output == REPO_ROOT:
        fail("--output must not be the repository root")
    if output.exists():
        shutil.rmtree(output)

    sources = json.loads(Path(args.sources).read_text(encoding="utf-8"))
    config = json.loads((REPO_ROOT / "docs.json").read_text(encoding="utf-8"))
    products = config.get("navigation", {}).get("products")
    if not products:
        fail("docs.json has no navigation.products")

    log(f"base: copying {REPO_ROOT.name} to {output}")
    copy_tree(REPO_ROOT, output, BASE_EXCLUDES)

    use_local = Path(args.use_local).resolve() if args.use_local else None
    sites: dict[str, str] = {}
    ignores = mintignore_rules(REPO_ROOT, "")

    with tempfile.TemporaryDirectory() as tmp:
        for source in sources:
            product, mount = source["product"], source["mount"]
            log(f"{product}:")

            docs = resolve_source(source, Path(tmp), use_local)
            source_config = json.loads((docs / "docs.json").read_text(encoding="utf-8"))
            entry = own_product(source_config, product, f"{source['owner']}/{source['repo']}")

            index = next(
                (i for i, p in enumerate(products) if p.get("product") == product), None
            )
            if index is None:
                fail(f"docs.json has no product {product!r} to replace")
            if "href" not in products[index]:
                fail(f"docs.json product {product!r} is already populated")

            mount_source(docs, output, mount, entry)
            products[index] = rewrite_navigation(entry, mount)
            ignores += mintignore_rules(docs, mount)
            if source.get("site"):
                sites[source["site"].rstrip("/")] = mount

    (output / ".mintignore").write_text("\n".join(ignores) + "\n", encoding="utf-8")

    changed = internalize_site_links(output, {**sites, BASE_SITE: ""})
    log(f"links: internalized cross-product URLs in {changed} pages")

    before = len(config.get("redirects", []))
    config["redirects"] = internalize_redirects(config.get("redirects", []), sites)
    log(f"redirects: {before} -> {len(config['redirects'])} after internalizing")

    (output / "docs.json").write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    log(f"done: {sum(1 for _ in output.rglob('*.mdx'))} pages in {output}")


if __name__ == "__main__":
    main()
