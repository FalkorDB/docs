# Documentation Improvement Tasks

Remaining issues identified during a full review of all markdown files (February 2026).
Critical issues have already been fixed. The tasks below are organized by priority.

---

## High Priority

### Metadata: Missing `description` on all UDF files
- **Scope:** All 49 files under `udfs/`
- **Issue:** No `description` frontmatter key anywhere in UDFs. Impacts SEO and page previews.
- **Action:** Add a meaningful one-line `description` to every UDF file.

### Metadata: Missing `nav_order` across many sections
- **Scope:**
  - Commands: `graph.config-set.md`, `graph.constraint-drop.md`, `graph.copy.md`, `graph.memory.md`, `graph.info.md`
  - Algorithms: all 6 algorithm files
  - Operations/Design: all 3 migration files, `client-spec.md`, `third-party.md`
  - UDFs: all ~40 individual function pages, plus `flex/index.md`
- **Action:** Add `nav_order` to all affected files for predictable navigation ordering.

### Standardize code block language tags in Cypher section
- **Scope:** Most files under `cypher/`
- **Issue:** Cypher queries tagged as `` ```sh `` or `` ```sql `` instead of `` ```cypher ``. Inconsistent within and across files.
- **Action:** Change all Cypher code blocks to use `` ```cypher ``.

### Expand thin command pages
- **Files:**
  - `commands/graph.query.md` — most critical command but lacks TIMEOUT docs, result set description, error handling, write operations
  - `commands/graph.info.md` — no multi-language examples, no arguments/return section, examples only show empty results
  - `commands/graph.explain.md` — no sample output showing how to interpret execution plans
- **Action:** Expand each page with missing sections, using `graph.memory.md` as the structural template.

### Add multi-language code tabs to inconsistent command pages
- **Files:** `commands/acl.md`, `commands/graph.info.md` (plain code blocks), `commands/graph.memory.md` (only shell + JS)
- **Action:** Add Python, Java, Rust, and JavaScript examples using `code_tabs.html`.

### Populate empty UDF category index pages
- **Files:** `udfs/flex/bitwise/index.md`, `collections/index.md`, `date/index.md`, `json/index.md`, `map/index.md`, `similarity/index.md`, `text/index.md`
- **Issue:** Each contains only a single sentence. Should list available functions and link to child pages.

### Fix `commands/graph.constraint-drop.md` stray frontmatter
- **Issue:** Lines 11-16 contain a second YAML-like `syntax:` block inside the markdown body that renders as broken content.
- **Action:** Remove or properly integrate the duplicate block.

### Verify GenAI code examples against current library versions
- **Files:** `genai-tools/llamaindex.md`, `genai-tools/langgraph.md`
- **Issues:**
  - LlamaIndex: `graph_store.get_graph_data()`, `KGTableSchema`, `download_loader("ImageReader")` may not exist in current API
  - LlamaIndex: `CustomQueryEngine` imported but never used
  - LangGraph: `ToolExecutor` removed from current LangGraph
  - LangGraph: `SqliteSaver` import path may have changed
- **Action:** Test all examples against current library versions; update or remove broken ones.

---

## Medium Priority

### Outdated references to RedisGraph and Redis tooling
- **Files:**
  - `design/client-spec.md` — references "RedisGraph v2.1.0", links to deprecated `redisgraph-py` repo
  - `design/third-party.md` — RedisGraph/Redis licensing may be outdated
  - `getting-started/clients.md` — many "Additional Clients" reference RedisGraph projects with no compatibility note
  - `commands/index.md` — "within Redis" phrasing may be misleading
  - `operations/k8s-support.md` — uses "master and slave" terminology
- **Action:** Update terminology, add compatibility notes, fix links.

### Update EOL Python version requirements
- **Files:** `operations/migration/kuzu-to-falkordb.md` (Python 3.6+), `operations/migration/neo4j-to-falkordb.md` (Python 3.6+), `operations/opentelemetry.md` (Python 3.8+)
- **Action:** Update to currently supported Python version (3.9+ minimum).

