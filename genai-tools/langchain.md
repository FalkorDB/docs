---
title: "LangChain"
nav_order: 3
description: "FalkorDB integration with LangChain for AI agents with memory."
parent: "GenAI Tools"
---

# LangChain

FalkorDB is integrated with [LangChain](https://www.langchain.com/), bringing powerful graph database capabilities to AI-driven applications. This integration enables the creation of AI agents with memory, enhancing their ability to retain state and context across interactions.

The FalkorDB LangChain integration is available for both **Python** and **JavaScript/TypeScript** environments, making it easy to build intelligent applications in your preferred language.

## Resources

- 🔗 [FalkorDBQAChain Documentation (Python)](https://python.langchain.com/docs/use_cases/more/graph/graph_falkordb_qa)
- 📦 [@falkordb/langchain-ts Package (JavaScript/TypeScript)](https://www.npmjs.com/package/@falkordb/langchain-ts)
- 💻 [FalkorDB-Langchain-js Repository](https://github.com/FalkorDB/FalkorDB-Langchain-js)
- 📓 [Blog: Build AI Agents with Memory – LangChain + FalkorDB](https://www.falkordb.com/blog/building-ai-agents-with-memory-langchain/)

---

## Python Integration

### Installation

Install LangChain with FalkorDB support:

```bash
pip install langchain langchain-community falkordb
```

### Quick Start

#### 1. Connect to FalkorDB

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

#### 2. Create a Knowledge Graph from Text

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

#### 3. Query the Graph

```python
# Ask natural language questions
response = chain.run("Who acted in The Matrix?")
print(response)

# Ask follow-up questions
response = chain.run("What other movies did they act in?")
print(response)
```

### Advanced Usage

#### Using Graph Memory for Conversational AI

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

#### Custom Cypher Generation

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

#### Loading Data into the Graph

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

#### Graph RAG Pattern

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

---

## JavaScript/TypeScript Integration

FalkorDB also provides a JavaScript/TypeScript integration for LangChain applications through the [@falkordb/langchain-ts](https://www.npmjs.com/package/@falkordb/langchain-ts) package.

### Installation

```bash
npm install @falkordb/langchain-ts falkordb
npm install langchain @langchain/openai
```

### Quick Start (JS/TS)

```typescript
import { FalkorDBGraph } from "@falkordb/langchain-ts";
import { ChatOpenAI } from "@langchain/openai";
import { GraphCypherQAChain } from "@langchain/community/chains/graph_qa/cypher";

// Initialize FalkorDB connection
const graph = await FalkorDBGraph.initialize({
  host: "localhost",
  port: 6379,
  graph: "movies"
});

// Set up the language model
const model = new ChatOpenAI({ temperature: 0 });

// Create and populate the graph
await graph.query(
  "CREATE (a:Actor {name:'Bruce Willis'})" +
  "-[:ACTED_IN]->(:Movie {title: 'Pulp Fiction'})"
);

// Refresh the graph schema
await graph.refreshSchema();

// Create a graph QA chain
const chain = GraphCypherQAChain.fromLLM({
  llm: model,
  graph: graph as any,
});

// Ask questions about your graph
const response = await chain.run("Who played in Pulp Fiction?");
console.log(response);
// Output: Bruce Willis played in Pulp Fiction.

await graph.close();
```

### Key Features (JS/TS)

- **Natural Language Querying**: Convert questions to Cypher queries automatically
- **Schema Management**: Automatic schema refresh and retrieval
- **Type Safety**: Full TypeScript support with type definitions
- **Promise-based API**: Modern async/await patterns

### API Reference (JS/TS)

#### `FalkorDBGraph.initialize(config)`

Create and initialize a new FalkorDB connection.

**Config Options:**
- `host` (string): Database host (default: "localhost")
- `port` (number): Database port (default: 6379)
- `graph` (string): Graph name to use
- `url` (string): Alternative connection URL format
- `enhancedSchema` (boolean): Enable enhanced schema details

#### `query(query: string)`

Execute a Cypher query on the graph.

```typescript
const result = await graph.query(
  "MATCH (n:Person) RETURN n.name LIMIT 10"
);
```

#### `refreshSchema()`

Update the graph schema information.

```typescript
await graph.refreshSchema();
console.log(graph.getSchema());
```

For more detailed JavaScript/TypeScript examples and documentation, see the [LangChain JS/TS Integration Guide](/integration/langchain-js.html) and the [@falkordb/langchain-ts repository](https://github.com/FalkorDB/FalkorDB-Langchain-js).

---

## Use Cases

- **Conversational AI with Memory**: Build chatbots that remember user context across sessions
- **Question Answering over Knowledge Graphs**: Convert natural language to Cypher queries automatically
- **Document Q&A with Graph Context**: Combine vector search with graph relationships
- **Multi-hop Reasoning**: Leverage graph traversal for complex queries
- **Entity Extraction and Linking**: Build knowledge graphs from unstructured text

## Best Practices

1. **Schema Design**: Design your graph schema with clear node labels and relationship types
2. **Cypher Optimization**: Review generated Cypher queries and optimize for performance
3. **Error Handling**: Implement fallbacks for cases where Cypher generation fails
4. **Context Management**: Use graph memory to maintain conversation context efficiently
5. **Prompt Engineering**: Customize prompts to improve Cypher query generation quality

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [FalkorDBQAChain API Reference](https://python.langchain.com/docs/integrations/graphs/falkordb)
- [Blog: Build AI Agents with Memory](https://www.falkordb.com/blog/building-ai-agents-with-memory-langchain/)
