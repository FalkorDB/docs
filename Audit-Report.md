# FalkorDB/docs Documentation Audit Report

## Executive Summary

The FalkorDB docs site (187 pages, Jekyll \+ Just the Docs theme, deployed at docs.falkordb.com) has solid coverage of its core areas — Cypher, commands, operations, and GenAI integrations — but has meaningful gaps in onboarding clarity, security guidance, performance/benchmarking, cross-referencing, and content consistency. The findings below are organized by focus area, with specific file and line citations.  
---

## 1\. First User Experience / Onboarding

### 1.1 Homepage (index.md) — Strong but has gaps

What works well:

* index.md:46–51 — Docker one-liner and Browser URL are immediately visible  
* index.md:29–32 — "Choose Your Path" fork between graph-database and GraphRAG audiences  
* Multi-language code tabs (Python/JS/Java/Rust/Shell) provide a fast "try it" experience

Issues:  
\[O1\] nav\_exclude: true on the homepage (index.md:4)  
The homepage (/) is excluded from the sidebar (nav\_exclude: true, index.md:4). This is intentional but means there is no "Home" entry in the left nav; users who land on a sub-page have no sidebar link back to the root. The logo\_link: "/" in \_config.yml:7 provides only a logo click — not obvious on mobile.  
\[O2\] No explicit quickstart/getting-started CTA on the homepage  
index.md:44 says "Launch an instance using Docker" and then dives directly into code. There is no prominent "→ Read the Getting Started guide" call-to-action. getting-started/index.md contains a richer, step-by-step walkthrough (including a schema diagram) that new users never see if they read only the homepage.  
\[O3\] Homepage example dataset (MotoGP) conflicts with Getting Started example (social network)  
index.md uses MotoGP riders as the introductory example; getting-started/index.md uses a social network. Two different beginner examples in the first two pages a user reads is disorienting. There is no reference from index.md to the social network example or vice versa.  
\[O4\] Docker image confusion on first encounter  
The homepage (index.md:49) shows falkordb/falkordb:latest with both ports. getting-started/index.md:26–29 also shows falkordb/falkordb:latest. getting-started/configuration.md:23–26 introduces falkordb/falkordb-server as a lighter production image. A first-time user reading only the homepage does not know a server-only image exists; they may deploy the dev image in production.  
\[O5\] Prerequisites section is incomplete in Getting Started  
getting-started/index.md:19–21 notes that Redis 8.0.0+ is required for self-hosting, but the homepage (index.md) has no such note. A user who runs the Docker command from the homepage never reads the requirement and could encounter runtime errors if they already have Redis 7.x and try to load FalkorDB manually.  
---

### 1.2 Getting Started (getting-started/index.md)

What works well: Structured 4-step walkthrough, schema diagram, multi-language code, authentication note.  
\[O6\] No link to FalkorDB Browser in the Getting Started guide  
getting-started/index.md links to Docker, clients, Cypher, Operations, and GenAI Tools in its "Explore Further" section, but never mentions http://localhost:3000 or the Browser. After running docker run \-p 6379:6379 \-p 3000:3000 ..., the user has no prompt to open the visual interface.  
\[O7\] getting-started has only 3 pages (index, configuration, clients)  
There is no dedicated installation guide, no troubleshooting page, no FAQ. The installation path (Docker/Cloud/self-hosted from source) is split across getting-started/index.md, operations/docker.md, and operations/building-docker.md with no single "Install FalkorDB" landing page.  
\[O8\] Java client version is pinned at 0.4.0 (getting-started/clients.md:58)  
The jfalkordb Maven dependency is pinned to 0.4.0. If newer versions have been released this is stale and may cause new users to install an old client.  
---

## 2\. Coverage of Core Features and Related Solutions

### 2.1 Core FalkorDB Database

