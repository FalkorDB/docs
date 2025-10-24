---
title: "LlamaIndex"
nav_order: 5
description: "Build efficient GraphRAG systems with LlamaIndex and FalkorDB."
parent: "GenAI Tools"
---

# LlamaIndex

[LlamaIndex](https://www.llamaindex.ai/) is an open-source framework designed to simplify the development of LLM-powered applications. It provides tools for ingesting, indexing, and querying diverse data sources.

In a typical RAG (Retrieval-Augmented Generation) setup, LlamaIndex orchestrates both the retrieval and generation phases. FalkorDB powers the retrieval module using Cypher queries, while any LLM trained on Cypher can handle the generation step—making it a natural fit for graph-native workflows.

## Resources

- 🔗 [FalkorDB Graph Store Demo](https://gpt-index.readthedocs.io/en/latest/examples/index_structs/knowledge_graph/FalkorDBGraphDemo.html)  
- 📓 [Blog: LlamaIndex RAG – Build Efficient GraphRAG Systems](https://www.falkordb.com/blog/llamaindex-rag-implementation-graphrag/)
- 🔗 [LlamaIndex Documentation](https://docs.llamaindex.ai/)

## Installation

Install LlamaIndex with FalkorDB support:

```bash
pip install llama-index llama-index-graph-stores-falkordb
```

## Quick Start

### 1. Initialize FalkorDB Graph Store

```python
from llama_index.graph_stores.falkordb import FalkorDBGraphStore
from llama_index.core import (
    KnowledgeGraphIndex,
    SimpleDirectoryReader,
    StorageContext,
)
import os

# Initialize FalkorDB graph store
graph_store = FalkorDBGraphStore(
    hostname=os.getenv("FALKORDB_HOST", "localhost"),
    port=int(os.getenv("FALKORDB_PORT", 6379)),
    username=os.getenv("FALKORDB_USERNAME"),
    password=os.getenv("FALKORDB_PASSWORD"),
    database="my_knowledge_graph",
)

# Create storage context
storage_context = StorageContext.from_defaults(graph_store=graph_store)
```

### 2. Build Knowledge Graph from Documents

```python
from llama_index.core import Document

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Or create documents manually
documents = [
    Document(text="John Smith is the CEO of TechCorp."),
    Document(text="TechCorp is based in San Francisco."),
    Document(text="TechCorp develops AI software."),
]

# Build knowledge graph index
index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    max_triplets_per_chunk=10,
    include_embeddings=True,
)
```

### 3. Query the Knowledge Graph

```python
# Create query engine
query_engine = index.as_query_engine(
    include_text=True,
    response_mode="tree_summarize",
    embedding_mode="hybrid",
)

# Query with natural language
response = query_engine.query("Who is the CEO of TechCorp?")
print(response)

# Follow-up questions
response = query_engine.query("Where is TechCorp located?")
print(response)
```

## Advanced Usage

### Custom Cypher Queries

```python
from llama_index.core.query_engine import CustomQueryEngine

# Execute custom Cypher query
cypher_query = """
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE c.name = 'TechCorp'
RETURN p.name, p.title, c.name
"""

result = graph_store.query(cypher_query)
print(result)
```

### Graph RAG with Embedding-Based Retrieval

```python
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding

# Initialize embedding model
embed_model = OpenAIEmbedding()

# Create knowledge graph with embeddings
kg_index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=embed_model,
    include_embeddings=True,
)

# Create query engine with hybrid retrieval
query_engine = kg_index.as_query_engine(
    embedding_mode="hybrid",
    similarity_top_k=5,
    response_mode="tree_summarize",
)

response = query_engine.query(
    "What are the main products of companies in the tech sector?"
)
print(response)
```

### Building Knowledge Graph from Structured Data

```python
import pandas as pd
from llama_index.core.schema import TextNode

# Load structured data
df = pd.read_csv("companies.csv")

# Convert to documents
nodes = []
for _, row in df.iterrows():
    text = f"{row['company_name']} is located in {row['city']}. "
    text += f"It operates in the {row['industry']} sector. "
    text += f"Founded in {row['founded_year']}."
    
    node = TextNode(
        text=text,
        metadata={
            "company_id": row["id"],
            "industry": row["industry"],
        }
    )
    nodes.append(node)

# Build index from nodes
index = KnowledgeGraphIndex(
    nodes=nodes,
    storage_context=storage_context,
)
```

### Multi-Modal Knowledge Graphs

```python
from llama_index.core import download_loader

# Load image documents
ImageReader = download_loader("ImageReader")
image_documents = ImageReader().load_data(file_path="./images")

# Load text documents
text_documents = SimpleDirectoryReader("./text").load_data()

# Combine and index
all_documents = text_documents + image_documents

index = KnowledgeGraphIndex.from_documents(
    all_documents,
    storage_context=storage_context,
    show_progress=True,
)
```

### Incremental Updates

```python
# Add new documents to existing graph
new_documents = [
    Document(text="TechCorp acquired StartupXYZ in 2024."),
    Document(text="StartupXYZ specializes in machine learning."),
]

# Insert into existing index
for doc in new_documents:
    index.insert(doc)

# Query with updated data
response = query_engine.query("What companies has TechCorp acquired?")
print(response)
```

### Graph Visualization and Export

```python
# Get graph data
graph_data = graph_store.get_graph_data()

# Export to NetworkX format for visualization
import networkx as nx

G = nx.DiGraph()

for node in graph_data.nodes:
    G.add_node(node.id, **node.properties)

for edge in graph_data.edges:
    G.add_edge(edge.source, edge.target, **edge.properties)

# Visualize (requires matplotlib)
import matplotlib.pyplot as plt

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', 
        node_size=500, font_size=8, arrows=True)
plt.show()
```

### Custom Schema Definition

```python
from llama_index.core.indices.knowledge_graph import KGTableSchema

# Define custom schema
schema = KGTableSchema(
    entity_types=["Person", "Company", "Product", "Location"],
    relation_types=["WORKS_AT", "LOCATED_IN", "PRODUCES", "FOUNDED_BY"],
)

# Build index with custom schema
index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context=storage_context,
    kg_table_schema=schema,
)
```

## Use Cases

- **Document Q&A**: Extract entities and relationships from unstructured documents
- **Enterprise Knowledge Management**: Build searchable knowledge graphs from company data
- **Research and Discovery**: Link concepts across large document collections
- **Recommendation Systems**: Leverage graph relationships for personalized recommendations
- **Data Integration**: Unify data from multiple sources into a coherent knowledge graph

## Best Practices

1. **Chunk Size**: Adjust chunk size based on document structure (default: 512 tokens)
2. **Triplet Extraction**: Tune `max_triplets_per_chunk` based on content density
3. **Embedding Strategy**: Use hybrid mode for better retrieval (combines text and structure)
4. **Schema Design**: Define clear entity and relationship types for consistent graphs
5. **Incremental Updates**: Use `insert()` for adding new data without full re-indexing
6. **Query Optimization**: Use `similarity_top_k` to control retrieval scope

## Performance Tips

- **Batch Processing**: Process documents in batches for large datasets
- **Parallel Indexing**: Enable parallel processing for faster indexing
- **Caching**: Cache embeddings to avoid recomputation
- **Index Persistence**: Save and load indexes to avoid rebuilding

```python
# Save index
index.storage_context.persist(persist_dir="./storage")

# Load index
from llama_index.core import load_index_from_storage

storage_context = StorageContext.from_defaults(
    persist_dir="./storage",
    graph_store=graph_store,
)
index = load_index_from_storage(storage_context)
```

## Resources

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [FalkorDB Graph Store Documentation](https://docs.llamaindex.ai/en/stable/examples/index_structs/knowledge_graph/FalkorDBGraphDemo/)
- [Blog: LlamaIndex RAG Implementation](https://www.falkordb.com/blog/llamaindex-rag-implementation-graphrag/)
- [LlamaIndex GitHub Repository](https://github.com/run-llama/llama_index)
