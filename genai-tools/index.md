---
title: "GenAI Tools"
description: "Build intelligent GenAI applications with FalkorDB and LLMs using popular GraphRAG and agent frameworks like LangChain and LlamaIndex."
has_children: true
nav_order: 8
redirect_from:
  - /llm_integrations.html
  - /llm_integrations
  - /llm-integrations.html
  - /llm-integrations
  - /llm_support.html
  - /llm_support
---

# GenAI Tools

FalkorDB provides powerful tools and integrations for building intelligent GenAI applications with graph databases and Large Language Models (LLMs).

## Topics in This Section

- [GraphRAG-SDK](./graphrag-sdk.md): Build intelligent GraphRAG applications with FalkorDB and LLMs.
- [AG2](./ag2.md): Build multi-agent AI systems with AG2 (formerly AutoGen) and FalkorDB GraphRAG.
- [LangChain](./langchain.md): Integration with LangChain for AI agents with memory (Python and JavaScript/TypeScript).
- [LangGraph](./langgraph.md): Build stateful, multi-actor agentic applications with LangGraph.
- [LlamaIndex](./llamaindex.md): Simplify development of LLM-powered applications with LlamaIndex.
- [GraphRAG Toolkit](./graphrag-toolkit.md): AWS GraphRAG Toolkit integration for building knowledge graph applications.
- [FalkorDB MCP Server](./mcpserver/): Enable AI assistants like Claude to interact with FalkorDB using the Model Context Protocol.
- [QueryWeaver](./queryweaver.md): Open-source Text2SQL tool that converts plain-English questions into SQL using graph-powered schema understanding.
- [Code-Graph](./code-graph.md): Visualize codebases as knowledge graphs to analyze dependencies, detect bottlenecks, and query code structure.

{% include faq_accordion.html title="Frequently Asked Questions" q1="What are FalkorDB GenAI Tools?" a1="FalkorDB GenAI Tools are a collection of integrations and SDKs that enable developers to build intelligent AI applications using graph-based knowledge retrieval. They include GraphRAG SDK, LangChain/LlamaIndex integrations, AG2 multi-agent framework, LangGraph, MCP Server, QueryWeaver, and Code-Graph." q2="Which LLM providers are supported?" a2="FalkorDB GenAI Tools support multiple LLM providers including **OpenAI**, **Google Gemini**, **Anthropic**, **Groq**, **Cohere**, and **Azure OpenAI**. The specific providers available depend on the tool you are using." q3="Do I need a running FalkorDB instance to use these tools?" a3="Yes, all GenAI Tools require a FalkorDB instance. You can run one locally with `docker run -p 6379:6379 -it --rm falkordb/falkordb:edge` or use [FalkorDB Cloud](https://app.falkordb.cloud) for a managed solution." q4="What is GraphRAG and how does FalkorDB implement it?" a4="GraphRAG (Graph Retrieval-Augmented Generation) combines knowledge graphs with LLMs to provide more accurate, contextual, and explainable AI responses. FalkorDB implements GraphRAG by storing data as a graph, converting natural language to Cypher queries, and using the retrieved graph data to generate answers." q5="Which programming languages are supported?" a5="Most FalkorDB GenAI Tools support **Python** as the primary language. The LangChain integration also supports **JavaScript/TypeScript**. The MCP Server is built with Node.js. Code-Graph analyzes Python, Java, and C# codebases." %}
