---
title: "GraphRAG-SDK"
nav_order: 8
description: "FalkorDB supports a number of LLM frameworks."
---

# GraphRAG-SDK
### A specialized toolkit for building Graph Retrieval-Augmented Generation (GraphRAG) systems.

- Integrates knowledge graphs, ontology management, and LLMs to deliver accurate, efficient, and customizable RAG workflows.
- Build GraphRAG systems easily with FalkorDB and LLMs (GPT, Gemini and more). 
- Create and query knowledge graphs using Cypher.


## Get started
### Setting up FalkorDB
You can install FalkorDB using Docker, or sign up to FalkorDB cloud for a managed instance. Here’s how you can install it using Docker:

```
docker run -p 6379:6379 -p 3000:3000 -it --rm -v ./data:/data falkordb/falkordb:edge
```

> ℹ️ That will launch the FalkorDB server. You can also visit http://localhost:3000 to view the [FalkorDB Browser](https://browser.falkordb.com/).

### Install Libraries
You're now ready to launch the Jupyter Notebook and install the necessary libraries. First, create a Python virtual environment and then install and launch Jupyter Lab: 
```
$ pip install jupyterlab
$ jupyter lab
```

> ℹ️ This will launch the Jupyter Notebook. In this example, we'll use Groq to access the LLMs, so you need to procure an API key.

You can install the following libraries:
```
! pip install falkordb
! pip install groq
! pip install sentence-transformers llama-index-embeddings-huggingface langchain-core langgraph
! pip install falkordb langchain-experimental pandas langchain-groq
```

### Load Data
> We recommend you download a dataset and save it as a CSV file.




## How it works
### 1️⃣ Transform raw data into structured knowledge models automatically
- Use generative AI to detect and construct ontologies from your datasets
- Define custom parameters to scope and control ontology detection processes
- Review, modify and iterate on detected ontologies to optimize graph structures

### 2️⃣ Ingest diverse data formats through a streamlined ETL process
- Process multiple file formats including PDF, CSV, HTML, TXT, JSON and URLs
- Deploy FalkorDB instances via cloud infrastructure or containerized environments
- Utilize genAI capabilities to construct knowledge graphs efficiently

### 3️⃣ Coordinate specialized agents for complex knowledge operations
- Configure domain-specific Knowledge Graph agents for targeted analysis
- Implement orchestration layer for automated agent coordination and planning
- Execute sophisticated queries through multi-agent collaboration

#### Useful resources:
> 📓 [A Guide to Implementing a GraphRAG Workflow Using FalkorDB, LangChain and LangGraph](https://www.falkordb.com/blog/graphrag-workflow-falkordb-langchain/)

> 📓 [Build AI Agents with Memory: LangChain + FalkorDB](https://www.falkordb.com/blog/building-ai-agents-with-memory-langchain/)

> 📓  [LlamaIndex RAG: Build Efficient GraphRAG Systems](https://www.falkordb.com/blog/llamaindex-rag-implementation-graphrag/)

> 📓  [Understanding Ontologies and Knowledge Graphs](https://www.falkordb.com/blog/understanding-ontologies-knowledge-graph-schemas/)


## LLMs & integrations

### LangChain
LangChain now integrates with FalkorDB, enabling graph database capabilities for AI-driven applications. This combination facilitates the creation of AI agents with memory, enhancing their ability to retain state and context across interactions.


[LangChain](https://www.langchain.com/) - [FalkorDBQAChain](https://python.langchain.com/docs/use_cases/more/graph/graph_falkordb_qa)

### LangGraph
LangGraph is an open-source framework for building stateful, multi-actor agentic applications using LLMs. It enables you to design complex agent and multi-agent workflows by representing application logic as directed graphs—where nodes define tasks or functions, and edges determine the flow of information.


### LlamaIndex
LlamaIndex is an open-source framework that makes it easy for you to build LLM-powered applications. With its tools for ingesting different data structures, indexing, and querying, you can effortlessly create AI applications that tap into external knowledge.

There are two parts to a RAG system: the retrieval module and the generation module. We will use LlamaIndex to orchestrate the two steps. To power our retrieval module, we will use FalkorDB. For the generation, you can use any LLM that has been trained on Cypher queries, which are needed for fetching data from modern graph databases like FalkorDB.

[LlamaIndex](https://www.llamaindex.ai/) - [FalkorDB Graph Store](https://gpt-index.readthedocs.io/en/latest/examples/index_structs/knowledge_graph/FalkorDBGraphDemo.html)

### Grafitti


## Use cases
| Use Case | Description | Key Features |
|----------|-------------|--------------|
| **Regulatory Compliance Analyzer** | Stay ahead of financial regulations with GraphRAG-SDK. | • **Extract Key Requirements**: NLP-driven analysis organizes regulatory mandates into a knowledge graph for precise insights.<br>• **Map Regulations to Processes**: Link policies to workflows, ensuring compliance across departments.<br>• **Identify Compliance Gaps**: Query relationships to spot misalignments and track updates.<br>• **Suggest Improvements**: Get data-driven recommendations to refine policies, training, and risk management. |
| **AML Network Analyzer** | Detect and analyze financial crime with GraphRAG-SDK. | • **Trace Fund Flows**: Visualize transaction networks across institutions to track money movement with clarity.<br>• **Identify Shell Companies**: Uncover hidden relationships and detect illicit entities within financial ecosystems.<br>• **Flag Suspicious Patterns**: Use graph-based analysis to detect anomalies, refine detection over time, and scale AML efforts effectively. |
| **Financial Product Recommendation Engine** | Deliver precise financial recommendations using GraphRAG-SDK. | • **Analyze Customer Data**: Structure financial records and life events into knowledge graphs for relevant, personalized insights.<br>• **Map Product Relationships**: Clearly visualize connections between products, customer segments, and risk profiles.<br>• **Tailored Recommendations**: Leverage graph reasoning to offer transparent, explainable suggestions, boosting trust and satisfaction. |


## Ontologies
Ontologies are foundational to knowledge graphs because they play key roles in:

| Concept | Description |
|---------|-------------|
| **Defining the schema** | They provide a structured framework for categorizing entities and specifying relationships, ensuring a coherent organization of knowledge. |
| **Ensuring consistency** | By imposing rules and constraints, ontologies maintain the integrity and logical correctness of the graph. |
| **Facilitating interoperability** | They standardize terminology and relationships, enabling seamless communication and integration between different knowledge graphs. |
| **Ontology** | A blueprint or schema that defines the structure and relationships between different classes of data. It is a conceptual model and does not include specific data points. |
| **Knowledge Graph** | The result of applying an ontology to actual data. It represents real-world data in a structured, interconnected format, allowing for complex queries and insights. |




