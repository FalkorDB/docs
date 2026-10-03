
# AllNodeScan

## Description

The `AllNodeScan` operation performs a complete scan of all nodes in the graph. It retrieves every node without applying any filters, making it a fundamental operation for queries that require accessing all nodes.

## Example Query

```cypher
MATCH (n) RETURN n
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| AllNodeScan    |
+----------------+
```

## Details

- **Purpose**: Retrieve all nodes in the graph.
- **Usage**: Typically used in queries with no filtering criteria on nodes.

# NodeByLabelScan

## Description

The `NodeByLabelScan` operation scans all nodes with a specific label in the graph. It retrieves nodes that match the given label, making it efficient for queries targeting specific node types.

## Example Query

```cypher
MATCH (n:LabelName) RETURN n
```

## Example Execution Plan

```
+--------------------+
| Operator           |
+--------------------+
| NodeByLabelScan    |
+--------------------+
```

## Details

- **Purpose**: Retrieve all nodes with a specified label.
- **Usage**: Used in queries that target nodes of a particular label.

# NodeByIdSeek

## Description

The `NodeByIdSeek` operation retrieves nodes from the graph by their unique identifiers (IDs). It efficiently fetches nodes based on specified ID ranges or individual IDs, making it suitable for queries that target specific nodes directly.

## Example Query

```cypher
MATCH (n) WHERE id(n) = 123 RETURN n
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| NodeByIdSeek   |
+----------------+
```

## Details

- **Purpose**: Efficiently retrieve nodes by their unique IDs.
- **Usage**: Used in queries that specify node IDs directly or through ranges.

# NodeByIndexScan

## Description

The `NodeByIndexScan` operation retrieves nodes from the graph using a specified index. It efficiently fetches nodes that match certain criteria by leveraging the index, making it suitable for queries that filter nodes based on indexed properties.

## Example Query

```cypher
MATCH (n:LabelName {property: 'value'}) RETURN n
```

## Example Execution Plan

```
+-------------------+
| Operator          |
+-------------------+
| NodeByIndexScan   |
+-------------------+
```

## Details

- **Purpose**: Efficiently retrieve nodes that match specific criteria using an index.
- **Usage**: Used in queries that filter nodes based on properties that are indexed.

# Skip

## Description

The `Skip` operation is used to bypass a specified number of records in the result set. It is commonly used in conjunction with the `Limit` operation to implement pagination in query results.

## Example Query

```cypher
MATCH (n) RETURN n SKIP 10 LIMIT 5
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| Skip           |
+----------------+
```

## Details

- **Purpose**: Skip a specified number of records in the result set.
- **Usage**: Typically used for pagination in combination with the `Limit` operation.

# Update

## Description

The `Update` operation is responsible for applying updates to nodes and edges in the graph based on specified update expressions. It consumes records from the child operator and performs the updates, committing changes to the graph once all updates are completed.

## Example Query

```cypher
MATCH (n:Node) SET n.property = 'new value'
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| Update         |
+----------------+
```

## Details
- **Purpose**: Apply updates to nodes and edges based on defined update expressions.
- **Usage**: Used for modifying node or edge properties in the graph.


# Unwind

## Description

The `Unwind` operation is used to flatten a list into separate records. It takes a list expression, evaluates it, and returns each element of the list as a separate record. If the list is empty or not evaluated, it will skip over it.

## Example Query

```cypher
UNWIND [1, 2, 3] AS x RETURN x
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| Unwind         |
+----------------+
```

## Details
- **Purpose**: Flatten a list into separate records.
- **Usage**: Typically used to unwind arrays or lists for further processing.


# Sort

## Description

The `Sort` operation orders records based on specified expressions. It can handle both limited and unlimited sorting. When a limit is set, it uses a heap to maintain the top records, otherwise, it uses quicksort. It processes records from the child operator and outputs them in sorted order.

## Example Query

```cypher
MATCH (n:Node) RETURN n ORDER BY n.property
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| Sort           |
+----------------+
```

## Details
- **Purpose**: Sort records based on expressions.
- **Usage**: Used in queries to order results by one or more properties.


# ValueHashJoin

## Description

