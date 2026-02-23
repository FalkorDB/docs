---
title: "Mem0"
parent: "Agentic Memory"
nav_order: 3
description: "Add FalkorDB as a graph memory backend for Mem0 AI agents with per-user graph isolation, hybrid search, and seamless integration."
---

# Mem0

[Mem0](https://github.com/mem0ai/mem0) is a memory management framework for AI agents that enables persistent, contextual memory across interactions. The [mem0-falkordb](https://github.com/FalkorDB/mem0-falkordb) plugin adds FalkorDB as a graph store backend for Mem0 without modifying any Mem0 source code.

## Overview

The mem0-falkordb plugin provides:
- **Graph-structured memory**: Store relationships between entities, not just flat facts
- **Per-user graph isolation**: Each user gets their own isolated FalkorDB graph
- **Context-aware retrieval**: Semantic search with vector embeddings
- **Memory evolution**: Support for updates and conflict resolution
- **Runtime patching**: No modifications to Mem0 source code required

## Why Mem0 + FalkorDB?

### FalkorDB's Added Value

- **Native multi-graph support**: Isolated memory spaces for different users or agents
- **Natural data isolation**: No user_id filtering needed in Cypher queries
- **Simpler, faster queries**: No WHERE clauses on user_id
- **Easy cleanup**: `delete_all` simply drops the user's graph
- **High performance**: Fast graph operations and efficient memory usage
- **Cloud and on-premises ready**: Works with FalkorDB Cloud or your own deployment

### Use Cases

- **Multi-agent systems**: Persistent memory for each agent with graph-based relationships
- **Conversational AI**: Track facts, entities, and relationships across conversations
- **Personalized assistants**: Build context-aware AI that remembers user preferences and history
- **Customer support**: Provide context-rich responses based on customer interaction history
- **Knowledge management**: Aggregate and navigate complex information networks

## Getting Started

### Prerequisites

- Python 3.10 or higher
- FalkorDB instance (Cloud or self-hosted)
- OpenAI API key (or other supported LLM provider)

### Installation

Install both Mem0 and the FalkorDB plugin:

```bash
pip install mem0ai
pip install mem0-falkordb
```

### Quick Start Example

Here's a complete example to get you started:

```python
from mem0_falkordb import register
register()

from mem0 import Memory

config = {
    "graph_store": {
        "provider": "falkordb",
        "config": {
            "host": "localhost",
            "port": 6379,
            "database": "mem0",
        },
    },
    "llm": {
        "provider": "openai",
        "config": {"model": "gpt-4o-mini"},
    },
}

m = Memory.from_config(config)

# Add memories for a user
m.add("I love pizza", user_id="alice")
m.add("Alice is a software engineer", user_id="alice")
m.add("Alice works on AI projects", user_id="alice")

# Search the memory
results = m.search("what does alice like?", user_id="alice")
print(results)
```

### Understanding the Code

1. **Register the plugin**: Call `register()` to patch FalkorDB into Mem0's factory system
2. **Configure Mem0**: Set FalkorDB as the graph store provider with connection details
3. **Add memories**: Store information with user_id for automatic graph isolation
4. **Search**: Query memories using natural language

## Running FalkorDB

### Using Docker

```bash
docker run --rm -p 6379:6379 falkordb/falkordb:latest
```

### Using FalkorDB Cloud

Sign up for a free account at [app.falkordb.cloud](https://app.falkordb.cloud) and use the connection details in your config:

```python
config = {
    "graph_store": {
        "provider": "falkordb",
        "config": {
            "host": "your-instance.falkordb.cloud",
            "port": 6379,
            "username": "default",
            "password": "your-password",
            "database": "mem0",
        },
    },
    # ... rest of config
}
```

## Configuration Options

### Graph Store Configuration

```python
config = {
    "graph_store": {
        "provider": "falkordb",
        "config": {
            "host": "localhost",       # FalkorDB server host
            "port": 6379,              # FalkorDB server port
            "database": "mem0",        # Graph name prefix
            "username": None,          # Authentication username (optional)
            "password": None,          # Authentication password (optional)
            "base_label": True,        # Use __Entity__ base label
        },
    },
}
```

| Parameter    | Type   | Default     | Description                                |
|-------------|--------|-------------|--------------------------------------------|
| `host`      | str    | `localhost` | FalkorDB server host                       |
| `port`      | int    | `6379`      | FalkorDB server port                       |
| `database`  | str    | `mem0`      | Graph name prefix (each user gets `{database}_{user_id}`) |
| `username`  | str    | `None`      | Authentication username (optional)         |
| `password`  | str    | `None`      | Authentication password (optional)         |
| `base_label`| bool   | `True`      | Use `__Entity__` base label                |

### Per-User Graph Isolation

Each user automatically gets their own isolated FalkorDB graph (e.g., `mem0_alice`, `mem0_bob`). This provides:

- **Natural data isolation**: No user_id filtering needed in Cypher queries
- **Simpler, faster queries**: No WHERE clauses on user_id
- **Easy cleanup**: `delete_all` simply drops the user's graph
- **Scalability**: Leverage FalkorDB's native multi-graph support

## Advanced Features

### Working with Multiple Users

```python
# Add memories for different users
m.add("Alice loves pizza", user_id="alice")
m.add("Bob prefers pasta", user_id="bob")

# Each user gets their own isolated graph
alice_results = m.search("what food?", user_id="alice")
bob_results = m.search("what food?", user_id="bob")

# Results are isolated per user
print(alice_results)  # Returns info about pizza
print(bob_results)    # Returns info about pasta
```

### Getting All Memories

```python
# Get all memories for a user
all_memories = m.get_all(user_id="alice")
for memory in all_memories:
    print(memory)
```

### Updating Memories

```python
# Mem0 automatically handles memory updates and conflict resolution
m.add("Alice now prefers sushi", user_id="alice")
results = m.search("what food does alice like?", user_id="alice")
# Results will reflect the updated preference
```

### Deleting Memories

```python
# Delete specific memories
m.delete(memory_id="specific-id", user_id="alice")

# Delete all memories for a user (drops the user's graph)
m.delete_all(user_id="alice")
```

### Memory History

```python
# Get memory history for a specific memory
history = m.history(memory_id="specific-id")
for entry in history:
    print(f"Version: {entry['version']}, Changed: {entry['changed_at']}")
```

## Demo

The mem0-falkordb repository includes a comprehensive demo showcasing:
- Graph-structured memory with relationships
- Per-user graph isolation
- Context-aware retrieval
- Memory evolution and updates
- Visual graph inspection

```bash
# Clone the repository
git clone https://github.com/FalkorDB/mem0-falkordb.git
cd mem0-falkordb

# Start FalkorDB
docker run --rm -p 6379:6379 falkordb/falkordb:latest

# Run the demo
cd demo
uv sync
export OPENAI_API_KEY='your-key-here'
uv run python demo.py
```

See the [demo README](https://github.com/FalkorDB/mem0-falkordb/blob/main/demo/README.md) for complete instructions.

## How It Works

The plugin uses Python's runtime patching to integrate with Mem0 without modifying its source code:

1. `GraphStoreFactory.provider_to_class` gets a new `"falkordb"` entry
2. `GraphStoreConfig` is patched to accept `FalkorDBConfig`
3. A `MemoryGraph` class translates Mem0's graph operations to FalkorDB-compatible Cypher
4. The `register()` function must be called before creating a Mem0 `Memory` instance

### Key Cypher Translations

The plugin translates Neo4j-style Cypher (used by Mem0) to FalkorDB-compatible Cypher:

| Neo4j                                    | FalkorDB                                          |
|------------------------------------------|---------------------------------------------------|
| `elementId(n)`                           | `id(n)`                                           |
| `vector.similarity.cosine()`             | `db.idx.vector.queryNodes()` procedure            |
| `db.create.setNodeVectorProperty()`      | `SET n.embedding = vecf32($vec)`                  |
| `CALL { ... UNION ... }` subqueries      | Separate outgoing + incoming queries              |

## Best Practices

1. **Call register() once**: Always call `register()` before creating a Mem0 `Memory` instance
2. **Use user_id consistently**: Always provide user_id for proper graph isolation
3. **Configure LLM**: Ensure your LLM provider is properly configured for entity extraction
4. **Monitor graph size**: Use `GRAPH.MEMORY USAGE` command to track memory usage
5. **Clean up**: Use `delete_all()` to remove user graphs when no longer needed
6. **Connection pooling**: Reuse Memory instances when possible

## Troubleshooting

### Installation Issues

If you have trouble installing:
- Ensure you have Python 3.10 or higher
- Install Mem0 and mem0-falkordb separately
- Try installing in a fresh virtual environment

### Connection Issues

If you can't connect to FalkorDB:
- Verify FalkorDB is running: `redis-cli -h localhost -p 6379 ping`
- Check your connection details (host, port, credentials)
- Ensure FalkorDB is accessible on the specified host and port

### Memory Not Being Stored

- Make sure to call `register()` before creating the Memory instance
- Verify your LLM API key is set correctly
- Check that the user_id is provided when adding memories
- Ensure FalkorDB has enough memory available

### Search Returns No Results

- Verify memories were added successfully with `get_all()`
- Check that you're using the correct user_id
- Ensure your embeddings configuration is correct
- Try more specific or different search queries

## Resources

- 📦 [PyPI Package](https://pypi.org/project/mem0-falkordb/)
- 💻 [GitHub Repository](https://github.com/FalkorDB/mem0-falkordb)
- 📚 [Mem0 Documentation](https://github.com/mem0ai/mem0)
- 🎥 [Demo Application](https://github.com/FalkorDB/mem0-falkordb/tree/main/demo)
- 🔗 [FalkorDB Cloud](https://app.falkordb.cloud)

## Next Steps

- Explore [Graphiti](./graphiti.md) for temporal knowledge graph capabilities
- Learn about [Cognee](./cognee.md) for alternative memory management approaches
- Review [GenAI Tools](/genai-tools) for graph reasoning and LLM integrations
