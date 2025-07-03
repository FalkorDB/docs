---
title: "GraphRAG-SDK"
nav_order: 8
description: "Build intelligent GraphRAG applications with FalkorDB and LLMs."
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
from falkordb import FalkorDB
from graphrag_sdk import KnowledgeGraph
from graphrag_sdk.ontology import Ontology
from graphrag_sdk.models.litellm import LiteModel
from graphrag_sdk.model_config import KnowledgeGraphModelConfig

# Connect to your knowledge graph
db = FalkorDB()
graph = db.select_graph("my_existing_graph")

# Extract ontology from existing knowledge graph
ontology = Ontology.from_kg_graph(graph, sample_size=100)

# Configure model and create GraphRAG instance
model = LiteModel()
model_config = KnowledgeGraphModelConfig.with_model(model)
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
