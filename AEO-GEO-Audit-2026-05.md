# FalkorDB Docs — AEO/GEO Audit (May 2026)

**Repository:** https://github.com/FalkorDB/docs  
**Site:** https://docs.falkordb.com  
**Files in scope:** 172 markdown files  
**Approach:** 25 per-file reports (high-impact pages) + 4 template-level reports (~110 repetitive pages) + site-wide summary

---

## Site-Wide Context

- ✅ `jekyll-seo-tag`, `jekyll-sitemap`, `jekyll-redirect-from` enabled in `_config.yml`
- ❌ **Zero JSON-LD anywhere** — no `application/ld+json`, `@context`, or `schema.org` on any page
- ❌ **Zero pages have a `date:` or `last_modified:` frontmatter field**
- ✅ Every file has a `description:` field
- ⚠️ Mixed internal link styles (some use absolute `/path`, some use relative `./file.md`)

---

## PART 1 — PER-FILE AUDITS (25 high-impact pages)

---

### `index.md` (homepage)

**Primary entity:** FalkorDB  
**Best extractable snippet:** "FalkorDB delivers an accurate, multi-tenant RAG solution powered by a low-latency, scalable graph database technology."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 3 | Tagline is marketing prose; no "FalkorDB is X" sentence in first 100 words | Add: "FalkorDB is an open-source graph database built as a Redis module, designed for low-latency Cypher queries and GraphRAG over knowledge graphs." |
| Q&A Structure | 2 | No FAQ section; headings are categorical, not query-shaped | Add H2s: "What is FalkorDB?", "How does FalkorDB compare to Neo4j?", "How do I install FalkorDB?" |
| Snippet Quality | 3 | Good code example but no standalone definition snippet | Add a TL;DR callout box at the top |
| Heading Hierarchy | 4 | One H1; `## The Graph platform...` after `# FalkorDB` is an orphan tagline H2 | Demote tagline to a `<p class="lead">` |
| Factual Density | 3 | "low-latency", "accurate", "scalable" are unsupported assertions | Add: "FalkorDB executes typical 1-hop traversals in <1 ms and scales to billions of edges" |
| Comparative Signals | 1 | No mention of Neo4j, RedisGraph, Memgraph by name | Add a 3-row "FalkorDB vs Neo4j vs RedisGraph" table or link |
| Structured Data | 1 | No JSON-LD | Add `SoftwareApplication` JSON-LD (see below) |
| Freshness Signals | 1 | No `date` / `last_modified` | Add `last_modified_at` via `_config.yml` defaults |
| Internal Linking | 4 | Links to Cypher, GenAI, Clients, Indexing | Link "GraphRAG", "Knowledge Graph", "Property Graph Model" to definition pages |
| Voice & Register | 3 | Mix of declarative and marketing | Replace with: "FalkorDB stores knowledge graphs that LLMs query with Cypher to ground answers in your data." |

**Overall AEO/GEO Score:** 25 / 50

**Top 3 Quick Wins:**
1. Insert a 1-sentence "What is FalkorDB?" definition as the very first paragraph (before badges/banner)
2. Add a `SoftwareApplication` JSON-LD block via `_includes/head_custom.html`
3. Replace "Choose Your Path" with FAQ-style block: "Should I use FalkorDB or Neo4j?", "Is FalkorDB the same as RedisGraph?"

**Rewritten Passage:**
- Before: "FalkorDB delivers an accurate, multi-tenant RAG solution powered by a low-latency, scalable graph database technology."
- After: "FalkorDB is an open-source graph database that runs as a Redis module. It uses sparse-matrix linear algebra to execute OpenCypher queries with sub-millisecond latency, and is designed for GraphRAG over multi-tenant knowledge graphs."

**Suggested JSON-LD:**
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "FalkorDB",
  "applicationCategory": "DatabaseApplication",
  "operatingSystem": "Linux, macOS, Windows (Docker)",
  "description": "Open-source graph database built as a Redis module, optimized for low-latency Cypher queries and GraphRAG.",
  "url": "https://docs.falkordb.com/",
  "softwareVersion": "latest",
  "license": "https://github.com/FalkorDB/FalkorDB/blob/master/LICENSE.txt",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" }
}
```

---

### `getting-started/index.md`

**Primary entity:** FalkorDB Getting Started workflow  
**Best extractable snippet:** "FalkorDB requires Redis 8.0.0 or later. Earlier versions (including the Redis 7.x series) are not supported."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 4 | Workflow named clearly | Add 1-line "What you'll build" intro |
| Q&A Structure | 3 | Steps are well-numbered but headings aren't questions | Convert to "How do I install FalkorDB?", "How do I run my first Cypher query?" |
| Snippet Quality | 4 | Redis-version callout is highly extractable | Add a TL;DR: "Run `docker run -p 6379:6379 falkordb/falkordb:latest`, install the client, run your first MATCH query." |
| Heading Hierarchy | 4 | Single H1, logical Step H2s | OK |
| Factual Density | 4 | Concrete versions, ports, commands | Add expected wall-clock time ("under 5 minutes") |
| Comparative Signals | 2 | No mention of Neo4j/RedisGraph onboarding differences | Add "Coming from Neo4j?" callout linking to migration guide |
| Structured Data | 1 | No JSON-LD | Add `HowTo` JSON-LD with steps |
| Freshness Signals | 1 | No `date`; Redis 8.0 requirement is time-sensitive | Add `last_modified_at` |
| Internal Linking | 4 | Good cross-links | Link "Property Graph", "Cypher" first occurrences to glossary |
| Voice & Register | 4 | Direct, declarative | Strong |

**Overall AEO/GEO Score:** 31 / 50

**Top 3 Quick Wins:**
1. Add `HowTo` JSON-LD with 4 numbered steps
2. Convert step headings to natural questions
3. Insert a 3-line TL;DR snippet box at the top

**Suggested JSON-LD:**
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Get started with FalkorDB",
  "description": "Install FalkorDB, model a social network as a graph, and run your first Cypher query.",
  "step": [
    {"@type": "HowToStep", "name": "Install FalkorDB", "text": "Run `docker run -p 6379:6379 falkordb/falkordb:latest`."},
    {"@type": "HowToStep", "name": "Install a client", "text": "Install the Python, Node.js, Java, Go, Rust, PHP, or C# client."},
    {"@type": "HowToStep", "name": "Model the graph", "text": "Define User and Post nodes and FRIENDS_WITH and CREATED relationships."},
    {"@type": "HowToStep", "name": "Run a Cypher query", "text": "Use MATCH and RETURN to traverse the graph."}
  ]
}
```

