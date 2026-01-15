---
title: "Social Network Tutorial"
description: "Build and query a simple social graph with FalkorDB."
---

<!-- markdownlint-disable MD025 -->

# Social Network Tutorial

This walkthrough mirrors the quickstart in Getting Started and keeps everything in one place for workshops.

## Steps

1. **Model**: Users and Posts connected by `FRIENDS_WITH` and `CREATED` relationships.
2. **Load data**: Run the Cypher block below to create the sample graph.
3. **Query**: Try the example reads to explore the graph.

### Load the graph

```cypher
CREATE (alice:User {id: 1, name: "Alice", email: "alice@example.com"})
CREATE (bob:User {id: 2, name: "Bob", email: "bob@example.com"})
CREATE (charlie:User {id: 3, name: "Charlie", email: "charlie@example.com"})

CREATE (post1:Post {id: 101, content: "Hello World!", date: 1701388800})
CREATE (post2:Post {id: 102, content: "Graph Databases are awesome!", date: 1701475200})

CREATE (alice)-[:FRIENDS_WITH {since: 1640995200}]->(bob)
CREATE (bob)-[:FRIENDS_WITH {since: 1684108800}]->(charlie)
CREATE (alice)-[:CREATED {time: 1701388800}]->(post1)
CREATE (bob)-[:CREATED {time: 1701475200}]->(post2)
```

### Query examples

```cypher
MATCH (alice:User {name: 'Alice'})-[:FRIENDS_WITH]->(friend)
RETURN friend.name AS Friend;
```

```cypher
MATCH (bob:User {name: "Bob"})-[:CREATED]->(post:Post)
RETURN post.content AS PostContent;
```

For multi-language client samples, see [Getting Started](/getting-started).
