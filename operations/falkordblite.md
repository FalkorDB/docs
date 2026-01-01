---
title: "FalkorDBLite"
nav_order: 6
parent: Operations
description: "Self-contained Python interface to FalkorDB"
---

# FalkorDBLite

FalkorDBLite is a self-contained Python interface to the FalkorDB graph database. It provides an embedded Redis server with the FalkorDB module that is automatically installed, configured, and managed when the bindings are used.

## Key Features

- **Easy to Use** - Built-in Redis server with FalkorDB module that is automatically installed, configured, and managed
- **Graph Database** - Full support for FalkorDB graph operations using Cypher queries through a simple Python API
- **Flexible** - Create a single server shared by multiple programs or multiple independent servers with graph capabilities
- **Compatible** - Provides both Redis key-value operations and FalkorDB graph operations in a unified interface
- **Secure** - Uses a secure default Redis configuration that is only accessible by the creating user on the local system
- **Persistent** - Data persists between sessions when using the same database file

## Requirements

- Python 3.12 or higher

## Installation

Install FalkorDBLite using pip:

```bash
pip install falkordblite
```

The package will automatically install its dependencies, including:
- `redis>=4.5` - Redis Python client
- `psutil` - Process and system utilities

### macOS Runtime Requirement

**Important:** On macOS, the FalkorDB module requires the OpenMP runtime library (`libomp`). If you encounter an error like `Library not loaded: /opt/homebrew/opt/libomp/lib/libomp.dylib`, install it using Homebrew:

```bash
brew install libomp
```

## Getting Started

FalkorDBLite provides two main interfaces:

1. **FalkorDB Graph API** - A graph database interface using Cypher queries
2. **Redis API** - Traditional Redis key-value operations

The package includes both Redis and the FalkorDB module, automatically configured and managed.

### Basic Graph Database Usage

Here's a simple example of creating a graph database, adding nodes and relationships, and querying them using Cypher:

```python
from redislite.falkordb_client import FalkorDB

# Create a FalkorDB instance with embedded Redis + FalkorDB
db = FalkorDB('/tmp/falkordb.db')

# Select a graph
g = db.select_graph('social')

# Create nodes with Cypher
result = g.query('CREATE (p:Person {name: "Alice", age: 30}) RETURN p')
result = g.query('CREATE (p:Person {name: "Bob", age: 25}) RETURN p')

# Create a relationship
result = g.query('''
    MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
    CREATE (a)-[r:KNOWS]->(b)
    RETURN r
''')

# Query the graph
result = g.query('MATCH (p:Person) RETURN p.name, p.age')
for row in result.result_set:
    print(row)

# Read-only query
result = g.ro_query('MATCH (p:Person)-[r:KNOWS]->(f) RETURN p.name, f.name')
for row in result.result_set:
    print(f"{row[0]} knows {row[1]}")

# Delete the graph when done
g.delete()
```

### Complex Graph Example

Here's a more complex example demonstrating graph relationships:

```python
from redislite.falkordb_client import FalkorDB

db = FalkorDB('/tmp/graphs.db')
g = db.select_graph('social')

# Create a graph with multiple nodes and relationships
g.query('''
    CREATE (alice:Person {name: "Alice", age: 30}),
           (bob:Person {name: "Bob", age: 25}),
           (carol:Person {name: "Carol", age: 28}),
           (alice)-[:KNOWS]->(bob),
           (bob)-[:KNOWS]->(carol),
           (alice)-[:KNOWS]->(carol)
''')

# Find all friends of Alice
result = g.query('''
    MATCH (p:Person {name: "Alice"})-[:KNOWS]->(friend)
    RETURN friend.name, friend.age
''')

for row in result.result_set:
    print(f"Friend: {row[0]}, Age: {row[1]}")
```

### Using Redis Key-Value Operations

FalkorDBLite also supports traditional Redis operations:

```python
from redislite import Redis

# Create a Redis connection
redis_connection = Redis('/tmp/redis.db')

# Use standard Redis operations
redis_connection.set('key', 'value')
value = redis_connection.get('key')
print(value)  # b'value'

# List all keys
keys = redis_connection.keys()
print(keys)
```

### Working with Multiple Graphs

You can work with multiple independent graphs in the same database:

```python
from redislite.falkordb_client import FalkorDB

db = FalkorDB('/tmp/multi.db')

# Create different graphs for different domains
users = db.select_graph('users')
products = db.select_graph('products')
transactions = db.select_graph('transactions')

# Each graph is independent
users.query('CREATE (u:User {name: "Alice"})')
products.query('CREATE (p:Product {name: "Laptop"})')

# List all graphs
all_graphs = db.list_graphs()
print(all_graphs)
```

## Data Persistence

FalkorDB data persists between sessions when you use the same database file:

```python
from redislite.falkordb_client import FalkorDB

# First session - create data
db = FalkorDB('/tmp/falkordb.db')
g = db.select_graph('social')
g.query('CREATE (p:Person {name: "Alice", age: 30})')

# Close and reopen
db = FalkorDB('/tmp/falkordb.db')
g = db.select_graph('social')

# Data from previous session is still there
result = g.query('MATCH (p:Person) RETURN p.name, p.age')
for row in result.result_set:
    print(f"Name: {row[0]}, Age: {row[1]}")
```

## Use Cases

FalkorDBLite is ideal for:

- **Development and Testing** - Quickly test graph database functionality without setting up a full server
- **Prototyping** - Rapidly prototype graph-based applications
- **Educational Purposes** - Learn graph databases and Cypher queries without infrastructure setup
- **Small-Scale Applications** - Lightweight applications that need graph database capabilities
- **CI/CD Pipelines** - Automated testing environments that require an embedded database

## Production

For production environments, consider using:
- [FalkorDB Cloud](https://app.falkordb.cloud) - Managed cloud service
- [FalkorDB Docker](/getting-started) - Self-hosted server deployment
- [FalkorDB Kubernetes](/operations/k8s_support) - Kubernetes deployment

## Additional Resources

- [FalkorDBLite GitHub Repository](https://github.com/FalkorDB/falkordblite)
- [FalkorDBLite on PyPI](https://pypi.org/project/falkordblite/)
- [FalkorDB Documentation](/index)
- [FalkorDB Cypher Language](/cypher)
- [FalkorDB Python Client](https://github.com/FalkorDB/falkordb-py)

## Getting Help

If you encounter issues with FalkorDBLite:

1. Check the [FalkorDBLite GitHub Issues](https://github.com/FalkorDB/falkordblite/issues)
2. Review the [troubleshooting guide](https://github.com/FalkorDB/falkordblite/blob/master/TROUBLESHOOTING.md)