---

### `getting-started/configuration.md`

**Primary entity:** FalkorDB configuration parameters  
**Best extractable snippet:** "FalkorDB exposes the GRAPH.CONFIG command for setting and retrieving configuration parameters at run-time."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 4 | Clear | OK |
| Q&A Structure | 2 | "Setting Configuration Parameters on Module Load" is procedural, not a question | "How do I set FalkorDB config at startup?", "How do I change config without restarting?" |
| Snippet Quality | 3 | Good code blocks; each param needs a one-line "What this controls" definition | Add inline definitions |
| Heading Hierarchy | 4 | Sensible | OK |
| Factual Density | 5 | Specific defaults, ranges, commands | Strong |
| Comparative Signals | 2 | No "Equivalent in Redis/Neo4j" mapping | Add column to parameter table |
| Structured Data | 1 | No JSON-LD | Add `TechArticle` |
| Freshness Signals | 1 | TIMEOUT deprecation noted but no date | Add `last_modified_at` and `since: vX.Y` per parameter |
| Internal Linking | 4 | Links to Redis docs and command pages | Good |
| Voice & Register | 4 | Declarative | OK |

**Overall AEO/GEO Score:** 30 / 50

**Top 3 Quick Wins:**
1. Add a parameter quick-index table at top: `name | default | runtime-mutable | since`
2. Add `TechArticle` JSON-LD
3. Convert top-level H2s to question form

---

### `getting-started/clients.md`

**Primary entity:** FalkorDB official client libraries  
**Best extractable snippet:** "FalkorDB provides official clients for Python, Node.js, Java, Rust, Go, PHP, and C#, plus official OGM libraries for Python, Go, and Java (Spring Data)."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 4 | Tables are entity-rich | Add 1-line definition above first table |
| Q&A Structure | 2 | No question headings | "Which FalkorDB client should I use?", "Does FalkorDB have an OGM?" |
| Snippet Quality | 2 | Tables don't extract well as snippets | Add a prose summary paragraph before the table |
| Heading Hierarchy | 4 | OK | — |
| Factual Density | 5 | Languages, licenses, packages all listed | Strong |
| Comparative Signals | 2 | No "Recommended for X use case" | Add a "Which client to choose" decision matrix |
| Structured Data | 2 | No JSON-LD | Add `ItemList` of `SoftwareSourceCode` |
| Freshness Signals | 1 | No version pinning; clients evolve weekly | Add `last_modified_at` |
| Internal Linking | 3 | Mostly external links | Link client pages to per-client docs |
| Voice & Register | 4 | Direct | OK |

**Overall AEO/GEO Score:** 29 / 50

---

### `cloud/index.md`

**Primary entity:** FalkorDB Cloud DBaaS  
**Best extractable snippet:** "FalkorDB Cloud DBaaS offers four tiers — Free, Startup, Pro, and Enterprise — with multi-tenancy, high availability, and deployment on AWS, GCP, and Azure (Enterprise BYOC)."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 4 | Named clearly | Add "FalkorDB Cloud is a managed graph database service" sentence |
| Q&A Structure | 2 | No question headings | "What is FalkorDB Cloud?", "How much does it cost?", "Which cloud providers does FalkorDB Cloud support?" |
| Snippet Quality | 3 | Tier descriptions lack pricing/limits | Add a tier comparison table with concrete RAM/storage/connections |
| Heading Hierarchy | 4 | One H1, tier H2s | OK |
| Factual Density | 2 | "robust", "highest levels of security" — vague | Replace with concrete numbers (RAM caps, throughput, RPO/RTO) |
| Comparative Signals | 1 | No mention of Neo4j Aura, Aiven, Redis Cloud | Add "FalkorDB Cloud vs Neo4j Aura" table |
| Structured Data | 1 | No JSON-LD | Add `Service` with `Offer`s per tier |
| Freshness Signals | 1 | No date; pricing/tiers change | Add `last_modified_at` |
| Internal Linking | 4 | Links to all tier pages | OK |
| Voice & Register | 3 | Marketing-leaning; "extracting insights" is fluff | Replace with concrete capability statements |

**Overall AEO/GEO Score:** 25 / 50

