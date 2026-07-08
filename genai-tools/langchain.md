---
title: "LangChain"
nav_order: 4
description: "Build AI agents with memory using FalkorDB and LangChain. Python and JavaScript/TypeScript integration for conversational AI, GraphRAG, and knowledge graph question answering."
parent: "GenAI Tools"
---

# LangChain

FalkorDB is integrated with [LangChain](https://www.langchain.com/), bringing powerful graph database capabilities to AI-driven applications. This integration enables the creation of AI agents with memory, enhancing their ability to retain state and context across interactions.

The FalkorDB LangChain integration is available for both **Python** and **JavaScript/TypeScript** environments, making it easy to build intelligent applications in your preferred language.

## Resources

- 📦 [langchain-falkordb Package (Python)](https://pypi.org/project/langchain-falkordb/)
- 💻 [langchain-falkordb Repository](https://github.com/FalkorDB/langchain-falkordb)
- 📦 [@falkordb/langchain-ts Package (JavaScript/TypeScript)](https://www.npmjs.com/package/@falkordb/langchain-ts)
- 💻 [FalkorDB-Langchain-js Repository](https://github.com/FalkorDB/FalkorDB-Langchain-js)
- 📓 [Blog: Build AI Agents with Memory – LangChain + FalkorDB](https://www.falkordb.com/blog/building-ai-agents-with-memory-langchain/)

---

## Python Integration

The Python integration is provided by the dedicated [`langchain-falkordb`](https://pypi.org/project/langchain-falkordb/) package. It provides:

- **`FalkorDBGraph`** — a graph wrapper with schema introspection and `GraphDocument` ingestion, for building knowledge graphs.
- **`FalkorDBVector`** — a LangChain vector store backed by FalkorDB vector indexes, with support for metadata filtering, maximal marginal relevance (MMR) search, and hybrid (vector + full-text) search.
- **`FalkorDBQAChain`** — a natural-language-to-Cypher question-answering chain over a FalkorDB graph.
- **`FalkorDBSaver`** — a [LangGraph](./langgraph.md) checkpointer that persists agent state in FalkorDB.
- **`FalkorDBChatMessageHistory`** — a LangChain chat message history that persists conversations in FalkorDB.

### Installation

Install the FalkorDB LangChain integration:

```bash
pip install langchain-falkordb
```

The examples below also use [`langchain-openai`](https://pypi.org/project/langchain-openai/):

```bash
pip install langchain-openai
```

### Quick Start

#### 1. Connect to FalkorDB

```python
from langchain_falkordb import FalkorDBGraph

# Connect to FalkorDB
graph = FalkorDBGraph(
    "movies",           # graph (database) name
    host="localhost",
    port=6379,
    username=None,      # optional, or set FALKORDB_USERNAME
    password=None,  # optional, or set FALKORDB_PASSWORD
    ssl=False,          # optional
)
```

#### 2. Create a QA Chain

```python
from langchain_falkordb import FalkorDBQAChain
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")

# Create QA chain
chain = FalkorDBQAChain.from_llm(
    llm,
    graph=graph,
    allow_dangerous_requests=True,  # explicit opt-in, see security note below
)
```

> **Security note**: the chain executes LLM-generated Cypher against your
> database. Use narrowly-scoped credentials and set
> `allow_dangerous_requests=True` only after understanding the risks.

#### 3. Query the Graph

```python
# Ask natural language questions
response = chain.invoke({"query": "Who acted in The Matrix?"})
print(response["result"])

# Ask follow-up questions
response = chain.invoke({"query": "What other movies did they act in?"})
print(response["result"])
```

### Advanced Usage

#### Building a Knowledge Graph

`FalkorDBGraph` ingests `GraphDocument` objects (e.g. produced by an LLM
graph transformer such as `LLMGraphTransformer` from `langchain-experimental`):

```python
from langchain_core.documents import Document
from langchain_falkordb import FalkorDBGraph
from langchain_falkordb.graphs import GraphDocument, Node, Relationship

graph = FalkorDBGraph("movies", host="localhost", port=6379)

tom = Node(id="Tom Hanks", type="Actor")
gump = Node(id="Forrest Gump", type="Movie")
graph.add_graph_documents(
    [
        GraphDocument(
            nodes=[tom, gump],
            relationships=[Relationship(source=tom, target=gump, type="ACTED_IN")],
            source=Document(page_content="Tom Hanks acted in Forrest Gump."),
        )
    ],
    include_source=True,  # links entities to their source Document node
)

graph.refresh_schema()
print(graph.get_schema)
print(graph.query("MATCH (a:Actor)-[:ACTED_IN]->(m:Movie) RETURN a.id, m.id"))
```

#### Persistent Chat Message History

`FalkorDBChatMessageHistory` persists conversations in FalkorDB. Each
session is stored in its own graph named after the `session_id`, so
histories are isolated per session and survive reconnects:

```python
from langchain_falkordb import FalkorDBChatMessageHistory

history = FalkorDBChatMessageHistory(
    session_id="user-42",
    host="localhost",
    port=6379,
)

history.add_user_message("Hello!")
history.add_ai_message("Hi! How can I help?")
print(history.messages)
```

#### Custom Cypher Generation

```python
from langchain_core.prompts import PromptTemplate
from langchain_falkordb import FalkorDBQAChain

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
chain = FalkorDBQAChain.from_llm(
    llm,
    graph=graph,
    cypher_prompt=CYPHER_GENERATION_PROMPT,
    allow_dangerous_requests=True,
)

response = chain.invoke({"query": "Find all products in the electronics category"})
print(response["result"])
```

#### Loading Data into a Vector Store

This example also uses LangChain document loading utilities (`pip install langchain-community langchain-text-splitters`):

```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_falkordb import FalkorDBVector

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

# Similarity search with optional metadata filtering
results = vector_store.similarity_search(
    "graph databases",
    k=4,
    filter={"topic": "search"},
)
```

`FalkorDBVector` also supports maximal marginal relevance (MMR) search via
`max_marginal_relevance_search`, hybrid (vector + full-text) search via
`search_type=SearchType.HYBRID`, and reusing existing indexes and graphs
via `from_existing_index` and `from_existing_graph`.

#### Graph RAG Pattern

This example uses `RetrievalQA` from the `langchain` package (`pip install langchain`):

```python
from langchain.chains import RetrievalQA
from langchain_falkordb import FalkorDBVector
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Connect to a vector index that already contains data
vector_store = FalkorDBVector.from_existing_index(
    embedding=OpenAIEmbeddings(),
    host="localhost",
    port=6379,
    database="rag_database",
    node_label="Chunk",
)

# Create retrieval QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 5}),
)

# Query with retrieval
response = qa_chain.invoke({"query": "What are the key features of our product?"})
print(response["result"])
```

---

## JavaScript/TypeScript Integration

FalkorDB also provides a JavaScript/TypeScript integration for LangChain applications through the [@falkordb/langchain-ts](https://www.npmjs.com/package/@falkordb/langchain-ts) package.

### Installation

```bash
npm install @falkordb/langchain-ts falkordb langchain @langchain/openai
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

> **Alternative Connection:** You can also connect using a URL format:
> ```typescript
> const graph = await FalkorDBGraph.initialize({
>   url: "falkor://localhost:6379",
>   graph: "movies"
> });
> ```

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
- `url` (string): Alternative connection URL format: `falkor[s]://[[username][:password]@][host][:port][/db-number]`
- `enhancedSchema` (boolean): Enable enhanced schema details

**Example with URL:**
```typescript
// Connect using URL format
const graph = await FalkorDBGraph.initialize({
  url: "falkor://localhost:6379",
  graph: "myGraph"
});

// With authentication
const graph = await FalkorDBGraph.initialize({
  url: "falkor://username:password@localhost:6379",
  graph: "myGraph"
});
```

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

### Advanced Usage (JS/TS)

#### Custom Cypher Queries

```typescript
const graph = await FalkorDBGraph.initialize({
  host: "localhost",
  port: 6379,
  graph: "movies"
});

// Complex query
const result = await graph.query(`
  MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
  WHERE m.year > 2000
  RETURN a.name, m.title, m.year
  ORDER BY m.year DESC
  LIMIT 10
`);

console.log(result.data);
```

#### Working with Schema (JS/TS)

```typescript
await graph.refreshSchema();

// Get formatted schema
const schema = graph.getSchema();
console.log(schema);

// Get structured schema
const structuredSchema = graph.getStructuredSchema();
console.log(structuredSchema.nodeProps);
console.log(structuredSchema.relationships);
```

For more examples and source code, see the [@falkordb/langchain-ts repository](https://github.com/FalkorDB/FalkorDB-Langchain-js).

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
- [langchain-falkordb on PyPI](https://pypi.org/project/langchain-falkordb/)
- [langchain-falkordb Repository](https://github.com/FalkorDB/langchain-falkordb)
- [Blog: Build AI Agents with Memory](https://www.falkordb.com/blog/building-ai-agents-with-memory-langchain/)

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What languages does the FalkorDB LangChain integration support?"
  a1="The FalkorDB LangChain integration supports both **Python** (via the `langchain-falkordb` PyPI package) and **JavaScript/TypeScript** (via the `@falkordb/langchain-ts` npm package)."
  q2="How do I connect LangChain to FalkorDB?"
  a2="In Python, use `FalkorDBGraph('my_graph', host='localhost', port=6379)` from `langchain_falkordb`. In TypeScript, use `FalkorDBGraph.initialize({ host: 'localhost', port: 6379, graph: 'my_graph' })` from `@falkordb/langchain-ts`."
  q3="Can I use FalkorDB as a vector store with LangChain?"
  a3="Yes. Use `FalkorDBVector` from `langchain_falkordb` to store and retrieve document embeddings. It supports similarity search with metadata filtering, maximal marginal relevance (MMR) search, hybrid (vector + full-text) search, and can be used as a retriever in RAG chains."
  q4="What is FalkorDBQAChain?"
  a4="FalkorDBQAChain is a chain from the `langchain-falkordb` package that converts natural language questions into Cypher queries, executes them against FalkorDB, and returns natural language answers. Because it executes LLM-generated Cypher, you must explicitly opt in with `allow_dangerous_requests=True`."
  q5="Can I give agents persistent memory with FalkorDB?"
  a5="Yes. Use `FalkorDBChatMessageHistory` to persist conversations per session, or `FalkorDBSaver` (a LangGraph checkpointer, installed with `pip install langchain-falkordb[langgraph]`) to persist agent state across restarts."
%}
