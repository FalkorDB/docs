---
title: "LangGraph"
nav_order: 4
description: "Build stateful, multi-actor agentic applications with LangGraph and FalkorDB."
parent: "GenAI Tools"
---

# LangGraph

[LangGraph](https://www.langgraph.dev/) is an open-source framework for building **stateful, multi-actor agentic applications** using LLMs. It allows you to design complex single- and multi-agent workflows as directed graphs, where nodes represent tasks and edges define the information flow.

## Resources

* 📓 [Blog: Implementing GraphRAG with FalkorDB, LangChain & LangGraph](https://www.falkordb.com/blog/graphrag-workflow-falkordb-langchain/)
* 🔗 [LangGraph Documentation](https://www.langgraph.dev/)

## Installation

Install LangGraph with required dependencies:

```bash
pip install langgraph langchain langchain-community falkordb langchain-openai
```

## Quick Start

### 1. Define Your Graph Workflow

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_community.graphs import FalkorDBGraph
from langchain_openai import ChatOpenAI

# Define state
class GraphState(TypedDict):
    question: str
    cypher_query: str
    graph_data: str
    answer: str

# Initialize FalkorDB
graph_db = FalkorDBGraph(
    database="knowledge_graph",
    host="localhost",
    port=6379,
)

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)
```

### 2. Create Agent Nodes

```python
def generate_cypher(state: GraphState) -> GraphState:
    """Generate Cypher query from natural language question"""
    question = state["question"]
    schema = graph_db.get_schema
    
    prompt = f"""
    Given the graph schema:
    {schema}
    
    Generate a Cypher query to answer: {question}
    """
    
    response = llm.invoke(prompt)
    state["cypher_query"] = response.content
    return state

def execute_query(state: GraphState) -> GraphState:
    """Execute Cypher query on FalkorDB"""
    cypher = state["cypher_query"]
    result = graph_db.query(cypher)
    state["graph_data"] = str(result)
    return state

def generate_answer(state: GraphState) -> GraphState:
    """Generate natural language answer from graph data"""
    question = state["question"]
    data = state["graph_data"]
    
    prompt = f"""
    Question: {question}
    Graph Data: {data}
    
    Provide a clear, natural language answer based on the data.
    """
    
    response = llm.invoke(prompt)
    state["answer"] = response.content
    return state
```

### 3. Build the Workflow

```python
# Create workflow
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("generate_cypher", generate_cypher)
workflow.add_node("execute_query", execute_query)
workflow.add_node("generate_answer", generate_answer)

# Define edges
workflow.set_entry_point("generate_cypher")
workflow.add_edge("generate_cypher", "execute_query")
workflow.add_edge("execute_query", "generate_answer")
workflow.add_edge("generate_answer", END)

# Compile the graph
app = workflow.compile()
```

### 4. Run the Agent

```python
# Execute the workflow
result = app.invoke({
    "question": "Who are the top 5 customers by purchase amount?",
    "cypher_query": "",
    "graph_data": "",
    "answer": "",
})

print(result["answer"])
```

## Advanced Usage

### Multi-Agent GraphRAG System

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation

class RAGState(TypedDict):
    question: str
    context: str
    entities: list[str]
    relationships: list[str]
    answer: str
    next_step: str

def extract_entities(state: RAGState) -> RAGState:
    """Extract entities from the question"""
    question = state["question"]
    
    prompt = f"Extract key entities from: {question}"
    response = llm.invoke(prompt)
    
    state["entities"] = response.content.split(",")
    state["next_step"] = "find_relationships"
    return state

def find_relationships(state: RAGState) -> RAGState:
    """Find relationships between entities in the graph"""
    entities = state["entities"]
    
    # Query graph for relationships
    cypher = f"""
    MATCH (a)-[r]->(b)
    WHERE a.name IN {entities} OR b.name IN {entities}
    RETURN a, r, b
    LIMIT 20
    """
    
    result = graph_db.query(cypher)
    state["relationships"] = result
    state["next_step"] = "retrieve_context"
    return state

def retrieve_context(state: RAGState) -> RAGState:
    """Retrieve relevant context from the graph"""
    entities = state["entities"]
    
    cypher = f"""
    MATCH (n)
    WHERE n.name IN {entities}
    RETURN n
    """
    
    result = graph_db.query(cypher)
    state["context"] = str(result)
    state["next_step"] = "generate_answer"
    return state

def generate_final_answer(state: RAGState) -> RAGState:
    """Generate the final answer using all context"""
    question = state["question"]
    context = state["context"]
    relationships = state["relationships"]
    
    prompt = f"""
    Question: {question}
    Context: {context}
    Relationships: {relationships}
    
    Provide a comprehensive answer using the graph context.
    """
    
    response = llm.invoke(prompt)
    state["answer"] = response.content
    state["next_step"] = END
    return state

# Build RAG workflow
rag_workflow = StateGraph(RAGState)

rag_workflow.add_node("extract_entities", extract_entities)
rag_workflow.add_node("find_relationships", find_relationships)
rag_workflow.add_node("retrieve_context", retrieve_context)
rag_workflow.add_node("generate_answer", generate_final_answer)

rag_workflow.set_entry_point("extract_entities")
rag_workflow.add_edge("extract_entities", "find_relationships")
rag_workflow.add_edge("find_relationships", "retrieve_context")
rag_workflow.add_edge("retrieve_context", "generate_answer")
rag_workflow.add_edge("generate_answer", END)

rag_app = rag_workflow.compile()

# Execute
result = rag_app.invoke({
    "question": "What is the relationship between Company A and Person B?",
    "context": "",
    "entities": [],
    "relationships": [],
    "answer": "",
    "next_step": "",
})

print(result["answer"])
```

### Conditional Routing

```python
def should_continue(state: GraphState) -> str:
    """Decide next step based on state"""
    if state.get("cypher_query") and "ERROR" in state["cypher_query"]:
        return "regenerate"
    elif state.get("graph_data") == "[]":
        return "no_results"
    else:
        return "continue"

# Add conditional edges
workflow.add_conditional_edges(
    "execute_query",
    should_continue,
    {
        "regenerate": "generate_cypher",
        "no_results": "handle_no_results",
        "continue": "generate_answer",
    }
)
```

### Memory Integration

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Add persistence
memory = SqliteSaver.from_conn_string(":memory:")

# Compile with checkpointing
app = workflow.compile(checkpointer=memory)

# Use with thread ID for conversation memory
config = {"configurable": {"thread_id": "user_123"}}

result1 = app.invoke({
    "question": "Who is the CEO?",
    "cypher_query": "",
    "graph_data": "",
    "answer": "",
}, config)

result2 = app.invoke({
    "question": "What companies do they lead?",
    "cypher_query": "",
    "graph_data": "",
    "answer": "",
}, config)
```

## Use Cases

* **Complex Query Decomposition**: Break down complex questions into multiple graph queries
* **Multi-Step Reasoning**: Chain multiple graph operations for advanced analytics
* **Agentic RAG**: Combine retrieval, reasoning, and generation in a graph-based workflow
* **Error Recovery**: Implement retry logic and fallback mechanisms in graph queries
* **Conversational GraphRAG**: Maintain context across multiple turns of conversation

## Best Practices

1. **State Management**: Keep state minimal and well-typed
2. **Error Handling**: Add nodes for handling query errors and edge cases
3. **Conditional Logic**: Use conditional edges for dynamic workflow routing
4. **Checkpointing**: Enable persistence for long-running workflows
5. **Observability**: Add logging at each node for debugging

## Additional Resources

* [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
* [Blog: Implementing GraphRAG with FalkorDB, LangChain & LangGraph](https://www.falkordb.com/blog/graphrag-workflow-falkordb-langchain/)
* [LangGraph GitHub Repository](https://github.com/langchain-ai/langgraph)
