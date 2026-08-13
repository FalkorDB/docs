# Repository guidelines

This repository holds the **FalkorDB core documentation**, published with
[Mintlify](https://mintlify.com) at <https://docs.falkordb.com>.

FalkorDB documentation is split across three repositories, surfaced to readers
as three products in one site (see `navigation.products` in `docs.json`):

| Product | Repository |
| --- | --- |
| FalkorDB (this repo) | `FalkorDB/docs` |
| FalkorDB Cloud | `FalkorDB/falkordb-cloud-docs` |
| FalkorDB Enterprise | `FalkorDB/FalkorDB-Enterprise` (`docs/`) |

Only edit FalkorDB core content here. Cloud and Enterprise pages live in their
own repositories and are linked from the product switcher.

## Authoring rules

- Every page is an `.mdx` file with YAML front matter containing at least
  `title`, and `description` where it adds value.
- **Do not write an H1 in the body.** Mintlify renders `title` as the H1.
  Start the body at `##`.
- Register every new page in `docs.json`. A page that is not in `navigation`
  is not reachable.
- Internal links are root-relative and omit the extension:
  `[Configuration](/getting-started/configuration)`.
- A folder's landing page is `index.mdx` and is wired up as the group `root`.

## MDX gotchas

MDX parses `{`, `}` and `<` as JSX. Outside fenced code blocks and inline code
spans you must escape them, self-close void elements (`<br />`, `<img ... />`),
use `className` instead of `class`, and pass `style` as an object. Use MDX
comments (`{/* ... */}`) rather than HTML comments.

## Components

Prefer Mintlify components over hand-rolled HTML:

- `<CodeGroup>` for the same example in multiple languages.
- `<AccordionGroup>` / `<Accordion>` for FAQs and collapsible argument lists.
- `<Note>`, `<Tip>`, `<Warning>`, `<Info>` for callouts.

## Local development

```bash
npm i -g mint
mint dev            # preview at http://localhost:3000
mint broken-links   # verify every internal link resolves
```

`mint` requires an LTS release of Node.

To validate MDX syntax across every page in one pass:

```bash
npm install --no-save @mdx-js/mdx remark-gfm
node scripts/check_mdx.mjs
```

## Scripts

- `scripts/check_mdx.mjs` — compiles every `.mdx` page and reports all syntax
  errors at once.
- `scripts/migrate_to_mintlify.py` — the one-shot Jekyll to Mintlify conversion.
  Kept for reference; it is a no-op now that no `.md` pages remain.
