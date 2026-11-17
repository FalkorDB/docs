# FalkorDB UI documentation design

## Intent

Help developers discover and use FalkorDB's shared UI toolkit to build
FalkorDB-themed interfaces, while explaining that FalkorDB Browser uses the
toolkit and that the same repository also publishes the graph Canvas component.

## Goals and non-goals

- Add a short, navigable developer page under the Browser docs and link to it
  from the Browser overview.
- Link to the toolkit repository, its getting-started documentation, Storybook,
  and npm package.
- Describe `@falkordb/ui` (React components and theme) and
  `@falkordb/canvas` (standalone graph web component) as distinct packages
  published from the same repository.
- Mention that FalkorDB Browser uses both packages.
- Do not duplicate the component reference or the existing Canvas guide.

## Approaches

- **Brief Browser overview section:** quickest and keeps the links near the
  Browser introduction, but leaves no focused developer guidance.
- **Short developer page under Browser docs (selected):** gives developers a
  clear starting point while keeping the Browser overview concise. Link it
  from the overview and register it in `docs.json`.

## Constraints and implementation calls

Use the existing Mintlify MDX conventions. Keep package installation and
getting-started details linked to the toolkit's own maintained resources.
Describe Canvas as a sibling package in the `falkordb-ui` repository, not a
dependency bundled inside `@falkordb/ui`. The Browser's upstream package
manifest lists both `@falkordb/ui` and `@falkordb/canvas`.
