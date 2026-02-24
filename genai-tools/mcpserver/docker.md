---
title: "Docker Deployment"
parent: "MCP Server"
nav_order: 3
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