### Fix `_config.yml` issues
- Missing `url` key for canonical URL generation
- Missing `exclude` list (README.md, Gemfile, etc. will be built into the site)
- Unpinned `remote_theme` version
- Protocol-relative URLs (`//github.com/...`) should use `https://`
- Consider adding `jekyll-seo-tag` plugin
- Ruby docs link references EOL Ruby 2.7

### Standardize command page structure
- **Issue:** Inconsistent formatting across command pages — some use headings for Arguments/Returns, some use inline text, some use `<details>` HTML.
- **Action:** Adopt `graph.memory.md` structure (Syntax, Arguments, Return, Examples) as template for all command pages.

### Standardize shell prompt style in examples
- **Issue:** Varies between `127.0.0.1:6379>`, `redis>`, `>`, and no prompt.
- **Action:** Pick one convention and apply it consistently.

### Fix inconsistent code example completeness
- **Issue:** Some command examples show full imports/client setup, others show only the call.
- **Files:** `graph.query.md`, `graph.ro-query.md` (no setup) vs `graph.list.md`, `graph.config-set.md` (full setup)
- **Action:** Make all examples copy-paste ready with setup code.

### De-duplicate Rust Loader content in migration guides
- **Files:** `operations/migration/kuzu-to-falkordb.md`, `operations/migration/neo4j-to-falkordb.md`
- **Issue:** The FalkorDB-Loader-RS section is nearly identical in both files.
- **Action:** Extract to a shared page and reference from both.

### De-duplicate content in `agentic-memory/cognee.md`
- **Issue:** LLM config appears twice, database config appears twice, "Managing Knowledge" duplicates "Adding Multiple Documents".
- **Action:** Consolidate to reduce page length by ~30%.

### Reconcile cloud pricing tables
- **Files:** `cloud/free-tier.md`, `cloud/startup-tier.md`, `cloud/enterprise-tier.md`
- **Issues:** Discrepancies in Azure/BYOC notation, last-row labels ("Call-to-Action" vs "Get started"), feature highlighting
- **Action:** Unify table content across all tier pages.

### Fix `cloud/free-tier.md` heading level
- **Issue:** Uses `#### Terms` (H4) while all other tier pages use `## Terms` (H2).

### Fix `cloud/features.md` hierarchy
- **Issue:** "Solution Architecture" incorrectly nested under "Graph Browser" as H3. Should be its own H2.
- **Issue:** Missing docs for Graph Access Control, Cluster Deployment, HA, Multi-zone, Automated Backups, Advanced Monitoring.

### Expand `commands/index.md` landing page
- **Issue:** Very short, does not list or link to any child command pages.
- **Action:** Add a table or list of all available commands with brief descriptions.

### Fix `design/client-spec.md` outdated claims
- Line 192: "each node can have either 0 or 1 labels" — multi-label is now supported
- Lines 38-40: Links to specific commit hash for enum definitions — will drift
- **Action:** Update content to reflect current capabilities.

### Add missing `redirect_from` in Cypher section
- **Files:** `call.md`, `foreach.md`, `merge.md`, `skip.md`, `limit.md`, `remove.md`, `match.md`, `procedures.md`, `set.md`, `unwind.md`, `where.md`, `with.md`

### Expand thin Cypher pages
- **Files:** `cypher/skip.md`, `cypher/limit.md`, `cypher/order-by.md`
- **Action:** Add edge-case docs (SKIP beyond total records, LIMIT without ORDER BY, NULL sort ordering), cross-references, and complete query examples.

### Add missing Go and C# to getting-started installation tabs
- **File:** `getting-started/index.md`
- **Issue:** Both are official clients but missing from the tabbed examples.

### Fix `udfs/index.md` structural issues
- Line 274: `falkor.register` heading is H5 instead of H4
- Line 251-253: Misplaced paragraph about multi-source traversal
- Line 394: Grammar — missing comma and conjunction

### Fix `operations/opentelemetry.md` scope and accuracy
- Title doesn't indicate Python-only focus
- `RedisInstrumentor` imported but never used
- Jaeger exporter is deprecated — should note OTLP alternative
- Only covers traces despite claiming metrics/logs