**Suggested JSON-LD:**
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "FalkorDB Cloud",
  "serviceType": "Managed Graph Database",
  "provider": {"@type": "Organization", "name": "FalkorDB"},
  "areaServed": ["AWS", "GCP", "Azure"],
  "offers": [
    {"@type": "Offer", "name": "Free", "price": "0", "priceCurrency": "USD"},
    {"@type": "Offer", "name": "Startup", "url": "https://docs.falkordb.com/cloud/startup-tier"},
    {"@type": "Offer", "name": "Pro", "url": "https://docs.falkordb.com/cloud/pro-tier"},
    {"@type": "Offer", "name": "Enterprise", "url": "https://docs.falkordb.com/cloud/enterprise-tier"}
  ]
}
```

---

### `operations/index.md`

**Primary entity:** FalkorDB Operations / production deployment  
**Best extractable snippet:** "For production deployments, use the `falkordb/falkordb-server` Docker image, which excludes the FalkorDB Browser and is lighter and more efficient."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 4 | Clear | — |
| Q&A Structure | 2 | Numbered link list, not questions | Reframe as "How do I deploy FalkorDB to Kubernetes?" etc. |
| Snippet Quality | 4 | Production tip is highly extractable | OK |
| Heading Hierarchy | 5 | Clean | — |
| Factual Density | 3 | Mostly a link list | Add concrete deployment-choice criteria ("Use cluster if >X graphs") |
| Comparative Signals | 2 | No "Docker vs Kubernetes vs Cloud" decision matrix | Add |
| Structured Data | 1 | None | `CollectionPage` or `TableOfContents` |
| Freshness Signals | 1 | None | Add `last_modified_at` |
| Internal Linking | 5 | All sub-sections linked | — |
| Voice & Register | 4 | Direct | — |

**Overall AEO/GEO Score:** 31 / 50

---

### `cypher/index.md`

**Primary entity:** FalkorDB Cypher language support  
**Best extractable snippet:** "FalkorDB supports the OpenCypher query language with proprietary extensions. Cypher is a declarative graph query language that allows you to express what data to retrieve from a graph using pattern matching, filtering, and projections."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Excellent definition | — |
| Q&A Structure | 3 | Section headings are categorical | Add "What Cypher features does FalkorDB support?", "Can I run Neo4j Cypher queries on FalkorDB?" |
| Snippet Quality | 4 | First paragraph is snippet-ready | Add a TL;DR box |
| Heading Hierarchy | 4 | OK | — |
| Factual Density | 4 | Comments syntax table is concrete | Mention Cypher version supported (Cypher 9) |
| Comparative Signals | 2 | "Proprietary extensions" mentioned but not enumerated | Link to specific extension pages and Neo4j compat note |
| Structured Data | 1 | None | `TechArticle` |
| Freshness Signals | 1 | None | Add `last_modified_at` |
| Internal Linking | 5 | Excellent — every clause linked | — |
| Voice & Register | 5 | Declarative | — |

**Overall AEO/GEO Score:** 34 / 50

---

### `cypher/cypher-support.md`

**Primary entity:** Cypher feature coverage matrix  
**Best extractable snippet:** "FalkorDB implements OpenCypher 9 with the following exceptions: hexadecimal and octal numeric literals are not supported; nodes and relationships are not internally comparable."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 4 | Doc named clearly | — |
| Q&A Structure | 2 | Pure feature inventory, no Q&A | Add intro: "Does FalkorDB support all of Cypher?" |
| Snippet Quality | 2 | Long bullet lists; nothing self-contained | Add a 1-paragraph executive summary |
| Heading Hierarchy | 4 | Logical | — |
| Factual Density | 5 | Very dense | Strong |
| Comparative Signals | 4 | Implicitly compares to OpenCypher 9 spec | Add explicit Neo4j-vs-FalkorDB column |
| Structured Data | 1 | None | — |
| Freshness Signals | 1 | HIGHLY version-sensitive; no date | Add `last_modified_at` + `cypher_version: 9` |
| Internal Linking | 2 | Few links to feature pages | Each ✓ feature should link to its clause page |
| Voice & Register | 4 | Direct | — |

**Overall AEO/GEO Score:** 29 / 50

---

### `cypher/known-limitations.md`

**Primary entity:** FalkorDB Cypher known limitations  
**Best extractable snippet:** "When a relation in a match pattern is not referenced elsewhere in the query, FalkorDB will only verify that at least one matching relation exists, rather than operating on every matching relation."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Excellent — each limitation is named | — |
| Q&A Structure | 3 | Headings are descriptive but not query-shaped | "Why does COUNT return 1 when there are 2 relationships?" |
| Snippet Quality | 5 | Each section is a perfect AI quote | Strong |
| Heading Hierarchy | 5 | OK | — |
| Factual Density | 5 | Reproducible Cypher examples | Strong |
| Comparative Signals | 3 | Implicitly differs from Neo4j | Add "Neo4j behavior:" notes |
| Structured Data | 2 | Could be `FAQPage` | Add |
| Freshness Signals | 1 | Limitations get fixed; no date | Add `last_modified_at` |
| Internal Linking | 3 | Few | Link each limitation to a tracking issue |
| Voice & Register | 5 | Excellent | — |

**Overall AEO/GEO Score:** 37 / 50 *(one of the best AEO pages on the site)*

---

### `commands/graph.query.md`

**Primary entity:** GRAPH.QUERY command  
**Best extractable snippet:** "GRAPH.QUERY executes the given Cypher query against a specified graph. Syntax: `GRAPH.QUERY graph_name \"query\" [timeout value] [--compact] [version value]`."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Strong | — |
| Q&A Structure | 2 | No Q&A headings | "How do I run a Cypher query in FalkorDB?", "How do I set a query timeout?" |
| Snippet Quality | 4 | Syntax line is snippet-perfect | Add return-shape JSON example |
| Heading Hierarchy | 4 | OK | — |
| Factual Density | 5 | Argument table, 5-language examples | Strong |
| Comparative Signals | 2 | No "Neo4j equivalent: cypher-shell" | Add |
| Structured Data | 1 | None | `TechArticle` |
| Freshness Signals | 1 | None | Add `last_modified_at` + `since: v1.0` |
| Internal Linking | 4 | Good cross-links | Link `--compact` to response-format diff |
| Voice & Register | 5 | Direct | — |

**Overall AEO/GEO Score:** 33 / 50

---

### `commands/graph.profile.md`