The `ValueHashJoin` operation performs a join between two sets of records based on a specified value. It evaluates expressions on both sides of the join and matches records from the left side with records from the right side by comparing the evaluated values. It uses a hash table to store records from the left side and efficiently matches them with records from the right side based on a computed key.

## Example Query

```cypher
MATCH (n:Node), (m:Node)
WHERE n.property = m.property
RETURN n, m
```

## Example Execution Plan

```
+----------------------+
| Operator             |
+----------------------+
| ValueHashJoin        |
+----------------------+
```

## Details
- **Purpose**: Join records from two sources based on a computed key.
- **Usage**: Used when performing joins that match records from different sources based on computed expressions or properties.


# ApplyMultiplexer

## Description

The `ApplyMultiplexer` operation coordinates the application of records across multiple branches of an execution plan, utilizing logical operators like AND or OR. It processes records from a bounded branch and multiple other branches, applying specified logical conditions to determine when to return results.

## Example Query

```cypher
MATCH (n:Node), (m:Node)
WHERE n.property = m.property
RETURN n, m
```

## Example Execution Plan

```
+------------------------+
| Operator               |
+------------------------+
| ApplyMultiplexer (AND)  |
+------------------------+
```

## Details
- **Purpose**: Coordinate record application across multiple branches with logical operators.
- **Usage**: Used when logical conditions between different branches need to be evaluated and coordinated.

# Aggregate

## Description

The `Aggregate` operation groups records based on specified key expressions and applies aggregate functions over them. It processes records from its child operator, evaluates the aggregation expressions, and returns the final results, which include the aggregated data for each group.

## Example Query

```cypher
MATCH (n:Node) RETURN count(n), avg(n.property)
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| Aggregate      |
+----------------+
```

## Details
- **Purpose**: Group and aggregate data based on key expressions.
- **Usage**: Used to compute aggregate functions (like count, avg) for groups of records.


# Apply

## Description

The `Apply` operation evaluates two branches of an execution plan, the "bound" branch and the "right-hand side" (RHS) branch. It processes records from the bound branch and then propagates those records through the RHS branch, applying specified arguments and merging results accordingly.

## Example Query

```cypher
MATCH (n:Node) OPTIONAL MATCH (m:Node) WHERE n.property = m.property RETURN n, m
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| Apply          |
+----------------+
```

## Details
- **Purpose**: Evaluate two branches of a query and combine results.
- **Usage**: Used in queries that require the application of multiple operations to different branches of the execution plan.


# Argument

## Description

The `Argument` operation is used to manage and pass arguments within a query execution. It handles the creation and consumption of records associated with the argument values, and supports the resetting and cloning of argument states.

## Example Query

```cypher
WITH 1 AS x, 2 AS y RETURN x + y
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| Argument       |
+----------------+
```

## Details
- **Purpose**: Manage and pass argument values during query execution.
- **Usage**: Typically used for processing intermediate results and passing arguments in queries.

# ArgumentList

## Description

The `ArgumentList` operation processes a list of argument records. It manages and consumes a list of records, providing a mechanism for iterating over the list and passing the records to subsequent operations. It is used to handle multiple arguments, facilitating their manipulation within an execution plan.

## Example Query

```cypher
WITH [1, 2, 3] AS list UNWIND list AS x RETURN x
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| ArgumentList   |
+----------------+
```

## Details
- **Purpose**: Handle and process lists of arguments during execution.
- **Usage**: Common in operations that require handling multiple arguments or lists.

# CallSubquery

## Description

The `CallSubquery` operation executes a subquery in the context of a parent query. It manages the flow of records between the left-hand side (LHS) and right-hand side (RHS) branches, consuming records from the LHS, and either passing them to the RHS or returning records produced by the subquery. It supports both eager and non-eager evaluation.

## Example Query

```cypher
CALL subquery RETURN *
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| CallSubquery   |
+----------------+
```

## Details
- **Purpose**: Execute and handle records within a subquery.
- **Usage**: Used in queries that involve subqueries with potentially eager evaluation and record merging.


# CartesianProduct

## Description

The `CartesianProduct` operation computes the Cartesian product of multiple streams of records. It pulls records from all child operators, combining them in every possible way. The operation continues to generate new records by iterating through combinations of child records until all combinations have been exhausted.

## Example Query

