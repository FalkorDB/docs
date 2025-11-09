---
title: "Graphiti MCP Server"
parent: "Agentic Memory"
nav_order: 3
description: "Run Graphiti MCP server with FalkorDB for AI agent memory in Claude Desktop and other MCP clients"
---

# [EXPERIMENTAL] Graphiti MCP Server

{: .warning }
> **Experimental Feature**: The Graphiti MCP Server integration is experimental and under active development. Features and configurations may change in future releases.

The Graphiti MCP (Model Context Protocol) Server enables AI clients like Claude Desktop and Cursor IDE to interact with FalkorDB-powered knowledge graphs for persistent agent memory. This allows AI assistants to store and retrieve information across conversations, building a rich, contextual memory over time.

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open standard that enables AI applications to connect to external data sources and tools. The Graphiti MCP Server implements this protocol to provide AI agents with access to graph-based knowledge storage powered by FalkorDB.

## Overview

The Graphiti MCP Server provides:

- **Persistent Memory**: Store conversation history, facts, and relationships in a knowledge graph
- **Contextual Retrieval**: Query the graph to retrieve relevant information for AI responses
- **Cross-Session Memory**: Maintain knowledge across multiple conversations and sessions
- **Multi-Tenant Support**: Isolated memory spaces for different users or agents
- **Real-Time Updates**: Add new information to the graph as conversations evolve

## Prerequisites

Before you begin, ensure you have:

- Docker installed on your system
- An OpenAI API key (for LLM operations)
- A FalkorDB instance running (or use the bundled Docker setup)

## Quick Start with Docker

The easiest way to run the Graphiti MCP Server with FalkorDB is using Docker:

### Step 1: Pull the Docker Image

```bash
docker pull falkordb/graphiti-knowledge-graph-mcp:latest
```

### Step 2: Run the MCP Server

Run the server with required environment variables:

```bash
docker run -d \
  --name graphiti-mcp \
  -e OPENAI_API_KEY="your-openai-api-key" \
  -e DATABASE_TYPE="falkordb" \
  -e FALKORDB_HOST="host.docker.internal" \
  -e FALKORDB_PORT="6379" \
  -p 8000:8000 \
  falkordb/graphiti-knowledge-graph-mcp:latest
```

**Note**: If you're running FalkorDB on your local machine, use `host.docker.internal` as the `FALKORDB_HOST` to allow the container to access your host's localhost.

#### Alternative: Using a .env File

For easier management of environment variables, create a `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key
DATABASE_TYPE=falkordb
FALKORDB_HOST=host.docker.internal
FALKORDB_PORT=6379
FALKORDB_USERNAME=
FALKORDB_PASSWORD=
```

Then run the container with the `--env-file` option:

```bash
docker run -d \
  --name graphiti-mcp \
  --env-file .env \
  -p 8000:8000 \
  falkordb/graphiti-knowledge-graph-mcp:latest
```

### Step 3: Run FalkorDB (if needed)

If you don't have a FalkorDB instance running, start one:

```bash
docker run -d \
  --name falkordb \
  -p 6379:6379 \
  -p 3000:3000 \
  falkordb/falkordb:latest
```

## Docker Compose Setup

For a complete setup with both FalkorDB and the MCP server, create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  falkordb:
    image: falkordb/falkordb:latest
    ports:
      - "6379:6379"      # Redis protocol port
      - "3000:3000"      # FalkorDB Browser UI
    volumes:
      - falkordb-data:/data

  graphiti-mcp:
    image: falkordb/graphiti-knowledge-graph-mcp:latest
    depends_on:
      - falkordb
    ports:
      - "8000:8000"      # MCP Server HTTP/SSE port
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_TYPE=falkordb
      - FALKORDB_HOST=falkordb
      - FALKORDB_PORT=6379
      - FALKORDB_USERNAME=${FALKORDB_USERNAME:-}
      - FALKORDB_PASSWORD=${FALKORDB_PASSWORD:-}

volumes:
  falkordb-data:
```

Create a `.env` file in the same directory:

```env
OPENAI_API_KEY=your-openai-api-key
DATABASE_TYPE=falkordb
FALKORDB_USERNAME=
FALKORDB_PASSWORD=
```

Then start both services:

```bash
docker-compose up -d
```

## Configuration

### Environment Variables

The MCP server accepts the following environment variables:

| Variable | Description | Default | Required | Example |
|----------|-------------|---------|----------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key for LLM operations | - | Yes | `sk-proj-...` |
| `DATABASE_TYPE` | Database backend type (must be "falkordb") | - | Yes | `falkordb` |
| `FALKORDB_HOST` | FalkorDB server hostname | `localhost` | No | `host.docker.internal` |
| `FALKORDB_PORT` | FalkorDB server port | `6379` | No | `6379` |
| `FALKORDB_USERNAME` | FalkorDB username (if authentication enabled) | - | No | `default` |
| `FALKORDB_PASSWORD` | FalkorDB password (if authentication enabled) | - | No | `your-password` |
| `PORT` | MCP server port | `8000` | No | `8000` |
| `MODEL_NAME` | OpenAI model to use | `gpt-4o-mini` | No | `gpt-5` |

### FalkorDB Cloud Configuration

To use FalkorDB Cloud with the MCP server:

```bash
docker run -d \
  --name graphiti-mcp \
  -e OPENAI_API_KEY="your-openai-api-key" \
  -e DATABASE_TYPE="falkordb" \
  -e FALKORDB_HOST="your-instance.falkordb.cloud" \
  -e FALKORDB_PORT="6379" \
  -e FALKORDB_USERNAME="default" \
  -e FALKORDB_PASSWORD="your-cloud-password" \
  -p 8000:8000 \
  falkordb/graphiti-knowledge-graph-mcp:latest