**Primary entity:** GRAPH.PROFILE command  
**Best extractable snippet:** "GRAPH.PROFILE executes a query and returns the execution plan augmented with records-produced and execution-time metrics for each operation. Unlike GRAPH.EXPLAIN, it actually runs the query and applies any modifications."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Excellent — names PROFILE, EXPLAIN, QUERY relationship explicitly | — |
| Q&A Structure | 2 | None | "How do I profile a Cypher query in FalkorDB?", "Profile vs Explain — what's the difference?" |
| Snippet Quality | 5 | First two paragraphs are snippet-perfect | — |
| Heading Hierarchy | 4 | OK | — |
| Factual Density | 5 | Real example with timings | — |
| Comparative Signals | 4 | Compares to QUERY and EXPLAIN | Add Neo4j PROFILE comparison |
| Structured Data | 1 | None | — |
| Freshness Signals | 1 | None | — |
| Internal Linking | 4 | Links to QUERY/EXPLAIN | — |
| Voice & Register | 5 | Direct | — |

**Overall AEO/GEO Score:** 36 / 50

---

### `cypher/indexing/vector-index.md`

**Primary entity:** Vector Index (HNSW)  
**Best extractable snippet:** "Create a vector index using `CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}`. FalkorDB supports euclidean and cosine similarity functions."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 4 | Vector index defined; HNSW algorithm never named | Add: "FalkorDB's vector index uses the HNSW (Hierarchical Navigable Small World) algorithm." |
| Q&A Structure | 2 | None | "How do I create a vector index in FalkorDB?", "Does FalkorDB support cosine similarity?" |
| Snippet Quality | 4 | Syntax block is great | Add "When to use vector index" 1-liner |
| Heading Hierarchy | 3 | Some sections are paragraphs rather than H2/H3 | Promote "Searching" / "Updating" to H2 |
| Factual Density | 5 | Concrete defaults (M=16, efC=200, efR=10) | — |
| Comparative Signals | 2 | No comparison to pgvector, Pinecone, Weaviate | Add brief comparison |
| Structured Data | 1 | None | `TechArticle` |
| Freshness Signals | 1 | None; vector features evolve quickly | Add `last_modified_at` + `since: vX.Y.Z` |
| Internal Linking | 3 | Few | Link to fulltext-index, range-index for "which index to choose" |
| Voice & Register | 4 | Declarative | — |

**Overall AEO/GEO Score:** 29 / 50

**Quick Win:** Add this sentence at the top: "FalkorDB's vector index uses the HNSW (Hierarchical Navigable Small World) algorithm with cosine or euclidean similarity, supporting 1–4096-dimensional vectors." This single line will dominate AI answers to "Does FalkorDB support vector search?"

---

### `operations/cluster.md`

**Primary entity:** FalkorDB cluster setup  
**Best extractable snippet:** "A FalkorDB cluster shards the keyspace across multiple master nodes using Redis Cluster's hash-slot mechanism (16,384 slots). Each graph is a single Redis key living entirely on the shard whose slot range covers the hash of its name."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Excellent — entity, mechanism, routing model explained immediately | — |
| Q&A Structure | 3 | Step headings, not question headings | "How do I shard a graph in FalkorDB?", "Can a single graph span multiple shards?" |
| Snippet Quality | 5 | Architecture paragraphs are top-tier | — |
| Heading Hierarchy | 5 | Clean | — |
| Factual Density | 5 | 16,384 slots, 3 masters, 1 replica each | — |
| Comparative Signals | 3 | Implicitly compares to standalone; no Neo4j Causal Cluster comparison | Add |
| Structured Data | 1 | None | `HowTo` |
| Freshness Signals | 1 | None | Add `last_modified_at` |
| Internal Linking | 4 | Links to Replication | — |
| Voice & Register | 5 | Excellent | — |

**Overall AEO/GEO Score:** 37 / 50

---

### `operations/replication.md`

**Primary entity:** FalkorDB replication  
**Best extractable snippet:** "FalkorDB replication follows a single-primary model: one master instance accepts all writes and asynchronously streams its changes to one or more replicas. Replicas serve read-only traffic via GRAPH.RO_QUERY."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Excellent | — |
| Q&A Structure | 3 | Procedural | "How does FalkorDB replication work?", "Can replicas accept writes?", "How do I monitor replication lag?" |
| Snippet Quality | 5 | Architecture overview is snippet-perfect | — |
| Heading Hierarchy | 4 | Clean | — |
| Factual Density | 4 | Could use concrete lag numbers / thresholds | Add |
| Comparative Signals | 2 | No "Neo4j Causal Cluster vs FalkorDB Replication" | Add |
| Structured Data | 1 | None | `HowTo` |
| Freshness Signals | 1 | None | Add `last_modified_at` |
| Internal Linking | 4 | Links to cluster, GRAPH.RO_QUERY | — |
| Voice & Register | 5 | Direct | — |

**Overall AEO/GEO Score:** 34 / 50

---

### `operations/migration/neo4j-to-falkordb.md`

**Primary entity:** Neo4j → FalkorDB migration  
**Best extractable snippet:** "Migrate from Neo4j to FalkorDB by extracting nodes, edges, constraints, and indexes to CSV files, then loading them into FalkorDB. The Neo4j-to-FalkorDB migration toolkit (Python 3.9+) automates ontology extraction and CSV conversion."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Excellent | — |
| Q&A Structure | 4 | Numbered steps | Add "How do I migrate from Neo4j to FalkorDB?" as the H1 alt-text |
| Snippet Quality | 4 | Good | Add a 3-line TL;DR with the 3 key commands |
| Heading Hierarchy | 5 | Clean | — |
| Factual Density | 5 | Specific scripts, args, repos | — |
| Comparative Signals | 4 | This page IS the comparison | Add "What changes between Neo4j and FalkorDB Cypher" section |
| Structured Data | 1 | None | `HowTo` |
| Freshness Signals | 1 | None; migration tool is updated | Add `last_modified_at` |
| Internal Linking | 4 | Links to migration repo | — |
| Voice & Register | 5 | Direct | — |

