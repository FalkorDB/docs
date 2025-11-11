---
title: "LangChain JS/TS"
nav_order: 2
description: "LangChain JavaScript/TypeScript integration for FalkorDB"
parent: "Integration"
---

![falkordb-langchain](https://github.com/user-attachments/assets/b5ebbef1-6943-4493-a33a-af5bcac87a60)

# LangChain JS/TS Integration with FalkorDB

The [@falkordb/langchain-ts](https://www.npmjs.com/package/@falkordb/langchain-ts) package enables developers to integrate FalkorDB with LangChain applications. The integration allows applications to accept natural language questions, generate Cypher queries automatically, retrieve relevant context from the graph database, and return responses in natural language.

## Installation

### Step 1

```bash
npm install @falkordb/langchain-ts falkordb
```

### Step 2
>
> Ensure LangChain and a language model are installed

```bash
npm install langchain @langchain/openai
```

## Getting Started

### Movie data example

In this example, we'll initialize the connection to FalkorDB, define a language model (E.g, OpenAI), and both create and populate the graph with movie-related data. **We'll then query the graph in natural language to see the integration at work.**
> Note: You can change the LLM's temperature

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

// Create and populate the graph with some data
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

// Clean up
await graph.close();
```

## API Reference

### FalkorDBGraph
>
> The following command creates and initializes a new FalkorDB connection.

#### `initialize(config: FalkorDBGraphConfig): Promise<FalkorDBGraph>`

**Config Options:**

- `host` (string, optional): Database host. Default: `"localhost"`
- `port` (number, optional): Database port. Default: `6379`
- `graph` (string, optional): Graph name to use
- `url` (string, optional): Alternative connection URL format
- `enhancedSchema` (boolean, optional): Enable enhanced schema details. Default: `false`

**Example:**

```typescript
const graph = await FalkorDBGraph.initialize({
  host: "localhost",
  port: 6379,
  graph: "myGraph",
  enhancedSchema: true
});
```

#### `query(query: string): Promise<any>`

Executes a Cypher query on the graph.

```typescript
const result = await graph.query(
  "MATCH (n:Person) RETURN n.name LIMIT 10"
);
```

#### `refreshSchema(): Promise<void>`

Updates the graph schema information.

```typescript
await graph.refreshSchema();
console.log(graph.getSchema());
```

#### `getSchema(): string`

Returns the current graph schema as a formatted string.

#### `getStructuredSchema(): StructuredSchema`

Returns the structured schema object containing node properties, relationship properties, and relationships.

#### `close(): Promise<void>`

Closes the database connection.

```typescript
await graph.close();
```

## Advanced Usage

### Custom Cypher Queries

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

### Multiple Queries

```typescript
await graph.executeQueries([
  "CREATE (p:Person {name: 'Alice'})",
  "CREATE (p:Person {name: 'Bob'})",
  "MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) CREATE (a)-[:KNOWS]->(b)"
]);
```

### Working with Schema

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

## Prerequisites

- Node.js >= 18
- FalkorDB server running
- LangChain >= 0.1.0

## Additional Examples

For more examples and source code, see the [@falkordb/langchain-ts repository](https://github.com/FalkorDB/FalkorDB-Langchain-js) on GitHub.
