---
title: "FalkorDB MCP Server"
nav_order: 7
description: "Enable AI assistants like Claude to interact with FalkorDB graph databases using the Model Context Protocol (MCP)."
parent: "GenAI Tools"
---

# FalkorDB MCP Server

### Enable AI assistants to query and interact with FalkorDB graph databases

A Model Context Protocol (MCP) server that allows AI models like Claude to interact with FalkorDB using natural language. Query your graph data, create relationships, and manage your knowledge graph through conversational AI.

- Query graph databases using OpenCypher (with read-only mode support)
- Create and manage nodes and relationships
- List and explore multiple graphs
- Delete graphs when needed
- Support for replica instances with read-only queries

## What is the Model Context Protocol?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io) is an open protocol that standardizes how AI applications provide context to Large Language Models (LLMs). It enables AI assistants to securely connect to external data sources and tools, making them more powerful and context-aware.

## Quick Start

### Prerequisites

- Node.js 18+
- FalkorDB instance (running locally or remotely)
- Claude Desktop app (for AI integration)

### Running from npm

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "falkordb": {
      "command": "npx",
      "args": [
        "-y",
        "@falkordb/mcpserver@latest"
      ],
      "env": {
        "FALKORDB_HOST": "localhost",
        "FALKORDB_PORT": "6379",
        "FALKORDB_USERNAME": "",
        "FALKORDB_PASSWORD": ""
      }
    }
  }
}
```

Restart Claude Desktop and you'll see the FalkorDB tools available!

### Running with npx

You can run the server directly from the command line:

```bash
# Run with stdio transport (default)
FALKORDB_HOST=localhost FALKORDB_PORT=6379 npx -y @falkordb/mcpserver

# Run with HTTP transport
MCP_TRANSPORT=http MCP_PORT=3005 FALKORDB_HOST=localhost FALKORDB_PORT=6379 npx -y @falkordb/mcpserver

# Using a .env file with dotenv-cli
npx dotenv-cli -e .env -- npx @falkordb/mcpserver
```

### Docker Compose

Run FalkorDB and the MCP server together:

```bash
git clone https://github.com/FalkorDB/FalkorDB-MCPServer.git
cd FalkorDB-MCPServer
cp .env.example .env   # Edit to set MCP_API_KEY, FALKORDB_PASSWORD, etc.
docker compose up -d
```

This starts both FalkorDB and the MCP server with health checks and persistent volumes.

## Available MCP Tools

Once connected to Claude or another MCP-compatible AI assistant, you can:

### Query Graphs

```text
"Show me all people who know each other"
"Find the shortest path between two nodes"
"What relationships does John have?"
"Run a read-only query on the replica instance"
```

The `query_graph` tool supports a `readOnly` parameter to execute queries using `GRAPH.RO_QUERY`, ideal for:
- Running queries on replica instances
- Preventing accidental write operations
- Ensuring data integrity in production environments

### Manage Data

```text
"Create a new person named Alice who knows Bob"
"Add a 'WORKS_AT' relationship between Alice and TechCorp"
```

### Explore Structure

```text
"List all available graphs"
"Show me the structure of the user_data graph"
"Delete the old_test graph"
```

## Configuration

### Environment Variables

```env
# FalkorDB Configuration
FALKORDB_HOST=localhost
FALKORDB_PORT=6379
FALKORDB_USERNAME=          # Optional
FALKORDB_PASSWORD=          # Optional
FALKORDB_DEFAULT_READONLY=false  # Set to 'true' for read-only mode

# Transport Mode
MCP_TRANSPORT=stdio         # 'stdio' (default) or 'http'
MCP_PORT=3000              # Port for HTTP transport
MCP_API_KEY=               # Optional API key for HTTP transport

# Logging (optional)
ENABLE_FILE_LOGGING=false
```

### Transport Modes

#### stdio (default)
Used for direct integration with AI clients like Claude Desktop. Communication happens via standard input/output.

```env
MCP_TRANSPORT=stdio
```

#### HTTP
Exposes the MCP server over HTTP for remote or networked access:

```env
MCP_TRANSPORT=http
MCP_PORT=3000
MCP_API_KEY=your-secret-api-key  # Optional but recommended
```

When using HTTP transport, clients connect via the MCP Streamable HTTP protocol. API key authentication is enforced via the `Authorization: Bearer <key>` header when `MCP_API_KEY` is set.

### Read-Only Mode for Replica Instances

Enable read-only mode by default to prevent writes to replica instances:

```env
FALKORDB_DEFAULT_READONLY=true
```

**Use cases:**
- **Replica instances**: Prevent writes to read replicas in replication setups
- **Production safety**: Ensure critical data isn't accidentally modified
- **Reporting/analytics**: Run queries for dashboards without risk of data changes
- **Multi-tenant environments**: Provide read-only access to certain users

### Running Multiple Instances

You can configure multiple MCP servers for different FalkorDB instances:

```json
{
  "mcpServers": {
    "falkordb-dev": {
      "command": "npx",
      "args": ["-y", "@falkordb/mcpserver@latest"],
      "env": {
        "FALKORDB_HOST": "dev.falkordb.local",
        "FALKORDB_DEFAULT_READONLY": "false"
      }
    },
    "falkordb-prod-replica": {
      "command": "npx",
      "args": ["-y", "@falkordb/mcpserver@latest"],
      "env": {
        "FALKORDB_HOST": "replica.falkordb.com",
        "FALKORDB_DEFAULT_READONLY": "true"
      }
    }
  }
}
```

## Example Usage

Once connected, Claude can help you write and execute queries:

```cypher
// Query relationships
MATCH (p:Person)-[:KNOWS]->(friend:Person)
WHERE p.name = 'Alice'
RETURN friend.name, friend.age

// Create data structures
CREATE (alice:Person {name: 'Alice', age: 30})
CREATE (bob:Person {name: 'Bob', age: 25})
CREATE (alice)-[:KNOWS {since: 2020}]->(bob)

// Analyze your graph
MATCH path = shortestPath((start:Person)-[*]-(end:Person))
WHERE start.name = 'Alice' AND end.name = 'Charlie'
RETURN path
```

## Docker Deployment

### Using Docker Hub Images

```bash
# Use the latest stable release
docker pull falkordb/mcpserver:latest
docker run -p 3000:3000 \
  -e FALKORDB_HOST=host.docker.internal \
  -e FALKORDB_PORT=6379 \
  -e MCP_API_KEY=your-secret-key \
  falkordb/mcpserver:latest

# Or use the edge version (latest main branch)
docker pull falkordb/mcpserver:edge

# Or pin to a specific version
docker pull falkordb/mcpserver:1.0.0
```

## Resources

- 📦 [npm Package](https://www.npmjs.com/package/@falkordb/mcpserver)
- 💻 [GitHub Repository](https://github.com/FalkorDB/FalkorDB-MCPServer)
- 🐳 [Docker Hub](https://hub.docker.com/r/falkordb/mcpserver)
- 📖 [MCP Specification](https://modelcontextprotocol.io/docs)
- 📚 [FalkorDB Documentation](https://docs.falkordb.com)
- 🔍 [OpenCypher Query Language](https://opencypher.org/)