```cypher
MATCH (a:Node), (b:Node) RETURN a, b
```

## Example Execution Plan

```
+-------------------+
| Operator          |
+-------------------+
| CartesianProduct  |
+-------------------+
```

## Details
- **Purpose**: Compute the Cartesian product of multiple child streams.
- **Usage**: Used in queries that require the combination of all records from multiple sources.

# CondVarLenTraverse

## Description

The `CondVarLenTraverse` operation handles conditional variable-length traversals in a graph. It performs a dynamic edge traversal where the number of hops (edges) can vary based on certain conditions, such as edge types and direction. This operation is ideal for graph queries that require flexible traversal conditions over variable-length paths.

## Example Query

```cypher
MATCH (a)-[:L*2..4]->(b) RETURN b
```

## Example Execution Plan

```
+----------------------+
| Operator             |
+----------------------+
| CondVarLenTraverse   |
+----------------------+
```

##Details
- **Purpose**: Perform a conditional variable-length traversal over edges.
- **Usage**: Used for graph queries requiring dynamic length traversal with conditions.


# Create

## Description

The `Create` operation in the execution plan is responsible for creating new nodes and edges in the graph. It constructs nodes and edges based on the specified node and edge blueprints, and inserts them into the graph. This operation can consume records and apply changes dynamically.

## Example Query

```cypher
CREATE (a:Node {name: 'Alice'})-[:FRIEND]->(b:Node {name: 'Bob'})
```

## Example Execution Plan

```
+------------------+
| Operator         |
+------------------+
| Create           |
+------------------+
```

## Details
- **Purpose**: Create nodes and edges in the graph.
- **Usage**: Used for adding new nodes or relationships to the graph during query execution.

# Delete

## Description

The `Delete` operation in the execution plan is responsible for deleting nodes and edges from the graph. It identifies nodes, edges, and paths marked for deletion and ensures they are properly removed from the graph. This operation also handles duplicates and ensures entities are only deleted once.

## Example Query

```cypher
MATCH (a:Node)-[r:REL]->(b:Node) DELETE a, r
```

## Example Execution Plan

```
+-----------------+
| Operator        |
+-----------------+
| Delete          |
+-----------------+
```

## Details
- **Purpose**: Delete specified nodes, edges, and paths from the graph.
- **Usage**: Used in queries where data needs to be removed from the graph, including nodes and relationships.


# Delete

## Description

The `Delete` operation is responsible for removing nodes, relationships, or both from the graph during query execution. It identifies the entities to be deleted and ensures they are properly removed. The operation also handles cleanup and prevents deleting entities more than once.

## Example Query

```cypher
MATCH (a:Node)-[r:REL]->(b:Node) DELETE a, r
```

## Example Execution Plan

```
+-----------------+
| Operator        |
+-----------------+
| Delete          |
+-----------------+
```

## Details
- **Purpose**: Delete nodes, relationships, and paths from the graph.
- **Usage**: Used in queries where data needs to be removed from the graph.


# Distinct

## Description

The `Distinct` operation eliminates duplicate records from a query's result set. It works by computing a hash of the values deemed distinct in each record and ensuring that only unique records are returned. This operation is useful for refining query results, ensuring no redundancy in the output.

## Example Query

```cypher
MATCH (n:Node) RETURN n DISTINCT
```

## Example Execution Plan

```
+------------------+
| Operator         |
+------------------+
| Distinct         |
+------------------+
```

## Details
- **Purpose**: Remove duplicate records from the query results.
- **Usage**: Used in queries to enforce uniqueness on the result set.


# Filter

## Description

The `Filter` operation applies a filtering process to a graph query's result set. It passes records through a filter tree, evaluating conditions defined by the filter. Only records that meet the criteria are allowed to pass; others are discarded.

## Example Query

```cypher
MATCH (n:Node) WHERE n.property = 'value' RETURN n
```

## Example Execution Plan

```
+-----------------+
| Operator        |
+-----------------+
| Filter          |
+-----------------+
```

## Details
- **Purpose**: Filter records based on specified conditions.
- **Usage**: Commonly used to refine query results by filtering nodes or relationships based on properties.


# ExpandInto

## Description

