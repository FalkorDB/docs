# FalkorDB UI Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Document how developers can use FalkorDB's shared UI toolkit, clarify that Browser uses it, and explain the sibling Canvas package.

**Architecture:** Add one focused developer page to the Browser docs and link it from the Browser overview. Register the page in Mintlify navigation; link to the toolkit's maintained usage resources and the existing Canvas guide rather than duplicating their detail.

**Tech Stack:** Mintlify MDX, `docs.json`, Node.js MDX validation, Mintlify broken-link check.

**Spec:** `docs/superpowers/specs/2026-11-17-document-falkordb-ui.md`

## Global Constraints

- Every page is an `.mdx` file with YAML front matter containing at least `title`.
- **Do not write an H1 in the body.** Mintlify renders `title` as the H1. Start the body at `##`.
- Register every new page in `docs.json`.
- Internal links are root-relative and omit the extension.
- Describe Canvas as a sibling package in the `falkordb-ui` repository, not a dependency bundled inside `@falkordb/ui`.

## Review Focus

- **Discoverability:** confirm the page is reachable from Browser navigation and the Browser overview.
- **MDX validity:** compile the new page with `node scripts/check_mdx.mjs`.
- **Internal links:** run `mint broken-links` and ensure new internal links resolve.
- **Package relationship:** verify the copy distinguishes React package `@falkordb/ui` from web-component package `@falkordb/canvas`.
- **Browser usage claim:** retain the claim that Browser uses both packages only with the verified upstream Browser manifest as evidence.

---

### Task 1: Add FalkorDB UI developer documentation

**Files:**
- Create: `browser/ui-toolkit.mdx`
- Modify: `browser/index.mdx`
- Modify: `docs.json`

**Interfaces:**
- Consumes: the existing `/browser/canvas` guide and the toolkit's repository, getting-started guide, Storybook, and npm package.
- Produces: the `/browser/ui-toolkit` route and a link to it from the Browser overview.

- [ ] **Step 1: Verify upstream package and usage references**

Confirm the `falkordb-ui` README documents `npm install @falkordb/ui` and its getting-started guide, Storybook, and npm package links. Confirm the Browser manifest includes both `@falkordb/ui` and `@falkordb/canvas`.

- [ ] **Step 2: Create the developer page**

Create `browser/ui-toolkit.mdx` with YAML front matter, no body H1, and a concise explanation that `@falkordb/ui` provides themeable React components for building FalkorDB-styled interfaces. State that FalkorDB Browser uses the toolkit. Link to the maintained getting-started guide, Storybook, and npm package. Explain that `@falkordb/canvas` is a separate graph web-component package in the same repository and link to `npm install @falkordb/canvas` instructions and `/browser/canvas`.

- [ ] **Step 3: Make the page discoverable**

Add `"browser/ui-toolkit"` to the Browser group's page list in `docs.json`, adjacent to `"browser/canvas"`. Add a short link to the page from `browser/index.mdx`.

- [ ] **Step 4: Validate the documentation**

Run `node scripts/check_mdx.mjs` and `mint broken-links`. Confirm both pass and inspect the resulting diff to ensure the new page is registered and the package relationships are accurate.

- [ ] **Step 5: Open a pull request**

Push the isolated branch and create a PR against the repository's default branch. The PR description should summarize the new developer guide and validation results.
