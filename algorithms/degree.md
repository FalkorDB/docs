# Degree Procedure Documentation

## Introduction

The **Degree Procedure** calculates the degree of nodes in a graph based on the specified parameters.
This allows users to analyze the connectivity of nodes in terms of incoming or outgoing edges, filtered by node labels and relationship types.

---

## Use Cases

Here are some practical scenarios where the **Degree Procedure** can be applied:

1. **Social Network Analysis**: Identify influencers or highly connected individuals by calculating the degree of `Person` nodes in a social graph.
2. **Infrastructure Planning**: Determine bottlenecks in a transportation network by analyzing nodes with high incoming or outgoing connections.
3. **E-commerce Recommendations**: Identify popular products or categories by computing the degree of `Product` or `Category` nodes based on customer interactions.
4. **Fraud Detection**: Spot suspicious activities by analyzing nodes with unusually high degrees in financial transaction graphs.

---

## Syntax

```plaintext
CALL algo.degree(config)
```

### Parameters

The `config` parameter is a Map object containing the following optional keys:

| Key           | Type   | Default    | Description                                                            |
| ------------- | ------ | ---------- | ---------------------------------------------------------------------- |
| `source`      | String | `null`     | Specifies the label of nodes for which the degree is computed.         |
| `dir`         | String | `outgoing` | Direction of edges to consider: `incoming` or `outgoing`.              |
| `relation`    | String | `null`     | Specifies the type of edges to consider.                               |
| `destination` | String | `null`     | Specifies the label of nodes reachable via the edges being considered. |

---

## Output

The procedure returns a result set where each row corresponds to a node and includes the following fields:

| Field    | Type | Description                      |
| -------- | ---- | -------------------------------- |
| `node`   | Node | The Node object.                 |
| `degree` | Int  | The computed degree of the node. |

---

## Setting Up the Graph

To run the examples below, create the following graph structure:

### Nodes:

| ID | Label  |
| -- | ------ |
| 1  | Person |
| 2  | Person |
| 3  | City   |
| 4  | City   |

### Relationships:

| Source | Target | Type    |
| ------ | ------ | ------- |
| 1      | 2      | FRIEND  |
| 1      | 3      | VISITED |
| 2      | 3      | VISITED |
| 2      | 4      | VISITED |

Create this graph using the following commands:

```plaintext
CREATE (:Person {id: 1})
CREATE (:Person {id: 2})
CREATE (:City {id: 3})
CREATE (:City {id: 4})
CREATE (p1:Person {id: 1})-[:FRIEND]->(p2:Person {id: 2})
CREATE (p1)-[:VISITED]->(c1:City {id: 3})
CREATE (p2)-[:VISITED]->(c1)
CREATE (p2)-[:VISITED]->(c2:City {id: 4})
```

---

## Examples and Results

### Example 1: Compute the outgoing degree for all nodes

```plaintext
CALL algo.degree({})
```

#### Result:

| Node | Degree |
| ---- | ------ |
| 1    | 2      |
| 2    | 3      |
| 3    | 0      |
| 4    | 0      |

---

### Example 2: Compute the outgoing degree for specific node types

```plaintext
CALL algo.degree({source: 'Person'})
```

#### Result:

| Node | Degree |
| ---- | ------ |
| 1    | 2      |
| 2    | 3      |

---

### Example 3: Compute the outgoing degree for a specific relationship type

```plaintext
CALL algo.degree({source: 'Person', relation: 'FRIEND', dir: 'outgoing'})
```

#### Result:

| Node | Degree |
| ---- | ------ |
| 1    | 1      |

---

### Example 4: Compute the incoming degree for reachable nodes of a specific type

```plaintext
CALL algo.degree({source: 'Person', relation: 'VISITED', dir: 'incoming', destination: 'City'})
```

#### Result:

| Node | Degree |
| ---- | ------ |
| 3    | 2      |
| 4    | 1      |