Well-covered: Cypher clauses (MATCH, CREATE, MERGE, DELETE, SET, etc.), data types, indexing (range/full-text/vector), constraints (mandatory/unique), commands (GRAPH.QUERY, GRAPH.RO\_QUERY, GRAPH.EXPLAIN, GRAPH.PROFILE, GRAPH.SLOWLOG, GRAPH.CONFIG GET/SET, GRAPH.CONSTRAINT, GRAPH.COPY, GRAPH.MEMORY, GRAPH.INFO, GRAPH.LIST, GRAPH.DELETE), UDFs, algorithms.  
\[C1\] No performance or query optimization guide  
There is no dedicated page covering query performance tuning: when to use indexes, how to read GRAPH.PROFILE output, effect of CACHE\_SIZE, query plan interpretation. The GRAPH.EXPLAIN and GRAPH.PROFILE command pages describe syntax but do not teach users to act on the output. The cypher/indexing/range-index.md and cypher/indexing/vector-index.md pages have some notes, but no consolidated "Performance Best Practices" guide exists.  
\[C2\] Memory management is undocumented beyond GRAPH.MEMORY  
commands/graph.memory.md documents the command; getting-started/configuration.md covers QUERY\_MEM\_CAPACITY. But there is no guide on FalkorDB's memory model (GraphBLAS sparse matrices), memory estimation for large graphs, or eviction behavior under maxmemory pressure (Redis eviction vs. FalkorDB graph persistence). The llms.txt:3 summarizes the GraphBLAS architecture but this information is absent from user-facing docs.  
\[C3\] GRAPH.BULK endpoint spec is not surfaced for new users  
design/bulk-spec.md documents the binary bulk-load endpoint. integration/bulk-loader.md documents the Python CLI. Neither page links to the other. The homepage (index.md:261–268) links to integration/bulk-loader, but not to the lower-level spec. Users building custom loaders cannot discover design/bulk-spec.md without already knowing to look in "Design".  
\[C4\] GRAPH.MEMORY command documentation  
commands/graph.memory.md exists but is not linked from operations/durability/index.md, the configuration page, or anywhere in the Getting Started guide.  
\[C5\] No dedicated security guide  
Security is scattered: ACL commands (commands/acl.md), ACL persistence (operations/durability/acl-persistence.md), authentication in Docker (operations/docker.md:55–58), TLS mentioned only in the Cloud section. There is no top-level "Security" page covering: network isolation, authentication, ACL design, TLS/SSL configuration for self-hosted instances, and least-privilege patterns.  
\[C6\] No "Troubleshooting" or "FAQ" section  
operations/docker.md:444–488 has a small "Troubleshooting" section; operations/replication.md:140–153 has a brief one; cypher/indexing/vector-index.md:415–421 has a short one. But there is no site-wide troubleshooting hub or FAQ page. Common issues like "connection refused", "graph not found", "query timeout exceeded", "out of memory", and "MOVED redirect" are not documented in an accessible way.  
\[C7\] Constraints docs don't mention interaction with indexes  
commands/graph.constraint-create.md and commands/graph.constraint-drop.md do not explain whether unique constraints automatically create an underlying range index. FalkorDB creates a unique index for unique constraints; this undocumented behavior means users may unknowingly create redundant indexes.  
---

### 2.2 Vector Search

Well-covered: cypher/indexing/vector-index.md is comprehensive (HNSW parameters, performance tradeoffs, examples, troubleshooting).  
\[VS1\] No end-to-end vector \+ graph hybrid search tutorial  
The vector index page documents the API, but there is no walkthrough that combines a CALL db.idx.vector.queryNodes(...) with graph traversal filters (WHERE, MATCH expansion). The "No support for filtering" limitation (cypher/indexing/vector-index.md:311) is stated but a workaround pattern (run vector search first, then graph-filter results in a WITH clause) is not shown.  
\[VS2\] vecf32 function is only mentioned in cypher/indexing/vector-index.md  
cypher/functions.md has a "Vector functions" section that lists vecf32 (referenced at cypher/indexing/vector-index.md:115), but the link /cypher/functions\#vector-functions in cypher/indexing/vector-index.md and commands/graph.query.md:26 points to a fragment anchor. If that heading changes, the anchor breaks.  
---

