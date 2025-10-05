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

Install Cognee with FalkorDB support:

```bash
pip install cognee
pip install falkordb
```

### Quick Start Example

Here's a complete example to get you started with Cognee and FalkorDB:

```python
import asyncio
import cognee
from cognee.infrastructure.databases.graph import get_graph_engine

async def main():
    # Configure Cognee to use FalkorDB
    await cognee.config.set_graph_database_config({
        "graph_database_provider": "falkordb",
        "graph_database_url": "falkor://localhost:6379",
        # For FalkorDB Cloud:
        # "graph_database_url": "falkor://your-instance.falkordb.cloud:6379",
        # "graph_database_username": "default",
        # "graph_database_password": "your-password"
    })
    
    # Add data to cognee
    text_data = """
    Sarah is a software engineer at TechCorp. She specializes in machine learning
    and has been working on implementing graph-based recommendation systems.
    Sarah recently collaborated with Mike on a new project using FalkorDB.
    Mike is the lead data scientist at TechCorp.
    """
    
    # Process and store the data
    await cognee.add(text_data)
    await cognee.cognify()
    
    # Search the knowledge graph
    search_results = await cognee.search(
        "SEARCH",
        query="What does Sarah work on?"
    )
    
    print("Search Results:")
    print(search_results)
    
    # Query with graph traversal
    graph_engine = await get_graph_engine()
    
    # Find all connections for Sarah
    query = """
    MATCH (sarah:Person {name: 'Sarah'})-[r]-(connected)
    RETURN sarah, r, connected
    """
    
    results = await graph_engine.query(query)
    
    print("\nGraph Traversal Results:")
    for record in results:
        print(record)

# Run the example
asyncio.run(main())
```

### Understanding the Code

1. **Configure Cognee**: Set up the connection to your FalkorDB instance
2. **Add Data**: Provide text or structured data to be processed
3. **Cognify**: Process the data to extract entities and relationships
4. **Search**: Query the knowledge using natural language or Cypher queries
5. **Graph Traversal**: Use direct graph queries for complex relationship exploration

## Advanced Features

### Hybrid Search

Combine semantic search with graph relationships:

```python
# Semantic search
semantic_results = await cognee.search(
    "SEARCH",
    query="machine learning projects",
    search_type="SIMILARITY"
)

# Graph-based search
graph_results = await cognee.search(
    "SEARCH", 
    query="machine learning projects",
    search_type="GRAPH_TRAVERSAL"
)

# Hybrid search (default)
hybrid_results = await cognee.search(
    "SEARCH",
    query="machine learning projects"
)
```

### Custom Entity Extraction

Configure how Cognee extracts entities:

```python
await cognee.config.set_llm_config({
    "llm_provider": "openai",
    "llm_model": "gpt-4",
    "llm_temperature": 0.7
})

# Define custom entity types
entity_config = {
    "entity_types": ["Person", "Organization", "Project", "Technology"],
    "relationship_types": ["WORKS_AT", "COLLABORATES_WITH", "USES"]
}

await cognee.add(text_data, entity_config=entity_config)
await cognee.cognify()
```

### Managing Knowledge

```python
# Add multiple documents
documents = [
    "Document 1 content...",
    "Document 2 content...",
    "Document 3 content..."
]

for doc in documents:
    await cognee.add(doc)

await cognee.cognify()

# Reset memory (clear all data)
await cognee.prune.prune_data()
await cognee.prune.prune_system()
```

### Direct Graph Access

For advanced use cases, access FalkorDB directly:

```python
from cognee.infrastructure.databases.graph import get_graph_engine

# Get the graph engine
graph_engine = await get_graph_engine()

# Run custom Cypher queries
query = """
MATCH (p:Person)-[:WORKS_AT]->(o:Organization)
WHERE o.name = 'TechCorp'
RETURN p.name AS employee, p.role AS role
ORDER BY p.name
"""

results = await graph_engine.query(query)

for record in results:
    print(f"Employee: {record['employee']}, Role: {record['role']}")
```

## Configuration Options

### Database Configuration

```python
# FalkorDB configuration
await cognee.config.set_graph_database_config({
    "graph_database_provider": "falkordb",
    "graph_database_url": "falkor://localhost:6379",
    "graph_database_username": "your-username",
    "graph_database_password": "your-password",
    "graph_name": "cognee_memory"  # Custom graph name
})

# Vector store configuration (optional)
await cognee.config.set_vector_database_config({
    "vector_database_provider": "qdrant",
    "vector_database_url": "http://localhost:6333"
})
```

### LLM and Embedding Configuration

```python
# LLM configuration for entity extraction
await cognee.config.set_llm_config({
    "llm_provider": "openai",
    "llm_model": "gpt-4",
    "llm_api_key": "your-api-key",
    "llm_temperature": 0.7
})

# Embedding configuration for semantic search
await cognee.config.set_embedding_config({
    "embedding_provider": "openai",
    "embedding_model": "text-embedding-3-small",
    "embedding_api_key": "your-api-key"
})
```

## Best Practices

1. **Batch Processing**: Process multiple documents together for better performance
2. **Schema Design**: Plan your entity and relationship types before ingestion
3. **Incremental Updates**: Add new information incrementally without reprocessing everything
4. **Query Optimization**: Use specific Cypher queries for complex graph traversals
5. **Monitor Resources**: Track memory usage and query performance as your graph grows

## Integration Patterns

### With LangChain

```python
from langchain.memory import ConversationBufferMemory
from cognee import cognee

# Use Cognee as a knowledge base for LangChain
async def get_context(query):
    results = await cognee.search("SEARCH", query=query)
    return results

# Integrate with your LangChain application
context = await get_context("previous conversations about AI")
```

### With LlamaIndex

```python
from llama_index import Document
import cognee

# Add documents to Cognee
documents = [
    Document(text="Your document content...")
]

for doc in documents:
    await cognee.add(doc.text)

await cognee.cognify()
```

## Troubleshooting

### Connection Issues

If you experience connection problems:
- Verify FalkorDB is running: `redis-cli -h localhost -p 6379 ping`
- Check the connection URL format: `falkor://host:port`
- Ensure authentication credentials are correct

### Data Not Appearing in Graph

- Make sure to call `await cognee.cognify()` after adding data
- Check that entity extraction is working with your LLM configuration
- Verify the graph is being populated: use FalkorDB Browser or CLI

### Performance Issues

- Consider batching operations for large datasets
- Monitor graph size with `GRAPH.MEMORY USAGE` command
- Use pagination for large result sets
- Optimize Cypher queries with appropriate indices

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
