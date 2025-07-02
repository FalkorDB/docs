---
title: "GraphRAG-SDK"
nav_order: 8
description: "FalkorDB supports a number of LLM frameworks."
---

# GraphRAG-SDK
### Build intelligent GraphRAG applications with FalkorDB and LLMs

- Convert natural language questions into Cypher queries automatically
- Generate contextual answers from knowledge graph data
- Support for streaming responses and conversational sessions
- Compatible with multiple LLM providers (OpenAI, Gemini, Groq, etc.)

## Quick Start

### Install & Setup
```bash
# Start FalkorDB
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:edge

# Install SDK
pip install graphrag-sdk
```

### Basic Usage
```python
from graphrag_sdk import KnowledgeGraph
from graphrag_sdk.model_config import KnowledgeGraphModelConfig
from graphrag_sdk.ontology import Ontology
from falkordb import FalkorDB

# Connect to your knowledge graph
db = FalkorDB()
graph = db.select_graph("my_existing_graph")

# Extract ontology from existing knowledge graph
ontology = Ontology.from_kg_graph(graph, sample_size=100)

# Configure model and create GraphRAG instance
model_config = KnowledgeGraphModelConfig.with_model(your_llm)
kg = KnowledgeGraph(graph, model_config, ontology)

# Start chat session
chat = kg.start_chat()

# Ask questions
response = chat.send_message("What products are available?")
print(response["response"])

# Ask follow-up questions
response = chat.send_message("Tell me about user relationships")
print(response["response"])
```

## Key Features

- **Ontology Extraction**: Automatically extract schema and attributes from existing knowledge graphs
- **Smart Query Generation**: Convert natural language questions to optimized Cypher queries
- **Conversational Context**: Maintain chat history for contextual follow-up questions  
- **Streaming Support**: Real-time response chunks for better user experience
- **Flexible Sources**: Create ontologies from JSON, existing graphs, or data sources
- **Schema Management**: Build ontologies from graph schemas or knowledge graphs with sampling

## How it works

### 1️⃣ Extract and Build Ontologies from Multiple Sources
- **From Existing Graphs**: Automatically extract schema and attributes from knowledge graphs using `Ontology.from_kg_graph()`
- **From Data Sources**: Generate ontologies from diverse formats (PDF, CSV, HTML, TXT, JSON, URLs) using AI
- **From Schema Graphs**: Import ontologies directly from graph schemas with `Ontology.from_schema_graph()`
- **From JSON**: Load pre-defined ontologies from JSON configurations

### 2️⃣ Intelligent Query Generation and Execution
- **Natural Language Processing**: Convert user questions into optimized Cypher queries using LLMs
- **Context-Aware Generation**: Leverage ontology schema to ensure accurate and relevant queries
- **Multi-Step Pipeline**: Execute graph queries and synthesize natural language responses

### 3️⃣ Interactive Chat Sessions with Graph Context
- **Conversational Interface**: Maintain chat history for contextual follow-up questions
- **Streaming Responses**: Real-time response chunks for better user experience
- **Flexible Model Support**: Compatible with multiple LLM providers (OpenAI, Gemini, Groq)

> 📓  [Understanding Ontologies and Knowledge Graphs](https://www.falkordb.com/blog/understanding-ontologies-knowledge-graph-schemas/)


## LLMs & integrations

### LangChain
LangChain now integrates with FalkorDB, enabling graph database capabilities for AI-driven applications. This combination facilitates the creation of AI agents with memory, enhancing their ability to retain state and context across interactions.


[LangChain](https://www.langchain.com/) - [FalkorDBQAChain](https://python.langchain.com/docs/use_cases/more/graph/graph_falkordb_qa)

> 📓 [Build AI Agents with Memory: LangChain + FalkorDB](https://www.falkordb.com/blog/building-ai-agents-with-memory-langchain/)

### LangGraph
LangGraph is an open-source framework for building stateful, multi-actor agentic applications using LLMs. It enables you to design complex agent and multi-agent workflows by representing application logic as directed graphs—where nodes define tasks or functions, and edges determine the flow of information.
> 📓 [A Guide to Implementing a GraphRAG Workflow Using FalkorDB, LangChain and LangGraph](https://www.falkordb.com/blog/graphrag-workflow-falkordb-langchain/)

### LlamaIndex
LlamaIndex is an open-source framework that makes it easy for you to build LLM-powered applications. With its tools for ingesting different data structures, indexing, and querying, you can effortlessly create AI applications that tap into external knowledge.

There are two parts to a RAG system: the retrieval module and the generation module. We will use LlamaIndex to orchestrate the two steps. To power our retrieval module, we will use FalkorDB. For the generation, you can use any LLM that has been trained on Cypher queries, which are needed for fetching data from modern graph databases like FalkorDB.

[LlamaIndex](https://www.llamaindex.ai/) - [FalkorDB Graph Store](https://gpt-index.readthedocs.io/en/latest/examples/index_structs/knowledge_graph/FalkorDBGraphDemo.html)

> 📓  [LlamaIndex RAG: Build Efficient GraphRAG Systems](https://www.falkordb.com/blog/llamaindex-rag-implementation-graphrag/)


### Graphiti

Graphiti is a Python framework for building temporally-aware, multi-tenant live knowledge graph designed for multi-agent AI systems with persistent memory. It enables real-time integration of structured and unstructured data, supporting advanced hybrid search, temporal reasoning, and collaborative agent memory.

#### What does FalkorDB bring?

- **Multi-tenant, multi-agent memory**: Isolated graph instances for different users or agents, each with their own persistent memory.
- **High performance**: Fast graph operations and efficient memory usage.
- **Cloud and on-premises ready**: Works with FalkorDB Cloud or your own deployment.
- **Easy integration**: Seamless connection with Graphiti for scalable, production-ready knowledge graphs.

#### Use Cases

- **AI memory for multi-agent systems**: Provide persistent, context-rich memory for each agent.
- **Enterprise knowledge management**: Aggregate and search across documents, conversations, and structured data.
- **Conversational AI**: Track facts, entities, and relationships over time for more accurate responses.
- **E-commerce**: Manage inventory, personalize recommendations, and track customer interactions over time.
- **Research and analytics**: Temporal and semantic search across large, heterogeneous datasets.

#### Quickstart Usage

1. **Install Graphiti**  
   `pip install graphiti-core`

2. **Connect to your FalkorDB instance**  
   (Cloud or on-premises, see your FalkorDB dashboard for connection details.)

3. **Build indices, add episodes, and search**  
   - Initialize Graphiti with FalkorDB connection.
   - Build indices and constraints.
   - Add episodes (text or JSON).
   - Perform hybrid and node searches.

See the full quickstart example in the [Graphiti repository: examples/quickstart/quickstart_falkordb.py](https://github.com/getzep/graphiti/blob/main/examples/quickstart/quickstart_falkordb.py).