---

## Low Priority

### Heading capitalization consistency in `datatypes.md`
- Currently: "Scalar types", "Temporal Types", "Collection types" — three different styles.
- **Action:** Pick one convention (Title Case or Sentence case).

### Fix `commands/graph.query.md` spelling inconsistency
- Uses both "Parametrized" and "Parameterized" in the same file.

### Fix description casing in `commands/graph.copy.md`
- Starts lowercase ("creates a copy"); all other command descriptions start uppercase.

### Improve `README.md`
- No frontmatter, no project description, no prerequisites, no contribution guidelines.
- Should be excluded from Jekyll build via `_config.yml` or given proper content.

### Fix `index.md` minor issues
- Line 37: OpenCypher link uses `http://` instead of `https://`
- Line 60: Missing comma after "Once loaded"
- Line 262: "Mailing List / Forum" heading is misleading for GitHub Discussions link

### Algorithm pages consistency
- Add Performance Considerations and Error Handling sections to all (only BFS has them)
- Fix recurring "Lets" → "Let's" typo in `sppath.md`, `wcc.md`, `sspath.md`, `betweenness-centrality.md`
- Remove trailing colons from headings ("Examples:", "Example:")
- Verify and unify procedure naming: `algo.bfs` vs `algo.WCC`/`algo.wcc` vs `pagerank.stream`
- Fix missing commas in path results in `sppath.md` and `sspath.md`

### Fix `getting-started/configuration.md` minor issues
- Line 320: `//` comment in shell example should be `#`
- "V" and "X" markers in config table are non-standard — use "Yes"/"No" or checkmarks
- Missing examples for `VKEY_MAX_ENTITY_COUNT`, `CMD_INFO`, `MAX_INFO_QUERIES`

### Fix `getting-started/clients.md` title mismatch
- Frontmatter `title` is "Client Libraries" but H1 heading is "Official Clients"

### Fix `integration/jena.md` placeholder issues
- Port 7474 is Neo4j default, not FalkorDB (should be 6379)
- Thin content — essentially just links to external repos

### Improve `cypher/known-limitations.md` currency
- Review whether listed limitations still apply
- "researching designs" language implies ongoing work with no timeline
- Add language tags to code blocks

### Asymmetric "See Also" cross-references in UDF pages
- If A links to B, B should link back to A (e.g., `jaroWinkler` ↔ `jaccard`)

### Inconsistent parameter naming in UDF text functions
- `text.indexOf` uses `offset`; `text.indexesOf` uses `from` for the same concept

### LlamaIndex page: duplicate Resources section
- Resources appear at both lines 14-18 and 300-305. Consolidate.

### LlamaIndex page: potentially broken link
- `gpt-index.readthedocs.io` migrated to `docs.llamaindex.ai`

### GraphRAG SDK page improvements
- No link to GitHub repository
- "GPT-4.1" model name is unusual — verify accuracy
- Emoji keycap headings may cause rendering issues

### `operations/k8s-support.md` improvements
- `allowInsecureImages: true` needs explanation
- Sentinel config not actually enabled despite heading claiming it
- Legacy `bitnamilegacy/redis-cluster` image may be unmaintained
- Informal/promotional closing paragraph

### `operations/migration/kuzu-to-falkordb.md` inconsistencies
- Export defaults to `_csv_` but loader defaults to `csv_output`
- GitHub links point to different organizations (`FalkorDB-POCs` vs `FalkorDB`)

### `cypher/call.md` cleanup
- Lines 80-129: Large blocks of commented-out HTML should be removed or completed
- Line 133: "withholding" should be "holding"
- Code blocks use `sh` for Cypher

### `cypher/fulltext-index.md` issues
- Line 458: Description says "enable phonetic search" but example doesn't
- Fuzzy matching syntax should be verified against RediSearch docs

### `cypher/range-index.md` issues
- Line 484-486: Uses `#` comment syntax in Cypher (should be `//`)

### Add version/compatibility info to UDF pages
- No pages indicate which FalkorDB/FLEX version introduced the functions