### 2.3 GenAI / GraphRAG

Well-covered: LangChain, LlamaIndex, LangGraph, AG2, GraphRAG-SDK, MCP Server, Graphiti, Cognee, Mem0, Code-Graph, QueryWeaver, GraphRAG-Toolkit.  
\[G1\] genai-tools/index.md doesn't mention QueryWeaver or Code-Graph in its description tag  
genai-tools/index.md:3–4 description: "Build intelligent GenAI applications with FalkorDB and LLMs using popular GraphRAG and agent frameworks like LangChain and LlamaIndex." This description doesn't hint at MCP Server, Code-Graph, or QueryWeaver, which are distinct capabilities. SEO/crawler metadata is incomplete for this section.  
\[G2\] No comparison guide: GraphRAG-SDK vs. LangChain vs. LlamaIndex  
A user wanting to build a GraphRAG application faces three nearly equivalent choices (GraphRAG-SDK, LangChain FalkorDB Graph, LlamaIndex FalkorDB store) with no guidance on when to use which.  
\[G3\] /graphrag-sdk link is broken  
agentic-memory/graphiti-mcp-server.md links to /graphrag-sdk (graphiti-mcp-server.md line with "Check out [GraphRAG SDK](https://github.com/graphrag-sdk)"). The page lives at /genai-tools/graphrag-sdk not /graphrag-sdk. No redirect\_from covers this in genai-tools/graphrag-sdk.md. This is a broken internal link.  
---

### 2.4 Integrations

\[I1\] integration/rest.md documents the Browser REST API, not a database REST API  
The page title is "Rest API" and its parent is "Integration", implying it's a FalkorDB REST interface. But the content (line 6: "FalkorDB Browser REST API") documents the Browser management interface. Users looking for "how do I access FalkorDB via HTTP" will be misled.  
\[I2\] Bolt support page (integration/bolt-support.md) lacks a connection string example  
The Bolt page explains the protocol and libraries but doesn't show a working connection string, e.g., bolt://localhost:7687. Neo4j users migrating to FalkorDB would benefit from a direct comparison showing port mapping (FalkorDB Bolt defaults) and any auth differences.  
\[I3\] Spring Data FalkorDB (integration/spring-data-falkordb.md) — no version information  
The Spring Data page describes the library but doesn't specify which Spring Boot or Spring Data versions are supported or tested.  
---

### 2.5 Cloud (cloud/)

\[CL1\] "Learn More" badges in cloud/index.md link to GitHub raw file paths, not live docs pages  
cloud/index.md:42–64: All "Learn More" buttons link to https://github.com/FalkorDB/docs/blob/main/cloud/... (raw GitHub). Users who click these on the live docs site are sent to GitHub instead of staying on docs.falkordb.com. One even links to an unreleased branch: https://github.com/FalkorDB/docs/edit/Cloud-Docs/cloud/features.md (line 26).  
\[CL2\] Inconsistent cloud provider claims across tier pages

* cloud/index.md:21: "Azure (BYOC)" is mentioned as available  
* cloud/free-tier.md (pricing table): Azure is listed only for Enterprise  
* cloud/enterprise-tier.md (pricing table): All tiers including Free show "AWS, GCP, Azure"  
* cloud/startup-tier.md:3: "You can deploy on AWS, GCP, or Azure (BYOC)"

These are contradictory. Four different pages describe which cloud providers are available per tier differently.  
\[CL3\] Duplicate pricing table appears on every tier page (free, startup, pro, enterprise)  
Each cloud tier page embeds the full 4-tier pricing comparison table. When prices change, all four pages must be updated identically. This is a maintainability problem and provides no additional value on the individual tier pages (users are already on the tier-specific page).  
\[CL4\] Cloud connection guide is missing  
There is no page covering "How to connect to FalkorDB Cloud with Python/JS/Java". The Cloud section describes tiers and features but not the connection workflow. Relevant details (endpoint URL format, TLS certificates, authentication) are absent.  
---