**Overall AEO/GEO Score:** 38 / 50 *(highest in this audit set)*

---

### `operations/migration/redisgraph-to-falkordb.md`

**Primary entity:** RedisGraph → FalkorDB migration  
**Best extractable snippet:** "FalkorDB is fully compatible with RedisGraph RDB files. Create a snapshot with SAVE or BGSAVE in RedisGraph and mount the resulting `dump.rdb` into a FalkorDB Docker container."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Compatibility statement is gold | — |
| Q&A Structure | 3 | Step format | Make "Is FalkorDB compatible with RedisGraph?" an explicit H2 |
| Snippet Quality | 5 | First sentence is the perfect AI answer | — |
| Heading Hierarchy | 4 | OK | — |
| Factual Density | 5 | Concrete commands | — |
| Comparative Signals | 3 | Implicit | Add "What's different from RedisGraph" section (highly searched) |
| Structured Data | 1 | None | — |
| Freshness Signals | 1 | None | — |
| Internal Linking | 3 | Few | Link to `docker.md`, persistence |
| Voice & Register | 5 | Direct | — |

**Overall AEO/GEO Score:** 35 / 50

---

### `genai-tools/index.md`

**Primary entity:** FalkorDB GenAI integrations  
**Best extractable snippet:** *(none ideal; description is generic)*

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 3 | Vague intro | "FalkorDB integrates with GraphRAG-SDK, AG2, LangChain, LangGraph, LlamaIndex, AWS GraphRAG Toolkit, MCP, QueryWeaver, and Code-Graph for building LLM-powered graph applications." |
| Q&A Structure | 2 | Bulleted TOC | "Which GraphRAG framework should I use with FalkorDB?" |
| Snippet Quality | 2 | TOC only | Add a decision-matrix table |
| Heading Hierarchy | 4 | OK | — |
| Factual Density | 2 | Generic | Add concrete "use X if you need Y" criteria |
| Comparative Signals | 2 | None between integrations | Add |
| Structured Data | 1 | None | `CollectionPage` |
| Freshness Signals | 1 | None | — |
| Internal Linking | 5 | All children linked | — |
| Voice & Register | 3 | Marketing-ish; "powerful" is fluff | Replace with concrete capabilities |

**Overall AEO/GEO Score:** 25 / 50

---

### `genai-tools/graphrag-sdk.md`

**Primary entity:** GraphRAG-SDK  
**Best extractable snippet:** "GraphRAG-SDK is an open-source Python SDK for FalkorDB that converts natural-language questions into Cypher queries, generates contextually relevant answers from knowledge graph data, and supports OpenAI, Gemini, and Groq LLM providers."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 3 | Bullet-led; no definition sentence | Add a 1-sentence definition before the bullets |
| Q&A Structure | 3 | "Quick Start" is procedural | "What is GraphRAG-SDK?", "How do I install GraphRAG-SDK?" |
| Snippet Quality | 3 | Bullets fragment the message | Convert to prose paragraph + retain bullets as features list |
| Heading Hierarchy | 4 | OK | — |
| Factual Density | 4 | Concrete LLM providers, env vars | Add SDK version pinning |
| Comparative Signals | 2 | No "vs LangChain GraphCypherQAChain" | Add |
| Structured Data | 1 | None | `SoftwareApplication` |
| Freshness Signals | 1 | None | — |
| Internal Linking | 3 | Links to GitHub | Link to other GenAI pages for comparison |
| Voice & Register | 4 | Direct | — |

**Overall AEO/GEO Score:** 28 / 50

---

### `genai-tools/mcpserver/quickstart.md`

**Primary entity:** FalkorDB MCP Server  
**Best extractable snippet:** "Install the FalkorDB MCP Server in Claude Desktop by adding `@falkordb/mcpserver` to the `mcpServers` block in `claude_desktop_config.json`. Run `npx -y @falkordb/mcpserver` to start the server."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 4 | Clear | — |
| Q&A Structure | 4 | Sections are practical | "How do I add FalkorDB to Claude Desktop?" |
| Snippet Quality | 4 | JSON snippet is gold | Add explanation of `mcpServers` block |
| Heading Hierarchy | 4 | OK | — |
| Factual Density | 5 | Specific paths, env vars, transports | — |
| Comparative Signals | 2 | No "stdio vs http transport — when to use which" | Add |
| Structured Data | 1 | None; also `search_exclude: true` blocks Jekyll search | Remove `search_exclude: true` or explain why |
| Freshness Signals | 1 | None | — |
| Internal Linking | 3 | Links to docker.md, configuration | — |
| Voice & Register | 5 | Direct | — |

**Overall AEO/GEO Score:** 33 / 50

---

### `agentic-memory/index.md`

**Primary entity:** Agentic memory with FalkorDB  
**Best extractable snippet:** "Agentic memory enables AI agents to maintain persistent, contextual memory across interactions. FalkorDB supports agentic memory via Graphiti, Cognee, and Mem0 frameworks."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Defines agentic memory upfront | — |
| Q&A Structure | 5 | "What is Agentic Memory?", "Why FalkorDB?" — exemplary Q&A structure | **This is the model template — replicate site-wide** |
| Snippet Quality | 5 | Multiple snippet-ready paragraphs | — |
| Heading Hierarchy | 5 | Clean | — |
| Factual Density | 4 | Bullet-heavy with some brand claims | Add "FalkorDB-vs-MongoDB-as-memory-backend" data |
| Comparative Signals | 4 | Decision matrix exists ("If you need X, use Y") | Strengthen by naming non-FalkorDB alternatives |
| Structured Data | 1 | None | `FAQPage` — perfect fit |
| Freshness Signals | 1 | None | — |
| Internal Linking | 5 | Each framework linked | — |
| Voice & Register | 4 | Mostly direct; some "uniquely suited" hedging | Replace with concrete benchmarks |

