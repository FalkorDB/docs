---
title: "QueryWeaver"
nav_order: 8
description: "Open-source Text2SQL tool that converts plain-English questions into SQL using graph-powered schema understanding."
parent: "GenAI Tools"
---

# QueryWeaver

[QueryWeaver](https://www.queryweaver.ai/) is an open-source Text2SQL tool that converts plain-English questions into SQL using **graph-powered schema understanding**. It helps you query databases with natural language and returns both the generated SQL and the results.

QueryWeaver uses FalkorDB to store and reason over database schema relationships as a graph, enabling more accurate and context-aware SQL generation.

## Resources

- 🔗 [QueryWeaver Website](https://www.queryweaver.ai/)
- 💻 [GitHub Repository](https://github.com/FalkorDB/QueryWeaver)
- 🐳 [Docker Hub](https://hub.docker.com/r/falkordb/queryweaver)
- 📖 [Swagger API Docs](https://app.queryweaver.ai/docs)
- ☁️ [Try Free on FalkorDB Cloud](https://app.falkordb.cloud)

## Quick Start

### Docker

The fastest way to get started is with Docker:

```bash
docker run -p 5000:5000 -it falkordb/queryweaver
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

### Using an `.env` File (Recommended)

For a configured deployment, copy the example environment file and pass it to Docker:

```bash
cp .env.example .env
# Edit .env with your values, then:
docker run -p 5000:5000 --env-file .env falkordb/queryweaver
```

## AI/LLM Configuration

QueryWeaver supports multiple AI providers. Set one API key and QueryWeaver auto-detects which provider to use.

**Priority order:** Ollama > OpenAI > Gemini > Anthropic > Cohere > Azure

| Provider | Environment Variable |
|----------|---------------------|
| Ollama | `OLLAMA_MODEL` |
| OpenAI | `OPENAI_API_KEY` |
| Google Gemini | `GEMINI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| Cohere | `COHERE_API_KEY` |
| Azure OpenAI | `AZURE_API_KEY` |

Example using OpenAI:

```bash
docker run -p 5000:5000 -it \
  -e FASTAPI_SECRET_KEY=your_secret_key \
  -e OPENAI_API_KEY=your_openai_api_key \
  falkordb/queryweaver
```

## REST API

QueryWeaver exposes a REST API for managing database schemas (graphs) and running Text2SQL queries. All endpoints require a bearer token for authentication.

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/graphs` | List available graphs for the authenticated user |
| `GET` | `/graphs/{graph_id}/data` | Return schema (tables, columns, foreign keys) for a graph |
| `POST` | `/graphs` | Upload or create a graph |
| `POST` | `/graphs/{graph_id}` | Run a Text2SQL chat query against the named graph |

### Authentication

Add an `Authorization` header with your API token:

```bash
Authorization: Bearer <API_TOKEN>
```

### Examples

**List graphs:**

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  https://app.queryweaver.ai/graphs
```

**Run a Text2SQL query:**

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"chat": ["How many users signed up last month?"]}' \
  https://app.queryweaver.ai/graphs/my_database
```

**Python example:**

```python
import requests

TOKEN = "your_api_token"
url = "https://app.queryweaver.ai/graphs/my_database"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

resp = requests.post(url, headers=headers, json={"chat": ["Count orders last week"]})
print(resp.text)
```

## MCP Server Support

QueryWeaver includes built-in support for the [Model Context Protocol (MCP)](https://modelcontextprotocol.io), exposing Text2SQL operations as MCP tools:

- `list_databases`
- `connect_database`
- `database_schema`
- `query_database`

To connect an MCP client to a local QueryWeaver instance, use this configuration:

```json
{
  "servers": {
    "queryweaver": {
      "type": "http",
      "url": "http://127.0.0.1:5000/mcp",
      "headers": {
        "Authorization": "Bearer your_token_here"
      }
    }
  }
}
```

To disable the built-in MCP endpoints:

```bash
docker run -p 5000:5000 -it --env DISABLE_MCP=true falkordb/queryweaver
```

## Use Cases

- **Natural Language Database Queries**: Ask questions in plain English and get SQL answers
- **Schema Exploration**: Browse and understand database schemas through conversation
- **Data Analysis**: Run ad-hoc queries without knowing SQL syntax
- **API Integration**: Embed Text2SQL capabilities in your own applications

## Related Tools

- [FalkorDB MCP Server](./mcpserver/): Enable AI assistants to interact with FalkorDB using MCP
- [GraphRAG-SDK](./graphrag-sdk.md): Build intelligent GraphRAG applications with FalkorDB and LLMs
