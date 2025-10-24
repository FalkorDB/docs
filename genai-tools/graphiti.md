---
title: "Graphiti"
nav_order: 2
description: "Temporally-aware, multi-tenant live knowledge graph for multi-agent AI systems."
parent: "GenAI Tools"
---

# Graphiti

[Graphiti](https://help.getzep.com/graphiti/configuration/graph-db-configuration#falkordb) is a Python framework for building temporally-aware, multi-tenant live knowledge graph designed for multi-agent AI systems with persistent memory. It enables real-time integration of structured and unstructured data, supporting advanced hybrid search, temporal reasoning, and collaborative agent memory.

> **August 2025 Update**: Watch our "How to Build a Knowledge Graph ft. Gaphiti" in collaboration with Graphiti:
> 
> [Workshop recording](https://www.youtube.com/watch?v=F4hwuLlISP4&lc=UgwPSaR6GAM_86g9AxJ4AaABAg)
> [Google Collab](https://colab.research.google.com/drive/1HbDPKlsz9tYfRGeWHn60vsWeGhFIsqyF?usp=sharing)

## FalkorDB's Added Value

- **Multi-tenant, multi-agent memory**: Isolated graph instances for different users or agents, each with their own persistent memory.
- **High performance**: Fast graph operations and efficient memory usage.
- **Cloud and on-premises ready**: Works with FalkorDB Cloud or your own deployment.
- **Easy integration**: Seamless connection with Graphiti for scalable, production-ready knowledge graphs.

## Use Cases

- **AI memory for multi-agent systems**: Provide persistent, context-rich memory for each agent.
- **Enterprise knowledge management**: Aggregate and search across documents, conversations, and structured data.
- **Conversational AI**: Track facts, entities, and relationships over time for more accurate responses.
- **E-commerce**: Manage inventory, personalize recommendations, and track customer interactions over time.
- **Research and analytics**: Temporal and semantic search across large, heterogeneous datasets.

## Installation

Install Graphiti with FalkorDB support:

```bash
pip install graphiti-core[falkordb]
```

## Quick Start

### 1. Connect to FalkorDB

```python
import os
from graphiti_core import Graphiti
from graphiti_core.edges import EntityEdge
from graphiti_core.nodes import EpisodeType

# Initialize FalkorDB connection
graphiti = Graphiti(
    host=os.getenv("FALKORDB_HOST", "localhost"),
    port=int(os.getenv("FALKORDB_PORT", 6379)),
    username=os.getenv("FALKORDB_USERNAME"),
    password=os.getenv("FALKORDB_PASSWORD"),
)
```

### 2. Build Indices

```python
# Build required indices and constraints
await graphiti.build_indices_and_constraints()
```

### 3. Add Episodes

```python
# Add an episode (a piece of information)
episode_text = """
John Smith is the CEO of TechCorp, a software company based in San Francisco.
He has over 15 years of experience in the technology industry.
"""

await graphiti.add_episode(
    name="john_smith_info",
    episode_body=episode_text,
    episode_type=EpisodeType.text,
    source_description="Company directory",
)
```

### 4. Search the Knowledge Graph

```python
# Perform a hybrid search
results = await graphiti.search(
    query="Who is the CEO of TechCorp?",
    num_results=5,
)

for result in results:
    print(f"Entity: {result.name}")
    print(f"Summary: {result.summary}")
    print("---")
```

## Advanced Usage

### Multi-Tenant Configuration

```python
# Create separate graph instances for different tenants
tenant_a_graphiti = Graphiti(
    host="localhost",
    port=6379,
    graph_name="tenant_a_knowledge",
)

tenant_b_graphiti = Graphiti(
    host="localhost",
    port=6379,
    graph_name="tenant_b_knowledge",
)
```

### Adding JSON Episodes

```python
# Add structured data
episode_data = {
    "customer_id": "C12345",
    "name": "Jane Doe",
    "purchases": ["laptop", "mouse", "keyboard"],
    "total_spent": 1500.00,
}

await graphiti.add_episode(
    name="customer_purchase",
    episode_body=episode_data,
    episode_type=EpisodeType.json,
    source_description="E-commerce database",
)
```

### Node Search

```python
# Search for specific entities
nodes = await graphiti.search_nodes(
    query="TechCorp employees",
    num_results=10,
)

for node in nodes:
    print(f"Entity: {node.name}, Type: {node.label}")
```

## Resources

- [Graphiti Documentation](https://help.getzep.com/graphiti/)
- [Graphiti GitHub Repository](https://github.com/getzep/graphiti)
- [Quickstart Example with FalkorDB](https://github.com/getzep/graphiti/blob/main/examples/quickstart/quickstart_falkordb.py)
