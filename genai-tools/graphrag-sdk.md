---
title: "GraphRAG-SDK"
nav_order: 1
description: "Build intelligent GraphRAG applications with FalkorDB and LLMs."
parent: "GenAI Tools"
redirect_from:
  - /graphrag_sdk.html
  - /graphrag_sdk
  - /graphrag-sdk.html
  - /graphrag-sdk
---

# GraphRAG-SDK

## Build intelligent GraphRAG applications with FalkorDB and LLMs

- Ingest raw documents (text, PDF, Markdown) directly into a FalkorDB knowledge graph with schema-guided entity extraction.
- Retrieve cited answers via a hybrid pipeline that combines vector search, full-text search, Cypher generation, and relationship expansion.
- Update the graph **incrementally** on PR merges with `apply_changes()` — re-sync individual documents without rebuilding.
- Plug in any LLM or embedder via LiteLLM (OpenAI, Azure, Anthropic, Gemini, Groq, Cohere, local models, etc.).
- **Benchmark-leading accuracy** — the top score on [GraphRAG-Bench](https://graphrag-bench.github.io) across both multi-document and single-document question sets. See [benchmark methodology and results](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/benchmark.md).

**Resources:**
- [GraphRAG-SDK GitHub Repository](https://github.com/FalkorDB/GraphRAG-SDK)
- [Examples](#examples) — runnable starters covering quick start, schemas, custom strategies, and incremental updates
- [API Reference](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/api-reference.md)

| Guide | Description |
|-------|-------------|
| [Getting Started](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/getting-started.md) | Step-by-step tutorial from install to first query |
| [Architecture](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/architecture.md) | Pipeline design, graph schema, retrieval strategy |
| [Configuration](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/configuration.md) | Connection, providers, and tuning reference |
| [Strategies](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/strategies.md) | All ABCs and built-in implementations |
| [Providers](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/providers.md) | LLM and embedder configuration guide |
| [Benchmark](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/docs/benchmark.md) | Methodology, results, and reproduction instructions |

## Quick Start

### Install and start FalkorDB

```bash
pip install graphrag-sdk[litellm]
docker run -d -p 6379:6379 -p 3000:3000 --name falkordb falkordb/falkordb:latest
export OPENAI_API_KEY="sk-..."
```

For PDF ingestion, install the `pdf` extra instead: `pip install graphrag-sdk[litellm,pdf]`.

Or sign up for [FalkorDB Cloud](https://app.falkordb.cloud).

### Ingest and query

```python
import asyncio
from graphrag_sdk import GraphRAG, ConnectionConfig, LiteLLM, LiteLLMEmbedder

async def main():
    async with GraphRAG(
        connection=ConnectionConfig(host="localhost", graph_name="my_graph"),
        llm=LiteLLM(model="openai/gpt-4o-mini"),
        embedder=LiteLLMEmbedder(model="openai/text-embedding-3-large", dimensions=256),
    ) as rag:
        # Ingest raw text (or pass a file path for .md / .txt / .pdf)
        result = await rag.ingest(
            text="Alice Johnson is a software engineer at Acme Corp in London.",
            document_id="my_doc",
        )
        print(f"Nodes: {result.nodes_created}, Edges: {result.relationships_created}")

        # Finalize: deduplicate entities, backfill embeddings, build indexes
        await rag.finalize()

        # Full RAG: retrieve + generate with provenance
        answer = await rag.completion("Where does Alice work?")
        print(answer.answer)

asyncio.run(main())
```

### Define a schema (optional)

A schema constrains which entity and relation types the extractor produces. Without one the SDK runs open-world extraction; with one you get a tighter, more queryable graph.

> 💡 **Schema vs. ontology**: the SDK's `GraphSchema` is the concrete, code-level implementation of the broader concept often called an "ontology" in knowledge-graph literature — a controlled vocabulary of entity and relation types. This page uses **schema** throughout because that's the actual class and parameter name in the API (`GraphSchema`, `schema=...`); reach for "ontology" only when discussing the conceptual design behind a schema.

```python
from graphrag_sdk import GraphSchema, EntityType, RelationType

schema = GraphSchema(
    entities=[
        EntityType(label="Person", description="A human being"),
        EntityType(label="Organization", description="A company or institution"),
        EntityType(label="Location", description="A geographic location"),
    ],
    relations=[
        RelationType(label="WORKS_AT", description="Is employed by", patterns=[("Person", "Organization")]),
        RelationType(label="LOCATED_IN", description="Is situated in", patterns=[("Organization", "Location")]),
    ],
)

async with GraphRAG(
    connection=ConnectionConfig(host="localhost", graph_name="my_graph"),
    llm=LiteLLM(model="openai/gpt-4o-mini"),
    embedder=LiteLLMEmbedder(model="openai/text-embedding-3-large", dimensions=256),
    schema=schema,
) as rag:
    ...  # ingest / completion as above
```

## Incremental Updates

Re-sync individual documents without rebuilding the graph. The canonical CI use case is updating the graph on PR merge — added, modified, and deleted files in one batch:

```python
async with GraphRAG(connection=ConnectionConfig(...), llm=..., embedder=...) as graph:
    result = await graph.apply_changes(
        added=["docs/new_feature.md"],
        modified=["docs/api.md"],
        deleted=["docs/removed_page.md"],
    )
    await graph.finalize()  # once per batch — finalize is O(graph size)

    # Per-file outcomes are wrapped in BatchEntry — the batch never raises.
    for entry in result.added + result.modified + result.deleted:
        if not entry.is_success:
            print(f"failed: {entry.error_type}: {entry.error}")
```

The three primitives behind the wrapper:

| Method | When to use |
|---|---|
| `update(source, document_id=...)` | Document content changed. A SHA-256 content hash short-circuits no-op updates (touch-only PRs cost ~1 Cypher query). Pass `if_missing="ingest"` for upsert semantics. |
| `delete_document(document_id)` | Document removed. Cleans up entities orphaned by the deletion; preserves entities still referenced by other documents. |
| `apply_changes(added=..., modified=..., deleted=...)` | Heterogeneous batch. Per-file errors are collected, not raised. Does not call `finalize()` — caller drives that cadence. |

**Cost model.** `finalize()` runs cross-document deduplication, which scans the full entity table — its cost is **O(graph size)**, not O(change size). Embedding backfill within `finalize()` is O(change size) — only nodes/edges missing embeddings get touched. For CI use cases, batch all PR changes through `apply_changes` and call `finalize` **once** at the end of the run, not per file — per-file `finalize` multiplies the dedup constant by the number of files touched.

**Crash safety.** `update()` uses an idempotent rollforward cutover: new content is written to a `__pending__` document, a single atomic Cypher statement marks it `ready_to_commit=true`, then the live document is replaced. A crash before the marker discards the pending write on retry; a crash after the marker rolls forward to completion. Retrying the same `update()` call is always safe.

**Concurrency.** `apply_changes` exposes `max_concurrency` (adds, default `3`) and `update_concurrency` (modifies, default `1`). Updates default to `1` because orphan-cleanup correctness under concurrent updates depends on a pipeline-ordering invariant — raise it only if you've verified your concurrent updates never share an entity.

## Key Features

- **Schema-guided extraction** — Constrain the entity and relation types the LLM produces, or run open-world if you don't have a schema yet.
- **Hybrid retrieval** — Vector search, full-text search, Cypher generation, and relationship expansion combined in one pipeline.
- **Cited answers** — Every answer is traceable to its source chunks via `MENTIONS` edges; pass `return_context=True` to `completion()` to get the retrieval trail.
- **Incremental updates** — `apply_changes()` handles added/modified/deleted documents in one call, with crash-safe rollforward cutover.
- **Multi-tenant** — `graph_name` on the connection provides per-tenant isolation in a single FalkorDB instance.
- **Provider-agnostic** — Any LLM or embedder reachable via LiteLLM works out of the box; custom providers plug in behind clean ABCs.

### Getting the retrieval trail behind an answer

```python
answer = await rag.completion("Where does Alice work?", return_context=True)
print(answer.answer)
for chunk in answer.context.chunks:
    print(chunk.document_id, chunk.text)
```

## Examples

Runnable starters live in [`graphrag_sdk/examples`](https://github.com/FalkorDB/GraphRAG-SDK/tree/main/graphrag_sdk/examples):

| # | Example | What you'll build |
|---|---------|-------------------|
| 1 | [Quick Start](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/graphrag_sdk/examples/01_quickstart.py) | Your first ingest-and-query loop in under 30 lines |
| 2 | [PDF with Schema](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/graphrag_sdk/examples/02_pdf_with_schema.py) | A PDF Q&A bot with your own entity and relation types |
| 3 | [Custom Strategies](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/graphrag_sdk/examples/03_custom_strategies.py) | The benchmark-winning pipeline, ready to drop in |
| 4 | [Custom Provider](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/graphrag_sdk/examples/04_custom_provider.py) | Plug in any LLM or embedder behind a clean interface |
| 5 | [Notebook Demo](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/graphrag_sdk/examples/05_notebook_demo.ipynb) | An interactive walkthrough that shows the provenance trail |
| 7 | [Incremental Updates](https://github.com/FalkorDB/GraphRAG-SDK/blob/main/graphrag_sdk/examples/07_incremental_updates.py) | `update`, `delete_document`, and `apply_changes` for CI-driven graph syncs |

## How it works

### 1️⃣ Ingest documents into a knowledge graph
- **Document loading**: Markdown, plain text, and (with the `pdf` extra) PDF inputs go through structural-aware chunkers.
- **Entity extraction**: An LLM-driven extractor reads each chunk, optionally constrained by your schema.
- **Resolution**: Surface forms of the same entity are merged via exact-match plus optional LLM-verified resolution.
- **Provenance**: Chunks, entities, and relationships are connected by `PART_OF`, `NEXT_CHUNK`, and `MENTIONS` edges so every answer can be traced back to its source text.

### 2️⃣ Retrieve relevant context
- **Vector search** ranks chunks and entities by embedding similarity.
- **Full-text search** complements vectors with keyword precision.
- **Cypher generation** (experimental) lets the LLM emit graph queries directly for aggregate or structural questions.
- **Relationship expansion** traverses the graph from the seed hits to surface multi-hop context.
- **Reranking** orders the final passages by cosine similarity to the question.

### 3️⃣ Generate cited answers
- **Retrieval-grounded completion** combines the retrieved context with the user's question and feeds it to the LLM.
- **Source attribution** is built into the response — every answer points back to the chunks that supported it.

> 📓  [Understanding Ontologies and Knowledge Graphs](https://www.falkordb.com/blog/understanding-ontologies-knowledge-graph-schemas/)
