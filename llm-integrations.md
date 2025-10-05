---
title: "LLM Framework Integrations"
nav_order: 9
description: "FalkorDB integrations with popular LLM frameworks and tools."
redirect_from:
  - /llm_integrations.html
  - /llm_integrations
---

# LLM Framework Integrations

FalkorDB integrates with various LLM frameworks to enhance AI-powered applications with graph database capabilities.

## Graphiti

[Graphiti](https://help.getzep.com/graphiti/configuration/graph-db-configuration#falkordb) is a Python framework for building temporally-aware, multi-tenant live knowledge graph designed for multi-agent AI systems with persistent memory. It enables real-time integration of structured and unstructured data, supporting advanced hybrid search, temporal reasoning, and collaborative agent memory.

> **August 2025 Update**: Watch our "How to Build a Knowledge Graph ft. Gaphiti" in collaboration with Graphiti:
> 
> [Workshop recording](https://www.youtube.com/watch?v=F4hwuLlISP4&lc=UgwPSaR6GAM_86g9AxJ4AaABAg)
> [Google Collab](https://colab.research.google.com/drive/1HbDPKlsz9tYfRGeWHn60vsWeGhFIsqyF?usp=sharing)

### FalkorDB's Added Value

- **Multi-tenant, multi-agent memory**: Isolated graph instances for different users or agents, each with their own persistent memory.
- **High performance**: Fast graph operations and efficient memory usage.
- **Cloud and on-premises ready**: Works with FalkorDB Cloud or your own deployment.
- **Easy integration**: Seamless connection with Graphiti for scalable, production-ready knowledge graphs.

### Use Cases

- **AI memory for multi-agent systems**: Provide persistent, context-rich memory for each agent.
- **Enterprise knowledge management**: Aggregate and search across documents, conversations, and structured data.
- **Conversational AI**: Track facts, entities, and relationships over time for more accurate responses.
- **E-commerce**: Manage inventory, personalize recommendations, and track customer interactions over time.
- **Research and analytics**: Temporal and semantic search across large, heterogeneous datasets.

### Quickstart Usage

1. **Install Graphiti**  
   `pip install graphiti-core[falkord-db]`

2. **Connect to your FalkorDB instance**  
   (Cloud or on-premises, see your FalkorDB dashboard for connection details.)

3. **Build indices, add episodes, and search**  
   - Initialize Graphiti with FalkorDB connection.
   - Build indices and constraints.
   - Add episodes (text or JSON).
   - Perform hybrid and node searches.

See the full quickstart example in the [Graphiti repository: examples/quickstart/quickstart_falkordb.py](https://github.com/getzep/graphiti/blob/main/examples/quickstart/quickstart_falkordb.py).

---

## LangChain

FalkorDB is now integrated with [LangChain](https://www.langchain.com/), bringing powerful graph database capabilities to AI-driven applications. This integration enables the creation of AI agents with memory, enhancing their ability to retain state and context across interactions.

- 🔗 [FalkorDBQAChain Documentation](https://python.langchain.com/docs/use_cases/more/graph/graph_falkordb_qa)  
- 📓 [Blog: Build AI Agents with Memory – LangChain + FalkorDB](https://www.falkordb.com/blog/building-ai-agents-with-memory-langchain/)

---

## LangGraph

[LangGraph](https://www.langgraph.dev/) is an open-source framework for building **stateful, multi-actor agentic applications** using LLMs. It allows you to design complex single- and multi-agent workflows as directed graphs, where nodes represent tasks and edges define the information flow.

- 📓 [Blog: Implementing GraphRAG with FalkorDB, LangChain & LangGraph](https://www.falkordb.com/blog/graphrag-workflow-falkordb-langchain/)

---

## LlamaIndex

[LlamaIndex](https://www.llamaindex.ai/) is an open-source framework designed to simplify the development of LLM-powered applications. It provides tools for ingesting, indexing, and querying diverse data sources.

In a typical RAG (Retrieval-Augmented Generation) setup, LlamaIndex orchestrates both the retrieval and generation phases. FalkorDB powers the retrieval module using Cypher queries, while any LLM trained on Cypher can handle the generation step—making it a natural fit for graph-native workflows.

- 🔗 [FalkorDB Graph Store Demo](https://gpt-index.readthedocs.io/en/latest/examples/index_structs/knowledge_graph/FalkorDBGraphDemo.html)  
- 📓 [Blog: LlamaIndex RAG – Build Efficient GraphRAG Systems](https://www.falkordb.com/blog/llamaindex-rag-implementation-graphrag/)