### 2.6 Operations — Kubernetes / Helm

\[K1\] K8s page (operations/k8s-support.md) uses Bitnami Redis Helm chart with a manual \--loadmodule flag  
The guide (k8s-support.md:20–53) uses bitnami/redis with extraFlags: \["--loadmodule /var/lib/falkordb/bin/falkordb.so"\]. This approach ties documentation to Bitnami's chart structure, which may drift. There is no mention of a FalkorDB-native Helm chart, if one exists, or of the KubeBlocks operator as a preferred path.  
\[K2\] Operations index (operations/index.md:32) links to /operations/k8s\_support (underscore)  
The file is k8s-support.md (hyphen). k8s-support.md:6–8 has redirect\_from: /operations/k8s\_support and /operations/k8s\_support.html, so the redirect is there — but the index page is pointing to a redirect rather than the canonical URL. This creates an unnecessary redirect hop.  
\[K3\] Migration guide (operations/migration/) is not listed in operations/index.md  
The operations index lists 11 sub-items but Migration is not among them, despite having 5 child pages and a dedicated index. Discovery path for migration guidance requires knowing to type the URL or find it via search.  
---

### 2.7 Observability / Monitoring

\[M1\] OpenTelemetry page is Python-only  
operations/opentelemetry.md covers only the Python SDK's OTel integration. There is no guidance for Node.js, Java, or Rust tracing. The page title says "FalkorDB-py Guide" but lives in Operations with no language qualifier in the nav.  
\[M2\] No metrics/monitoring guide beyond OTel  
There is no page covering Redis INFO command output, GRAPH.SLOWLOG usage patterns, Prometheus/Grafana integration for self-hosted deployments, or alerting thresholds (e.g., replication lag, memory usage, thread saturation).  
---

## 3\. SEO / Readability / Information Architecture

### 3.1 URL Structure

\[SEO1\] Inconsistent URL naming conventions

* cypher/load-csv.md — hyphenated slug ✓  
* cypher/optional-match.md — hyphenated slug ✓  
* cypher/order-by.md — hyphenated slug ✓  
* operations/k8s-support.md — hyphenated slug ✓ (but linked with underscore in index)  
* operations/falkordblite/ — no hyphen, camelCase component ✓  
* operations/durability/acl-persistence.md — hyphenated slug ✓

Minor inconsistency: some sections use snake\_case in legacy redirect targets while canonical URLs are kebab-case. The redirect infrastructure (via jekyll-redirect-from) covers these cases, but the inconsistency complicates maintenance.  
\[SEO2\] Algorithms URL vs. nav hierarchy inconsistency  
algorithms/index.md has nav\_order: 4 but the memory says the order is nav\_order: 3\. The stored memory ("nav\_order for top-level sections: Algorithms=3") and algorithms/index.md:4 should be verified against the current \_config.yml. (Not critical, but contributes to mismatched documentation.)  
\[SEO3\] Two top-level sections share the same nav\_order: 10  
Both cloud/index.md:4 and operations/index.md:3 have nav\_order: 10\. In Just the Docs, when two pages have the same nav\_order, the order is undefined (alphabetical fallback). This can make the sidebar ordering unpredictable across builds.  
\[SEO4\] integration/rest.md has a poor description: "Rest API detailed doc"  
integration/rest.md:3: description: "Rest API detailed doc" — this is a placeholder description. It will appear in Google search results as the meta description and is unlikely to drive clicks.  
\[SEO5\] Missing description on MCP Server child pages  
genai-tools/mcpserver/quickstart.md, genai-tools/mcpserver/configuration.md, and genai-tools/mcpserver/docker.md all lack a description key in their front matter. The Jekyll SEO tag plugin will fall back to the site-level description or nothing, hurting search result snippets.  
\[SEO6\] References/index.md is almost entirely about RedisGraph, not FalkorDB  
The References page (References/index.md:13–38) lists videos, slides, articles, and blog posts — nearly all referencing "RedisGraph" with content from 2018–2020. These are stale, brand-inconsistent references that will confuse new users and send negative signals to search engines about content freshness.  
---

