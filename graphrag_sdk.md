---
title: "GraphRAG-SDK"
nav_order: 8
description: "Build intelligent GraphRAG applications with FalkorDB and LLMs."
---

# GraphRAG-SDK
### Build intelligent GraphRAG applications with FalkorDB and LLMs

- Automatically converts natural language questions into high-quality [Cypher](https://docs.falkordb.com/cypher/) queries.
- Automatically generates contextually relevant answers from knowledge graph data.
- Supports streaming responses and conversational sessions.
- Integrates with multiple language model providers (OpenAI, Gemini, Groq, etc.).

## Quick Start

### Start FalkorDB Graph Instance
```bash
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:edge
```

Or sign up for [FalkorDB Cloud](https://app.falkordb.cloud)

### Install SDK & Environment Configuration
```bash
pip install graphrag_sdk

# FalkorDB Connection (defaults are for on-premises)
export FALKORDB_HOST="localhost" 
export FALKORDB_PORT=6379 
export FALKORDB_USERNAME="your-username"  # optional for on-premises
export FALKORDB_PASSWORD="your-password"  # optional for on-premises

# LLM Provider (choose one)
export OPENAI_API_KEY="your-key"  # or GOOGLE_API_KEY, GROQ_API_KEY, etc.
```

### Basic Usage
```python
import os
from falkordb import FalkorDB
from graphrag_sdk import KnowledgeGraph
from graphrag_sdk.ontology import Ontology
from graphrag_sdk.models.litellm import LiteModel
from graphrag_sdk.model_config import KnowledgeGraphModelConfig

graph_name = "my_existing_graph"

# Connect to FalkorDB using environment variables
db = FalkorDB(
    host=os.getenv("FALKORDB_HOST", "localhost"),
    port=os.getenv("FALKORDB_PORT", 6379),
    username=os.getenv("FALKORDB_USERNAME"),  # optional for on-premises
    password=os.getenv("FALKORDB_PASSWORD")   # optional for on-premises
)

# Select graph
graph = db.select_graph(graph_name)

# Extract ontology from existing knowledge graph
ontology = Ontology.from_kg_graph(graph)

# Configure model and create GraphRAG instance
model = LiteModel()  # Default is OpenAI GPT-4.1, can specify different model
model_config = KnowledgeGraphModelConfig.with_model(model)

# Create KnowledgeGraph instance
kg = KnowledgeGraph(
    name=graph_name,
    model_config=model_config,
    ontology=ontology,
    host=os.getenv("FALKORDB_HOST", "localhost"),
    port=os.getenv("FALKORDB_PORT", 6379),
    username=os.getenv("FALKORDB_USERNAME"),
    password=os.getenv("FALKORDB_PASSWORD")
)

# Start chat session
chat = kg.chat_session()

# Ask questions
response = chat.send_message("What products are available?")
print(response["response"])

# Ask follow-up questions
response = chat.send_message("Tell me which one of them is the most expensive")
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
