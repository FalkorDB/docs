---
title: "MCP Server Configuration"
parent: "MCP Server"
nav_order: 2
description: "Configure FalkorDB MCP Server environment variables, transport modes (stdio/SSE), connection settings, and multi-instance deployments."
search_exclude: true
---

# MCP Server Configuration

## Environment Variables

```bash
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

## Transport Modes

### stdio (default)
Used for direct integration with AI clients like Claude Desktop. Communication happens via standard input/output.

```bash
MCP_TRANSPORT=stdio
```

### HTTP
Exposes the MCP server over HTTP for remote or networked access:

```bash
MCP_TRANSPORT=http
MCP_PORT=3000
MCP_API_KEY=your-secret-api-key  # Optional but recommended
```

When using HTTP transport, clients connect via the MCP Streamable HTTP protocol. API key authentication is enforced via the `Authorization: Bearer <key>` header when `MCP_API_KEY` is set.

## Read-Only Mode for Replica Instances

Enable read-only mode by default to prevent writes to replica instances:

```bash
FALKORDB_DEFAULT_READONLY=true
```

**Use cases:**
- **Replica instances**: Prevent writes to read replicas in replication setups
- **Production safety**: Ensure critical data isn't accidentally modified
- **Reporting/analytics**: Run queries for dashboards without risk of data changes
- **Multi-tenant environments**: Provide read-only access to certain users

## Running Multiple Instances

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

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What environment variables are required?"
  a1="Only `FALKORDB_HOST` and `FALKORDB_PORT` are required (defaulting to `localhost` and `6379`). Username, password, transport mode, and logging are all optional configuration options."
  q2="What is the difference between stdio and HTTP transport?"
  a2="**stdio** is the default mode for direct integration with AI clients like Claude Desktop, communicating via standard input/output. **HTTP** exposes the server over a network port for remote access, supporting API key authentication via Bearer tokens."
  q3="How do I secure the HTTP transport mode?"
  a3="Set `MCP_API_KEY` to a secret value. When configured, clients must include an `Authorization: Bearer <key>` header in their requests. This is optional but recommended for any network-exposed deployment."
  q4="Can I connect to multiple FalkorDB instances?"
  a4="Yes. Configure multiple MCP server entries in your client config, each with different `FALKORDB_HOST` values and settings. For example, have a `falkordb-dev` instance with writes enabled and a `falkordb-prod-replica` in read-only mode."
  q5="When should I use read-only mode?"
  a5="Enable `FALKORDB_DEFAULT_READONLY=true` for replica instances, production environments where accidental writes must be prevented, reporting/analytics dashboards, and multi-tenant setups where certain users should only have read access."
%}
```
