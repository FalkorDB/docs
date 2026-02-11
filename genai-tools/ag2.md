---
title: "AG2"
nav_order: 2
description: "Build multi-agent AI systems with AG2 (formerly AutoGen) and FalkorDB GraphRAG. Orchestrate collaborative agents with structured knowledge graphs for intelligent applications."
parent: "GenAI Tools"
---

# AG2

[AG2](https://ag2.ai/) (formerly AutoGen) is an open-source agentic AI operating system (AgentOS) for building, orchestrating, and deploying multi-agent AI systems. Developed from OpenAI and Microsoft Research's AutoGen, AG2 provides a modular framework for creating sophisticated AI agents that can collaborate, use tools, and integrate with knowledge graphs.

The integration of AG2 with FalkorDB brings powerful GraphRAG capabilities to multi-agent systems, enabling agents to leverage structured knowledge graphs for more accurate, explainable, and contextually-aware responses.

## Installation

Install AG2 with FalkorDB GraphRAG support:

```bash
pip install -U ag2[openai,graph-rag-falkor-db]
```

Or install the GraphRAG-SDK separately:

```bash
pip install ag2 graphrag_sdk
```

## Quick Start

### 1. Set Up FalkorDB

Start FalkorDB using Docker:

```bash
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:latest
```

Or use [FalkorDB Cloud](https://app.falkordb.cloud) for a managed instance.

### 2. Configure Environment

Set up your API credentials:

```bash
export FALKORDB_HOST="localhost"
export FALKORDB_PORT=6379
export OPENAI_API_KEY="your-openai-api-key"
```

### 3. Create a GraphRAG Agent

```python
import os
from autogen import ConversableAgent
from autogen.agentchat.contrib.graph_rag.document import Document, DocumentType
from autogen.agentchat.contrib.graph_rag.falkor_graph_query_engine import (
    FalkorGraphQueryEngine,
)
from autogen.agentchat.contrib.graph_rag.falkor_graph_rag_capability import (
    FalkorGraphRagCapability,
)

# Specify input document to create knowledge graph
input_documents = [
    Document(doctype=DocumentType.TEXT, path_or_url="company_data.txt")
]

# Connect to FalkorDB and initialize knowledge graph
query_engine = FalkorGraphQueryEngine(
    name="company_knowledge",
    host="localhost",
    port=6379,
)

# Ingest documents into the knowledge graph
query_engine.init_db(input_doc=input_documents)

# Create AG2 agent
agent = ConversableAgent(
    name="knowledge_agent",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.getenv("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

# Attach GraphRAG capability to the agent
FalkorGraphRagCapability.attach(agent, query_engine)

# Query the knowledge graph
response = agent.generate_reply(
    messages=[{"role": "user", "content": "Who is the CEO of the company?"}]
)
print(response)
```

## Advanced Usage

### Multi-Agent Collaboration

Build a multi-agent system where agents collaborate using shared knowledge:

```python
from autogen import ConversableAgent, GroupChat, GroupChatManager

# Create multiple agents with different roles
researcher = ConversableAgent(
    name="researcher",
    system_message="You are a research analyst. Extract and analyze information from the knowledge graph.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.getenv("OPENAI_API_KEY")}]},
)

planner = ConversableAgent(
    name="planner",
    system_message="You are a strategic planner. Use research findings to create actionable plans.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.getenv("OPENAI_API_KEY")}]},
)

critic = ConversableAgent(
    name="critic",
    system_message="You are a critical reviewer. Evaluate plans and provide constructive feedback.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.getenv("OPENAI_API_KEY")}]},
)

# Attach GraphRAG to all agents
FalkorGraphRagCapability.attach(researcher, query_engine)
FalkorGraphRagCapability.attach(planner, query_engine)
FalkorGraphRagCapability.attach(critic, query_engine)

# Create group chat
groupchat = GroupChat(
    agents=[researcher, planner, critic],
    messages=[],
    max_round=10,
)

manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": [{"model": "gpt-4"}]})

# Start the conversation
researcher.initiate_chat(
    manager,
    message="Analyze our company's market position and suggest growth strategies.",
)
```

### Building Knowledge Graphs from Multiple Sources

```python
from autogen.agentchat.contrib.graph_rag.document import Document, DocumentType

# Create documents from various sources
documents = [
    Document(doctype=DocumentType.TEXT, path_or_url="product_catalog.txt"),
    Document(doctype=DocumentType.TEXT, path_or_url="customer_reviews.txt"),
    Document(doctype=DocumentType.TEXT, path_or_url="market_research.txt"),
]

# Initialize query engine with multiple documents
query_engine = FalkorGraphQueryEngine(
    name="business_intelligence",
    host="localhost",
    port=6379,
)

query_engine.init_db(input_doc=documents)
```

### Custom Query Engine Configuration

```python
from autogen.agentchat.contrib.graph_rag.falkor_graph_query_engine import (
    FalkorGraphQueryEngine,
    GraphStoreQueryResult,
)

# Configure query engine with custom settings
query_engine = FalkorGraphQueryEngine(
    name="custom_graph",
    host=os.getenv("FALKORDB_HOST", "localhost"),
    port=int(os.getenv("FALKORDB_PORT", 6379)),
    username=os.getenv("FALKORDB_USERNAME"),
    password=os.getenv("FALKORDB_PASSWORD"),
)

# Query with custom Cypher
cypher_query = """
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE c.industry = 'Technology'
RETURN p.name, c.name, c.founded_year
ORDER BY c.founded_year DESC
LIMIT 10
"""

result = query_engine.query(cypher_query)
print(result)
```

### Conversational Context Management

```python
# Agent maintains context across multiple queries
agent = ConversableAgent(
    name="contextual_agent",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.getenv("OPENAI_API_KEY")}]},
    human_input_mode="NEVER",
)

FalkorGraphRagCapability.attach(agent, query_engine)

# First question
response1 = agent.generate_reply(
    messages=[{"role": "user", "content": "Tell me about TechCorp."}]
)

# Follow-up question (agent remembers context)
response2 = agent.generate_reply(
    messages=[{"role": "user", "content": "Who founded that company?"}]
)

# Another follow-up
response3 = agent.generate_reply(
    messages=[{"role": "user", "content": "What products do they make?"}]
)
```

### Human-in-the-Loop Workflows

```python
# Create agent with human input for critical decisions
human_agent = ConversableAgent(
    name="human_supervisor",
    human_input_mode="ALWAYS",
    llm_config=False,
)

ai_agent = ConversableAgent(
    name="ai_assistant",
    system_message="You help humans make data-driven decisions using the knowledge graph.",
    llm_config={"config_list": [{"model": "gpt-4", "api_key": os.getenv("OPENAI_API_KEY")}]},
)

FalkorGraphRagCapability.attach(ai_agent, query_engine)

# AI agent proposes, human approves
ai_agent.initiate_chat(
    human_agent,
    message="Based on the knowledge graph, I recommend expanding into the European market. What do you think?",
)
```

### Integrating External Tools

```python
from autogen import register_function

# Define custom tools for agents
def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of text"""
    # Your sentiment analysis logic
    return "positive"

def fetch_market_data(company: str) -> dict:
    """Fetch real-time market data"""
    # Your data fetching logic
    return {"price": 150.25, "volume": 1000000}

# Register tools with agents
register_function(
    analyze_sentiment,
    caller=agent,
    executor=agent,
    description="Analyze sentiment of text",
)

register_function(
    fetch_market_data,
    caller=agent,
    executor=agent,
    description="Fetch market data for a company",
)

# Agent can now use both GraphRAG and custom tools
```

## Use Cases

- **Multi-Agent Research Systems**: Teams of agents collaborating to research complex topics using knowledge graphs
- **Customer Support Automation**: Intelligent agents answering queries with contextual knowledge from company databases
- **Business Intelligence**: Agents analyzing business data and providing strategic insights
- **Content Generation**: Creating factually accurate content grounded in knowledge graphs
- **Decision Support Systems**: Multi-agent systems helping humans make informed decisions
- **Knowledge Management**: Automated extraction and organization of information from documents
- **Trip Planning**: Collaborative agents using graph data for personalized travel recommendations

## Key Features

### GraphRAG Advantages

- **Structured Knowledge**: Query relationships and entities in a graph database
- **Reduced Hallucinations**: Ground agent responses in factual graph data
- **Explainable AI**: Trace reasoning paths through graph queries
- **Real-Time Updates**: Knowledge graphs can be updated dynamically
- **Multi-Tenancy**: Isolate knowledge graphs for different projects or users
- **High Performance**: FalkorDB's speed enables real-time agent interactions

### AG2 Core Capabilities

- **Multi-Agent Orchestration**: Coordinate multiple AI agents with different roles
- **LLM Agnostic**: Works with OpenAI, Google, Anthropic, Azure, and more
- **Tool Integration**: Agents can use external APIs, databases, and functions
- **Human-in-the-Loop**: Seamlessly integrate human oversight and feedback
- **State Management**: Maintain conversation context and agent state
- **Flexible Workflows**: Define custom agent behaviors and interaction patterns

## Best Practices

1. **Schema Design**: Structure your knowledge graph with clear entities and relationships
2. **Document Quality**: Provide high-quality, well-structured input documents for better graph extraction
3. **Agent Roles**: Define clear, specific roles for each agent in multi-agent systems
4. **Error Handling**: Implement fallback mechanisms for failed queries or agent responses
5. **Context Management**: Balance context window size with response quality
6. **Query Optimization**: Use specific, targeted queries for better performance
7. **Incremental Updates**: Update knowledge graphs incrementally as new data arrives
8. **Security**: Implement proper authentication and authorization for graph access
9. **Monitoring**: Track agent performance and query patterns for optimization
10. **Testing**: Validate agent behavior with diverse query scenarios

## Performance Considerations

- **Batch Processing**: Process multiple documents in batches for efficient graph building
- **Caching**: Cache frequently accessed graph patterns and results
- **Connection Pooling**: Reuse FalkorDB connections across agents
- **Parallel Queries**: Execute independent queries in parallel when possible
- **Graph Optimization**: Regularly optimize graph structure for query performance

## Resources

- 🔗 [AG2 Documentation](https://docs.ag2.ai/)
- 🔗 [AG2 API Reference](https://docs.ag2.ai/latest/docs/reference/)
- 🔗 [AG2 GitHub Repository](https://github.com/ag2ai/ag2)
- 📓 [AG2 GitHub Examples](https://github.com/ag2ai/ag2/tree/main/notebook)
- 📓 [AG2 GraphRAG with FalkorDB Notebook](https://docs.ag2.ai/latest/docs/use-cases/notebooks/notebooks/agentchat_graph_rag_falkordb/)
- 🔗 [FalkorDB GraphRAG-SDK](https://docs.falkordb.com/graphrag-sdk.html)
- 📝 [Blog: FalkorDB-AG2.ai Integration for Multi-Agent Systems](https://www.falkordb.com/news-updates/ag2-integration-multi-agent-systems/)
- 📝 [Blog: Structured Knowledge with FalkorDB Graph RAG](https://docs.ag2.ai/latest/docs/blog/2024/12/06/FalkorDB-Structured/)
- 📝 [Blog: Knowledgeable Agents with FalkorDB Graph RAG](https://dev.to/ag2ai/knowledgeable-agents-with-falkordb-graph-rag-9d)
