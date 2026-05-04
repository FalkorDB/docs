---
title: "Quick Start"
parent: "MCP Server"
nav_order: 1
description: "Get started with FalkorDB MCP Server in minutes using Docker Compose or direct installation for Claude Desktop, Cursor IDE, and other MCP clients."
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

{% include faq_accordion.html title="Frequently Asked Questions" q1="What do I need to get started with the FalkorDB MCP Server?" a1="You need **Node.js 18+**, a running FalkorDB instance (locally via Docker or FalkorDB Cloud), and an MCP-compatible AI client like Claude Desktop. No additional dependencies are required since the server runs via `npx`." q2="How do I connect Claude Desktop to FalkorDB?" a2="Add the MCP server configuration to your Claude Desktop config file (`claude_desktop_config.json`). Set the command to `npx` with args `['-y', '@falkordb/mcpserver@latest']` and provide your FalkorDB connection details as environment variables." q3="Can I run the MCP Server without Claude Desktop?" a3="Yes. Run it directly with `npx -y @falkordb/mcpserver` using stdio transport, or set `MCP_TRANSPORT=http` and `MCP_PORT=3005` for HTTP transport that any MCP-compatible client can connect to." q4="How do I use Docker Compose for a full setup?" a4="Clone the FalkorDB-MCPServer repository, copy `.env.example` to `.env`, configure your settings, and run `docker compose up -d`. This starts both FalkorDB and the MCP server with health checks and persistent volumes." q5="What can I ask Claude once connected to FalkorDB?" a5="You can ask Claude to query graphs ('Show me all people who know each other'), create data ('Create a person named Alice who knows Bob'), explore structure ('List all available graphs'), and run read-only queries on replica instances." %}
