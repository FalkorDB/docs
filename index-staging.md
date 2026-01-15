---
title: Home (Staging)
description: "Build intelligent applications with the fastest graph database for knowledge graphs and GraphRAG"
---

[![Docker Hub](https://img.shields.io/docker/pulls/falkordb/falkordb?label=Docker&style=flat-square)](https://hub.docker.com/r/falkordb/falkordb/)
[![Discord](https://img.shields.io/discord/1146782921294884966?style=flat-square)](https://discord.gg/ErBEqN9E) 
[![Try Free](https://img.shields.io/badge/Try%20Free-FalkorDB%20Cloud-FF8101?labelColor=FDE900&style=flat-square)](https://app.falkordb.cloud)
[![Trendshift](https://trendshift.io/api/badge/repositories/14787)](https://trendshift.io/repositories/14787)

# FalkorDB

**A blazing-fast graph database that makes it simple to build knowledge graphs, recommendation engines, fraud detection systems, and intelligent GenAI applications.**

FalkorDB combines the power of a low-latency property graph database with native GraphRAG capabilities—enabling developers to query complex, interconnected data using OpenCypher while seamlessly integrating with LLMs for next-generation AI applications.

---

## Why Choose FalkorDB?

<table>
<tr>
<td width="50%">

### ⚡ **Built for Speed**
Sub-millisecond query latency using sparse adjacency matrix storage. Handle millions of relationships without compromising performance.

</td>
<td width="50%">

### 🎯 **Production-Ready**
Multi-tenant architecture, ACID transactions, and support for both RESP and Bolt protocols. Deploy on Docker, Kubernetes, or FalkorDB Cloud.

</td>
</tr>
<tr>
<td>

### 🧠 **AI-Native**
Native vector similarity search and GraphRAG SDK for building accurate RAG applications that understand relationships, not just keywords.

</td>
<td>

### 🛠️ **Developer-First**
OpenCypher query language, clients in 6+ languages, integrations with LangChain, LlamaIndex, and popular data tools.

</td>
</tr>
</table>

---

## What Can You Build?

<table>
<tr>
<td width="33%">

### **🔍 Fraud Detection**
Model complex transaction patterns and identify suspicious relationships in real-time across financial networks.

</td>
<td width="33%">

### **💡 Recommendation Engines**
Build collaborative filtering systems that understand user behavior, product relationships, and contextual connections.

</td>
<td width="33%">

### **🧩 Knowledge Graphs**
Create intelligent knowledge bases that power semantic search, question answering, and enterprise data discovery.

</td>
</tr>
<tr>
<td>

### **🤖 GraphRAG for GenAI**
Enhance LLM responses with structured knowledge graphs, reducing hallucinations and improving accuracy for domain-specific queries.

</td>
<td>

### **📊 Real-Time Analytics**
Analyze social networks, supply chains, and interconnected data with graph algorithms like PageRank and community detection.

</td>
<td>

### **🔗 Master Data Management**
Unify data across systems by modeling complex entity relationships and hierarchies in a flexible graph structure.

</td>
</tr>
</table>

---

## Quick Start

Get FalkorDB running in 30 seconds:

```bash
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:latest
```

**Alternative Options:**
- [Try FalkorDB Cloud](https://app.falkordb.cloud) (Free tier available)
- [Deploy to Kubernetes](/operations/k8s-support)
- [Railway Template](/operations/railway)

---

## Choose Your Path

<table>
<tr>
<td width="50%">

### 📚 **Learn Graph Database Concepts**

New to graph databases? Start here.

- [What is a Graph Database?](/getting-started)
- [Property Graph Model Overview](https://github.com/opencypher/openCypher/blob/master/docs/property-graph-model.adoc)
- [OpenCypher Query Language](/cypher)
- [When to Use Graphs vs. Relational](/getting-started#when-to-use-graphs)

</td>
<td width="50%">

### 🚀 **Quick Start Tutorial**

Ready to code? Jump right in.

- [5-Minute Tutorial](/getting-started)
- [Client Libraries (Python, JS, Java, Rust)](/getting-started/clients)
- [Connect & Query Guide](/getting-started#first-query)
- [Sample Applications](https://github.com/FalkorDB/demos)

</td>
</tr>
<tr>
<td>

### 🤖 **Explore GraphRAG & GenAI**

Build AI-powered applications.

- [GraphRAG SDK Overview](/genai-tools/graphrag-sdk)
- [LangChain Integration](/genai-tools/langchain)
- [LlamaIndex Integration](/genai-tools/llamaindex)
- [AG2 & AutoGen Support](/genai-tools/ag2)

</td>
<td>

### ⚙️ **Deploy to Production**

Scale your application confidently.

- [Configuration Guide](/getting-started/configuration)
- [Docker Deployment](/operations/docker)
- [Kubernetes & Helm](/operations/k8s-support)
- [Replication & High Availability](/operations/replication)

</td>
</tr>
</table>

---

## Core Features

<table>
<tr>
<td width="33%">

#### **🎯 Flexible Data Model**
[Property Graph Model](https://github.com/opencypher/openCypher/blob/master/docs/property-graph-model.adoc) with nodes, relationships, and properties. Model complex domains naturally.

</td>
<td width="33%">

#### **🔎 Advanced Indexing**
[Full-text search](/cypher/indexing/fulltext-index), [vector similarity](/cypher/indexing/vector-index), and [range indexes](/cypher/indexing/range-index) for lightning-fast queries.

</td>
<td width="33%">

#### **📝 OpenCypher Support**
Industry-standard [OpenCypher](/cypher) query language with FalkorDB enhancements for complex graph operations.

</td>
</tr>
<tr>
<td>

#### **⚡ High Performance**
Sparse adjacency matrix representation enables efficient graph traversal at scale with minimal memory overhead.

</td>
<td>

#### **🔌 Protocol Flexibility**
Native support for both [RESP](https://redis.io/docs/reference/protocol-spec/) (Redis) and [Bolt](https://en.wikipedia.org/wiki/Bolt_(network_protocol)) (Neo4j) protocols.

</td>
<td>

#### **📊 Graph Algorithms**
Built-in algorithms: [PageRank](/algorithms/pagerank), [BFS](/algorithms/bfs), [Shortest Path](/algorithms/sppath), [Community Detection](/algorithms/cdlp), and more.

</td>
</tr>
</table>

---

## Example: Build a Social Network Graph

Here's how simple it is to create and query a graph with FalkorDB:

```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host='localhost', port=6379)
g = db.select_graph('SocialNetwork')

# Create a small social network
g.query("""
    CREATE 
      (alice:Person {name: 'Alice', age: 30}),
      (bob:Person {name: 'Bob', age: 25}),
      (charlie:Person {name: 'Charlie', age: 35}),
      (alice)-[:FOLLOWS]->(bob),
      (bob)-[:FOLLOWS]->(charlie),
      (charlie)-[:FOLLOWS]->(alice)
""")

# Find who Alice follows
result = g.query("""
    MATCH (alice:Person {name: 'Alice'})-[:FOLLOWS]->(friend)
    RETURN friend.name
""")

print(result.result_set[0][0])  # Bob
```

**Want to see more examples?**
- [Complete tutorial with multiple languages](/getting-started)
- [GraphRAG examples with LangChain](/genai-tools/langchain)
- [Sample applications repository](https://github.com/FalkorDB/demos)

---

## Integrations & Ecosystem

FalkorDB works seamlessly with your favorite tools:

**Language Clients:** Python • JavaScript • Java • Rust • Go • C# • [View All](/getting-started/clients)

**GenAI Frameworks:** [LangChain](/genai-tools/langchain) • [LangGraph](/genai-tools/langgraph) • [LlamaIndex](/genai-tools/llamaindex) • [AG2](/genai-tools/ag2)

**Data Tools:** [Kafka Connect](/integration/kafka-connect) • [Spring Data](/integration/spring-data-falkordb) • [Apache Jena](/integration/jena)

**Deployment:** [Docker](/operations/docker) • [Kubernetes](/operations/k8s-support) • [Railway](/operations/railway) • [Lightning.AI](/operations/lightning-ai)

---

## Performance at Scale

- **Sub-10ms queries** for most graph traversals
- **Multi-tenant architecture** for SaaS applications
- **Horizontal scaling** via replication
- **ACID transactions** for data consistency
- **Sparse matrix storage** reduces memory by 90%+ vs dense graphs

[See detailed benchmarks →](https://github.com/FalkorDB/FalkorDB#benchmarks)

---

## Community & Support

<table>
<tr>
<td width="33%" align="center">

### 💬 Discord
Join our [Discord community](https://discord.gg/ErBEqN9E) for real-time help and discussions

</td>
<td width="33%" align="center">

### 📋 GitHub Discussions
Ask questions on [GitHub Discussions](https://github.com/FalkorDB/FalkorDB/discussions)

</td>
<td width="33%" align="center">

### 🐛 Issue Tracker
Report bugs on [GitHub Issues](https://github.com/FalkorDB/FalkorDB/issues)

</td>
</tr>
</table>

---

## Next Steps

1. **[Get Started](/getting-started)** — Follow our step-by-step tutorial
2. **[Learn OpenCypher](/cypher)** — Master the query language
3. **[Explore GraphRAG](/genai-tools/graphrag-sdk)** — Build AI-powered applications
4. **[Deploy to Cloud](https://app.falkordb.cloud)** — Try our managed service

---

## Open Source & License

FalkorDB is open source under the [Server Side Public License v1 (SSPLv1)](https://github.com/FalkorDB/FalkorDB/blob/master/LICENSE.txt).

⭐ [Star us on GitHub](https://github.com/FalkorDB/FalkorDB) | 📖 [Read the Blog](https://www.falkordb.com/blog) | 🌐 [Visit falkordb.com](https://www.falkordb.com)