**Overall AEO/GEO Score:** 39 / 50 *(best page in audit)*

---

### `algorithms/index.md`

**Primary entity:** FalkorDB graph algorithms catalog  
**Best extractable snippet:** "FalkorDB provides graph algorithms via the `CALL algo.<name>()` interface, built on matrix-based computation. Available: BFS, SPpath, SSpath, MSF, PageRank, Betweenness Centrality, WCC, and CDLP."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 4 | Strong | Add: "All algorithms are read-only and run in-process." |
| Q&A Structure | 3 | Categorical | "Does FalkorDB support PageRank?", "How do I run BFS in FalkorDB?" |
| Snippet Quality | 4 | Each algo has a 1-line description | Add master comparison table (algo, complexity, use case) |
| Heading Hierarchy | 5 | Clean | — |
| Factual Density | 4 | "Matrix-based computation" is concrete | Add per-algo complexity |
| Comparative Signals | 2 | No "Neo4j GDS equivalents" mapping | Add |
| Structured Data | 1 | None | `CollectionPage` |
| Freshness Signals | 1 | None | — |
| Internal Linking | 5 | All algos linked | — |
| Voice & Register | 5 | Direct | — |

**Overall AEO/GEO Score:** 34 / 50

---

### `algorithms/pagerank.md`

**Primary entity:** PageRank algorithm in FalkorDB  
**Best extractable snippet:** "Call PageRank in FalkorDB with `CALL algo.pageRank(label, relationship-type) YIELD node, score`. Pass `null` for label or relationship-type to include all nodes/types."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | History and definition both stated | — |
| Q&A Structure | 3 | Categorical | "How do I run PageRank in FalkorDB?", "What does PageRank compute?" |
| Snippet Quality | 4 | Definition + syntax | — |
| Heading Hierarchy | 5 | Clean | — |
| Factual Density | 4 | Missing: damping factor value, max iterations | Add |
| Comparative Signals | 2 | No comparison to GDS `gds.pageRank.stream` | Add |
| Structured Data | 1 | None | `TechArticle` |
| Freshness Signals | 1 | None | — |
| Internal Linking | 3 | Sparse | Link to other centrality algos |
| Voice & Register | 5 | Direct | — |

**Overall AEO/GEO Score:** 33 / 50

---

### `datatypes.md`

**Primary entity:** FalkorDB data types  
**Best extractable snippet:** "FalkorDB supports persistent graph types (Nodes, Relationships) and ephemeral graph types (Paths). Scalar property values can be strings, integers, doubles, booleans, lists, maps, vectors, points, and temporal types."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Excellent | — |
| Q&A Structure | 2 | Categorical | "What data types does FalkorDB support?", "Does FalkorDB support DateTime?" |
| Snippet Quality | 4 | First two paragraphs are great | — |
| Heading Hierarchy | 5 | Clean | — |
| Factual Density | 5 | Examples for each type | — |
| Comparative Signals | 2 | No "vs Neo4j: FalkorDB lacks X" | Add |
| Structured Data | 1 | None | — |
| Freshness Signals | 1 | None | — |
| Internal Linking | 4 | Cypher links | — |
| Voice & Register | 5 | Direct | — |

**Overall AEO/GEO Score:** 34 / 50

---

### `integration/index.md`

**Primary entity:** FalkorDB integrations catalog  
**Best extractable snippet:** "FalkorDB integrates via REST API, Bolt protocol, Kafka Connect sink, Apache Jena, Spring Data, Snowflake Native App, PyTorch Geometric, and a CSV bulk loader."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 4 | Solid intro | — |
| Q&A Structure | 2 | Bulleted TOC | "Does FalkorDB support Bolt?", "How do I import CSV into FalkorDB?" |
| Snippet Quality | 3 | TOC-style | Convert intro to a one-paragraph summary |
| Heading Hierarchy | 4 | OK | — |
| Factual Density | 3 | Generic | Add "Use REST when X, Bolt when Y" |
| Comparative Signals | 1 | None | Add |
| Structured Data | 1 | None | `CollectionPage` |
| Freshness Signals | 1 | None | — |
| Internal Linking | 5 | All linked | — |
| Voice & Register | 4 | Direct | — |

**Overall AEO/GEO Score:** 28 / 50

---

### `browser/index.md`

**Primary entity:** FalkorDB Browser  
**Best extractable snippet:** "FalkorDB Browser is a web UI for visualizing graphs, running Cypher queries, and managing FalkorDB. It runs inside the main FalkorDB Docker image on port 3000 and is also available in FalkorDB Cloud."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Strong | — |
| Q&A Structure | 2 | Feature tables | "How do I run a Cypher query in FalkorDB Browser?", "How do I visualize a graph?" |
| Snippet Quality | 4 | Tables compress well; first paragraph is snippet-ready | — |
| Heading Hierarchy | 5 | Clean | — |
| Factual Density | 5 | Very dense | — |
| Comparative Signals | 2 | No "vs Neo4j Browser / Bloom" | Add |
| Structured Data | 1 | None | `WebApplication` |
| Freshness Signals | 1 | None; UI changes frequently | Add `last_modified_at` urgently |
| Internal Linking | 4 | Links to UI subpages | — |
| Voice & Register | 5 | Direct | — |

**Overall AEO/GEO Score:** 34 / 50

---

### `udfs/flex/index.md`

**Primary entity:** FLEX UDF library  
**Best extractable snippet:** "FLEX is FalkorDB's open-source community UDF package, providing string and set similarity metrics (Jaccard, Jaro-Winkler, Levenshtein), date/time manipulation, JSON utilities, map operations, and bitwise operations."

