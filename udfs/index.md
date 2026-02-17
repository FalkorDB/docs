---
layout: default
title: UDFs
has_children: true
nav_order: 6
---

# UDFs

Every database comes with a set of built-in functions. For example, FalkorDB functions include:
- `abs` -  computes the absolute value of a number
- `pow` - computes v^x
- `trim` - removes leading and trailing spaces.

These functions are built into the database and are part of its source code. Introducing a new function (for example, `UpperCaseOdd`) is not always trivial. The function needs to be usable to a wide audience for it to be considered. In the past, FalkorDB has rejected requests for adding new functions when these were too specific and did not add significant value for most users.

However, with the support of UDFs, everyone can extend FalkorDB's functionality with their own set of functions. The following sections introduce UDFs and explain how to manage and use them within FalkorDB.


## Practical Example
To introduce UDFs, review the following complete example, which loads a new UDF library called "StringUtils" that includes a single function called "UpperCaseOdd". Once loaded, the script puts the function to use.

```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host='localhost', port=6379)

# Define UDF library name & script
lib = "StringUtils"

# UpperCaseOdd implementation in JavaScript
script = """
function UpperCaseOdd(s) {
    return s.split('')
        .map((char, i) => {
            if (i % 2 !== 0) {
                return char.toUpperCase();
            }
            return char;
        })
    .join('');
};

// expose UDF to FalkorDB
falkor.register('UpperCaseOdd', UpperCaseOdd);
"""

# Load UDF into the database
db.udf_load(lib, script)

# Call UDF
graph = db.select_graph("G")
s = graph.query("RETURN StringUtils.UpperCaseOdd('abcdef')").result_set[0][0]
print(f"s: {s}") # prints 'aBcDeF'
```
## Commands Specification

The FalkorDB-PY Python client provides convenient access to UDF functionality, but FalkorDB also exposes this functionality via a set of GRAPH.UDF <sub_cmd> commands.

### GRAPH.UDF LOAD [REPLACE] <Lib> <script>

To add a UDF, call `GRAPH.UDF LOAD` followed by an optional `REPLACE` keyword. When specified, the REPLACE keyword replaces an already registered UDF library. The command then takes two arguments: the library name and the library script (written in JavaScript).

A UDF library can expose multiple UDFs. The following example shows a script that includes both non-exposed utility functions and a number of callable functions:

```javascript
function ShapeType(shape) {
	return shape.type;
}

function Triangle() {
	return {type: 'triangle', a:2, b:3, c:5};
}

function RandomShape() {
	return Triangle();
}

function Area(shape) {
    if (ShapeType(shape) == 'triangle') {
		return (shape.a * shape.b) / 2;
    } else {
        throw new Error("Unsupported shape");
    }
}

function Perimeter(shape) {
   if (ShapeType(shape) == 'triangle') {
		return shape.a + shape.b + shape.c;
    } else {
        throw new Error("Unsupported shape");
    } 
}

// Expose functions
falkor.register('Area', Area);
falkor.register('Perimeter', Perimeter);
falkor.register('RandomShape', RandomShape);
```

For each UDF script, FalkorDB exposes the falkor object, through which you register UDFs. To register a function, call `falkor.register` and provide the name you wish to expose your function under, followed by either an anonymous function or the actual function.

For example:
```javascript
falkor.register('Area', Area);
falkor.register('Perimeter', function(s) {return s.a + s.b + s.c});
```

Once loaded your functions are available as if they were built-in functions and can be invoked in the same way.

For example:
```bash
WITH Shapes.RandomShape() AS s
WHERE s.a > 1
CREATE (p:Position {area: Shapes.Area(s), perimeter: Shapes.Perimeter(s)})
SET p += s
RETURN s
```

### GRAPH.UDF LIST [Lib] [WITHCODE]

To list loaded UDF libraries you can either use the FalkorDB-PY `udf_list` function or invoke the `GRAPH.UDF LIST` command via a direct connection to the DB.

The command takes two optional arguments:
- Lib: list only a specific library.
- WITHCODE: to include the library source code as part of the output.

For example:
Calling the command: `GRAPH.UDF LIST WITHCODE` will generate the following output:

```bash
1) 1) library_name
   2) Shapes
   3) functions
   4) 1) Area
      2) Perimeter
      3) RandomShape
   5) library_code
   6) "function ShapeType(shape) {return shape.type;} function Triangle() {return {type: 'triangle', a:2, b:3, c:5};}...
```

### GRAPH.UDF DELETE <library>

To remove a UDF library use either the `udf_delete` FalkorDB-PY function, or send a `GRAPH.UDF DELETE <library>` command via a direct connection to the database.

For example:
```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host='localhost', port=6379)

# Remove the Shapes UDF library
db.udf_delete("Shapes")
```

### GRAPH.UDF FLUSH
Similar to delete `GRAPH.UDF FLUSH` removes **all** UDF libraries from the database.