### 3.2 Headings and Structure

\[H1\] cypher/index.md starts with a \# Comments heading  
cypher/index.md:9: The page's first heading is \# Comments, which is a narrow first entry for what should be a landing page. The page title in the front matter is "Cypher Language" but the H1 is "Comments" — this is a mismatch that hurts SEO and usability. There is no introductory paragraph explaining what OpenCypher is before the content begins.  
\[H2\] operations/replication.md has duplicate section 1.1  
operations/replication.md:55 has \#\#\# 1.1 Creating a Network and line \~60 has \#\#\# 1.1 Setting up the Master Instance. Two sections are labeled \#\#\# 1.1 — this is a heading numbering error.  
\[H3\] commands/index.md has a "FalkorDB API" link pointing to /commands/?group=graph  
commands/index.md:15: The link /commands/?group=graph is a Redis command reference filter, not a docs page. This link will 404 on docs.falkordb.com. It appears to be a carry-over from RedisGraph-era docs that pointed to the Redis command reference.  
\[H4\] datatypes.md is a top-level page with no parent  
datatypes.md sits at the root, has no parent: key, and appears only if users navigate to it directly or via the sidebar. It's not linked from getting-started/index.md, cypher/index.md, or anywhere other users would naturally flow. It's effectively an orphan page.  
---

### 3.3 Internal Links

\[L1\] Multiple pages link to /configuration without the /getting-started/ prefix  
commands/graph.query.md:19,25,27, commands/graph.ro-query.md:18,23, commands/graph.config-get.md:6, commands/graph.config-set.md:8, design/concurrency.md:10,14 all link to /configuration or /configuration\#.... The page lives at /getting-started/configuration. These links work only because getting-started/configuration.md has redirect\_from: \[/configuration, /configuration.html\]. The redirect is in place, but the preferred canonical URL should be /getting-started/configuration.  
\[L2\] operations/falkordblite/falkordblite-py.md links to /index  
falkordblite-py.md contains a link \[FalkorDB Documentation\](/index). The root page permalink is /, not /index. This may route to a 404 or redirect depending on the Jekyll build.  
\[L3\] /graphrag-sdk link in agentic-memory/graphiti-mcp-server.md is broken  
No redirect exists from /graphrag-sdk to /genai-tools/graphrag-sdk.  
\[L4\] operations/index.md:32 uses /operations/k8s\_support (underscore)  
The canonical URL is /operations/k8s-support. A redirect is in place via redirect\_from:, but canonical links should use the canonical URL.  
\[L5\] operations/docker.md:488: link to /operations/k8s-support uses the correct hyphenated form — but the operations index doesn't. This inconsistency within the same section is confusing for contributors.  
---

### 3.4 Duplicate / Thin Content

\[D1\] Cloud tier pages repeat the full 4-tier pricing table on each individual tier page  
cloud/free-tier.md, cloud/startup-tier.md, cloud/pro-tier.md, and cloud/enterprise-tier.md all contain a copy of the full pricing comparison table. This is 4× duplication of the same data.  
\[D2\] design/third-party.md — very thin content  
design/third-party.md appears to contain minimal content and is in a nav\_order: 998 section. It should either be expanded or merged into another page.  
\[D3\] References/index.md is stale/thin  
The page has 1 non-RedisGraph link (FalkorDB Blog) and lists a development tutorial pointing to developer.redis.com/howtos/redisgraph/ (a RedisGraph tutorial). This page needs substantial refresh.  
\[D4\] docker-examples/ directory contains legacy Dockerfiles  
docker-examples/ contains Dockerfiles based on redisfab/redisgraph and redisfab/redis:6.2.4 — these are RedisGraph-era files, not FalkorDB files, and they are unlinked from any documentation page. They should be removed or replaced with current FalkorDB examples.  
---