| Criterion | Score (1–5) | Key Finding | Recommended Fix |
|-----------|-------------|-------------|-----------------|
| Entity Clarity | 5 | Strong; links to GitHub | — |
| Q&A Structure | 3 | Categorical with tables | "What functions does FLEX provide?", "How do I install FLEX?" |
| Snippet Quality | 4 | First paragraph is good | — |
| Heading Hierarchy | 4 | OK | — |
| Factual Density | 4 | Function tables are concrete | Add an installation section (currently missing) |
| Comparative Signals | 2 | No "Neo4j APOC equivalent" (APOC is the obvious comparison) | Add |
| Structured Data | 1 | None | `SoftwareSourceCode` |
| Freshness Signals | 1 | None | — |
| Internal Linking | 5 | Every function linked | — |
| Voice & Register | 5 | Direct | — |

**Overall AEO/GEO Score:** 34 / 50

---

## PART 2 — TEMPLATE-LEVEL AUDITS

### Template A — `udfs/flex/**` (50 function pages)

Representative page: `udfs/flex/text/jaroWinkler.md`

**Template strengths:**
- Excellent structure: Description → Syntax → Parameters table → Returns → Examples → Notes → See Also
- Each page has a frontmatter `description` ready for AI
- Multiple use-case examples; factually dense

| Criterion | Score | Issue |
|---|---|---|
| Entity Clarity | 5 | Function name and signature stated |
| Q&A Structure | 3 | Section names categorical; convert to question-form |
| Snippet Quality | 5 | Description sentences are perfect |
| Heading Hierarchy | 5 | Clean H1/H2/H3 |
| Factual Density | 5 | Strong |
| Comparative Signals | 3 | "See Also" present but no "Use X instead of Y when Z" |
| Structured Data | 1 | None — add `TechArticle` via a Liquid include in the FLEX layout |
| Freshness Signals | 1 | No `since:` or `last_modified` |
| Internal Linking | 4 | "See Also" links present |
| Voice & Register | 5 | Direct |

**Average Score:** ~37 / 50 *(best-templated content on the site)*

**Template fixes:**
1. Add `_includes/flex_jsonld.html` emitting `TechArticle` JSON-LD using frontmatter `title`/`description` — one change → 50 pages improved
2. Add `since: <version>` frontmatter to each function page
3. In `_config.yml` `defaults`, auto-set `last_modified_at` for `udfs/flex/**`

---

### Template B — `commands/graph.*.md` (13 command-reference pages)

| Criterion | Score | Issue |
|---|---|---|
| Entity Clarity | 5 | Strong |
| Q&A Structure | 2 | No question headings |
| Snippet Quality | 4 | Description + syntax work well |
| Heading Hierarchy | 4 | OK |
| Factual Density | 5 | Strong |
| Comparative Signals | 2 | None; no "Related commands" table on most pages |
| Structured Data | 1 | None |
| Freshness Signals | 1 | No `since:` field |
| Internal Linking | 4 | Some |
| Voice & Register | 5 | Direct |

**Average Score:** ~33 / 50

**Template fixes:**
1. Standardize a "Returns → Errors → Related commands → Since version" footer block on every command page
2. Add `since:` frontmatter
3. Template-level `TechArticle` JSON-LD include

---

### Template C — `algorithms/*.md` (8 algorithm pages)

| Criterion | Score | Issue |
|---|---|---|
| Entity Clarity | 5 | Strong |
| Q&A Structure | 3 | "Algorithm Overview" → should be "What does X compute?" |
| Snippet Quality | 4 | Good |
| Heading Hierarchy | 5 | OK |
| Factual Density | 3 | Missing: time complexity, memory complexity, weighted variant |
| Comparative Signals | 2 | No GDS / NetworkX equivalence |
| Structured Data | 1 | None |
| Freshness Signals | 1 | None |
| Internal Linking | 3 | Sparse |
| Voice & Register | 5 | Direct |

**Average Score:** ~32 / 50

**Template fixes:**
1. Add "Complexity" subsection (time/space, weighted-vs-unweighted) to every algo page
2. Add "Equivalent in" table (Neo4j GDS, NetworkX, igraph)
3. Template-level JSON-LD

---

### Template D — `browser/ui/*.md` (13 UI documentation pages)

| Criterion | Score | Issue |
|---|---|---|
| Entity Clarity | 4 | Each UI element named |
| Q&A Structure | 3 | Descriptive but not query-shaped |
| Snippet Quality | 4 | Good for procedural Qs |
| Heading Hierarchy | 4 | OK |
| Factual Density | 4 | Concrete defaults and behaviors |
| Comparative Signals | 1 | None |
| Structured Data | 1 | None |
| Freshness Signals | 1 | None — **Browser UI changes most frequently; highest priority for `last_modified_at`** |
| Internal Linking | 4 | Linked from browser/index.md |
| Voice & Register | 5 | Direct |

**Average Score:** ~31 / 50

**Template fixes:**
1. Add `last_modified_at` (most volatile section)
2. Add a "UI version" or "Screenshot date" field per page
3. Add `WebPage` JSON-LD

---

## PART 3 — SITE-WIDE SUMMARY

### Scores sorted worst-first

