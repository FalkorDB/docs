---
title: "Graphiti MCP Server"
description: "Run Graphiti MCP server with FalkorDB for AI agent memory in Claude Desktop and other MCP clients"
---

# Graphiti MCP Server

Graphiti is a framework for building and querying temporally-aware knowledge graphs, specifically tailored for AI agents operating in dynamic environments. The Graphiti MCP (Model Context Protocol) Server enables AI clients like Claude Desktop, Cursor IDE, and other MCP-compatible applications to interact with FalkorDB-powered knowledge graphs for persistent agent memory. This allows AI assistants to store and retrieve information across conversations, building a rich, contextual memory over time.

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open standard that enables AI applications to connect to external data sources and tools. The Graphiti MCP Server implements this protocol to provide AI agents with access to graph-based knowledge storage powered by FalkorDB.

## Features

The Graphiti MCP Server provides comprehensive knowledge graph capabilities:

- **Episode Management**: Add, retrieve, and delete episodes (text, messages, or JSON data)
- **Entity Management**: Search and manage entity nodes and relationships in the knowledge graph
- **Search Capabilities**: Search for facts (edges) and node summaries using semantic and hybrid search
- **Group Management**: Organize and manage groups of related data with group_id filtering
- **Graph Maintenance**: Clear the graph and rebuild indices
- **Multiple LLM Providers**: Support for OpenAI, Anthropic, Gemini, Groq, and Azure OpenAI
- **Multiple Embedding Providers**: Support for OpenAI, Voyage, Sentence Transformers, and Gemini embeddings
- **Rich Entity Types**: Built-in entity types including Preferences, Requirements, Procedures, Locations, Events, Organizations, Documents, and more for structured knowledge extraction
- **HTTP Transport**: Default HTTP transport with MCP endpoint at `/mcp/` for broad client compatibility
- **Queue-based Processing**: Asynchronous episode processing with configurable concurrency limits

## Prerequisites

Before you begin, ensure you have:
- Docker and Docker Compose installed on your system
- At least one LLM provider API key:
  - OpenAI API key (recommended)
  - Or Anthropic, Gemini, Groq, or Azure OpenAI API key
- (Optional) Python 3.10+ if running the MCP server standalone with an external FalkorDB instance

## Quick Start with Docker Compose

