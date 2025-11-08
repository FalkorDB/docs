---
title: "Text-to-Cypher"
nav_order: 7
description: >
    Convert natural language questions into Cypher queries using LLMs for intuitive graph querying.
parent: "GenAI Tools"
---

# Text-to-Cypher

Text-to-Cypher is a powerful feature that automatically converts natural language questions into Cypher queries using Large Language Models (LLMs). This enables developers and users to query graph databases using everyday language without needing to know the Cypher query language.

## Overview

Text-to-Cypher bridges the gap between natural language and graph queries by:

- **Converting questions to queries**: Automatically generates optimized Cypher queries from natural language
- **Understanding context**: Leverages graph ontology and schema to ensure accurate query generation
- **Supporting follow-up questions**: Maintains conversation context for multi-turn interactions
- **Working with multiple LLMs**: Compatible with various LLM providers (OpenAI, Gemini, Groq, etc.)

## How It Works

The Text-to-Cypher process involves several steps:

1. **Ontology Extraction**: The system analyzes your graph schema to understand node labels, relationship types, and properties
2. **Natural Language Processing**: User questions are processed by an LLM that understands both natural language and Cypher
3. **Query Generation**: The LLM generates an optimized Cypher query based on the question and graph schema
4. **Query Execution**: The generated query is executed against the graph database
5. **Response Synthesis**: Results are converted back into natural language answers

## Getting Started

Text-to-Cypher is available through the [GraphRAG SDK](/graphrag-sdk), which provides a complete solution for graph-based question answering.

### Prerequisites

- FalkorDB instance (local or cloud)
- Python 3.8 or higher
- API key for your chosen LLM provider (OpenAI, Gemini, Groq, etc.)

### Installation

```bash
pip install graphrag_sdk
```

### Basic Example

```python
import os
from falkordb import FalkorDB
from graphrag_sdk import KnowledgeGraph
from graphrag_sdk.ontology import Ontology
from graphrag_sdk.models.litellm import LiteModel
from graphrag_sdk.model_config import KnowledgeGraphModelConfig

# Connect to FalkorDB
db = FalkorDB(
    host=os.getenv("FALKORDB_HOST", "localhost"),
    port=os.getenv("FALKORDB_PORT", 6379),
    username=os.getenv("FALKORDB_USERNAME"),
    password=os.getenv("FALKORDB_PASSWORD")
)

# Select your graph
graph = db.select_graph("my_graph")

# Extract ontology from the graph
ontology = Ontology.from_kg_graph(graph)

# Configure the LLM
model = LiteModel()  # Uses OpenAI GPT-4.1 by default
model_config = KnowledgeGraphModelConfig.with_model(model)

# Create KnowledgeGraph instance
kg = KnowledgeGraph(
    name="my_graph",
    model_config=model_config,
    ontology=ontology,
    host=os.getenv("FALKORDB_HOST", "localhost"),
    port=os.getenv("FALKORDB_PORT", 6379),
    username=os.getenv("FALKORDB_USERNAME"),
    password=os.getenv("FALKORDB_PASSWORD")
)

# Start a chat session
chat = kg.chat_session()

# Ask questions in natural language
response = chat.send_message("What products are available?")
print(response["response"])

# Ask follow-up questions
response = chat.send_message("Which one is the most expensive?")
print(response["response"])
```

## Example Use Cases

### Product Catalog Queries

```python
# Natural language question
question = "Show me all electronics that cost less than $500"

# Generated Cypher query (automatic)
# MATCH (p:Product {category: 'Electronics'})
# WHERE p.price < 500
# RETURN p

response = chat.send_message(question)
```

### Relationship Traversal

```python
# Natural language question
question = "Who are the friends of Alice?"

# Generated Cypher query (automatic)
# MATCH (alice:Person {name: 'Alice'})-[:FRIENDS_WITH]->(friend)
# RETURN friend

response = chat.send_message(question)
```

### Complex Aggregations

```python
# Natural language question
question = "What is the average salary by department?"

# Generated Cypher query (automatic)
# MATCH (e:Employee)-[:WORKS_IN]->(d:Department)
# RETURN d.name AS department, avg(e.salary) AS avg_salary

response = chat.send_message(question)
```

