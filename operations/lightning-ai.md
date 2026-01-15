---
title: "Lightning.AI"
description: "Deploy FalkorDB on Lightning.AI"
---

# Deploy FalkorDB on Lightning.AI

[Lightning.AI](https://lightning.ai) is a platform for building and deploying AI applications with managed infrastructure. FalkorDB integrates seamlessly with Lightning.AI, enabling you to build fast, accurate GenAI applications using advanced RAG (Retrieval-Augmented Generation) with graph databases.

## Overview

FalkorDB on Lightning.AI provides a powerful combination for building advanced AI applications:

* **Graph-Enhanced RAG** - Leverage FalkorDB's graph database capabilities to enhance your RAG applications with contextual relationships
* **Managed Infrastructure** - Lightning.AI handles the infrastructure, so you can focus on building your application
* **Easy Deployment** - Get started quickly with pre-configured environments
* **Scalable** - Scale your applications as your needs grow

## Getting Started with FalkorDB on Lightning.AI

Lightning.AI provides a ready-to-use environment for building advanced RAG applications with FalkorDB.

### Access the Environment

1. Visit the [FalkorDB Lightning.AI Environment](https://lightning.ai/muhammadqadora/environments/build-fast-accurate-genai-apps-advanced-rag-with-falkordb)
2. Sign in to your Lightning.AI account or create one if needed
3. Fork or use the environment to start building your application

### Environment Features

The FalkorDB Lightning.AI environment includes:

* **Pre-configured FalkorDB Instance** - Ready-to-use graph database
* **Sample Code and Notebooks** - Examples demonstrating graph-enhanced RAG patterns
* **Required Dependencies** - All necessary libraries and tools pre-installed
* **Interactive Development** - Jupyter notebooks for interactive exploration

## Use Cases

### Advanced RAG with Graph Context

FalkorDB enhances traditional RAG applications by adding graph-based context:

```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host='localhost', port=6379)

# Select a graph for your knowledge base
graph = db.select_graph('knowledge_base')

# Create entities and relationships
graph.query("""
    CREATE (d:Document {id: 'doc1', content: 'FalkorDB is a graph database'}),
           (t:Topic {name: 'Graph Databases'}),
           (d)-[:RELATES_TO]->(t)
""")

# Query with graph context for RAG
result = graph.query("""
    MATCH (d:Document)-[:RELATES_TO]->(t:Topic {name: $topic})
    RETURN d.content
""", {'topic': 'Graph Databases'})
```

### Building GenAI Applications

Combine FalkorDB with LLMs to create intelligent applications:

1. **Knowledge Graph Construction** - Build structured knowledge from unstructured data
2. **Context-Aware Retrieval** - Use graph relationships to find relevant information
3. **Enhanced Generation** - Provide LLMs with rich, connected context
4. **Citation and Traceability** - Track information sources through graph relationships

## Integration Patterns

### Pattern 1: Graph-Enhanced Document Retrieval

```python
# Store documents with metadata and relationships
graph.query("""
    CREATE (d:Document {id: $doc_id, content: $content, embedding: $embedding}),
           (a:Author {name: $author}),
           (t:Topic {name: $topic}),
           (d)-[:WRITTEN_BY]->(a),
           (d)-[:ABOUT]->(t)
""", params={'doc_id': 'doc1', 'content': '...', 'embedding': [0.1, 0.2, 0.3],  # Example embedding vector
             'author': 'John Doe', 'topic': 'AI'})

# Retrieve with graph context
result = graph.query("""
    MATCH (d:Document)-[:ABOUT]->(t:Topic {name: $topic})
    MATCH (d)-[:WRITTEN_BY]->(a:Author)
    RETURN d.content, a.name, t.name
""", {'topic': 'AI'})
```

### Pattern 2: Entity Relationship Extraction

```python
# Extract entities and relationships from text
graph.query("""
    MERGE (e1:Entity {name: $entity1, type: $type1})
    MERGE (e2:Entity {name: $entity2, type: $type2})
    MERGE (e1)-[r:RELATES_TO {relation: $relation}]->(e2)
""", params={'entity1': 'FalkorDB', 'type1': 'Database',
             'entity2': 'Graph', 'type2': 'Concept',
             'relation': 'is_type_of'})

# Query relationships for context
result = graph.query("""
    MATCH (e1:Entity {name: $entity})-[r]->(e2:Entity)
    RETURN e2.name, type(r), e2.type
""", {'entity': 'FalkorDB'})
```

## Resources

### Documentation and Guides

* [GraphRAG Blog Post](https://www.falkordb.com/news-updates/falkordb-lightning-ai-integration-graphrag/)

## Next Steps

1. **Explore the Environment** - Try the [FalkorDB Lightning.AI environment](https://lightning.ai/muhammadqadora/environments/build-fast-accurate-genai-apps-advanced-rag-with-falkordb)
2. **Build Your First Graph** - Create a simple knowledge graph
3. **Integrate with LLMs** - Connect FalkorDB with your favorite LLM API
4. **Deploy Your Application** - Use Lightning.AI's deployment features to share your work

## Additional Deployment Options

While Lightning.AI provides an excellent platform for AI applications, FalkorDB can be deployed on various platforms:

* [FalkorDB Cloud](https://app.falkordb.cloud) - Managed cloud service
* [Railway Deployment](/operations/railway) - Quick deployment on Railway
* [Kubernetes](/operations/k8s_support) - Production-grade orchestration
* [Docker](/getting-started) - Local or self-hosted deployment
