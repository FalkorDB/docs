---
title: "MCP Server"
nav_order: 7
description: "Enable AI assistants like Claude to interact with FalkorDB graph databases using the Model Context Protocol (MCP)"
parent: "GenAI Tools"
has_children: true
---

# MCP Server

Enable AI assistants to query and interact with FalkorDB graph databases

A Model Context Protocol (MCP) server that allows AI models like Claude to interact with FalkorDB using natural language. Query your graph data, create relationships, and manage your knowledge graph through conversational AI.

- Query graph databases using OpenCypher (with read-only mode support)
- Create and manage nodes and relationships
- List and explore multiple graphs
- Delete graphs when needed
- Support for replica instances with read-only queries

## What is the Model Context Protocol?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io) is an open protocol that standardizes how AI applications provide context to Large Language Models (LLMs). It enables AI assistants to securely connect to external data sources and tools, making them more powerful and context-aware.

## Topics in This Section

- [Quick Start](./quickstart.md): Install and connect the MCP server to Claude Desktop in minutes.
- [Configuration](./configuration.md): Environment variables, transport modes, and multi-instance setup.
- [Docker Deployment](./docker.md): Run the MCP server using Docker Hub images.

## Resources

- 📦 [npm Package](https://www.npmjs.com/package/@falkordb/mcpserver)
- 💻 [GitHub Repository](https://github.com/FalkorDB/FalkorDB-MCPServer)
- 🐳 [Docker Hub](https://hub.docker.com/r/falkordb/mcpserver)
- 📖 [MCP Specification](https://modelcontextprotocol.io/docs)
- 📚 [FalkorDB Documentation](/)
- 🔍 [OpenCypher Query Language](https://opencypher.org/)