```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host='localhost', port=6379)

# Remove all UDF libraries
db.udf_flush()
```

## Datatypes
Any datatype available in FalkorDB is accessible within UDFs, these include:
Scalar, Node, Edge & Path objects.

### Node
In a UDF, a node object exposes its  `ID`, `labels` and `attributes` via the corresponding properties: 
- `id` - node internal ID
- `labels` - node's labels
- `attributes` - node's attributes

For example:
 ```javascript
function stringify_node(n) {
    return "id: " + n.id + " labels: " + JSON.stringify(n.labels) + " attributes: " + JSON.stringify(n.attributes);
}
```

You can also collect a node's neighbors by calling the node's `getNeighbors` function. The getNeighbors function accepts an optional config map:

| config name | type   | description                                          | example                                            |
|------------|------|--------------------------------|------------------------------|
| direction       | string | direction of edges to traverse          | 'incoming' / 'outgoing' / 'both'      |
| types             | string array  | edge relationship types to consider | ['KNOWS', 'WORKS_AT'] |
| labels            | string array | node types to consider | ['Person', 'City'] |
| returnType    | string | return type, array of nodes or edges | 'nodes' / 'edges'  |

### Edge
In a UDF, an edge object exposes its `ID`, `type`, `source`, `target` and `attributes` via the corresponding properties:

- `id` - edge internal ID
- `type` - edge's relationship type
- `source` - edge's start node
- `target` - edge's end node
- `attributes` - edge's attributes

 For example:
 ```javascript
function stringify_edge(e) {
    return "id: " + e.id +
			" type: " + e.type +
			" sourceNode: " + e.source.id +
			" targetNode: " + e.target.id +
			" attributes: " + JSON.stringify(e.attributes);
}
```

### Path
In a UDF, a path object exposes its  `nodes`, `length` and `relationships` via the corresponding properties:

- `nodes` - path's nodes
- `length` - path's length
- `relationships` - path's edges

 For example:
 ```javascript
function stringify_path(p) {
    return "nodes: " + p.nodes +
			"length: " + p.length +
			"relationships: " + p.relationships;
}
```

## Global objects

### Graph
UDFs have access to a global `graph` object which represents the current graph executing the UDF.
The object exposes a single function `traverse` which is similar to the node's `getNeighbors` function (see docs above)
but can perform multi-source traversal.

```javascript
function multi_source_bfs(sources, config) {
    const targets = graph.traverse(sources, config) ;
    // source i neighbors are in targets[i], which is an array of node or edge objects
    // depending on the optional config map passed to graph.traverse
    const s0_neighbors = targets[0];
    ...
}
```

### Falkor
The `falkor` global object represents the FalkorDB database and is used mostly to register UDFs. The object exposes two functions:

Using the multi source traversal can be faster than performing multiple individual calls to getNeighbors.

- `log` - logs a message to the database stdout.
- `register` - exposes a function to the database.

#### falkor.log

##### Description
Logs a message to the database stdout

##### Syntax
```javascript
falkor.log(msg)
```

##### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | message to log |

##### falkor.register

##### Description
Register a function to the database

##### Syntax
```javascript
falkor.register(name, function)
```

##### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | expose function under this name |
| `function` | function pointer | Yes | function to expose |

##### Example

```javascript
function add(a,b) {
    return a + b;
}

falkor.register('addition', add);
```

## Advanced examples
In this example, we'll implement Jaccard similarity for nodes.
Jaccard's formula is: J(A,B) = |A ∩ B| / |A ∪ B| = |A ∩ B| / (|A| + |B| - |A ∩ B|)

In simple terms, to compute Jaccard similarity for two nodes A and B, compute the number of shared neighbors between them and divide it by the total number of neighbors. If A and B have the same neighbors, their similarity value is 1. If they have no shared neighbors, their similarity value is 0.

To start, define two UDFs (union and intersection) in a collection.js file:

```javascript
function union (a, b) {
  return [...new Set([...a, ...b])];
}

function intersection (a, b) {
  const setB = new Set(b);
  return a.filter(x => setB.has(x));
}

falkor.register('union', union);
falkor.register('intersection', intersection);
```

With these functions defined, proceed to implement Jaccard similarity. Create `similarity.js` as follows:

```javascript
function jaccard(a, b) {
    const aIds = a.getNeighbors().map(x => x.id);
    const bIds = b.getNeighbors().map(x => x.id);

    const unionSize = union(aIds, bIds).length;
    const intersectionSize = intersection(aIds, bIds).length;

    return unionSize === 0 ? 0 : intersectionSize / unionSize;
}

falkor.register('jaccard', jaccard);
```

Notice that jaccard uses both `union` and `intersection` from `collection.js`, and also collects A's and B's neighbors via a call to `getNeighbors`.

The remaining step is to load these UDF libraries into FalkorDB and use them:

