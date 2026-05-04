---
title: "Docker Deployment"
parent: "MCP Server"
nav_order: 3
description: "Deploy FalkorDB MCP Server with Docker and Docker Compose including FalkorDB database, environment configuration, and production setup."
search_exclude: true
---

# Docker Deployment

## Using Docker Hub Images

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

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What Docker tags are available for the MCP Server?"
  a1="Three main tags are available: **latest** (stable release), **edge** (latest main branch build), and specific version tags like `1.0.0` for pinning to a known release."
  q2="How do I connect the Docker container to a local FalkorDB instance?"
  a2="Use `FALKORDB_HOST=host.docker.internal` to connect from inside the Docker container to a FalkorDB instance running on your host machine. Set `FALKORDB_PORT=6379` (or your custom port)."
  q3="How do I secure my Docker deployment?"
  a3="Set the `MCP_API_KEY` environment variable to require Bearer token authentication for all HTTP requests. Use `-e MCP_API_KEY=your-secret-key` when running the container."
  q4="Which port does the MCP Server expose in Docker?"
  a4="The MCP Server exposes port **3000** by default when running in HTTP transport mode. Map it with `-p 3000:3000` in your Docker run command."
%}