## 4\. Consistency and Maintainability

### 4.1 Stale / Legacy Content

\[ST1\] References/index.md is almost entirely RedisGraph content (2018–2020)  
All videos, blog posts, and slides reference RedisGraph. The FalkorDB brand is 2+ years old; this page needs a refresh with FalkorDB-specific content.  
\[ST2\] docker-examples/ directory contains RedisGraph-era Dockerfiles  
docker-examples/Dockerfile.alpine3 builds from redisfab/redisgraph:6.2.4-x64-alpine3. This is vestigial content that should be removed.  
\[ST3\] getting-started/configuration.md:241: TIMEOUT deprecation note references v2.10  
The deprecation note is accurate, but the version reference ("deprecated since v2.10") gives no indication of how old this is relative to the current version. Users don't know if they're on v2.10 or v4.x.  
\[ST4\] design/client-spec.md references v2.1.0 as a threshold for COLUMN\_SCALAR  
design/client-spec.md mentions that as of v2.1.0, ColumnType will always be COLUMN\_SCALAR. This is an old version. The text ("unless versions older than v2.1.0 must be supported") is stale context.

### 4.2 TODOs and WIPs

\[TODO1\] operations/kubeblocks.md contains a TODO  
The file is flagged in the TODO search. Needs review.  
\[TODO2\] Multiple UDF text pages contain WIP notes  
udfs/flex/text/join.md, udfs/flex/text/replace.md, udfs/flex/text/repeat.md, udfs/flex/text/lpad.md, udfs/flex/text/format.md, udfs/flex/text/rpad.md, udfs/flex/index.md contain "Coming soon" or similar markers. Shipping partially-complete UDF reference pages creates a confusing experience when users look up a specific function.  
\[TODO3\] commands/graph.constraint-create.md contains a TODO  
Flagged — requires review.  
\[TODO4\] browser/ui/login.md and browser/ui/query-editor.md contain TODOs  
Browser UI documentation is incomplete at several points.

### 4.3 Framework / Config

\[CFG1\] Jekyll \_config.yml uses remote\_theme (just-the-docs/just-the-docs) without pinning a version  
\_config.yml:1: remote\_theme: just-the-docs/just-the-docs with no version tag. Any breaking change in the upstream theme would immediately affect the site.  
\[CFG2\] operations/docker.md uses version: '3.8' in Docker Compose examples  
Docker Compose v3.8 version key is deprecated in Compose Specification (v3.x). Modern Docker Compose ignores the version key. The examples are not incorrect but may confuse users on current Docker Desktop versions that show warnings.  
\[CFG3\] cloud/index.md:26 links to an edit-mode GitHub URL (/edit/Cloud-Docs/cloud/features.md)  
cloud/index.md:26 contains https://github.com/FalkorDB/docs/edit/Cloud-Docs/cloud/features.md — this is an edit link to an unreleased branch. Users who click it will be sent to a GitHub login/edit page, not documentation content.  
---

## 5\. Prioritized Recommendations

### Priority 1 — High Impact / Low Effort (Quick Wins)