## Advanced Features

### Custom LLM Configuration

You can specify different LLM models and providers:

```python
from graphrag_sdk.models.litellm import LiteModel

# Use a specific model
model = LiteModel(model_name="gpt-4-turbo")

# Or use a different provider
model = LiteModel(model_name="gemini/gemini-pro")
```

### Streaming Responses

Enable streaming for real-time response generation:

```python
# Create a streaming chat session
chat = kg.chat_session()

# Stream the response
for chunk in chat.send_message("What are the top products?", stream=True):
    print(chunk, end="", flush=True)
```

### Ontology Management

The ontology defines the schema that the LLM uses to generate queries:

```python
# Extract from existing graph
ontology = Ontology.from_kg_graph(graph)

# Load from JSON
ontology = Ontology.from_json("ontology.json")

# Build from schema graph
ontology = Ontology.from_schema_graph(schema_graph)
```

## Best Practices

### 1. Maintain a Clear Schema

Ensure your graph has a well-defined schema with:
- Descriptive node labels and relationship types
- Consistent property names
- Proper indexing for frequently queried properties

### 2. Provide Context

Include relevant context in your questions:
- ✅ "What products in the Electronics category cost less than $500?"
- ❌ "cheap stuff"

### 3. Use Follow-up Questions

Take advantage of conversational context:
```python
chat.send_message("Show me all employees")
chat.send_message("Which ones work in Engineering?")  # Context maintained
chat.send_message("What's their average salary?")     # Still contextual
```

### 4. Validate Generated Queries

For production use, consider validating or logging generated queries:
```python
response = chat.send_message("Your question")
generated_query = response.get("cypher_query")  # If available
print(f"Generated query: {generated_query}")
```

## Integration Patterns

### With LangChain

```python
from langchain.chains import GraphCypherQAChain
from langchain.llms import OpenAI

# Use FalkorDB with LangChain
chain = GraphCypherQAChain.from_llm(
    OpenAI(temperature=0),
    graph=graph,
    verbose=True
)

result = chain.run("What products are available?")
```

### With LlamaIndex

```python
from llama_index import KnowledgeGraphIndex

# Create index with FalkorDB
index = KnowledgeGraphIndex.from_graph(
    graph=graph,
    service_context=service_context
)

# Query using natural language
response = index.query("What are the relationships between entities?")
```

## Performance Considerations

### Query Optimization

Text-to-Cypher generates optimized queries, but consider:

- **Indexing**: Create indexes on frequently queried properties
- **Graph size**: Larger graphs may require more specific questions
- **LLM selection**: Faster models for real-time applications, more capable models for complex queries

### Caching

Implement caching for common questions:
```python
# Pseudo-code for caching
cache = {}
question = "What products are available?"

if question in cache:
    response = cache[question]
else:
    response = chat.send_message(question)
    cache[question] = response
```

## Troubleshooting

### Common Issues

**Query doesn't return expected results**
- Verify the ontology accurately represents your graph schema
- Check that property names match exactly
- Try rephrasing the question with more specifics

**LLM generates invalid Cypher**
- Ensure your graph schema is clean and consistent
- Update the ontology if schema changes
- Consider using a more capable LLM model

**Slow response times**
- Use faster LLM models for real-time applications
- Implement query result caching
- Optimize graph indexes

## Resources

- 📚 [GraphRAG SDK Documentation](/graphrag-sdk)
- 🔗 [GraphRAG SDK GitHub Repository](https://github.com/FalkorDB/GraphRAG-SDK)
- 📓 [Blog: Natural Language to Cypher Queries](https://www.falkordb.com/blog/)
- 💡 [LangChain Integration](https://python.langchain.com/docs/use_cases/more/graph/graph_falkordb_qa)
- 🦙 [LlamaIndex Integration](https://gpt-index.readthedocs.io/en/latest/examples/index_structs/knowledge_graph/FalkorDBGraphDemo.html)

## Next Steps

- Learn about [Cypher Query Language](/cypher)
- Explore [GraphRAG SDK](/graphrag-sdk) for advanced features
- Check out [LLM Framework Integrations](/llm-integrations)
- Try [Agentic Memory](/agentic-memory) for persistent context
