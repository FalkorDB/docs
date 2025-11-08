---
title: "LangChain"
nav_order: 3
description: "FalkorDB integration with LangChain for AI agents with memory."
parent: "GenAI Tools"
---

# LangChain

FalkorDB is integrated with [LangChain](https://www.langchain.com/), bringing powerful graph database capabilities to AI-driven applications. This integration enables the creation of AI agents with memory, enhancing their ability to retain state and context across interactions.

## Resources

* 🔗 [FalkorDBQAChain Documentation](https://python.langchain.com/docs/use_cases/more/graph/graph_falkordb_qa)  
* 📓 [Blog: Build AI Agents with Memory – LangChain + FalkorDB](https://www.falkordb.com/blog/building-ai-agents-with-memory-langchain/)

## Installation

Install LangChain with FalkorDB support:

```bash
pip install langchain langchain-community falkordb
```

## Quick Start

### 1. Connect to FalkorDB

```python
from langchain_community.graphs import FalkorDBGraph

# Connect to FalkorDB
graph = FalkorDBGraph(
    database="movies",
    host="localhost",
    port=6379,
    username="",  # optional
    password="",  # optional
)
```

### 2. Create a Knowledge Graph from Text

```python
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Create QA chain
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
)
```

### 3. Query the Graph

```python
# Ask natural language questions
response = chain.run("Who acted in The Matrix?")
print(response)

# Ask follow-up questions
response = chain.run("What other movies did they act in?")
print(response)
```

## Advanced Usage

### Using Graph Memory for Conversational AI

```python
from langchain.memory import ConversationGraphMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

# Initialize graph memory
memory = ConversationGraphMemory(
    graph=graph,
    llm=ChatOpenAI(temperature=0),
)

# Create conversation chain with graph memory
conversation = ConversationChain(
    llm=ChatOpenAI(temperature=0),
    memory=memory,
    verbose=True,
)

# Have a conversation
conversation.predict(input="Hi, my name is Alice")
conversation.predict(input="I work as a software engineer")
conversation.predict(input="What do you know about me?")
```

### Custom Cypher Generation

```python
from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain.prompts import PromptTemplate

# Custom Cypher generation prompt
CYPHER_GENERATION_TEMPLATE = """
You are an expert in Cypher query language for graph databases.
Task: Generate a Cypher query to answer the user's question.

Schema:
{schema}

Question: {question}

Cypher query:
"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"],
    template=CYPHER_GENERATION_TEMPLATE,
)

# Create chain with custom prompt
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    cypher_prompt=CYPHER_GENERATION_PROMPT,
    verbose=True,
)

response = chain.run("Find all products in the electronics category")
```

### Loading Data into the Graph

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.falkordb_vector import FalkorDBVector

# Load and split documents
loader = TextLoader("company_data.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# Create vector store with FalkorDB
embeddings = OpenAIEmbeddings()
vector_store = FalkorDBVector.from_documents(
    docs,
    embeddings,
    host="localhost",
    port=6379,
    database="company_knowledge",
)
```

### Graph RAG Pattern

```python
from langchain.chains import RetrievalQA
from langchain_community.vectorstores.falkordb_vector import FalkorDBVector
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Set up vector store
vector_store = FalkorDBVector(
    embedding=OpenAIEmbeddings(),
    host="localhost",
    port=6379,
    database="rag_database",
)

# Create retrieval QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
)

# Query with retrieval
response = qa_chain.run("What are the key features of our product?")
print(response)
```

## Use Cases

* **Conversational AI with Memory**: Build chatbots that remember user context across sessions
* **Question Answering over Knowledge Graphs**: Convert natural language to Cypher queries automatically
* **Document Q&A with Graph Context**: Combine vector search with graph relationships
* **Multi-hop Reasoning**: Leverage graph traversal for complex queries
* **Entity Extraction and Linking**: Build knowledge graphs from unstructured text

## Best Practices

1. **Schema Design**: Design your graph schema with clear node labels and relationship types
2. **Cypher Optimization**: Review generated Cypher queries and optimize for performance
3. **Error Handling**: Implement fallbacks for cases where Cypher generation fails
4. **Context Management**: Use graph memory to maintain conversation context efficiently
5. **Prompt Engineering**: Customize prompts to improve Cypher query generation quality

## Resources

* [LangChain Documentation](https://python.langchain.com/)
* [FalkorDBQAChain API Reference](https://python.langchain.com/docs/integrations/graphs/falkordb)
* [Blog: Build AI Agents with Memory](https://www.falkordb.com/blog/building-ai-agents-with-memory-langchain/)
