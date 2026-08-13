#!/usr/bin/env python3
"""One-shot migration of the Jekyll (just-the-docs) site to Mintlify.

Converts every `.md` page to `.mdx`, rewrites Jekyll/Liquid constructs into
Mintlify components, and generates `docs.json` from the existing
`nav_order` / `parent` front matter.

Usage:
    python3 scripts/migrate_to_mintlify.py [--dry-run]

The script is idempotent in the sense that it reads `.md` and writes `.mdx`;
re-running after the `.md` files are deleted is a no-op.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories that hold documentation pages. Everything else is left alone.
SKIP_DIRS = {".git", ".github", "_includes", "_sass", "images", "scripts", "node_modules"}
SKIP_FILES = {"README.md", "AGENTS.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md"}

# `References/` becomes `references/` so URLs stay lowercase.
DIR_RENAMES = {"References": "references"}

LANG_LABELS = {
    "python": ("python", "Python"),
    "javascript": ("javascript", "JavaScript"),
    "java": ("java", "Java"),
    "rust": ("rust", "Rust"),
    "cpp": ("cpp", "C++"),
    "shell": ("bash", "Shell"),
}

# Tags that stay as real elements when we escape stray `<` characters.
HTML_TAGS = {
    "a", "abbr", "b", "blockquote", "br", "code", "col", "colgroup", "dd", "details",
    "div", "dl", "dt", "em", "figcaption", "figure", "h1", "h2", "h3", "h4", "h5",
    "h6", "hr", "i", "iframe", "img", "input", "kbd", "li", "ol", "p", "picture",
    "pre", "s", "small", "source", "span", "strong", "sub", "summary", "sup",
    "table", "tbody", "td", "tfoot", "th", "thead", "tr", "u", "ul", "video",
}
MDX_COMPONENTS = {
    "Accordion", "AccordionGroup", "Card", "CardGroup", "Check", "CodeGroup",
    "Columns", "Expandable", "Frame", "Icon", "Info", "Note", "ParamField",
    "ResponseField", "Step", "Steps", "Tab", "Tabs", "Tip", "Tooltip", "Update",
    "Warning",
}
KNOWN_TAGS = HTML_TAGS | MDX_COMPONENTS
VOID_TAGS = {"br", "hr", "img", "input", "col", "source"}


# --------------------------------------------------------------------------- #
# Front matter
# --------------------------------------------------------------------------- #

def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end]
    body = text[end + 4:].lstrip("\n")
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        return {}, text
    return data, body


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


# --------------------------------------------------------------------------- #
# Liquid -> MDX
# --------------------------------------------------------------------------- #

CAPTURE_RE = re.compile(r"\{%\s*capture\s+(\w+)\s*%\}\n?(.*?)\n?\{%\s*endcapture\s*%\}", re.S)
CODE_TABS_RE = re.compile(r"^([ \t]*)\{%\s*include\s+code_tabs\.html\s+(.*?)%\}", re.S | re.M)
FAQ_RE = re.compile(r"\{%\s*include\s+faq_accordion\.html\s+(.*?)\n?%\}", re.S)
ARG_RE = re.compile(r'(\w+)\s*=\s*(?:"((?:[^"\\]|\\.)*)"|(\S+))', re.S)
DETAILS_RE = re.compile(
    r"<details(\s+open)?\s*>\s*<summary>(.*?)</summary>(.*?)</details>", re.S | re.I
)
HTML_COMMENT_RE = re.compile(r"<!--(.*?)-->", re.S)
# Legacy redis-doc metadata that leaked into the page body.
SYNTAX_BLOCK_RE = re.compile(r"^---\nsyntax:\s*\|\n(.*?)\n---$", re.S | re.M)


def convert_code_tabs(body: str) -> str:
    """`{% capture %}` + `{% include code_tabs.html %}` -> `<CodeGroup>`."""
    captures: dict[str, str] = {}

    def stash(match: re.Match) -> str:
        captures[match.group(1)] = match.group(2)
        return "\x00CAPTURE\x00"

    body = CAPTURE_RE.sub(stash, body)

    def build(match: re.Match) -> str:
        indent = match.group(1)
        args = {m.group(1): (m.group(2) if m.group(2) is not None else m.group(3))
                for m in ARG_RE.finditer(match.group(2))}
        blocks = []
        for lang, (fence_lang, label) in LANG_LABELS.items():
            var = args.get(lang)
            if not var or var not in captures:
                continue
            code = captures[var].strip("\n")
            fence = "```"
            while fence in code:
                fence += "`"
            blocks.append(f"{fence}{fence_lang} {label}\n{code}\n{fence}")
        if not blocks:
            return ""
        rendered = "<CodeGroup>\n\n" + "\n\n".join(blocks) + "\n\n</CodeGroup>"
        if not indent:
            return rendered
        return "\n".join(indent + line if line else line
                         for line in rendered.split("\n"))

    body = CODE_TABS_RE.sub(build, body)

    # Drop the placeholder lines left behind by the captures.
    body = re.sub(r"[ \t]*\x00CAPTURE\x00\n?", "", body)
    return body


def convert_faq(body: str) -> str:
    """`{% include faq_accordion.html %}` -> `<AccordionGroup>`."""

    def build(match: re.Match) -> str:
        args = {m.group(1): (m.group(2) if m.group(2) is not None else m.group(3))
                for m in ARG_RE.finditer(match.group(1))}
        title = args.get("title", "Frequently Asked Questions")
        items = []
        index = 1
        while True:
            question = args.get(f"q{index}")
            answer = args.get(f"a{index}")
            if not question:
                break
            question = question.replace('\\"', '"').strip()
            answer = (answer or "").replace('\\"', '"').strip()
            items.append(f'  <Accordion title={json.dumps(question)}>\n'
                         f"    {answer}\n"
                         f"  </Accordion>")
            index += 1
        if not items:
            return ""
        heading = f"## {title}\n\n" if title else ""
        return heading + "<AccordionGroup>\n" + "\n".join(items) + "\n</AccordionGroup>"

    return FAQ_RE.sub(build, body)


def convert_syntax_block(body: str) -> str:
    """`---\\nsyntax: |\\n…\\n---` -> a fenced shell block."""

    def build(match: re.Match) -> str:
        lines = [line[2:] if line.startswith("  ") else line
                 for line in match.group(1).rstrip().split("\n")]
        return "```sh\n" + "\n".join(lines) + "\n```"

    return SYNTAX_BLOCK_RE.sub(build, body)


def convert_details(body: str) -> str:
    """`<details><summary>x</summary>…</details>` -> `<Accordion>`."""

    def build(match: re.Match) -> str:
        is_open = bool(match.group(1))
        title = re.sub(r"<[^>]+>", "", match.group(2)).strip()
        inner = match.group(3).strip("\n")
        attrs = f"title={json.dumps(title)}" + (" defaultOpen" if is_open else "")
        return f"<Accordion {attrs}>\n{inner}\n</Accordion>"

    return DETAILS_RE.sub(build, body)


def convert_callouts(body: str) -> str:
    """kramdown `{: .warning }` + blockquote -> `<Warning>`."""
    lines = body.split("\n")
    out: list[str] = []
    index = 0
    mapping = {"warning": "Warning", "note": "Note", "important": "Info", "highlight": "Tip"}
    while index < len(lines):
        match = re.match(r"^\{:\s*\.(\w+)\s*\}\s*$", lines[index])
        if match and match.group(1) in mapping:
            component = mapping[match.group(1)]
            index += 1
            quoted = []
            while index < len(lines) and lines[index].startswith(">"):
                quoted.append(re.sub(r"^>\s?", "", lines[index]))
                index += 1
            out.append(f"<{component}>")
            out.extend("  " + line if line else "" for line in quoted)
            out.append(f"</{component}>")
            continue
        out.append(lines[index])
        index += 1
    return "\n".join(out)


def drop_leading_h1(body: str) -> str:
    """Mintlify renders the front matter title as the page H1."""
    lines = body.split("\n")
    in_fence = False
    for i, line in enumerate(lines):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## "):
            break  # a section started before any H1; leave the page alone
        if line.startswith("# "):
            del lines[i]
            while i < len(lines) and not lines[i].strip():
                del lines[i]
            break
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# MDX safety
# --------------------------------------------------------------------------- #

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
INLINE_CODE_RE = re.compile(r"(`+)(?:(?!\1).)*\1", re.S)
STYLE_RE = re.compile(r'style="([^"]*)"')
TAG_OPEN_RE = re.compile(r"<(/?)([A-Za-z][A-Za-z0-9._-]*)")


def to_style_object(css: str) -> str:
    parts = []
    for declaration in css.split(";"):
        if ":" not in declaration:
            continue
        name, _, value = declaration.partition(":")
        name = name.strip()
        prop = re.sub(r"-([a-z])", lambda m: m.group(1).upper(), name)
        parts.append(f"{json.dumps(prop)}: {json.dumps(value.strip())}")
    return "style={{" + ", ".join(parts) + "}}"


def fix_html(text: str) -> str:
    """Make raw HTML valid JSX: self-closing voids, className, style objects."""
    text = STYLE_RE.sub(lambda m: to_style_object(m.group(1)), text)
    text = re.sub(r"\bclass=", "className=", text)
    for tag in VOID_TAGS:
        text = re.sub(
            rf"<{tag}\b([^>]*?)\s*/?>",
            lambda m: f"<{tag}{m.group(1).rstrip()} />",
            text,
            flags=re.I,
        )
    return text


def escape_mdx(text: str) -> str:
    """Escape braces and stray `<` so MDX does not read them as expressions."""
    text = text.replace("{", "\\{").replace("}", "\\}")

    def keep_or_escape(match: re.Match) -> str:
        if match.group(2) in KNOWN_TAGS:
            return match.group(0)
        return "\\<" + match.group(1) + match.group(2)

    text = TAG_OPEN_RE.sub(keep_or_escape, text)
    # Any `<` not starting a tag at all (e.g. `a < b`).
    text = re.sub(r"<(?![A-Za-z/!\\])", "\\\\<", text)
    return text


def protect_and_escape(body: str) -> str:
    """Apply MDX escaping to prose only, leaving code blocks untouched."""
    out: list[str] = []
    fence: str | None = None
    for line in body.split("\n"):
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(2)
            if fence is None:
                fence = marker[0] * len(marker)
                out.append(line)
                continue
            if marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
                out.append(line)
                continue
        if fence is not None:
            out.append(line)
            continue

        # Split the line into inline-code spans (kept) and prose (escaped).
        pieces: list[str] = []
        cursor = 0
        for span in INLINE_CODE_RE.finditer(line):
            pieces.append(fix_html(escape_mdx(line[cursor:span.start()])))
            pieces.append(span.group(0))
            cursor = span.end()
        pieces.append(fix_html(escape_mdx(line[cursor:])))
        out.append("".join(pieces))
    return "\n".join(out)


# --------------------------------------------------------------------------- #
# Links
# --------------------------------------------------------------------------- #

LINK_RE = re.compile(r"\]\((?!https?:|mailto:|#)([^)\s]+)(\s+\"[^\"]*\")?\)")

# just-the-docs served these via `redirect_from`; Mintlify has no such page.
LINK_FIXUPS = {"/configuration": "/getting-started/configuration"}


def rewrite_links(body: str, page_dir: str) -> str:
    def fix(match: re.Match) -> str:
        target, title = match.group(1), match.group(2) or ""
        anchor = ""
        if "#" in target:
            target, _, anchor = target.partition("#")
            anchor = "#" + anchor
        if not target:
            return match.group(0)
        if target.startswith("/"):
            path = target
        else:
            path = "/" + os.path.normpath(os.path.join(page_dir, target)).lstrip("./")
        path = re.sub(r"\.(md|html)$", "", path)
        path = re.sub(r"/index$", "", path)
        if path.endswith("/") and len(path) > 1:
            path = path[:-1]
        for old, new in DIR_RENAMES.items():
            path = re.sub(rf"^/{old}(/|$)", rf"/{new}\1", path)
        path = LINK_FIXUPS.get(path, path)
        return f"]({path}{anchor}{title})"

    return LINK_RE.sub(fix, body)


# --------------------------------------------------------------------------- #
# Page collection
# --------------------------------------------------------------------------- #

class Page:
    def __init__(self, src: str, meta: dict, body: str):
        self.src = src                      # repo-relative .md path
        self.meta = meta
        self.body = body
        rel = src
        for old, new in DIR_RENAMES.items():
            if rel.startswith(old + "/"):
                rel = new + rel[len(old):]
        self.dst = rel[:-3] + ".mdx"        # repo-relative .mdx path
        self.slug = self.dst[:-4]           # docs.json page reference
        self.dir = os.path.dirname(src)

    @property
    def title(self) -> str:
        return self.meta.get("title") or "FalkorDB"

    @property
    def order(self) -> int:
        try:
            return int(self.meta.get("nav_order", 500))
        except (TypeError, ValueError):
            return 500

    @property
    def is_index(self) -> bool:
        return os.path.basename(self.src) == "index.md"


def collect_pages() -> list[Page]:
    pages: list[Page] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for filename in sorted(filenames):
            if not filename.endswith(".md") or filename in SKIP_FILES:
                continue
            src = os.path.relpath(os.path.join(dirpath, filename), ROOT)
            with open(os.path.join(ROOT, src), encoding="utf-8") as handle:
                meta, body = split_front_matter(handle.read())
            pages.append(Page(src, meta, body))
    return pages


def convert(page: Page) -> str:
    body = page.body

    # HTML comments are not valid MDX; park them and re-emit as `{/* */}`.
    comments: list[str] = []

    def stash_comment(match: re.Match) -> str:
        comments.append(match.group(1))
        return f"\x01C{len(comments) - 1}\x01"

    body = HTML_COMMENT_RE.sub(stash_comment, body)

    body = convert_syntax_block(body)
    body = convert_code_tabs(body)
    body = convert_faq(body)
    body = convert_details(body)
    body = convert_callouts(body)
    body = drop_leading_h1(body)
    body = rewrite_links(body, page.dir)
    body = protect_and_escape(body)
    body = re.sub(
        r"\x01C(\d+)\x01",
        lambda m: "{/*" + comments[int(m.group(1))].replace("*/", "*\\/") + "*/}",
        body,
    )
    body = re.sub(r"^[ \t]+$", "", body, flags=re.M)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"

    front = [f"title: {yaml_quote(' '.join(page.title.split()))}"]
    description = page.meta.get("description")
    if isinstance(description, str) and description.strip():
        front.append(f"description: {yaml_quote(' '.join(description.split()))}")
    return "---\n" + "\n".join(front) + "\n---\n\n" + body


# --------------------------------------------------------------------------- #
# docs.json
# --------------------------------------------------------------------------- #

def build_navigation(pages: list[Page]) -> list:
    by_dir: dict[str, list[Page]] = {}
    for page in pages:
        by_dir.setdefault(page.dir, []).append(page)

    def index_of(directory: str) -> Page | None:
        for page in by_dir.get(directory, []):
            if page.is_index:
                return page
        return None

    def children_dirs(directory: str) -> list[str]:
        prefix = directory + "/" if directory else ""
        found = set()
        for other in by_dir:
            if other and other.startswith(prefix) and other != directory:
                found.add(prefix + other[len(prefix):].split("/")[0])
        return sorted(found)

    def build_group(directory: str) -> dict:
        index = index_of(directory)
        entries: list = []
        leaves = [p for p in by_dir.get(directory, []) if not p.is_index]
        subgroups = [build_group(child) for child in children_dirs(directory)]
        combined = [(p.order, p.title, p.slug) for p in leaves]
        combined += [(g.pop("_order"), g["group"], g) for g in subgroups]
        for _, _, item in sorted(combined, key=lambda t: (t[0], t[1])):
            entries.append(item)
        group = {
            "group": index.title if index else directory.split("/")[-1].title(),
            "_order": index.order if index else 500,
            "pages": entries,
        }
        if index:
            group["root"] = index.slug
        return group

    root_pages = [p for p in by_dir.get("", []) if not p.is_index]
    top_groups = [build_group(d) for d in children_dirs("")]

    items = [(p.order, p.title, p.slug) for p in root_pages]
    items += [(g["_order"], g["group"], g) for g in top_groups]

    nav: list = ["index"]
    for _, _, item in sorted(items, key=lambda t: (t[0], t[1])):
        if isinstance(item, dict):
            item.pop("_order", None)
            nav.append(item)
        else:
            nav.append(item)

    home = [entry for entry in nav if isinstance(entry, str)]
    groups = [entry for entry in nav if isinstance(entry, dict)]
    for group in groups:
        strip_order(group)
    return [{"group": "Home", "pages": home}] + groups


def strip_order(group: dict) -> None:
    group.pop("_order", None)
    for entry in group.get("pages", []):
        if isinstance(entry, dict):
            strip_order(entry)


def build_docs_json(pages: list[Page]) -> dict:
    return {
        "$schema": "https://mintlify.com/docs.json",
        "theme": "mint",
        "name": "FalkorDB Docs",
        "description": (
            "Official FalkorDB documentation — the high-performance graph database "
            "for GraphRAG, Cypher queries, and knowledge graphs powering accurate "
            "GenAI applications."
        ),
        "colors": {"primary": "#FF8101", "light": "#FDE900", "dark": "#FF8101"},
        "favicon": "/images/favicon.ico",
        "logo": {"light": "/images/falkordb-logo.svg", "dark": "/images/falkordb-logo.svg",
                 "href": "https://www.falkordb.com"},
        "appearance": {"default": "dark"},
        "navigation": {
            "products": [
                {
                    "product": "FalkorDB",
                    "description": "The open source graph database, Cypher language, and tooling.",
                    "icon": "database",
                    "groups": build_navigation(pages),
                },
                {
                    "product": "FalkorDB Cloud",
                    "description": "The managed FalkorDB service and its provisioning API.",
                    "icon": "cloud",
                    "href": "https://docs.falkordb.cloud",
                },
                {
                    "product": "FalkorDB Enterprise",
                    "description": "Self-managed FalkorDB on your own Kubernetes clusters.",
                    "icon": "building",
                    "href": "https://docs.enterprise.falkordb.com",
                },
            ]
        },
        "navbar": {
            "links": [
                {"label": "Github", "href": "https://github.com/FalkorDB/FalkorDB",},
                {"label": "Support", "href": "https://support.falkordb.com"},
                {"label": "Discord", "href": "https://discord.com/invite/6M4QwDXn2w"},
            ],
            "primary": {"type": "button", "label": "Try FalkorDB Cloud",
                        "href": "https://app.falkordb.cloud"},
        },
        "footer": {
            "socials": {
                "github": "https://github.com/FalkorDB/FalkorDB",
                "x": "https://x.com/FalkorDB",
                "linkedin": "https://www.linkedin.com/company/falkordb",
                "discord": "https://discord.com/invite/6M4QwDXn2w",
            }
        },
        "integrations": {"gtm": {"tagId": "GTM-MBWB627H"}},
    }


# --------------------------------------------------------------------------- #

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    pages = collect_pages()
    if not pages:
        print("no .md pages found; nothing to do")
        return 0

    for page in pages:
        content = convert(page)
        if args.dry_run:
            continue
        destination = os.path.join(ROOT, page.dst)
        os.makedirs(os.path.dirname(destination) or ".", exist_ok=True)
        with open(destination, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.remove(os.path.join(ROOT, page.src))

    docs = build_docs_json(pages)
    if not args.dry_run:
        with open(os.path.join(ROOT, "docs.json"), "w", encoding="utf-8") as handle:
            json.dump(docs, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        for old in DIR_RENAMES:
            stale = os.path.join(ROOT, old)
            if os.path.isdir(stale) and not os.listdir(stale):
                shutil.rmtree(stale)

    print(f"converted {len(pages)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