The `ExpandInto` operation in an execution plan involves expanding a set of records into new nodes or relationships based on an algebraic expression. It performs matrix-based graph traversal, appending new results based on conditions like source and destination node connections.

## Example Query

```cypher
MATCH (a)-[:REL]->(b) RETURN a, b
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| ExpandInto     |
+----------------+
```

## Details
- **Purpose**: Expands a record into new nodes or relationships using graph traversal and algebraic expressions.
- **Usage**: Used in complex graph traversal queries where new nodes/relationships need to be computed from existing records.


# EdgeByIndexScan

## Description

The `EdgeByIndexScan` operation retrieves edges based on their index. It is used for efficient graph traversals by leveraging indexed properties of edges, improving the performance of operations that need to quickly fetch edges meeting certain criteria.

## Example Query

```cypher
MATCH (a)-[r:REL]->(b) WHERE r.property = 'value' RETURN r
```

## Example Execution Plan

```
+------------------------+
| Operator               |
+------------------------+
| EdgeByIndexScan        |
+------------------------+
```

## Details
- **Purpose**: Retrieve edges based on indexed properties for optimized traversal.
- **Usage**: Used in queries that filter edges based on indexed attributes.


# Foreach

## Description

The `Foreach` operation is used to iterate over records in an execution plan. It consumes records from a supplier (if provided) or from a static list, and applies the operation's body to each record. The records are passed to the embedded argument list for further processing, such as unwinding or cloning. 

## Example Query

```cypher
MATCH (n) FOREACH (n IN nodes RETURN n)
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| Foreach        |
+----------------+
```

## Details

- **Purpose**: Iterates over a set of records, applying a body operation to each.
Usage: Used in queries where records need to be processed iteratively, often for complex traversals or mutations.


# Join

## Description

The `Join` operation combines results from multiple streams into a single result set. It consumes records from different streams, processes them, and joins them together based on conditions. This operation is essential for merging results in complex queries where multiple datasets need to be combined.

## Example Query

```cypher
MATCH (a)-[r]->(b) RETURN a, b, r
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| Join           |
+----------------+
```

## Details

- **Purpose**: Combine multiple result streams into a single unified set of results.
Usage: Used in queries that need to combine results from two or more subqueries or data sources.


# Limit

## Description

The `Limit` operation restricts the number of records that pass through the execution plan. It applies a limit to the number of records that can be consumed by subsequent operators. The limit is defined by an expression, which is evaluated and used to control how many records to return.

## Example Query

```cypher
MATCH (n) RETURN n LIMIT 10
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| Limit          |
+----------------+
```

## Details

- **Purpose**: Restrict the number of records processed in the query result.
- **Usage**: Often used to implement pagination or to limit the scope of results.


# Load CSV

## Description

The `Load CSV` operation enables loading data from CSV files into the graph. It processes the file and generates corresponding graph entities, making it suitable for bulk data imports from CSV sources. It handles parsing of CSV data and mapping it to the appropriate nodes and relationships in the graph.

## Example Query

```cypher
LOAD CSV FROM 'file:///path/to/file.csv' AS line
```

## Example Execution Plan

```
+-------------------+
| Operator          |
+-------------------+
| Load CSV          |
+-------------------+
```

## Details

- **Purpose**: Import data from CSV files into the graph.
- **Usage**: Used for bulk loading data in CSV format into the database.


# Merge Operation
Description
The Merge operation is used in graph databases to either create a new entity (node or edge) or match an existing one based on a given pattern. It combines ON CREATE and ON MATCH clauses, ensuring the graph reflects either the creation of new entities or the update of existing ones. The operation handles the detection of duplications, updating properties as specified.

## Example Query

```cypher
MERGE (n:Node {id: 123})
ON CREATE SET n.created = true
ON MATCH SET n.updated = true
```

## Example Execution Plan

```
+----------------+
| Operator       |
+----------------+
| Merge          |
+----------------+
```

## Details

- **Purpose**: Performs a MERGE operation which either creates or matches entities based on the pattern and applies updates.
- **Usage**: Used to ensure that data in the graph is either created or matched, applying changes where necessary.
On Create: Executes when no matching node or edge exists and a new entity is created.
On Match: Executes when a matching node or edge is found, updating properties or performing other actions.