| \# | Recommendation | Affected Files | Impact Type |
| :---- | :---- | :---- | :---- |
| P1.1 | Fix /graphrag-sdk broken link in graphiti-mcp-server.md | agentic-memory/graphiti-mcp-server.md | User activation |
| P1.2 | Fix "Learn More" badges in cloud/index.md to point to /cloud/free-tier, /cloud/startup-tier, etc. instead of github.com/FalkorDB/docs/blob/main/... | cloud/index.md:42–64 | Adoption/conversion |
| P1.3 | Remove or update docker-examples/ directory (contains RedisGraph 6.2.4 Dockerfiles) | docker-examples/ | Maintainability |
| P1.4 | Refresh References/index.md — replace RedisGraph content with FalkorDB-specific references | References/index.md | SEO/discoverability |
| P1.5 | Fix duplicate \#\#\# 1.1 section heading in operations/replication.md | operations/replication.md:55–60 | Developer productivity |
| P1.6 | Fix operations/index.md:32 link to use /operations/k8s-support (hyphen, canonical URL) | operations/index.md:32 | Developer productivity |
| P1.7 | Fix cypher/index.md to have a proper introductory paragraph and rename the \# Comments H1 (or move Comments lower) | cypher/index.md:9 | SEO/discoverability |
| P1.8 | Add description: front matter to genai-tools/mcpserver/quickstart.md, configuration.md, docker.md | 3 files | SEO/discoverability |
| P1.9 | Fix integration/rest.md:3 description: "Rest API detailed doc" → meaningful description | integration/rest.md:3 | SEO/discoverability |
| P1.10 | Resolve nav\_order: 10 conflict between cloud/index.md and operations/index.md | cloud/index.md:4 or operations/index.md:3 | Developer productivity |
| P1.11 | Add Migration section link to operations/index.md | operations/index.md | User activation |

### Priority 2 — High Impact / Medium Effort

| \# | Recommendation | Affected Files | Impact Type |
| :---- | :---- | :---- | :---- |
| P2.1 | Create a Security guide (operations/security.md) covering ACL setup, TLS for self-hosted, network isolation, and least-privilege patterns | New page | Enterprise readiness |
| P2.2 | Create a Troubleshooting / FAQ page (getting-started/troubleshooting.md or operations/troubleshooting.md) aggregating common issues from Docker, replication, cluster, and query errors | New page | Support deflection |
| P2.3 | Add a prominent "→ Getting Started guide" CTA to the homepage (index.md) after the Docker quickstart | index.md | User activation |
| P2.4 | Add FalkorDB Browser link to getting-started/index.md:376–386 "Explore Further" | getting-started/index.md | User activation |
| P2.5 | Consolidate cloud tier pricing table into cloud/index.md or cloud/features.md and link to it from tier pages; remove duplicate tables | cloud/\*.md | Maintainability |
| P2.6 | Align cloud provider claims across cloud/index.md, cloud/free-tier.md, cloud/startup-tier.md, cloud/pro-tier.md, and cloud/enterprise-tier.md | cloud/\*.md | Adoption/conversion |
| P2.7 | Create Cloud Connection Guide (cloud/connecting.md): how to obtain the endpoint, TLS cert, and connect via each supported client library | New page | User activation, adoption |
| P2.8 | Create a Performance & Query Optimization guide covering index selection, GRAPH.EXPLAIN output interpretation, GRAPH.PROFILE output, CACHE\_SIZE effects, parameterized queries | New page | Developer productivity |
| P2.9 | Finish incomplete UDF reference pages (udfs/flex/text/join.md etc.) or add clear "not yet documented" stubs | udfs/flex/text/\*.md | Developer productivity |
| P2.10 | Add "Next Steps" cross-link from datatypes.md and link to it from getting-started/index.md and cypher/index.md | datatypes.md, getting-started/index.md, cypher/index.md | Discoverability |

### Priority 3 — Medium Impact / Higher Effort

