# FalkorDB Product Overview

## Executive Summary

**FalkorDB** is the graph platform developers use to achieve accurate GraphRAG for enterprise GenAI applications. It delivers an accurate, multi-tenant RAG solution powered by a low-latency, scalable graph database technology.

**Tagline:** *"The fastest way to your knowledge"*

---

## Core Value Proposition

FalkorDB is purpose-built for development teams working with complex, interconnected data—whether structured or unstructured—in real-time or interactive user environments. The platform combines:

- **Property graph database** with OpenCypher query language support
- **Advanced GraphRAG capabilities** for AI-powered knowledge retrieval
- **High-performance architecture** with low-latency operations
- **Multi-tenant design** for enterprise-scale deployments

---

## Two Paths to Success

### 1. Graph Database Path
Use FalkorDB as a high-performance property graph database with OpenCypher support for traditional graph data modeling and querying.

### 2. GraphRAG Path
Implement advanced graph reasoning and generative AI tasks using the integrated GraphRAG SDK for intelligent knowledge retrieval and question answering.

---

## Primary Features

### Graph Database Core
- **Property Graph Model**: Adopts industry-standard property graph model
- **OpenCypher Support**: Full support for OpenCypher query language with proprietary extensions
- **Protocol Flexibility**: Interacts via both RESP (Redis) and Bolt protocols
- **Sparse Adjacency Matrices**: Efficient graph representation for optimal performance

### Advanced Indexing
- **Range Indexing**: Single-property indexes for nodes and relationships (string, numeric, geospatial, array)
- **Full-Text Search**: Powered by RediSearch with language support and phonetic search
- **Vector Similarity**: Vector indexing for semantic search (euclidean, cosine similarity)
- **Geospatial Indexing**: Location-based queries with distance calculations

### Data Types
- **Scalar Types**: Strings, booleans, integers, floats, geospatial points
- **Temporal Types**: Date, Time, DateTime, Duration (ISO 8601 compliant)
- **Collection Types**: Arrays, maps with projection and merging capabilities
- **Vector Type**: Native vector data type for AI/ML applications

### Graph Algorithms
Built-in high-performance algorithms accessible via `CALL algo.<name>()`:

**Pathfinding:**
- BFS (Breadth-First Search)
- Shortest Path (SPpath)
- Single Source Path (SSpath)

**Centrality Measures:**
- PageRank
- Betweenness Centrality

**Community Detection:**
- Weakly Connected Components (WCC)
- Community Detection Label Propagation (CDLP)

---

## GraphRAG SDK

The GraphRAG SDK transforms FalkorDB into an intelligent question-answering system:

### Key Capabilities
- **Natural Language to Cypher**: Automatically converts questions into optimized Cypher queries
- **Contextual Answers**: Generates natural language responses from graph data
- **Ontology Extraction**: Automatically extracts schema from existing graphs
- **Conversational Context**: Maintains chat history for follow-up questions
- **Streaming Support**: Real-time response chunks for better UX
- **Multi-LLM Support**: Works with OpenAI, Gemini, Groq, and other providers

### How It Works
1. **Ontology Building**: Extract or define graph schema from multiple sources (existing graphs, JSON, data sources)
2. **Query Generation**: Convert natural language to context-aware Cypher queries using LLMs
3. **Interactive Sessions**: Maintain conversational context for multi-turn interactions

---

## Agentic Memory

FalkorDB enables AI agents to maintain persistent, contextual memory across interactions:

### Capabilities
- **Persistent Memory**: Remember past interactions and learn from them
- **Contextual Understanding**: Build knowledge through connected relationships
- **Temporal Reasoning**: Track how relationships evolve over time
- **Multi-Agent Support**: Share memory across agents with isolation
- **Hybrid Search**: Combine vector similarity with graph relationships

### Supported Frameworks
- **Graphiti**: Temporally-aware knowledge graph for multi-agent systems
- **Graphiti MCP Server**: Integrate with Claude Desktop, Cursor IDE (experimental)
- **Cognee**: Flexible memory management with hybrid storage

---

## LLM Framework Integrations

FalkorDB integrates seamlessly with popular AI frameworks:

### LangChain
- FalkorDBQAChain for graph-based question answering
- Enables AI agents with persistent memory

### LangGraph
- Stateful, multi-actor agentic applications
- Complex workflow design with FalkorDB as the knowledge layer

### LlamaIndex
- Retrieval-Augmented Generation (RAG) workflows
- FalkorDB as the retrieval module using Cypher queries

---

## Enterprise Operations

### Deployment Options
- **Docker**: Quick start with pre-built containers
- **FalkorDB Cloud**: Managed service (app.falkordb.cloud)
- **Kubernetes**: Helm charts for orchestrated deployments
- **On-Premises**: Full control with self-hosted deployments

### Production Features
- **Data Persistence**: Configurable persistence for data durability
- **Replication**: High availability with data redundancy
- **Clustering**: Horizontal scalability across multiple nodes
- **Multi-Tenancy**: Isolated graph instances per user/agent
- **OpenTelemetry**: Observability and tracing support

### Development Tools
- **FalkorDBLite**: Self-contained Python interface with embedded Redis
- **Bulk Loader**: Efficient CSV data import for large graphs
- **Migration Tools**: From Neo4j, Kuzu, RedisGraph, RDF

---

## Client Libraries

Multi-language support for diverse development environments:
- **Python**: falkordb-py
- **JavaScript/TypeScript**: falkordb-ts
- **Java**: JFalkorDB
- **Rust**: falkordb-rs
- **Additional**: Community-maintained clients for various languages

---

## Quick Start

### Launch FalkorDB
```bash
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:latest
```

### Create and Query a Graph
```python
from falkordb import FalkorDB

# Connect
db = FalkorDB(host='localhost', port=6379)
g = db.select_graph('MotoGP')

# Create data
g.query("""CREATE
    (:Rider {name:'Valentino Rossi'})-[:rides]->(:Team {name:'Yamaha'}),
    (:Rider {name:'Dani Pedrosa'})-[:rides]->(:Team {name:'Honda'})
""")

# Query
res = g.query("""
    MATCH (r:Rider)-[:rides]->(t:Team)
    WHERE t.name = 'Yamaha'
    RETURN r.name
""")
```

---

## Use Cases

### Enterprise GenAI
- Accurate GraphRAG for knowledge-intensive applications
- Context-aware question answering
- Multi-document reasoning

### AI Agent Memory
- Persistent memory for conversational AI
- Multi-agent knowledge sharing
- Temporal tracking of interactions

### Knowledge Management
- Enterprise knowledge graphs
- Document and data integration
- Semantic search with graph context

### Real-Time Analytics
- Fraud detection
- Recommendation engines
- Network analysis and social graphs

### E-Commerce
- Product catalogs with relationships
- Personalized recommendations
- Customer journey tracking

---

## Technical Advantages

1. **Performance**: Low-latency operations with matrix-based graph representation
2. **Scalability**: Horizontal scaling with clustering, vertical scaling with optimization
3. **Flexibility**: Multiple protocols (RESP, Bolt), multiple query paradigms
4. **AI-Native**: Built-in vector search, GraphRAG SDK, LLM integrations
5. **Production-Ready**: Replication, clustering, persistence, observability

---

## License

FalkorDB is licensed under the **Server Side Public License v1 (SSPLv1)**.

---

## Getting Started Resources

- **Documentation**: https://docs.falkordb.com
- **Docker Hub**: https://hub.docker.com/r/falkordb/falkordb
- **FalkorDB Cloud**: https://app.falkordb.cloud
- **GitHub Discussions**: https://github.com/FalkorDB/FalkorDB/discussions
- **Discord Community**: https://discord.gg/ErBEqN9E

---

## Key Differentiators

1. **Dual Purpose**: Traditional graph database + GraphRAG capabilities in one platform
2. **AI-First Design**: Native vector search, LLM integrations, agentic memory support
3. **Multi-Tenant Architecture**: Enterprise-ready isolation for users and agents
4. **Performance Focus**: Low-latency, high-throughput optimized for production
5. **Comprehensive Indexing**: Range, full-text, vector, and geospatial in one system
6. **Rich Ecosystem**: Multiple client libraries, framework integrations, migration tools

---

*Last Updated: November 2025*
