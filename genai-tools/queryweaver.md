---
title: "QueryWeaver"
nav_order: 8
description: "Open-source Text2SQL tool that converts plain-English questions into SQL using graph-powered schema understanding. Supports PostgreSQL, MySQL, and Snowflake."
parent: "GenAI Tools"
---

# QueryWeaver

<a href="https://www.queryweaver.ai/">QueryWeaver</a> is an open-source Text2SQL tool that converts plain-English questions into SQL using **graph-powered schema understanding**. It helps you query databases like **PostgreSQL**, **MySQL**, and **Snowflake** without writing a single line of SQL.

QueryWeaver uses FalkorDB to store and reason over database schema relationships as a graph, enabling more accurate and context-aware SQL generation.

![QueryWeaver UI Demo](https://github.com/user-attachments/assets/34663279-0273-4c21-88a8-d20700020a07)

## Supported Databases

QueryWeaver works with the following SQL databases:

| Database | Type |
|----------|------|
| PostgreSQL | Relational (open-source) |
| MySQL | Relational (open-source) |
| Snowflake | Cloud Data Warehouse |

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

> **Note:** You will need to connect a supported database (PostgreSQL, MySQL, or Snowflake) through the UI or via environment variables before running queries.

Then open [http://localhost:5000](http://localhost:5000) in your browser.

### Using an `.env` File (Recommended)

For a configured deployment, copy the example environment file and pass it to Docker:

```bash
cp .env.example .env
# Edit .env with your values, then:
docker run -p 5000:5000 --env-file .env falkordb/queryweaver
```

## AI/LLM Configuration

QueryWeaver supports multiple AI providers. Set one provider-specific environment variable and QueryWeaver auto-detects which provider to use. For Ollama, set `OLLAMA_MODEL` to your local model name; for all other providers, set the corresponding API key.

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

```http
Authorization: Bearer <API_TOKEN>
```

API tokens can be created from the web UI (account settings → API tokens) or via the `/tokens` routes. For a local Docker deployment, any token you create through the UI at `http://localhost:5000` will work.

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

To connect a VS Code (GitHub Copilot) MCP client to a local QueryWeaver instance, add the following to your `mcp.json` file:

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

For Claude Desktop (`claude_desktop_config.json`), QueryWeaver's HTTP MCP surface can be referenced using:

```json
{
  "mcpServers": {
    "queryweaver": {
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

- **Natural Language Database Queries**: Ask questions in plain English and get SQL answers against PostgreSQL, MySQL, or Snowflake databases
- **Snowflake Analytics**: Query your Snowflake data warehouse using plain English, no SQL expertise required
- **Multi-database Support**: Connect and query across PostgreSQL, MySQL, and Snowflake from a single interface
- **Schema Exploration**: Browse and understand database schemas through conversation
- **Data Analysis**: Run ad-hoc queries without knowing SQL syntax
- **API Integration**: Embed Text2SQL capabilities in your own applications

## Related Tools

- [FalkorDB MCP Server](./mcpserver/): Enable AI assistants to interact with FalkorDB using MCP
- [GraphRAG-SDK](./graphrag-sdk.md): Build intelligent GraphRAG applications with FalkorDB and LLMs

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What is QueryWeaver?"
  a1="QueryWeaver is an open-source Text2SQL tool that converts plain-English questions into SQL queries using graph-powered schema understanding. It uses FalkorDB to store and reason over database schema relationships as a graph, enabling more accurate SQL generation."
  q2="Which databases does QueryWeaver support?"
  a2="QueryWeaver supports **PostgreSQL**, **MySQL**, and **Snowflake**. Connect your database through the web UI or via environment variables, and QueryWeaver will introspect the schema to enable accurate Text2SQL generation."
  q3="Which AI providers does QueryWeaver support?"
  a3="QueryWeaver supports **Ollama** (local models), **OpenAI**, **Google Gemini**, **Anthropic**, **Cohere**, and **Azure OpenAI**. Set the appropriate environment variable and QueryWeaver auto-detects the provider. Priority order: Ollama > OpenAI > Gemini > Anthropic > Cohere > Azure."
  q4="Can I use QueryWeaver with MCP-compatible AI assistants?"
  a4="Yes. QueryWeaver includes built-in MCP server support, exposing tools like `list_databases`, `connect_database`, `database_schema`, and `query_database`. Configure your MCP client (Claude Desktop, VS Code Copilot) to connect to `http://127.0.0.1:5000/mcp`."
  q5="How do I get started quickly?"
  a5="Run `docker run -p 5000:5000 -it falkordb/queryweaver` and open http://localhost:5000 in your browser. Set an LLM provider API key (e.g., `OPENAI_API_KEY`) as an environment variable for AI-powered SQL generation."
  q6="Does QueryWeaver have a REST API?"
  a6="Yes. QueryWeaver exposes REST endpoints for managing graphs and running Text2SQL queries. Key endpoints include `GET /graphs` to list databases, `POST /graphs/{graph_id}` to run queries, and all require Bearer token authentication."
%}
