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

1. **FalkorDB Instance**: Set up FalkorDB (on-prem or cloud). [Learn More](/configuration).  
2. **Python Installed**: Ensure you have Python 3.8+ installed.  
3. **Install FalkorDB Python Client**:
   
   ```bash
   pip install falkordb
   ```
   
---

## Step 1: Model a Social Network as a Graph

Let's create a simple graph for a social network where:  
- **Nodes** represent `User` and `Post`.
- **Relationships** represent `FRIENDS_WITH` and `CREATED`.

### Graph Schema

| Node Type | Properties               |
|-----------|--------------------------|
| User      | `id`, `name`, `email`    |
| Post      | `id`, `content`, `date`  |

| Relationship Type | Start Node | End Node | Properties   |
|-------------------|------------|----------|--------------|
| FRIENDS_WITH      | User       | User     | `since`      |
| CREATED           | User       | Post     | `time`       |


![image](https://github.com/user-attachments/assets/213e47e7-1439-4f1e-beb4-64dceb9ecc9b)


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
client = FalkorDB(host="localhost", port=6379, password="your-password")
graph = client.select_graph('social')
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
MATCH (alice:User {name: "Alice"})-[:FRIENDS_WITH]->(friend)
RETURN friend.name AS Friend
"""
result = graph.ro_query(query)

print("Alice's friends:")
for record in result:
    print(record["Friend"])
```

#### Query Relationships

```python
# Find posts created by Bob
query = """
MATCH (bob:User {name: "Bob"})-[:CREATED]->(post:Post)
RETURN post.content AS PostContent
"""
result = graph.ro_query(query)

print("Posts created by Bob:")
for record in result:
    print(record["PostContent"])
```

---

## Step 4: Explore Further

Congratulations! 🎉 You've successfully modeled, loaded, and queried a social network graph with FalkorDB.  

Next, dive deeper into FalkorDB's powerful features:
- [Advanced Cypher](/cypher)
- [Database Operations](/operations)
- [Integration with ML Workflows](/llm_support)

For questions or support, visit our [community forums](https://www.falkordb.com/contact-us/)