| File / Group | Score / 50 | Biggest Gap | Priority |
|---|---|---|---|
| `cloud/index.md` | 25 | No comparative signals; vague superlatives | **High** |
| `index.md` (homepage) | 25 | No definition sentence; no JSON-LD; no competitor comparison | **High** |
| `genai-tools/index.md` | 25 | Generic intro; no decision matrix | **High** |
| `genai-tools/graphrag-sdk.md` | 28 | No definition sentence; no LangChain comparison | **High** |
| `integration/index.md` | 28 | Bulleted TOC; no decision criteria | Medium |
| `cypher/cypher-support.md` | 29 | No exec summary; not linked to clause pages | **High** |
| `getting-started/clients.md` | 29 | Tables don't extract; no "which to choose" | Medium |
| `cypher/indexing/vector-index.md` | 29 | Doesn't say "HNSW"; no comparison to vector DBs | **High** |
| `getting-started/configuration.md` | 30 | No question headings; no parameter quick-index | Medium |
| `getting-started/index.md` | 31 | No HowTo JSON-LD | Medium |
| `operations/index.md` | 31 | No deployment-decision matrix | Medium |
| Browser UI pages (template) | 31 | No freshness signal; UI changes constantly | **High** |
| `algorithms/*` (template) | 32 | No complexity / GDS comparison | Medium |
| `commands/graph.*.md` (template) | 33 | No `since:`, no errors section | Medium |
| `commands/graph.query.md` | 33 | No JSON-LD; no since version | Medium |
| `genai-tools/mcpserver/quickstart.md` | 33 | `search_exclude: true` blocks site search | **High** (1-line fix) |
| `algorithms/pagerank.md` | 33 | No GDS comparison | Medium |
| `algorithms/index.md` | 34 | No decision matrix vs Neo4j GDS | Medium |
| `cypher/index.md` | 34 | No question headings | Medium |
| `datatypes.md` | 34 | No Q&A; no Neo4j comparison | Medium |
| `browser/index.md` | 34 | No freshness; no "vs Neo4j Browser" | Medium |
| `udfs/flex/index.md` | 34 | No APOC comparison | Medium |
| `operations/replication.md` | 34 | No Causal Cluster comparison | Low |
| `operations/migration/redisgraph-to-falkordb.md` | 35 | No "what's different" section | Low |
| `commands/graph.profile.md` | 36 | No JSON-LD | Low |
| `operations/cluster.md` | 37 | No JSON-LD; otherwise excellent | Low |
| `cypher/known-limitations.md` | 37 | Should be FAQPage JSON-LD | Low |
| `udfs/flex/**` (template, 50 pages) | 37 | No JSON-LD; no `since:` | Medium (high leverage) |
| `operations/migration/neo4j-to-falkordb.md` | 38 | No HowTo JSON-LD | Low |
| `agentic-memory/index.md` | 39 | No FAQPage JSON-LD; otherwise model template | Low |

---

### Top 5 site-wide patterns

#### 1. Zero JSON-LD across 172 files (highest impact)

`jekyll-seo-tag` provides OG/Twitter tags but no structured data. Add a single `_includes/structured_data.html` that switches on `page.structured_type` frontmatter and emits `application/ld+json`. Wire it into the default layout. One change → every page improved.

```liquid
{% if page.structured_type %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "{{ page.structured_type }}",
  "name": "{{ page.title | escape }}",
  "description": "{{ page.description | escape }}",
  "url": "{{ page.url | absolute_url }}"
}
</script>
{% endif %}
```

Then add `structured_type: TechArticle` (or `HowTo`, `FAQPage`, `SoftwareApplication`) to each page's frontmatter.

#### 2. No `last_modified_at` on any page

AI engines treat undated content as low-confidence. Add to `_config.yml`:

```yaml
defaults:
  - scope: { path: "" }
    values:
      last_modified_at: true
```

Add to `_includes/head_custom.html`:
```html
<meta property="article:modified_time" content="{{ page.last_modified_at | default: site.time | date_to_xmlschema }}">
```

#### 3. Headings are categorical, not query-shaped

The `agentic-memory/index.md` H2 pattern ("What is Agentic Memory?", "Why FalkorDB for Agentic Memory?") should be the site standard. AI engines match user-query phrasing to headings. Adopt a style guide: every section H2 should be phrased as a question a user would type.

#### 4. No competitive / comparative signals anywhere except migration guides

The two highest-volume AI queries about any database are `"X vs Y"` and `"alternative to X"`. FalkorDB's most likely queries are `"FalkorDB vs Neo4j"` and `"alternative to RedisGraph"`. Yet no page mentions Neo4j by name except the migration guide. 

Add a `/comparisons/` section:
- `falkordb-vs-neo4j.md`
- `falkordb-vs-redisgraph.md`
- `falkordb-vs-memgraph.md`
- `falkordb-cloud-vs-neo4j-aura.md`

Plus "Neo4j equivalent: …" inline notes on every command and Cypher clause page.

#### 5. `description:` frontmatter is overlong and marketing-toned

Several `description:` fields exceed 160 characters or lead with adjectives. Tighten them to sub-160-char direct answers beginning with the entity name.

**Example:**
- Before: `"Build intelligent GenAI applications with FalkorDB and LLMs using popular GraphRAG and agent frameworks like LangChain and LlamaIndex."`
- After: `"FalkorDB integrates with LangChain, LlamaIndex, AG2, LangGraph, and the AWS GraphRAG Toolkit for building GraphRAG and agentic AI applications."`

---

### Highest-leverage immediate actions

| Action | Files affected | Effort | AEO impact |
|---|---|---|---|
| Add JSON-LD include to default Jekyll layout | 172 | 30 min | ★★★★★ |
| Add `last_modified_at` defaults in `_config.yml` + meta tag | 172 | 15 min | ★★★★ |
| Create `/comparisons/` section with `falkordb-vs-neo4j.md` | +5 new pages | 4 h | ★★★★★ |
| Add 1-line "What is X?" definition to every section index | 12 | 2 h | ★★★★ |
| Remove `search_exclude: true` from `genai-tools/mcpserver/quickstart.md` | 1 | 1 min | ★★★ |
| Add "HNSW" keyword to `cypher/indexing/vector-index.md` | 1 | 1 min | ★★★ |
