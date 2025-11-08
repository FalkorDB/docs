---
title: "Graphiti"
parent: "Agentic Memory"
nav_order: 1
description: "Build temporally-aware knowledge graphs with Graphiti and FalkorDB"
---

# Graphiti

[Graphiti](https://github.com/getzep/graphiti) is a Python framework for building **temporally-aware, multi-tenant knowledge graphs** designed for multi-agent AI systems with persistent memory. It enables real-time integration of structured and unstructured data, supporting advanced hybrid search, temporal reasoning, and collaborative agent memory.

## Overview

Graphiti provides a powerful abstraction layer for building knowledge graphs that:

* **Track temporal changes**: Understand how entities and relationships evolve over time
* **Support multi-tenancy**: Isolated memory spaces for different users or agents
* **Enable hybrid search**: Combine semantic search with graph traversal
* **Scale efficiently**: Built on top of FalkorDB's high-performance graph engine

## Why Graphiti + FalkorDB?

### FalkorDB's Added Value

* **Multi-tenant, multi-agent memory**: Isolated graph instances for different users or agents, each with their own persistent memory
* **High performance**: Fast graph operations and efficient memory usage
* **Cloud and on-premises ready**: Works with FalkorDB Cloud or your own deployment
* **Easy integration**: Seamless connection with Graphiti for scalable, production-ready knowledge graphs

### Use Cases

* **AI memory for multi-agent systems**: Provide persistent, context-rich memory for each agent
* **Enterprise knowledge management**: Aggregate and search across documents, conversations, and structured data
* **Conversational AI**: Track facts, entities, and relationships over time for more accurate responses
* **E-commerce**: Manage inventory, personalize recommendations, and track customer interactions over time
* **Research and analytics**: Temporal and semantic search across large, heterogeneous datasets

## Getting Started

### Prerequisites

* Python 3.10 or higher
* FalkorDB instance (Cloud or self-hosted)
* OpenAI API key (for embeddings and LLM features)

### Installation

Install Graphiti with FalkorDB support:

```bash
pip install graphiti-core[falkordb]
```

### Quick Start Example

Here's a complete example to get you started with Graphiti and FalkorDB:

```python
import asyncio
from datetime import datetime
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

async def main():
    # Initialize Graphiti with FalkorDB
    graphiti = Graphiti(
        uri="falkor://localhost:6379",  # Your FalkorDB connection string
        # For FalkorDB Cloud:
        # uri="falkor://your-instance.falkordb.cloud:6379",
        # username="default",
        # password="your-password"
    )
    
    # Build indices (run once during setup)
    await graphiti.build_indices_and_constraints()
    
    # Add an episode (information to be stored in the graph)
    episode_body = """
    Alice met Bob at the AI conference in San Francisco on March 15, 2024.
    They discussed the latest developments in graph databases and decided to 
    collaborate on a new project using FalkorDB.
    """
    
    await graphiti.add_episode(
        name="Conference Meeting",
        episode_body=episode_body,
        episode_type=EpisodeType.text,
        reference_time=datetime(2024, 3, 15),
        source_description="Conference notes"
    )
    
    # Search the knowledge graph
    search_results = await graphiti.search(
        query="What did Alice and Bob discuss?",
        num_results=5
    )
    
    print("Search Results:")
    for result in search_results:
        print(f"- {result}")
    
    # Close the connection
    await graphiti.close()

# Run the example
asyncio.run(main())
```

### Understanding the Code

1. **Initialize Graphiti**: Connect to your FalkorDB instance with the connection URI
2. **Build Indices**: Create necessary graph indices and constraints (one-time setup)
3. **Add Episodes**: Store information as "episodes" - chunks of text or structured data with temporal context
4. **Search**: Query the graph using natural language or specific parameters
5. **Close**: Clean up connections when done

## Advanced Features

### Hybrid Search

Graphiti supports multiple search types:

```python
# Node search - find specific entities
nodes = await graphiti.retrieve_nodes(
    query="Alice",
    num_results=10
)

# Episode search - find specific conversations/events
episodes = await graphiti.retrieve_episodes(
    query="conference meeting",
    num_results=5
)

# Combined hybrid search
results = await graphiti.search(
    query="project collaboration",
    num_results=10
)
```

### Temporal Queries

Query the graph at specific points in time:

```python
from datetime import datetime

# Get the state of knowledge at a specific time
results = await graphiti.search(
    query="What projects was Alice working on?",
    reference_time=datetime(2024, 3, 1),
    num_results=5
)
```

### Multi-Tenant Architecture

Create isolated graphs for different users or agents:

```python
# User 1's graph
graphiti_user1 = Graphiti(
    uri="falkor://localhost:6379",
    graph_name="user1_memory"
)

# User 2's graph
graphiti_user2 = Graphiti(
    uri="falkor://localhost:6379",
    graph_name="user2_memory"
)
```

## Configuration Options

### Connection Parameters

```python
graphiti = Graphiti(
    uri="falkor://localhost:6379",
    username="your-username",  # For authenticated instances
    password="your-password",
    graph_name="my_graph",     # Custom graph name
    llm_provider="openai",     # LLM provider for entity extraction
    embedding_provider="openai" # Embedding provider for vector search
)
```

### Custom LLM Configuration

```python
from graphiti_core.llm_client import OpenAIClient

llm_client = OpenAIClient(
    api_key="your-openai-key",
    model="gpt-4",
    temperature=0.7
)

graphiti = Graphiti(
    uri="falkor://localhost:6379",
    llm_client=llm_client
)
```

## Best Practices

1. **Batch Episodes**: When loading large amounts of data, batch your episodes for better performance
2. **Set Reference Times**: Always provide reference times for temporal tracking
3. **Use Descriptive Names**: Give episodes meaningful names for easier retrieval
4. **Index Strategy**: Build indices once during setup, not on every run
5. **Connection Pooling**: Reuse Graphiti instances when possible instead of creating new connections

## Troubleshooting

### Connection Issues

If you can't connect to FalkorDB:

* Verify your connection string format: `falkor://host:port`
* Check if FalkorDB is running: `redis-cli ping`
* Ensure credentials are correct for authenticated instances

### Performance Optimization

* Use batching for bulk operations
* Monitor memory usage with `GRAPH.MEMORY USAGE` command
* Consider graph partitioning for very large knowledge bases

## Resources

* 📚 [Graphiti Documentation](https://help.getzep.com/graphiti/)
* 🎥 [Workshop: How to Build a Knowledge Graph ft. Graphiti](https://www.youtube.com/watch?v=F4hwuLlISP4&lc=UgwPSaR6GAM_86g9AxJ4AaABAg)
* 📓 [Blog: Get Started with Graphiti](https://www.falkordb.com/blog/graphiti-get-started/)
* 💻 [Graphiti GitHub Repository](https://github.com/getzep/graphiti)
* 📝 [Google Colab Example](https://colab.research.google.com/drive/1HbDPKlsz9tYfRGeWHn60vsWeGhFIsqyF?usp=sharing)
* 🔗 [FalkorDB Configuration Guide](https://help.getzep.com/graphiti/configuration/graph-db-configuration#falkordb)

## Next Steps

* Explore [Cognee](./cognee.md) for alternative memory management approaches
* Learn about [GenAI Tools](/genai-tools) for graph reasoning and LLM integrations
