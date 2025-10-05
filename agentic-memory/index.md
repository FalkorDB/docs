---
title: "Agentic Memory"
description: "Learn how to implement agentic memory with FalkorDB for AI agents"
has_children: true
nav_order: 11
---

# Agentic Memory

Agentic memory enables AI agents to maintain persistent, contextual memory across interactions. FalkorDB provides an ideal foundation for implementing agentic memory systems through its graph database capabilities, allowing agents to store, retrieve, and reason over complex relationships and temporal information.

## What is Agentic Memory?

Agentic memory refers to the ability of AI agents to:
- **Remember past interactions** and learn from them
- **Build contextual understanding** through connected knowledge
- **Reason over temporal information** to understand how relationships evolve
- **Share memory across agents** in multi-agent systems
- **Scale efficiently** as knowledge grows

## Why FalkorDB for Agentic Memory?

FalkorDB's graph database architecture makes it uniquely suited for agentic memory:

- **Graph-Native Storage**: Natural representation of entities, relationships, and contexts
- **Fast Traversals**: Quick retrieval of connected information for context-aware responses
- **Temporal Support**: Track how knowledge and relationships change over time
- **Multi-Tenant Architecture**: Isolated memory spaces for different agents or users
- **Hybrid Search**: Combine vector similarity with graph relationships for precise retrieval
- **High Performance**: Scale from prototype to production seamlessly

## Agentic Memory Frameworks

This section covers popular frameworks that implement agentic memory with FalkorDB:

- [**Graphiti**](./graphiti.md): A temporally-aware knowledge graph framework designed for multi-agent AI systems with persistent memory
- [**Cognee**](./cognee.md): A memory management framework for AI agents that combines graph and vector storage

## Getting Started

Choose a framework based on your needs:
- If you need **temporal reasoning** and **multi-agent memory**, start with [Graphiti](./graphiti.md)
- If you need **flexible memory structures** with **hybrid storage**, explore [Cognee](./cognee.md)

Both frameworks integrate seamlessly with FalkorDB and can be used together in complex systems.
