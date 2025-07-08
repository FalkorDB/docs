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
   
   {% capture shell_0 %}
pip install falkordb
{% endcapture %}
   
   {% include code_tabs.html id="install_tabs" shell=shell_0 %}

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

{% capture cypher_0 %}
CREATE (alice:User {id: 1, name: "Alice", email: "alice@example.com"})
CREATE (bob:User {id: 2, name: "Bob", email: "bob@example.com"})
CREATE (charlie:User {id: 3, name: "Charlie", email: "charlie@example.com"})

CREATE (post1:Post {id: 101, content: "Hello World!", date: 1701388800})
CREATE (post2:Post {id: 102, content: "Graph Databases are awesome!", date: 1701475200})

CREATE (alice)-[:FRIENDS_WITH {since: 1640995200}]->(bob)
CREATE (bob)-[:FRIENDS_WITH {since: 1684108800}]->(charlie)
CREATE (alice)-[:CREATED {time: 1701388800}]->(post1)
CREATE (bob)-[:CREATED {time: 1701475200}]->(post2)
{% endcapture %}

{% include code_tabs.html id="cypher_create_tabs" cypher=cypher_0 %}

You can execute these commands using the FalkorDB Python client or any supported client.

---

## Step 3: Access Your Data

### Connect to FalkorDB

{% capture python_0 %}
from falkordb import FalkorDB

# Connect to FalkorDB
client = FalkorDB(host="localhost", port=6379, password="your-password")
graph = client.select_graph('social')
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';

const client = await FalkorDB.connect({
  host: "localhost",
  port: 6379,
  password: "your-password"
});
const graph = client.selectGraph('social');
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB("localhost", 6379, "your-password");
Graph graph = client.selectGraph("social");
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect("localhost", 6379, Some("your-password"));
let graph = client.select_graph("social");
{% endcapture %}