```

## Client Integration

### Claude Desktop

Configure Claude Desktop to use the Graphiti MCP server by editing your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the following configuration:

```json
{
  "mcpServers": {
    "graphiti-memory": {
      "transport": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

**Note**: The MCP server uses Server-Sent Events (SSE) for real-time communication between the AI client and the knowledge graph. The `OPENAI_API_KEY` is already configured in the MCP server's Docker environment, so you don't need to specify it again here.

**After configuration**:

1. Restart Claude Desktop to apply the changes
2. Look for the MCP server indicator in Claude's interface
3. Claude will now have access to persistent memory through the knowledge graph

### Cursor IDE

For Cursor IDE, add the MCP server configuration to your Cursor settings:

1. Open Cursor IDE settings
2. Navigate to the MCP configuration section
3. Add the server configuration:

```json
{
  "mcp": {
    "servers": {
      "graphiti-memory": {
        "url": "http://localhost:8000",
        "transport": "sse"
      }
    }
  }
}
```

### Testing the Connection

Once configured, test the connection with these steps:

1. **Restart your AI client** (Claude Desktop or Cursor)
2. **Look for the MCP indicator** in your client's interface
3. **Test with a simple prompt**:

   ```text
   "Remember that my favorite programming language is Python"
   ```

   The AI should confirm it has stored this information.

4. **Verify the memory**:

   ```text
   "What do you remember about my programming language preferences?"
   ```

   The AI should respond with "Python" or reference your previous statement.

5. **Check the graph** (optional):
   - Open [http://localhost:3000](http://localhost:3000) in your browser
   - Connect to the database
   - Run: `MATCH (n) RETURN n LIMIT 10`
   - You should see nodes representing the stored information

**More example prompts**:

- "Store this fact: I'm working on a project called MyApp"
- "What projects am I working on?"
- "Remember that I prefer dark mode in my IDE"

The AI will use the Graphiti MCP server to store and retrieve this information from the FalkorDB knowledge graph.

## MCP Server Capabilities

The Graphiti MCP server exposes the following capabilities to AI clients:

### Tools

- **`add_episode`**: Store new information as an episode in the knowledge graph
    - Extracts entities and relationships
    - Adds temporal context
    - Links to existing knowledge

- **`search`**: Query the knowledge graph for relevant information
    - Semantic search using embeddings
    - Graph traversal for connected information
    - Temporal filtering

- **`get_context`**: Retrieve contextual information for a conversation
    - Builds relevant context from the graph
    - Returns connected entities and relationships

### Graph Schema

The Graphiti MCP server stores information in FalkorDB using the following schema:

**Node Types**:

- **`Entity`**: Represents people, places, things, or concepts
    - Properties: `name`, `entity_type`, `summary`
- **`Episode`**: Represents events or pieces of information
    - Properties: `name`, `content`, `timestamp`, `source`

**Relationship Types**:

- **`RELATES_TO`**: Connects entities that are related
- **`MENTIONED_IN`**: Links entities to episodes where they appear
- **`OCCURRED_AFTER`**: Creates temporal ordering between episodes

**Graph Name**: All data is stored in a graph named `graphiti_memory`

## Advanced Usage

### Programmatic Access

{: .warning }
> **Important**: The Graphiti MCP server is designed to be used by MCP clients (like Claude Desktop or Cursor) via the Server-Sent Events (SSE) transport protocol. It does **not** expose HTTP REST API endpoints for direct programmatic access.

The server only exposes:

- `/sse` - Server-Sent Events endpoint for MCP protocol communication

To interact with the Graphiti knowledge graph programmatically, you have two options:

**Option 1: Use an MCP Client Library**

Use an MCP client library that implements the MCP protocol to communicate with the server via SSE. This is the intended way to interact with the server programmatically.

**Option 2: Access FalkorDB Directly**

Connect directly to FalkorDB to query the knowledge graph. See the "Custom Graph Queries" section below for details.

### Custom Graph Queries

For advanced users, you can connect directly to FalkorDB and run custom Cypher queries on the knowledge graph:

```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host='localhost', port=6379)

# Select the Graphiti memory graph
graph = db.select_graph('graphiti_memory')

# Example 1: Find all entities related to a specific entity
query = """
MATCH (e:Entity)-[r:RELATES_TO]->(e2:Entity)
WHERE e.name CONTAINS 'John'
RETURN e.name AS entity, type(r) AS relationship, e2.name AS related_entity
LIMIT 10
"""

result = graph.query(query)
for record in result.result_set:
    print(f"{record[0]} -> {record[1]} -> {record[2]}")

# Example 2: Find recent episodes
recent_episodes = """
MATCH (ep:Episode)
RETURN ep.name, ep.content, ep.timestamp
ORDER BY ep.timestamp DESC
LIMIT 5
"""

result = graph.query(recent_episodes)
for record in result.result_set:
    print(f"Episode: {record[0]} - {record[1]}")

# Example 3: Find entities mentioned in episodes
entity_episodes = """
MATCH (e:Entity)-[:MENTIONED_IN]->(ep:Episode)
WHERE e.name = 'John'
RETURN ep.name, ep.content
"""

result = graph.query(entity_episodes)
for record in result.result_set:
    print(f"Mentioned in: {record[0]}")
```

## Monitoring and Debugging

### View Server Logs

To view the MCP server logs:

```bash
docker logs -f graphiti-mcp
```

### Check FalkorDB Connection

Verify the connection to FalkorDB using the Redis CLI:

```bash
# Test from the FalkorDB container
docker exec -it falkordb redis-cli PING

# Test from the MCP container to FalkorDB
docker exec -it graphiti-mcp redis-cli -h falkordb -p 6379 PING
```

Both commands should return `PONG` if the connection is successful.

### Inspect the Knowledge Graph

Use the FalkorDB Browser to visualize the knowledge graph:

1. Open `http://localhost:3000` in your browser
2. Connect to the `graphiti_memory` graph
3. Run queries to explore stored knowledge:

```cypher
MATCH (n) RETURN n LIMIT 25
```

## Troubleshooting

### Connection Issues

**Problem**: MCP server cannot connect to FalkorDB

**Solutions**:

- Verify FalkorDB is running: `docker ps | grep falkordb`
- Test FalkorDB connection: `docker exec -it <falkordb-container-name> redis-cli PING` (should return `PONG`)
- Check network connectivity: Use `host.docker.internal` for local FalkorDB when running MCP server in Docker
- Verify port 6379 is accessible
- Check firewall settings
- Verify `DATABASE_TYPE=falkordb` environment variable is set (server won't start without it)

### Authentication Errors

**Problem**: FalkorDB authentication failed

**Solutions**:

- Ensure `FALKORDB_USERNAME` and `FALKORDB_PASSWORD` are set correctly
- For FalkorDB Cloud, use your cloud credentials
- For local instances without auth, leave username/password empty

### OpenAI API Issues

**Problem**: LLM operations fail

**Solutions**:

- Verify your `OPENAI_API_KEY` is valid
- Check you have sufficient API credits
- Ensure you have access to the specified model (default: `gpt-4o-mini`)
- Try setting `MODEL_NAME` to a different model

### Client Not Connecting

**Problem**: Claude Desktop or Cursor cannot connect to MCP server

**Solutions**:

- Verify the MCP server is running: `docker ps | grep graphiti-mcp`
- Check the server logs: `docker logs graphiti-mcp`
- Test the SSE endpoint: `curl http://localhost:8000/sse`
- Ensure the configuration file path is correct for your OS
- Restart the client application after changing configuration
- Check for port conflicts on port 8000: `lsof -i :8000` (macOS/Linux) or `netstat -ano | findstr :8000` (Windows)
- Verify JSON syntax in the configuration file

### Memory Not Persisting

**Problem**: Knowledge is lost between sessions

**Solutions**:

- Ensure FalkorDB has persistent storage configured
- Check that the Docker volume is mounted correctly
- Verify the graph name is consistent across sessions
- Use `docker-compose` with volumes for production

## Best Practices

1. **Use Environment Variables**: Store sensitive information like API keys in environment variables or `.env` files
2. **Enable Persistence**: Configure FalkorDB with persistent storage for production use
3. **Monitor Resources**: Track memory usage and query performance as the knowledge graph grows
4. **Regular Backups**: Back up your FalkorDB data regularly
5. **Use FalkorDB Cloud**: For production deployments, consider using FalkorDB Cloud for managed hosting
6. **Separate Graphs**: Use different graph names for different projects or users
7. **Clean Up**: Periodically review and clean up old or irrelevant data

## Performance Tips

- **Indexing**: FalkorDB automatically creates indexes for optimal query performance
- **Batch Operations**: For large data loads, consider batching multiple episodes
- **Graph Size**: Monitor graph size and consider archiving old episodes to separate graphs
- **Model Selection**:
    - Use `gpt-4o-mini` for cost-effective operations
    - Use `gpt-5` for better accuracy with complex relationships
- **Connection Pooling**: The MCP server handles connection pooling automatically
- **Query Optimization**: Use specific entity names and filters in search queries for faster results

## Resources

- 🐳 [Docker Hub Repository](https://hub.docker.com/r/falkordb/graphiti-knowledge-graph-mcp)
- 📚 [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- 📖 [Graphiti Documentation](https://help.getzep.com/graphiti/)
- 💻 [Graphiti GitHub Repository](https://github.com/getzep/graphiti)
- 🔗 [FalkorDB Documentation](https://docs.falkordb.com/)
- 📝 [MCP Integration Blog Post](https://www.falkordb.com/blog/mcp-integration-falkordb-graphrag/)

## Next Steps

- Explore [Graphiti Python Library](./graphiti.md) for direct integration
- Learn about [Cognee](./cognee.md) for flexible memory management
- Check out [GraphRAG SDK](/graphrag-sdk) for advanced reasoning
- Review [Cypher Query Language](/cypher) for custom graph queries

## Example Use Cases

### Personal Assistant Memory

Store personal preferences, tasks, and information:

```text
You: "Remember that I prefer Python over JavaScript"
AI: "I'll remember that you prefer Python over JavaScript."

You: "What programming languages do I prefer?"
AI: "You prefer Python over JavaScript."
```

### Project Knowledge Base

Build a knowledge base about your projects:

```text
You: "Store this: MyApp is a web application built with React and FastAPI"
AI: "I've stored that MyApp is a web application built with React and FastAPI."

You: "What technologies does MyApp use?"
AI: "MyApp uses React and FastAPI."
```

### Meeting Notes and Context

Remember meeting discussions and action items:

```text
You: "In today's meeting, we decided to migrate to FalkorDB for the knowledge graph backend"
AI: "I'll remember that decision from today's meeting."

You: "What did we decide about the knowledge graph backend?"
AI: "You decided to migrate to FalkorDB for the knowledge graph backend."
```