The easiest way to run the Graphiti MCP Server with FalkorDB is using the official Docker Compose configuration from [Zep's Graphiti repository](https://github.com/getzep/graphiti/tree/main/mcp_server).

### Option 1: Combined Image (Recommended)

This setup uses a single container that includes both FalkorDB and the MCP server.

1. **Create a directory for your setup:**

```bash
mkdir graphiti-mcp && cd graphiti-mcp
```

2. **Download the docker-compose configuration:**

```bash
curl -O https://raw.githubusercontent.com/getzep/graphiti/main/mcp_server/docker/docker-compose.yml
```

3. **Create a `.env` file with your API key:**

```env
OPENAI_API_KEY=your-openai-api-key
FALKORDB_PASSWORD=
GRAPHITI_GROUP_ID=main
```

4. **Start the services:**

```bash
docker-compose up -d
```

The combined image will start both FalkorDB and the MCP server in a single container, accessible at:
- **FalkorDB (Redis):** `localhost:6379`
- **FalkorDB Browser UI:** `http://localhost:3000`
- **MCP Server HTTP endpoint:** `http://localhost:8000/mcp/`
- **Health check:** `http://localhost:8000/health`

### Option 2: Separate Containers

For more flexibility, you can run FalkorDB and the MCP server in separate containers.

1. **Create a directory and download the configuration:**

```bash
mkdir graphiti-mcp && cd graphiti-mcp
curl -O https://raw.githubusercontent.com/getzep/graphiti/main/mcp_server/docker/docker-compose-falkordb.yml
mv docker-compose-falkordb.yml docker-compose.yml
```

2. **Create a `.env` file:**

```env
OPENAI_API_KEY=your-openai-api-key
FALKORDB_URI=redis://falkordb:6379
FALKORDB_PASSWORD=
FALKORDB_DATABASE=default_db
GRAPHITI_GROUP_ID=main
```

3. **Start the services:**

```bash
docker-compose up -d
```

This configuration starts FalkorDB and the MCP server as separate containers with the same accessible ports as the combined image.

## Manual Docker Setup (Alternative)

If you prefer to run containers manually without Docker Compose, you can use the standalone MCP server image:

### Step 1: Run FalkorDB

```bash
docker run -d \
  --name falkordb \
  -p 6379:6379 \
  -p 3000:3000 \
  falkordb/falkordb:latest
```

### Step 2: Run the MCP Server

```bash
docker run -d \
  --name graphiti-mcp \
  -e OPENAI_API_KEY="your-openai-api-key" \
  -e FALKORDB_URI="redis://host.docker.internal:6379" \
  -e FALKORDB_PASSWORD="" \
  -e FALKORDB_DATABASE="default_db" \
  -e GRAPHITI_GROUP_ID="main" \
  -p 8000:8000 \
  zepai/knowledge-graph-mcp:standalone
```

**Note**: Use `host.docker.internal` as the hostname to allow the container to access FalkorDB running on your host machine.

## Configuration

The Graphiti MCP server can be configured using environment variables in a `.env` file or through a `config.yaml` file.

### Default Configuration

The MCP server comes with sensible defaults:
- **Transport**: HTTP (accessible at `http://localhost:8000/mcp/`)
- **Database**: FalkorDB (combined in single container with MCP server)
- **LLM**: OpenAI with model gpt-4o-mini
- **Embedder**: OpenAI text-embedding-3-small

### LLM Provider Configuration

The server supports multiple LLM providers. Set the appropriate API key in your `.env` file:

**OpenAI (default)**:
```env
OPENAI_API_KEY=sk-proj-your-key-here
```

**Anthropic**:
```env
ANTHROPIC_API_KEY=your-anthropic-key
```

**Google Gemini**:
```env
GOOGLE_API_KEY=your-google-key
```

**Groq**:
```env
GROQ_API_KEY=your-groq-key
```

**Azure OpenAI**:
```env
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=your-endpoint-url
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

### Environment Variables

Key environment variables for the MCP server:

| Variable | Description | Default | Required | Example |
|----------|-------------|---------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key (or use another LLM provider) | - | Yes* | `sk-proj-...` |
| `FALKORDB_URI` | FalkorDB connection URI | `redis://localhost:6379` | No | `redis://falkordb:6379` |
| `FALKORDB_PASSWORD` | FalkorDB password (if authentication enabled) | - | No | `your-password` |
| `FALKORDB_DATABASE` | Database name | `default_db` | No | `default_db` |
| `SEMAPHORE_LIMIT` | Episode processing concurrency limit | `10` | No | `10` |
| `BROWSER` | Enable FalkorDB Browser UI (combined image) | `1` | No | `1` |

*At least one LLM provider API key is required

### Concurrency and Rate Limits

The `SEMAPHORE_LIMIT` controls how many episodes can be processed simultaneously. Adjust based on your LLM provider tier:

- **OpenAI Tier 1 (free)**: `SEMAPHORE_LIMIT=1-2`
- **OpenAI Tier 2**: `SEMAPHORE_LIMIT=5-8`
- **OpenAI Tier 3**: `SEMAPHORE_LIMIT=10-15`
- **OpenAI Tier 4**: `SEMAPHORE_LIMIT=20-50`
- **Anthropic default**: `SEMAPHORE_LIMIT=5-8`

If you see 429 rate limit errors, reduce the value. Monitor your LLM provider's dashboard for actual request rates.

### FalkorDB Cloud Configuration

To use FalkorDB Cloud with the MCP server, update your `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key
FALKORDB_URI=redis://your-instance.falkordb.cloud:6379
FALKORDB_PASSWORD=your-cloud-password
FALKORDB_DATABASE=default_db
GRAPHITI_GROUP_ID=main
```

Then use the docker-compose configuration with the separate containers option (docker-compose-falkordb.yml), as it's designed for external database connections.

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
      "transport": "http",
      "url": "http://localhost:8000/mcp/"
    }
  }
}
```

**Note**: The MCP server uses HTTP transport by default with the endpoint at `/mcp/`. The `OPENAI_API_KEY` is already configured in the MCP server's Docker environment, so you don't need to specify it again here.

**Alternative (stdio transport)**: If you have the Graphiti repository cloned locally and Python installed, you can use stdio transport for better integration with some clients. See the [official Graphiti documentation](https://github.com/getzep/graphiti/blob/main/mcp_server/README.md#integrating-with-mcp-clients) for stdio configuration details.

**After configuration**:
1. Restart Claude Desktop to apply the changes
2. Look for the MCP server indicator in Claude's interface
3. Claude will now have access to persistent memory through the knowledge graph

### Cursor IDE and VS Code

For Cursor IDE and VS Code with GitHub Copilot, add the MCP server configuration:

**Cursor IDE**: Add to Cursor settings

**VS Code**: Add to `.vscode/mcp.json` or global settings

```json
{
  "mcpServers": {
    "graphiti-memory": {
      "uri": "http://localhost:8000/mcp/",
      "transport": {
        "type": "http"
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

   ```
   "Remember that my favorite programming language is Python"
   ```
   
   The AI should confirm it has stored this information.

4. **Verify the memory**:

   ```
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

## Available Tools

The Graphiti MCP server exposes the following tools to AI clients:

- **`add_episode`**: Add an episode to the knowledge graph (supports text, JSON, and message formats)
- **`search_nodes`**: Search the knowledge graph for relevant node summaries
- **`search_facts`**: Search the knowledge graph for relevant facts (edges between entities)
- **`delete_entity_edge`**: Delete an entity edge from the knowledge graph
- **`delete_episode`**: Delete an episode from the knowledge graph
- **`get_entity_edge`**: Get an entity edge by its UUID
- **`get_episodes`**: Get the most recent episodes for a specific group
- **`clear_graph`**: Clear all data from the knowledge graph and rebuild indices

### Entity Types

Graphiti MCP Server includes built-in entity types for structured knowledge extraction. The MCP server automatically uses these entity types during episode ingestion to extract and structure information from conversations and documents.

**Available Entity Types:**

- **Preference**: User preferences, choices, opinions, or selections (prioritized for user-specific information)
- **Requirement**: Specific needs, features, or functionality that must be fulfilled
- **Procedure**: Standard operating procedures and sequential instructions
- **Location**: Physical or virtual places where activities occur
- **Event**: Time-bound activities, occurrences, or experiences
- **Organization**: Companies, institutions, groups, or formal entities
- **Document**: Information content in various forms (books, articles, reports, videos, etc.)
- **Topic**: Subject of conversation, interest, or knowledge domain (used as a fallback)
- **Object**: Physical items, tools, devices, or possessions (used as a fallback)

These entity types can be customized in the `config.yaml` file if you're running the MCP server from source.

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
> **Important**: The Graphiti MCP server is designed to be used by MCP clients (like Claude Desktop or Cursor) via the HTTP transport protocol. It does **not** expose direct REST API endpoints outside of the MCP protocol.

The server exposes:
- `/mcp/` - HTTP MCP protocol endpoint
- `/health` - Health check endpoint

To interact with the Graphiti knowledge graph programmatically, you have two options:

**Option 1: Use an MCP Client Library**

Use an MCP client library that implements the MCP protocol to communicate with the server via HTTP. This is the intended way to interact with the server programmatically.

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

To view the logs:

**For combined image:**
```bash
docker logs -f graphiti-falkordb
```

**For separate containers:**
```bash
# MCP server logs
docker logs -f graphiti-mcp

# FalkorDB logs
docker logs -f falkordb
```

### Check FalkorDB Connection

Verify the connection to FalkorDB using the Redis CLI:

**For combined image:**
```bash
docker exec -it graphiti-falkordb redis-cli PING
```

**For separate containers:**
```bash
# Test from the FalkorDB container
docker exec -it falkordb redis-cli PING

# Test from the MCP container to FalkorDB
docker exec -it graphiti-mcp redis-cli -h falkordb -p 6379 PING
```

All commands should return `PONG` if the connection is successful.

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
- Check the `FALKORDB_URI` format: `redis://hostname:port`
- For separate containers, use the service name: `redis://falkordb:6379`
- For external FalkorDB, use `redis://host.docker.internal:6379`
- Verify port 6379 is accessible
- Check firewall settings

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
- Verify the MCP server is running: `docker ps | grep graphiti`
- Check the server logs: `docker logs graphiti-mcp` (or `docker logs graphiti-falkordb` for combined image)
- Test the MCP endpoint: `curl http://localhost:8000/mcp/`
- Check the health endpoint: `curl http://localhost:8000/health`
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

- 🐳 [Graphiti MCP Server Docker Setup](https://github.com/getzep/graphiti/tree/main/mcp_server/docker)
- 📦 [Docker Hub Repository](https://hub.docker.com/r/zepai/knowledge-graph-mcp)
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

```
You: "Remember that I prefer Python over JavaScript"
AI: "I'll remember that you prefer Python over JavaScript."

You: "What programming languages do I prefer?"
AI: "You prefer Python over JavaScript."
```

### Project Knowledge Base

Build a knowledge base about your projects:

```
You: "Store this: MyApp is a web application built with React and FastAPI"
AI: "I've stored that MyApp is a web application built with React and FastAPI."

You: "What technologies does MyApp use?"
AI: "MyApp uses React and FastAPI."
```

### Meeting Notes and Context

Remember meeting discussions and action items:

```
You: "In today's meeting, we decided to migrate to FalkorDB for the knowledge graph backend"
AI: "I'll remember that decision from today's meeting."

You: "What did we decide about the knowledge graph backend?"
AI: "You decided to migrate to FalkorDB for the knowledge graph backend."
```
