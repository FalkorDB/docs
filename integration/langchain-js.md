---
title: "LangChain JS/TS"
nav_order: 2
description: "LangChain JavaScript/TypeScript integration for FalkorDB"
parent: "Integration"
---

# LangChain JS/TS Integration

The [@falkordb/langchain-ts](https://www.npmjs.com/package/@falkordb/langchain-ts) package enables developers to use FalkorDB with LangChain applications. This integration allows your application to take natural language questions, automatically generate Cypher queries, retrieve relevant context from your graph database, and return responses in plain language.

## Installation

```bash
npm install @falkordb/langchain-ts falkordb
```

You'll also need LangChain and a language model:

```bash
npm install langchain @langchain/openai
```

## Quick Start

### Basic Usage

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

#### `initialize(config: FalkorDBGraphConfig): Promise<FalkorDBGraph>`

Creates and initializes a new FalkorDB connection.

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

## Requirements

- Node.js >= 18
- FalkorDB server running
- LangChain >= 0.1.0

## Examples

For more examples and source code, see the [@falkordb/langchain-ts repository](https://github.com/FalkorDB/FalkorDB-Langchain-js) on GitHub.
