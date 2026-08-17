# Repository guidelines

This repository holds the **FalkorDB core documentation**, published with
[Mintlify](https://mintlify.com) at <https://docs.falkordb.com>.

FalkorDB documentation is split across four repositories and aggregated into a
single Mintlify deployment, so search and the AI assistant index every product
together. Each repository owns one entry in `navigation.products`:

| Product | Repository | Mounted at |
| --- | --- | --- |
| FalkorDB (this repo) | `FalkorDB/docs` | `/` |
| FalkorDB Cloud | `FalkorDB/mintlify-docs` | `/cloud` |
| FalkorDB Enterprise | `FalkorDB/FalkorDB-Enterprise` (`docs/`) | `/enterprise` |
| GraphRAG SDK | `FalkorDB/GraphRAG-SDK` (`docs/`) | `/graphrag` |

Only edit FalkorDB core content here. The other products live in their own
repositories.

## Aggregation

Each repository keeps the full `navigation.products` list and populates only its
own product, linking to the others with `href`. That way every repository still
builds and previews on its own.

`scripts/aggregate_docs.py` turns those four repositories into one site: it
clones each source listed in `scripts/sources.json`, copies its content under
the mount point, prefixes every path in its product entry, rewrites the repo's
own absolute links and assets, namespaces its snippets under
`/snippets/<mount>/`, and substitutes the result for the `href` placeholder in
this repository's `docs.json`. Redirects and links that point at a standalone
product site become internal paths.

```bash
python3 scripts/aggregate_docs.py --output build --use-local ..   # sibling checkouts
python3 scripts/aggregate_docs.py --output build                  # clone the sources
```

`.github/workflows/aggregate-docs.yml` runs this on every push to `main`, on a
`docs-updated` repository dispatch from a source repository, and nightly. It
publishes to the `docs-site` branch, which is the branch Mintlify deploys.

Adding a product means adding it to `navigation.products` here as an `href`
placeholder and appending an entry to `scripts/sources.json`.

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

- `scripts/aggregate_docs.py` — builds the combined multi-product site.
- `scripts/sources.json` — the repositories that get aggregated.
- `scripts/check_mdx.mjs` — compiles every `.mdx` page and reports all syntax
  errors at once.
- `scripts/migrate_to_mintlify.py` — the one-shot Jekyll to Mintlify conversion.
  Kept for reference; it is a no-op now that no `.md` pages remain.
