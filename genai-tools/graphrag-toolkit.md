---
title: "GraphRAG Toolkit"
nav_order: 6
description: "AWS GraphRAG Toolkit integration with FalkorDB for building knowledge graph applications. Semantic-guided search, LLM-powered retrieval, and FalkorDB Cloud support for RAG systems."
parent: "GenAI Tools"
---

# GraphRAG Toolkit

AWS GraphRAG Toolkit is an open-source framework for building knowledge graph applications with Large Language Models (LLMs). FalkorDB is supported as a graph store backend, enabling you to leverage FalkorDB's high-performance graph database capabilities in your GraphRAG applications.

## Overview

The GraphRAG Toolkit provides tools and patterns for building retrieval-augmented generation (RAG) applications that use knowledge graphs. With FalkorDB as the graph store, you can:

- Build and query knowledge graphs efficiently
- Use semantic-guided search for intelligent retrieval
- Connect to FalkorDB Cloud or local instances
- Integrate with LLM-powered applications

## Installation

The FalkorDB graph store is contained in a separate contributor package. Install it using:

```bash
pip install https://github.com/awslabs/graphrag-toolkit/archive/refs/tags/v3.13.3.zip#subdirectory=lexical-graph-contrib/falkordb
```

## Quick Start

### 1. Register FalkorDB as a Graph Store

Before creating a FalkorDB graph store, register the `FalkorDBGraphStoreFactory` with the `GraphStoreFactory`:

```python
from graphrag_toolkit.lexical_graph.storage import GraphStoreFactory
from graphrag_toolkit_contrib.lexical_graph.storage.graph.falkordb import FalkorDBGraphStoreFactory

GraphStoreFactory.register(FalkorDBGraphStoreFactory)
```

### 2. Create a FalkorDB Graph Store

You can use the `GraphStoreFactory.for_graph_store()` static factory method to create an instance of a FalkorDB graph store.

#### Using FalkorDB Cloud

To create a [FalkorDB Cloud](https://app.falkordb.cloud) graph store, supply a connection string that begins with `falkordb://`, followed by your FalkorDB endpoint:

```python
from graphrag_toolkit.lexical_graph.storage import GraphStoreFactory
from graphrag_toolkit_contrib.lexical_graph.storage.graph.falkordb import FalkorDBGraphStoreFactory

falkordb_connection_info = 'falkordb://your-falkordb-endpoint'

GraphStoreFactory.register(FalkorDBGraphStoreFactory)

with GraphStoreFactory.for_graph_store(falkordb_connection_info) as graph_store:
    # Your code here
    pass
```

You may need to pass credentials and SSL configuration:

```python
from graphrag_toolkit.lexical_graph.storage import GraphStoreFactory
from graphrag_toolkit_contrib.lexical_graph.storage.graph.falkordb import FalkorDBGraphStoreFactory

falkordb_connection_info = 'falkordb://<your-falkordb-endpoint>'

GraphStoreFactory.register(FalkorDBGraphStoreFactory)

with GraphStoreFactory.for_graph_store(
    falkordb_connection_info,
    username='<username>',
    password='<password>',
    ssl=True
) as graph_store:
    # Your code here
    pass
```

#### Using Local FalkorDB

To create a local FalkorDB graph store, supply a connection string with only `falkordb://`:

```python
from graphrag_toolkit.lexical_graph.storage import GraphStoreFactory
from graphrag_toolkit_contrib.lexical_graph.storage.graph.falkordb import FalkorDBGraphStoreFactory

falkordb_connection_info = 'falkordb://'

GraphStoreFactory.register(FalkorDBGraphStoreFactory)

with GraphStoreFactory.for_graph_store(falkordb_connection_info) as graph_store:
    # Your code here
    pass
```

### 3. Start FalkorDB (Local Setup)

If you're using a local instance, start FalkorDB with Docker:

```bash
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:edge
```

Or sign up for [FalkorDB Cloud](https://app.falkordb.cloud) for a managed solution.

## Features

### Semantic-Guided Search

The FalkorDB graph store supports semantic-guided search, enabling intelligent retrieval based on meaning and context rather than just keyword matching.

**Note:** The FalkorDB graph store currently does not support traversal-based search.

## Resources

- 🔗 [AWS GraphRAG Toolkit GitHub Repository](https://github.com/awslabs/graphrag-toolkit)
- 📖 [GraphRAG Toolkit Documentation](https://github.com/awslabs/graphrag-toolkit/tree/main/docs)
- 📓 [FalkorDB Graph Store Documentation](https://github.com/awslabs/graphrag-toolkit/blob/main/docs/lexical-graph/graph-store-falkor-db.md)
- ☁️ [FalkorDB Cloud](https://app.falkordb.cloud)

## Use Cases

- **Knowledge Graph Construction**: Build structured knowledge graphs from unstructured data
- **Semantic Search**: Implement context-aware search using graph-based retrieval
- **Question Answering**: Combine LLMs with graph data for accurate responses
- **Document Understanding**: Extract and organize information in a knowledge graph

## Related Tools

- [GraphRAG-SDK](./graphrag-sdk.md): FalkorDB's native GraphRAG solution
- [LangChain](./langchain.md): Build AI agents with graph memory
- [LlamaIndex](./llamaindex.md): LLM application framework with FalkorDB support

{% include faq_accordion.html title="Frequently Asked Questions" q1="What is the AWS GraphRAG Toolkit?" a1="The AWS GraphRAG Toolkit is an open-source framework from AWS Labs for building knowledge graph applications with LLMs. FalkorDB is supported as a graph store backend through a separate contributor package, enabling high-performance graph database capabilities in GraphRAG applications." q2="How do I install FalkorDB support for the GraphRAG Toolkit?" a2="Install the FalkorDB graph store contributor package using: `pip install https://github.com/awslabs/graphrag-toolkit/archive/refs/tags/v3.13.3.zip#subdirectory=lexical-graph-contrib/falkordb`" q3="Can I use FalkorDB Cloud with the GraphRAG Toolkit?" a3="Yes. Use a connection string starting with `falkordb://` followed by your FalkorDB Cloud endpoint. You can pass `username`, `password`, and `ssl=True` parameters to `GraphStoreFactory.for_graph_store()` for secure authentication." q4="Does the toolkit support traversal-based search?" a4="No, the FalkorDB graph store currently supports **semantic-guided search** only, enabling intelligent retrieval based on meaning and context. Traversal-based search is not yet supported." q5="How does this differ from the FalkorDB GraphRAG-SDK?" a5="The AWS GraphRAG Toolkit is a broader AWS framework where FalkorDB is one of several possible graph stores. The FalkorDB GraphRAG-SDK is FalkorDB's native solution with tighter integration, ontology extraction, and conversational sessions built specifically for FalkorDB." %}