# MergeCreate

## Description

The `MergeCreate` operation is used to create new entities (nodes or relationships) in the graph. It checks for the existence of the entity based on specific criteria and creates it if it does not already exist. If the entity exists, the operation does nothing, avoiding duplication.

## Example Query

```cypher
MERGE (n:Node {id: 123}) 
ON CREATE SET n.created = true
```

## Example Execution Plan

```
+-----------------------+
| Operator              |
+-----------------------+
| MergeCreate           |
+-----------------------+
```

## Details

- **Purpose**: Create a new node or relationship if one does not already exist.
- **Usage**: Used in queries where entities must be created but only if they don’t already exist in the graph.
On Create: Sets properties on newly created nodes or relationships.


# Optional

## Description

The `Optional` operation allows for producing results from an optional pattern in a query. It tries to consume records from the child operation, and if no record is produced, it still ensures an empty record is returned. This is helpful for queries with optional relationships or patterns that may not always match, ensuring that missing data does not prevent the query from completing.

## Example Query

```cypher
MATCH (a)-[r]->(b)
OPTIONAL MATCH (a)-[r2]->(c)
RETURN a, b, c
```

## Example Execution Plan

```
+-------------------+
| Operator          |
+-------------------+
| Optional          |
+-------------------+
```

## Details

- **Purpose**: Produce results for optional patterns or relationships.
- **Usage**: Used in queries where some relationships or patterns may not exist, but you still want to include the nodes with empty or null values for the missing parts.


# ProcedureCall

## Description

The `ProcedureCall` operation is used to invoke a procedure in the query execution plan. It supports passing arguments and retrieving the results. The operation handles both read and write procedures and ensures the appropriate locking when modifying the graph. The `ProcedureCall` operation ensures that each invocation steps through the procedure, evaluates arguments, and returns results accordingly.

## Example Query

```cypher
CALL myProcedure('arg1', 'arg2') YIELD result
```

## Example Execution Plan

```
+--------------------+
| Operator           |
+--------------------+
| ProcedureCall      |
+--------------------+
```

## Details

- **Purpose**: Execute a procedure and handle its arguments and results.
- **Usage**: Used for invoking procedures that are part of the query, potentially with different result handling, especially for modifying the graph.


# Project

## Description

The `Project` operation is responsible for projecting specific expressions into the result set, effectively selecting and renaming columns or calculated values. It is typically used when there is a need to define or transform the data output, such as for projection queries or returning specific expressions.

## Example Query

```cypher
MATCH (a) RETURN a.name, a.age
```

## Example Execution Plan

```
+-------------------+
| Operator          |
+-------------------+
| Project           |
+-------------------+
```

## Details

- **Purpose**: Project specific expressions into the result set.
- **Usage**: Used for selecting and transforming data to match specific return requirements in a query.


# Results

## Description

The `Results` operation collects and returns the final result set of a query. It manages the result set, enforcing a size limit and consuming records from child operations. It ensures the result set is correctly populated by mapping columns and limiting the result size.

## Example Query

```cypher
RETURN a, b, c
```

## Example Execution Plan

```
+-----------------+
| Operator        |
+-----------------+
| Results         |
+-----------------+
```

## Details

- **Purpose**: Return the final result set of a query.
- **Usage**: Used to collect and return results from the graph, often at the end of a query.
Result Set Size Limit: Enforces a maximum size for the result set to manage memory.


# SemiApply

## Description

The `SemiApply` operation performs a semi-join between two streams, retrieving records from the left stream (bound branch) and checking for matching records in the right stream (match branch). It only returns records from the left stream if a match is found in the right stream. The `AntiSemiApply` is the inverse operation, returning records from the left stream only when no match is found in the right stream.

## Example Query

```cypher
MATCH (n)-[:REL]->(m)
RETURN n
```

## Example Execution Plan

```
+-----------------+
| Operator        |
+-----------------+
| SemiApply       |
+-----------------+
```

## Details

- **Purpose**: Performs a semi-join (or anti-semi-join) between two streams, with the ability to return matching or non-matching records from the left stream.
- **Usage**: Typically used in graph traversals and joins where filtering based on existence of relationships is required.
Variants: Can be used as SemiApply or AntiSemiApply.


