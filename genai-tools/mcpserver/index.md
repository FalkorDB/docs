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

{% include faq_accordion.html title="Frequently Asked Questions" q1="What is the FalkorDB MCP Server?" a1="The FalkorDB MCP Server is a Model Context Protocol server that allows AI assistants like Claude to interact with FalkorDB graph databases using natural language. It enables querying, creating nodes/relationships, listing graphs, and managing data through conversational AI." q2="What is the Model Context Protocol (MCP)?" a2="MCP is an open protocol that standardizes how AI applications provide context to Large Language Models. It enables AI assistants to securely connect to external data sources and tools, making them more powerful and context-aware." q3="Which AI assistants work with the FalkorDB MCP Server?" a3="The MCP Server works with any MCP-compatible client including **Claude Desktop**, **Cursor IDE**, **VS Code with GitHub Copilot**, and other AI tools that support the Model Context Protocol." q4="Can I use the MCP Server in read-only mode?" a4="Yes. Set `FALKORDB_DEFAULT_READONLY=true` to prevent write operations. This is ideal for replica instances, production safety, reporting dashboards, and multi-tenant environments where certain users should only have read access." q5="What transport modes are available?" a5="The MCP Server supports two transport modes: **stdio** (default) for direct integration with AI clients like Claude Desktop via standard input/output, and **HTTP** for remote or networked access with optional API key authentication." %}