```python
from falkordb import FalkorDB

db = FalkorDB()
g = db.select_graph("G")
g.delete()

def load_script(name, script_path):
    with open(script_path, "r") as f:
        content = f.read()
        db.udf_load(name, content, True)

def load_graph(g):
    q = """CREATE
        (eve:Person   {name: 'Eve'}),
        (bob:Person   {name: 'Bob'}),
        (dave:Person  {name: 'Dave'}),
        (carol:Person {name: 'Carol'}),
        (alice:Person {name: 'Alice'}),
        (eve)-[:FRIEND]->(bob),
        (bob)-[:FRIEND]->(alice),
        (bob)-[:FRIEND]->(carol),
        (bob)-[:FRIEND]->(eve),
        (dave)-[:FRIEND]->(alice),
        (carol)-[:FRIEND]->(alice),
        (carol)-[:FRIEND]->(bob),
        (alice)-[:FRIEND]->(bob),
        (alice)-[:FRIEND]->(carol),
        (alice)-[:FRIEND]->(dave)"""

    g.query(q)

def compute_jaccard_sim(g):
    q = """MATCH (alice:Person {name: 'Alice'}), (n)
           RETURN alice.name, n.name, similarity.jaccard(alice, n) AS sim"""
    results = g.query(q).result_set

    for row in results:
        alice = row[0]
        node  = row[1]
        sim   = row[2]
        print(f"Jaccard similarity between {alice} and {node} is: {sim}")

# load UDFs
load_script("collection", "./collection.js")
load_script("similarity", "./similarity.js")

load_graph(g)
compute_jaccard_sim(g)
```

The scripts load our two UDF libraries `collection` and `similarity` construct a graph and computes Jaccard similarity between `Alice` and every other node in the graph via the query:

```bash
MATCH (alice:Person {name: 'Alice'}), (n)
RETURN alice.name, n.name, similarity.jaccard(alice, n) AS sim
```

Output:
```bash
Jaccard similarity between Alice and Eve is: 0.333
Jaccard similarity between Alice and Bob is: 0.2
Jaccard similarity between Alice and Dave is: 0
Jaccard similarity between Alice and Carol is: 0.25
Jaccard similarity between Alice and Alice is: 1
```

### Custom Traversals
In some situations where you want fine control over the way graph traversals are made, Cypher might not be flexible enough. Consider the following requirement: collect all reachable nodes from a given start node, where a neighbor node is added to the expanded path if its amount value is greater than the accumulated sum of amounts on the current path.

The following UDF accomplishes this traversal. It performs a DFS and only expands to neighbors whose `amount` value is greater than the accumulated sum of amounts along the current path:


```javascript
function DFS_IncreasingAmounts(n, visited, total, reachables) {
    // Add current node to visited to prevent infinite loops in cycles
    visited.push(n.id);
    
    for (const neighbor of n.getNeighbors()) {        
        // 1. Check if already visited
        // 2. Logic: neighbor.amount must be GREATER than accumulated amount
        if (visited.includes(neighbor.id) || neighbor.amount <= total) {
            continue;
        }

        // Add to the list of discovered reachable nodes
        reachables.push(neighbor);

        // Recurse: add the neighbor's amount to the accumulated sum
        DFS_IncreasingAmounts(
            neighbor, 
            visited, 
            total + neighbor.amount,
            reachables
        );
    }
}

function CollectIncreasingAmounts(n) {
    const visited = [];
    const reachables = [];

	DFS_IncreasingAmounts(n, visited, n.amount, reachables);

    return reachables;
}

// Register function to be later used in a query
falkor.register('CollectIncreasingAmounts', CollectIncreasingAmounts);
```

The remaining step is to load this UDF:

```python
from falkordb import FalkorDB

db = FalkorDB()
g = db.select_graph("G")

# Load UDF
with open("./traversals.js", "r") as f:
	content = f.read()
	db.udf_load("Traversals", content, True)

# Use our custom traversal to find relevant reachable nodes
q = """MATCH (n:Transaction)
	   WHERE n.id = 12
       RETURN Traversals.CollectIncreasingAmounts(n)"""

reachables = g.query(q).result_set[0][0]
for node in reachables:
    print(f"Node ID: {node.id}, Amount: {node.properties.get('amount')}")
```

## FLEX

FLEX (FalkorDB Library of Extensions) is FalkorDB's open source community UDF package, available at [github.com/FalkorDB/flex](https://github.com/FalkorDB/flex).

It contains a variety of useful functionality, including:
- String and set similarity metrics for fuzzy matching and comparison
- Date and time manipulation, formatting, and parsing
- Low-level bitwise operations on integers

Contributions to extend this library with additional functionality are welcome.

## Limitations
> Currently, UDFs are not allowed to modify the graph in any way. You cannot update graph entities within a UDF, nor can you add or delete entities.

