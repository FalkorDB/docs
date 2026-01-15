---
title: "Knowledge Graph RAG"
description: "Build a retrieval-augmented generation flow on top of FalkorDB."
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<!-- markdownlint-disable MD025 MD033 -->

# Knowledge Graph RAG

This tutorial shows how to ingest documents, create embeddings, and query FalkorDB for retrieval-augmented generation (RAG). Pair it with the [GraphRAG SDK](/genai-tools/graphrag-sdk) or your preferred LLM stack.

## 1) Model the data

Represent documents as `Doc` nodes and connect them to entities or topics you extract. Keep embeddings on the node for fast similarity search.

```cypher
// Minimal schema
CREATE CONSTRAINT doc_id IF NOT EXISTS FOR (d:Doc) REQUIRE d.id IS UNIQUE;
CREATE RANGE INDEX doc_title IF NOT EXISTS FOR (d:Doc) ON (d.title);
```

## 2) Create a vector index

Use FalkorDB’s vector index to support embedding search:

```cypher
CREATE VECTOR INDEX FOR (d:Doc) ON (d.embedding)
OPTIONS {dimension:768, similarityFunction:'cosine', efConstruction:200, efRuntime:20};
```

## 3) Ingest documents with embeddings

Choose any embedding provider (OpenAI, Azure, OSS). Insert the text, metadata, and the embedding vector. Example in Python:

<Tabs groupId="programming-language">
  <TabItem value="python" label="Python">

```python
from falkordb import FalkorDB

client = FalkorDB(host="localhost", port=6379, password="your-password")
graph = client.select_graph("rag")

# text -> embedding step (replace with your embedding API)
text = "FalkorDB supports Cypher and vector search."
embedding = [0.01] * 768  # placeholder vector; use real embeddings

query = """
CREATE (d:Doc {id: $id, title: $title, body: $body, embedding: vecf32($embedding)})
RETURN d.id
"""

graph.query(query, {
    "id": "doc-1",
    "title": "FalkorDB Overview",
    "body": text,
    "embedding": embedding,
})
```

  </TabItem>
</Tabs>

## 4) Run hybrid retrieval

Combine vector similarity with structured filters (labels, topics, recency):

```cypher
CALL db.idx.vector.queryNodes(
  label: 'Doc',
  attribute: 'embedding',
  k: 5,
  vector: vecf32($embedding)
) YIELD node, score
WITH node, score
WHERE score >= 0.5 AND node.title CONTAINS $keyword
RETURN node.id AS id, node.title AS title, score
ORDER BY score DESC
LIMIT 5;
```

## 5) Generate an answer

Send the retrieved snippets plus any related entities/relationships to your LLM. For example, fetch adjacent entities for grounding:

```cypher
MATCH (d:Doc {id: $id})-[r]->(neighbor)
RETURN d.title AS doc, type(r) AS relation, neighbor LIMIT 10;
```

## 6) Next steps

- Automate ingestion pipelines with the [GraphRAG Toolkit](/genai-tools/graphrag-toolkit) or [LangChain integration](/genai-tools/langchain).
- Monitor recall by adjusting vector index parameters (`M`, `efConstruction`, `efRuntime`) and the similarity threshold.
- Add provenance fields (source URL, checksum, createdAt) and return them with responses to improve traceability.