| \# | Recommendation | Affected Files | Impact Type |
| :---- | :---- | :---- | :---- |
| P3.1 | Create a "Choose Your GraphRAG Framework" comparison guide (GraphRAG-SDK vs. LangChain vs. LlamaIndex vs. AG2) | New page | User activation |
| P3.2 | Create an end-to-end hybrid vector \+ graph search tutorial | New page | Developer productivity |
| P3.3 | Consolidate the two beginner examples (MotoGP on homepage, social network in Getting Started) into one consistent dataset used throughout | index.md, getting-started/index.md | User activation |
| P3.4 | Create a top-level "Install FalkorDB" landing page consolidating Docker, Cloud, Kubernetes, Railway, Lightning.AI, and FalkorDBLite paths | New page | User activation |
| P3.5 | Expand operations/opentelemetry.md to cover JS/Java/Rust or explicitly note the scope limitation in the title | operations/opentelemetry.md | Developer productivity |
| P3.6 | Add Prometheus/Grafana monitoring guide for self-hosted FalkorDB | New page | Enterprise readiness |
| P3.7 | Clarify integration/rest.md title and description: "FalkorDB Browser REST API" is a narrow, specialized audience; most users expecting a REST interface will be confused | integration/rest.md | Support deflection |
| P3.8 | Pin remote\_theme in \_config.yml to a specific Just the Docs release tag | \_config.yml:1 | Maintainability |
| P3.9 | Update design/client-spec.md to remove v2.1.0 backward-compat notes or clarify supported version floor | design/client-spec.md | Developer productivity |
| P3.10 | Add unique constraint → index relationship note to commands/graph.constraint-create.md | commands/graph.constraint-create.md | Developer productivity |

---

## Summary by Impact Category

| Category | Issues | Key recommendations |
| :---- | :---- | :---- |
| User Activation | O2, O3, O6, O7, CL4, P2.3, P2.4 | CTA on homepage, Cloud connect guide, unified install page |
| Adoption / Conversion | CL1, CL2, G2 | Fix cloud badge links, cloud provider consistency, framework comparison |
| Support Deflection | C5, C6, M2, I1 | Security guide, troubleshooting page, REST API clarity |
| SEO / Discoverability | H1, SEO3–6, D3, ST1 | Fix cypher index H1, meta descriptions, refresh References |
| Developer Productivity | C1, C2, C3, H3, L1–L5, TODO2 | Perf guide, memory guide, fix broken links, fix nav |
| Enterprise Readiness | C5, CL3, CL4, M1, M2, K1 | Security, monitoring, K8s Helm, Cloud connect guide |
| Maintainability | D1–D4, ST2–ST4, CFG1–CFG3, K2, K3 | Dedup cloud tables, remove legacy files, pin theme version |

---

## Notable Specific File Issues (Quick Reference)

| File | Issue | Severity |
| :---- | :---- | :---- |
| cloud/index.md:26,42–64 | "Learn More" badges link to github.com/FalkorDB/docs/blob/main/... instead of docs pages; one links to unreleased branch | High |
| cloud/\*.md | Contradictory Azure availability claims | High |
| agentic-memory/graphiti-mcp-server.md | /graphrag-sdk link is broken (no redirect to /genai-tools/graphrag-sdk) | High |
| operations/index.md:32 | /operations/k8s\_support underscore (canonical is hyphen) | Medium |
| operations/index.md | Migration section not listed | Medium |
| operations/replication.md:55–60 | Two consecutive \#\#\# 1.1 headings | Low |
| cypher/index.md:9 | H1 is "Comments" despite page title being "Cypher Language" | Medium |
| commands/index.md:15 | /commands/?group=graph will 404 on docs.falkordb.com | Medium |
| integration/rest.md:3 | description: "Rest API detailed doc" — SEO placeholder | Low |
| References/index.md | Almost entirely RedisGraph content (2018–2020); one link to unreleased tutorial | High |
| docker-examples/ | Contains RedisGraph 6.2.4 Dockerfiles; unlinked, legacy | Medium |
| operations/falkordblite/falkordblite-py.md | Link to /index instead of / | Low |
| genai-tools/mcpserver/quickstart.md, configuration.md, docker.md | No description: front matter | Low |
| \_config.yml:1 | remote\_theme unpinned | Low |
| cloud/free-tier.md, startup-tier.md, pro-tier.md, enterprise-tier.md | Full pricing table duplicated on each tier page | Medium |
| udfs/flex/text/\*.md | Multiple pages with "Coming soon" stubs | Medium |