{% include code_tabs.html id="connect_tabs" python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

### Execute Cypher Queries

#### Create the Graph

{% capture python_1 %}
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
{% endcapture %}

{% capture javascript_1 %}
const createQuery = `
CREATE (alice:User {id: 1, name: "Alice", email: "alice@example.com"})
CREATE (bob:User {id: 2, name: "Bob", email: "bob@example.com"})
CREATE (charlie:User {id: 3, name: "Charlie", email: "charlie@example.com"})

CREATE (post1:Post {id: 101, content: "Hello World!", date: 1701388800})
CREATE (post2:Post {id: 102, content: "Graph Databases are awesome!", date: 1701475200})

CREATE (alice)-[:FRIENDS_WITH {since: 1640995200}]->(bob)
CREATE (bob)-[:FRIENDS_WITH {since: 1684108800}]->(charlie)
CREATE (alice)-[:CREATED {time: 1701388800}]->(post1)
CREATE (bob)-[:CREATED {time: 1701475200}]->(post2)
`;
await graph.query(createQuery);
console.log("Graph created successfully!");
{% endcapture %}

{% capture java_1 %}
String createQuery = """
CREATE (alice:User {id: 1, name: \"Alice\", email: \"alice@example.com\"})
CREATE (bob:User {id: 2, name: \"Bob\", email: \"bob@example.com\"})
CREATE (charlie:User {id: 3, name: \"Charlie\", email: \"charlie@example.com\"})

CREATE (post1:Post {id: 101, content: \"Hello World!\", date: 1701388800})
CREATE (post2:Post {id: 102, content: \"Graph Databases are awesome!\", date: 1701475200})

CREATE (alice)-[:FRIENDS_WITH {since: 1640995200}]->(bob)
CREATE (bob)-[:FRIENDS_WITH {since: 1684108800}]->(charlie)
CREATE (alice)-[:CREATED {time: 1701388800}]->(post1)
CREATE (bob)-[:CREATED {time: 1701475200}]->(post2)
""";
graph.query(createQuery);
System.out.println("Graph created successfully!");
{% endcapture %}

{% capture rust_1 %}
let create_query = r#"
CREATE (alice:User {id: 1, name: \"Alice\", email: \"alice@example.com\"})
CREATE (bob:User {id: 2, name: \"Bob\", email: \"bob@example.com\"})
CREATE (charlie:User {id: 3, name: \"Charlie\", email: \"charlie@example.com\"})

CREATE (post1:Post {id: 101, content: \"Hello World!\", date: 1701388800})
CREATE (post2:Post {id: 102, content: \"Graph Databases are awesome!\", date: 1701475200})

CREATE (alice)-[:FRIENDS_WITH {since: 1640995200}]->(bob)
CREATE (bob)-[:FRIENDS_WITH {since: 1684108800}]->(charlie)
CREATE (alice)-[:CREATED {time: 1701388800}]->(post1)
CREATE (bob)-[:CREATED {time: 1701475200}]->(post2)
"#;
graph.query(create_query)?;
println!("Graph created successfully!");
{% endcapture %}

{% include code_tabs.html id="create_graph_tabs" python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}

![image](https://github.com/user-attachments/assets/f67c9a1d-4b80-435d-9038-b7e1f931da74)

#### Query the Graph

{% capture python_2 %}
# Find all friends of Alice
query = """
MATCH (alice:User {name: 'Alice'})-[:FRIENDS_WITH]->(friend)
RETURN friend.name AS Friend
"""

result = graph.ro_query(query).result_set

print("Alice's friends:")
for record in result:
    print(record[0])
{% endcapture %}

{% capture javascript_2 %}
const query = `
MATCH (alice:User {name: "Alice"})-[:FRIENDS_WITH]->(friend)
RETURN friend.name AS Friend
`;
const result = await graph.ro_query(query);
console.log("Alice's friends:");
for (const record of result) {
  console.log(record["Friend"]);
}
{% endcapture %}

{% capture java_2 %}
String query = """
MATCH (alice:User {name: \"Alice\"})-[:FRIENDS_WITH]->(friend)
RETURN friend.name AS Friend
""";
ResultSet result = graph.ro_query(query);
System.out.println("Alice's friends:");
for (Record record : result) {
    System.out.println(record.get("Friend"));
}
{% endcapture %}

{% capture rust_2 %}
let query = r#"
MATCH (alice:User {name: \"Alice\"})-[:FRIENDS_WITH]->(friend)
RETURN friend.name AS Friend
"#;
let result = graph.ro_query(query)?;
println!("Alice's friends:");
for record in result {
    println!("{}", record["Friend"]);
}
{% endcapture %}

{% include code_tabs.html id="query_friends_tabs" python=python_2 javascript=javascript_2 java=java_2 rust=rust_2 %}

#### Query Relationships

{% capture python_3 %}
# Find posts created by Bob
query = """
MATCH (bob:User {name: 'Bob'})-[:CREATED]->(post:Post)
RETURN post.content AS PostContent
"""

result = graph.ro_query(query).result_set

print("Posts created by Bob:")
for record in result:
    print(record[0])
{% endcapture %}

{% capture javascript_3 %}
const query = `
MATCH (bob:User {name: "Bob"})-[:CREATED]->(post:Post)
RETURN post.content AS PostContent
`;
const result = await graph.ro_query(query);
console.log("Posts created by Bob:");
for (const record of result) {
  console.log(record["PostContent"]);
}
{% endcapture %}

{% capture java_3 %}
String query = """
MATCH (bob:User {name: \"Bob\"})-[:CREATED]->(post:Post)
RETURN post.content AS PostContent
""";
ResultSet result = graph.ro_query(query);
System.out.println("Posts created by Bob:");
for (Record record : result) {
    System.out.println(record.get("PostContent"));
}
{% endcapture %}

{% capture rust_3 %}
let query = r#"
MATCH (bob:User {name: \"Bob\"})-[:CREATED]->(post:Post)
RETURN post.content AS PostContent
"#;
let result = graph.ro_query(query)?;
println!("Posts created by Bob:");
for record in result {
    println!("{}", record["PostContent"]);
}
{% endcapture %}

{% include code_tabs.html id="query_posts_tabs" python=python_3 javascript=javascript_3 java=java_3 rust=rust_3 %}

---

## Step 4: Explore Further

Congratulations! 🎉 You have successfully modeled, loaded, and queried a social network graph with FalkorDB.

Next, dive deeper into FalkorDB's powerful features:
- [Advanced Cypher](/cypher)
- [Database Operations](/operations)
- [GraphRAG SDK](/graphrag_sdk)
- [LLM Framework Integrations](/llm_integrations)

For questions or support, visit our [community forums](https://www.falkordb.com/contact-us/)
