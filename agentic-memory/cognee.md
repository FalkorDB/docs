---
title: "Cognee"
parent: "Agentic Memory"
nav_order: 2
description: "Build flexible agentic memory with Cognee and FalkorDB"
---

# Cognee

[Cognee](https://github.com/topoteretes/cognee) is a memory management framework for AI agents that provides a flexible approach to storing and retrieving knowledge. It combines graph database capabilities with vector storage to create rich, context-aware memory systems.

## Overview

Cognee provides a comprehensive memory layer that:
- **Manages complex knowledge structures**: Store entities, relationships, and contextual information
- **Supports hybrid storage**: Combine graph databases with vector stores for optimal retrieval
- **Enables flexible querying**: Search by semantic similarity, graph relationships, or both
- **Scales with your needs**: From simple chatbots to complex multi-agent systems

## Why Cognee + FalkorDB?

### FalkorDB's Added Value

- **Native Graph Storage**: Efficient storage and traversal of entity relationships
- **Fast Queries**: Quick retrieval of connected information for context building
- **Flexible Schema**: Adapt to evolving knowledge structures without rigid schemas
- **Production Ready**: Scale from development to production seamlessly
- **Hybrid Capabilities**: Combine graph traversal with vector similarity search

### Use Cases

- **Conversational AI**: Build chatbots that remember and learn from past conversations
- **Knowledge Management**: Create organizational memory that captures relationships and context
- **Recommendation Systems**: Leverage connection patterns for personalized recommendations
- **Research Assistants**: Help AI agents navigate and understand complex information networks
- **Customer Support**: Provide context-aware responses based on customer history and relationships

## Getting Started

### Prerequisites

- Python 3.10 or higher
- FalkorDB instance (Cloud or self-hosted)
- API keys for LLM and embedding providers (if using those features)

### Installation

Install Cognee with the FalkorDB community adapter:

```bash
pip install cognee
pip install cognee-community-hybrid-adapter-falkor
```

### Quick Start Example

Here's a complete example to get you started with Cognee and FalkorDB:

```python
import asyncio
import os
import pathlib
from os import path
from cognee import config, prune, add, cognify, search, SearchType

# Import the register module to enable FalkorDB support
import cognee_community_hybrid_adapter_falkor.register

async def main():
    # Set up local directories
    system_path = pathlib.Path(__file__).parent
    config.system_root_directory(path.join(system_path, ".cognee_system"))
    config.data_root_directory(path.join(system_path, ".cognee_data"))
    
    # Configure relational database
    config.set_relational_db_config({
        "db_provider": "sqlite",
    })
    
    # Configure FalkorDB as both vector and graph database
    config.set_vector_db_config({
        "vector_db_provider": "falkordb",
        "vector_db_url": os.getenv("GRAPH_DB_URL", "localhost"),
        "vector_db_port": int(os.getenv("GRAPH_DB_PORT", "6379")),
    })
    config.set_graph_db_config({
        "graph_database_provider": "falkordb",
        "graph_database_url": os.getenv("GRAPH_DB_URL", "localhost"),
        "graph_database_port": int(os.getenv("GRAPH_DB_PORT", "6379")),
    })
    
    # Optional: Clean previous data
    await prune.prune_data()
    await prune.prune_system()
    
    # Add and process your content
    text_data = """
    Sarah is a software engineer at TechCorp. She specializes in machine learning
    and has been working on implementing graph-based recommendation systems.
    Sarah recently collaborated with Mike on a new project using FalkorDB.
    Mike is the lead data scientist at TechCorp.
    """
    
    await add(text_data)
    await cognify()
    
    # Search using graph completion
    search_results = await search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="What does Sarah work on?"
    )
    
    print("Search Results:")
    for result in search_results:
        print("\n" + result)

# Run the example
asyncio.run(main())
```

### Understanding the Code

1. **Import the FalkorDB Adapter**: Import `cognee_community_hybrid_adapter_falkor.register` to enable FalkorDB support
2. **Configure Directories**: Set up local directories for Cognee's system and data storage
3. **Configure Databases**: Set FalkorDB as both the vector and graph database for hybrid capabilities
4. **Add Data**: Provide text or structured data to be processed
5. **Cognify**: Process the data to extract entities and relationships
6. **Search**: Query the knowledge using different search types (graph completion, similarity, etc.)

## Advanced Features

### Search Types

Cognee supports different search types for various use cases:

```python
from cognee import search, SearchType

# Graph completion search - uses graph structure for context
graph_results = await search(
    query_type=SearchType.GRAPH_COMPLETION,
    query_text="machine learning projects"
)

# Similarity search - semantic vector search
similarity_results = await search(
    query_type=SearchType.SIMILARITY,
    query_text="machine learning projects"
)

# Insights search - combines multiple approaches
insights_results = await search(
    query_type=SearchType.INSIGHTS,
    query_text="machine learning projects"
)
```

### LLM Configuration

Configure the LLM provider for entity extraction and processing:

```python
import os
from cognee import config

# Set LLM API key
os.environ["LLM_API_KEY"] = "your-openai-api-key"

# Configure LLM provider
config.set_llm_config({
    "llm_provider": "openai",
    "llm_model": "gpt-4",
    "llm_temperature": 0.7
})
```

### Managing Knowledge

```python
from cognee import add, cognify, prune

# Add multiple documents
documents = [
    "Natural language processing is a subfield of AI.",
    "Machine learning models require training data.",
    "Graph databases excel at relationship queries."
]

for doc in documents:
    await add(doc)

await cognify()

# Reset memory (clear all data)
await prune.prune_data()
await prune.prune_system()
```

### Environment Variables

You can use environment variables for configuration:

```bash
export GRAPH_DB_URL="localhost"
export GRAPH_DB_PORT="6379"
export LLM_API_KEY="your-openai-api-key"
```

Then access them in your code:

```python
import os
from cognee import config

config.set_graph_db_config({
    "graph_database_provider": "falkordb",
    "graph_database_url": os.getenv("GRAPH_DB_URL", "localhost"),
    "graph_database_port": int(os.getenv("GRAPH_DB_PORT", "6379")),
})
```

## Configuration Options

### Database Configuration

```python
from cognee import config

# Relational database (for metadata)
config.set_relational_db_config({
    "db_provider": "sqlite",  # or "postgres"
})

# FalkorDB as graph database
config.set_graph_db_config({
    "graph_database_provider": "falkordb",
    "graph_database_url": "localhost",
    "graph_database_port": 6379,
})

# FalkorDB as vector database (hybrid mode)
config.set_vector_db_config({
    "vector_db_provider": "falkordb",
    "vector_db_url": "localhost",
    "vector_db_port": 6379,
})
```

### LLM Configuration

```python
import os
from cognee import config

# Set API key via environment variable
os.environ["LLM_API_KEY"] = "your-openai-api-key"

# Configure LLM
config.set_llm_config({
    "llm_provider": "openai",
    "llm_model": "gpt-4",
    "llm_temperature": 0.7
})
```

## Best Practices

1. **Import Registration First**: Always import `cognee_community_hybrid_adapter_falkor.register` before configuring Cognee
2. **Use Environment Variables**: Store connection details and API keys in environment variables
3. **Batch Processing**: Add multiple documents before calling `cognify()` for better performance
4. **Clean Up**: Use `prune.prune_data()` and `prune.prune_system()` to reset when needed
5. **Hybrid Mode**: Configure FalkorDB as both vector and graph database for optimal search capabilities
6. **Monitor Resources**: Track FalkorDB memory usage and query performance as your knowledge base grows

## Integration Patterns

### With LangChain

```python
from cognee import add, cognify, search, SearchType

# Use Cognee as a knowledge base for LangChain
async def get_context(query):
    results = await search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text=query
    )
    return results

# Integrate with your LangChain application
context = await get_context("previous conversations about AI")
```

### Adding Multiple Documents

```python
from cognee import add, cognify

# Add documents to Cognee
documents = [
    "Your first document content...",
    "Your second document content...",
    "Your third document content..."
]

for doc in documents:
    await add(doc)

await cognify()
```

## Troubleshooting

### Installation Issues

If you have trouble installing the community adapter:
- Ensure you have the correct package name: `cognee-community-hybrid-adapter-falkor`
- Check that you're using Python 3.10 or higher
- Try installing in a fresh virtual environment

### Connection Issues

If you experience connection problems:
- Verify FalkorDB is running: `redis-cli -h localhost -p 6379 ping`
- Check the `GRAPH_DB_URL` and `GRAPH_DB_PORT` environment variables
- Ensure FalkorDB is accessible on the specified host and port

### Data Not Appearing in Graph

- Make sure to import `cognee_community_hybrid_adapter_falkor.register` before using Cognee
- Call `await cognify()` after adding data to process and extract entities
- Check that your LLM API key is set correctly
- Verify the graph is being populated using FalkorDB CLI or Browser

### Performance Issues

- Consider batching operations for large datasets
- Monitor graph size with `GRAPH.MEMORY USAGE` command
- Clean up old data periodically using `prune.prune_data()`

## Resources

- 📚 [Cognee Documentation](https://github.com/topoteretes/cognee-community)
- 💻 [Cognee GitHub Repository](https://github.com/topoteretes/cognee)
- 🔗 [FalkorDB Integration Guide](https://github.com/topoteretes/cognee-community/blob/main/packages/hybrid/falkordb/README.md)
- 📖 [Cognee Examples](https://github.com/topoteretes/cognee/tree/main/examples)

## Next Steps

- Explore [Graphiti](./graphiti.md) for temporal knowledge graph capabilities
- Learn about [GraphRAG SDK](/graphrag-sdk) for advanced reasoning
- Check out [LLM Framework Integrations](/llm-integrations) for other tools
- Review [Cypher Query Language](/cypher) for custom graph queries
