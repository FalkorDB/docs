---
title: "GRAPH.EXPLAIN"
nav_order: 4
description: >
    Returns a query execution plan without running the query
parent: "Commands"    
---

# GRAPH.EXPLAIN

Constructs a query execution plan but does not run it. Inspect this execution plan to better
understand how your query will get executed.

Arguments: `Graph name, Query`

Returns: `String representation of a query execution plan`

{% capture shell_0 %}
GRAPH.EXPLAIN us_government "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p"
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
graph = client.select_graph('us_government')
query = "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p"
result = graph.explain(query)
print(result)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const graph = client.selectGraph('us_government');
const query = "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p";
const result = await graph.explain(query);
console.log(result);
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
Graph graph = client.selectGraph("us_government");
String query = "MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p";
String result = graph.explain(query);
System.out.println(result);
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
let graph = client.select_graph("us_government");
let query = r#"MATCH (p:President)-[:BORN]->(h:State {name:'Hawaii'}) RETURN p"#;
let result = graph.explain(query)?;
println!("{}", result);
{% endcapture %}

{% include code_tabs.html id="explain_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

## Sample Output

When you run `GRAPH.EXPLAIN`, you get a text representation of the execution plan that shows how FalkorDB will process your query. Here's an example:

```
Results
    Project
        Filter
            Node By Label Scan | (p:President)
```

### Interpreting Execution Plans

The execution plan is displayed as a tree structure, where operations are indented to show their hierarchy. The query is executed from bottom to top (innermost to outermost operations).

#### Common Operations

| Operation | Description | When It's Used |
|-----------|-------------|----------------|
| `Node By Label Scan` | Scans all nodes with a specific label | When querying nodes by label (e.g., `MATCH (n:User)`) |
| `All Node Scan` | Scans all nodes in the graph | When no label filter is specified (e.g., `MATCH (n)`) |
| `Filter` | Applies WHERE clause conditions | When filtering results with WHERE |
| `Conditional Traverse` | Follows relationships matching criteria | When traversing edges with conditions |
| `Expand Into` | Expands from one node to another specific node | When both endpoints are bound |
| `Project` | Selects specific properties/expressions | Corresponds to RETURN clause |
| `Aggregate` | Performs aggregation (COUNT, SUM, etc.) | When using aggregation functions |
| `Sort` | Orders results | When using ORDER BY |
| `Skip` | Skips the first N results | When using SKIP |
| `Limit` | Limits number of results | When using LIMIT |
| `Create Node` | Creates new nodes | When using CREATE with nodes |
| `Create Edge` | Creates new relationships | When using CREATE with relationships |

### Example: Complex Query Execution Plan

{% capture shell_1 %}
GRAPH.EXPLAIN social "MATCH (u:User)-[:FOLLOWS]->(f:User) WHERE u.age > 25 AND f.verified = true RETURN u.name, f.name ORDER BY u.age LIMIT 10"
{% endcapture %}

{% capture python_1 %}
query = """
MATCH (u:User)-[:FOLLOWS]->(f:User)
WHERE u.age > 25 AND f.verified = true
RETURN u.name, f.name
ORDER BY u.age
LIMIT 10
"""
plan = graph.explain(query)
print(plan)
{% endcapture %}

{% capture javascript_1 %}
const query = `
  MATCH (u:User)-[:FOLLOWS]->(f:User)
  WHERE u.age > 25 AND f.verified = true
  RETURN u.name, f.name
  ORDER BY u.age
  LIMIT 10
`;
const plan = await graph.explain(query);
console.log(plan);
{% endcapture %}

{% capture java_1 %}
String query = "MATCH (u:User)-[:FOLLOWS]->(f:User) " +
               "WHERE u.age > 25 AND f.verified = true " +
               "RETURN u.name, f.name " +
               "ORDER BY u.age LIMIT 10";
String plan = graph.explain(query);
System.out.println(plan);
{% endcapture %}

{% capture rust_1 %}
let query = r#"
  MATCH (u:User)-[:FOLLOWS]->(f:User)
  WHERE u.age > 25 AND f.verified = true
  RETURN u.name, f.name
  ORDER BY u.age
  LIMIT 10
"#;
let plan = graph.explain(query)?;
println!("{}", plan);
{% endcapture %}

{% include code_tabs.html id="complex_explain_tabs" shell=shell_1 python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}

**Sample Output:**
```
Results
    Limit
        Sort
            Project
                Filter
                    Conditional Traverse | (u:User)-[:FOLLOWS]->(f:User)
                        Filter
                            Node By Label Scan | (u:User)
```

**Reading the plan (bottom to top):**
1. `Node By Label Scan | (u:User)` - Find all User nodes and bind to 'u'
2. `Filter` - Apply condition `u.age > 25`
3. `Conditional Traverse | (u:User)-[:FOLLOWS]->(f:User)` - Follow FOLLOWS relationships to other User nodes
4. `Filter` - Apply condition `f.verified = true`
5. `Project` - Extract `u.name` and `f.name`
6. `Sort` - Order by `u.age`
7. `Limit` - Take only first 10 results

### Example: Indexed Query

When an index exists on a property used in a WHERE clause, the execution plan will show index usage:

```
Results
    Project
        Conditional Traverse | (u:User)-[:FOLLOWS]->(f:User)
            Node By Index Scan | (u:User)
```

The `Node By Index Scan` operation indicates that an index is being used, which is typically much faster than a full label scan.

## Use Cases

- **Query Optimization**: Identify operations that might be slow (e.g., `All Node Scan` on large graphs)
- **Index Verification**: Confirm that indexes are being used in your queries
- **Understanding Performance**: See how FalkorDB interprets your Cypher queries
- **Debugging**: Validate that your query logic matches your intentions

## See Also

- [`GRAPH.PROFILE`](/commands/graph.profile) - Similar to EXPLAIN but actually runs the query and provides detailed statistics
- [Cypher documentation](/cypher) - Learn about query optimization and best practices
