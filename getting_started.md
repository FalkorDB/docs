---
title: "Getting Started"
nav_order: 2
description: >
    Getting Started with FalkorDB Graph Database.
---


# Getting Started with FalkorDB

This guide will walk you through setting up FalkorDB, modeling a social network as a graph, 
and accessing it using the [FalkorDB Python client](/clients) with [Cypher](/cypher).

---

## Prerequisites

1. **FalkorDB Instance**: Set up FalkorDB (on-prem or cloud). 
   - [Run FalkorDB Docker](https://hub.docker.com/r/falkordb/falkordb/)
   - [Create a FalkorDB Cloud Instance](https://app.falkordb.cloud/signup)
2. **Python Installed**: Ensure you have Python 3.8+ installed.  
3. **Install FalkorDB Python Client**:
   
   ```bash
   pip install falkordb
   ```
   
---

## Step 1: Model a Social Network as a Graph

Let's create a simple graph for a social network where:  
- **Nodes** represent `User` and `Post`.
- **Relationships** connect `User`s with a `FRIENDS_WITH` relationship, and `User`s are connected via a `CREATED` relationship to `Post`s

### Graph Schema

| Node Type | Properties               |
|-----------|--------------------------|
| User      | `id`, `name`, `email`    |
| Post      | `id`, `content`, `date`  |

| Relationship Type | Start Node | End Node | Properties   |
|-------------------|------------|----------|--------------|
| FRIENDS_WITH      | User       | User     | `since`      |
| CREATED           | User       | Post     | `time`       |

![FalkorDB-Model a Social Network as a Graph](https://github.com/user-attachments/assets/57d9b837-661e-4500-a9f2-88e754382d29)

---

## Step 2: Load Data into FalkorDB

Here’s how you can model and load the data.

### Cypher Query to Create the Data

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

You can execute these commands using the FalkorDB Python client.

---

## Step 3: Access Your Data

### Connect to FalkorDB

```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host="localhost", port=6379, password="your-password")
graph = db.select_graph('social')
```

### Execute Cypher Queries

#### Create the Graph

```python
create_query = """
CREATE (alice:User {id: 1, name: "Alice", email: "alice@example.com"})
CREATE (bob:User {id: 2, name: "Bob", email: "bob@example.com"})
CREATE (charlie:User {id: 3, name: "Charlie", email: "charlie@example.com"})

CREATE (post1:Post {id: 101, content: "Hello World!", date: 1701388800})
CREATE (post2:Post {id: 102, content: "Graph Databases are awesome!", date: 1701475200})

CREATE (alice)-[:FRIENDS_WITH {since: 1640995200}]->(bob)
CREATE (bob)-[:FRIENDS_WITH {since: 1684108800}]->(charlie)
CREATE (alice)-[:CREATED {time: 1701388800}]->(post1)
CREATE (bob)-[:CREATED {time: 1701475200}]->(post2)
"""

graph.query(create_query)
print("Graph created successfully!")
```

![image](https://github.com/user-attachments/assets/f67c9a1d-4b80-435d-9038-b7e1f931da74)

#### Query the Graph

```python
# Find all friends of Alice
query = """
MATCH (alice:User {name: 'Alice'})-[:FRIENDS_WITH]->(friend)
RETURN friend.name AS Friend
"""

result = graph.ro_query(query).result_set

print("Alice's friends:")
for record in result:
    print(record[0])
```

#### Query Relationships

```python
# Find posts created by Bob
query = """
MATCH (bob:User {name: 'Bob'})-[:CREATED]->(post:Post)
RETURN post.content AS PostContent
"""

result = graph.ro_query(query).result_set

print("Posts created by Bob:")
for record in result:
    print(record[0])
```

---

## Step 4: Explore Further

Congratulations! 🎉 You have successfully modeled, loaded, and queried a social network graph with FalkorDB.

Next, dive deeper into FalkorDB's powerful features:
- [Advanced Cypher](/cypher)
- [Database Operations](/operations)
- [GraphRAG SDK](/graphrag_sdk)
- [LLM Framework Integrations](/llm_integrations)

For questions or support, visit our [community forums](https://www.falkordb.com/contact-us/)
