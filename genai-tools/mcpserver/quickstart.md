---
title: "Quick Start"
parent: "MCP Server"
nav_order: 1
search_exclude: true
---

# Quick Start

## Prerequisites

- Node.js 18+
- FalkorDB instance (running locally or remotely)
- Claude Desktop app (for AI integration)

## Running from npm

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

## Running with npx

You can run the server directly from the command line:

```bash
# Run with stdio transport (default)
FALKORDB_HOST=localhost FALKORDB_PORT=6379 npx -y @falkordb/mcpserver

# Run with HTTP transport
MCP_TRANSPORT=http MCP_PORT=3005 FALKORDB_HOST=localhost FALKORDB_PORT=6379 npx -y @falkordb/mcpserver

# Using a .env file with dotenv-cli
npx dotenv-cli -e .env -- npx @falkordb/mcpserver
```

## Docker Compose

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
