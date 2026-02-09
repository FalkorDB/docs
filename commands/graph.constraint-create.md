---
title: "GRAPH.CONSTRAINT CREATE"
description: >
    Create mandatory and unique constraints on FalkorDB graphs to enforce data integrity. Guarantee property existence and value uniqueness for nodes and relationships.
parent: "Commands"    
---

# GRAPH.CONSTRAINT CREATE

---
syntax: |
  GRAPH.CONSTRAINT CREATE key
    MANDATORY|UNIQUE
    NODE label | RELATIONSHIP reltype
    PROPERTIES propCount prop [prop...]  
---

Creates a graph constraint.

[Examples](#examples)

## Introduction to constraints

A constraint is a rule enforced on graph nodes or relationships, used to guarantee a certain structure of the data.

FalkorDB supports two types of constraints:

1. Mandatory constraints
2. Unique constraints

### Mandatory constraints

A mandatory constraint enforces existence of given attributes for all nodes with a given label or for all edges with a given relationship-type.

Consider a mandatory constraint over the attribute `id` of all nodes with the label `Person`.
This constraint will enforce that any `Person` node in the graph has an `id` attribute.
Any attempt to create or modify a `Person` node, such that the resulting node does not have an `id` attribute, will fail.

### Unique constraints

A unique constraint enforces uniqueness of values of a given set of attributes for all nodes with a given label or for all edges with a given relationship-type. I.e., no duplicates are allowed.

Consider a unique constraint over the attributes: `first_name` and `last_name` of all nodes with the label `Person`
This constraint will enforce that any combination of `first_name`, `last_name` is unique.
E.g., a graph can contain the following `Person` nodes:

```sql
(:Person {first_name:'Frank', last_name:'Costanza'})
(:Person {first_name:'Estelle', last_name:'Costanza'})
```

But trying to create a third node with `first_name` Frank and `last_name` Costanza, will issue an error and the query will fail.

<note><b>Notes:</b>

- A unique constraint requires the existence of an exact-match index prior to its creation. For example, trying to create a unique constraint governing attributes: `first_name` and `last_name` of nodes with label `Person` without having an exact-match index over `Person`'s `first_name` and `last_name` attributes will fail.

- A unique constraint is enforced for a given node or edge only if all the constrained properties are defined (non-null).
- Unique constraints are not enforced for array-valued properties.
- Trying to delete an index that supports a constraint will fail.

</note>

## Creating a constraint

To create a constraint, use the `GRAPH.CONSTRAINT CREATE` command as follows:

```sh
GRAPH.CONSTRAINT CREATE key constraintType {NODE label | RELATIONSHIP reltype} PROPERTIES propCount prop [prop...]
```

## Required arguments

<details open><summary><code>key</code></summary>

is key name for the graph.
</details>

<details open><summary><code>constraintType</code></summary>

is the constraint type: either `MANDATORY` or `UNIQUE`.

</details>

<details open><summary><code>NODE label | RELATIONSHIP reltype</code></summary>
  
is the graph entity type (`NODE` or `RELATIONSHIP`) and the name of the node label or relationship type on which the constraint should be enforced.

</details>

<details open><summary><code>propCount</code></summary>

is the number of properties following. Valid values are between 1 and 255.

</details>

<details open><summary><code>prop...</code></summary>

is a list of `propCount` property names.

</details>

<note><b>Notes:</b>

- Constraints are created asynchronously. The constraint creation command will reply with `PENDING` and the newly created constraint is enforced gradually on all relevant nodes or relationships.
  During its creation phase, a constraint's status is `UNDER CONSTRUCTION`. When all governed nodes or relationships confirm to the constraint - its status is updated to `OPERATIONAL`, otherwise, if a conflict is detected, the constraint status is updated to `FAILED` and the constraint is not enforced. The caller may try to resolve the conflict and recreate the constraint. To retrieve the status of all constraints - use the `db.constraints()` procedure.
- A constraint creation command may fail synchronously due to the following reasons:
  1. Syntax error
  2. Constraint already exists
  3. Missing supporting index (for unique constraint)

  In addition, a constraint creation command may fail asynchronously due to the following reasons:

  1. The graph contains data which violates the constraint

</note>

## Return value

@simple-string-reply - `PENDING` if executed correctly and the constraint is being created asynchronously, or @error-reply otherwise.

## Examples

### Creating a unique constraint for a node label

To create a unique constraint for all nodes with label `Person` enforcing uniqueness on the combination of values of attributes `first_name` and `last_name`, issue the following commands:

{% capture shell_0 %}
redis> GRAPH.QUERY g "CREATE INDEX FOR (p:Person) ON (p.first_name, p.last_name)"
redis> GRAPH.CONSTRAINT CREATE g UNIQUE NODE Person PROPERTIES 2 first_name last_name
# Output: PENDING
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
graph = client.select_graph('g')
graph.query("CREATE INDEX FOR (p:Person) ON (p.first_name, p.last_name)")
result = client.create_constraint('g', 'UNIQUE', 'NODE', 'Person', ['first_name', 'last_name'])
print(result)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const graph = client.selectGraph('g');
await graph.query("CREATE INDEX FOR (p:Person) ON (p.first_name, p.last_name)");
const result = await client.createConstraint('g', 'UNIQUE', 'NODE', 'Person', ['first_name', 'last_name']);
console.log(result);
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
Graph graph = client.selectGraph("g");
graph.query("CREATE INDEX FOR (p:Person) ON (p.first_name, p.last_name)");
String result = client.createConstraint("g", "UNIQUE", "NODE", "Person", Arrays.asList("first_name", "last_name"));
System.out.println(result);
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
let graph = client.select_graph("g");
graph.query("CREATE INDEX FOR (p:Person) ON (p.first_name, p.last_name)")?;
let result = client.create_constraint("g", "UNIQUE", "NODE", "Person", &["first_name", "last_name"])?;
println!("{}", result);
{% endcapture %}

{% include code_tabs.html id="unique_constraint_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

### Creating a mandatory constraint for a relationship type

To create a mandatory constraint for all edges with relationship-type `Visited`, enforcing the existence of a `date` attribute, issue the following command:

{% capture shell_1 %}
redis> GRAPH.CONSTRAINT CREATE g MANDATORY RELATIONSHIP Visited PROPERTIES 1 date
# Output: PENDING
{% endcapture %}

{% capture python_1 %}
result = client.create_constraint('g', 'MANDATORY', 'RELATIONSHIP', 'Visited', ['date'])
print(result)
{% endcapture %}

{% capture javascript_1 %}
const result = await client.createConstraint('g', 'MANDATORY', 'RELATIONSHIP', 'Visited', ['date']);
console.log(result);
{% endcapture %}

{% capture java_1 %}
String result = client.createConstraint("g", "MANDATORY", "RELATIONSHIP", "Visited", Arrays.asList("date"));
System.out.println(result);
{% endcapture %}

{% capture rust_1 %}
let result = client.create_constraint("g", "MANDATORY", "RELATIONSHIP", "Visited", &["date"])?;
println!("{}", result);
{% endcapture %}

{% include code_tabs.html id="mandatory_constraint_tabs" shell=shell_1 python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}

### Listing constraints

To list all constraints enforced on a given graph, use the `db.constraints` procedure:

{% capture shell_2 %}
redis> GRAPH.RO_QUERY g "call db.constraints()"
# Output: ...
{% endcapture %}

{% capture python_2 %}
result = graph.ro_query("call db.constraints()")
print(result)
{% endcapture %}

{% capture javascript_2 %}
const result = await graph.ro_query("call db.constraints()");
console.log(result);
{% endcapture %}

{% capture java_2 %}
ResultSet result = graph.ro_query("call db.constraints()");
System.out.println(result);
{% endcapture %}

{% capture rust_2 %}
let result = graph.ro_query("call db.constraints()")?;
println!("{:?}", result);
{% endcapture %}

{% include code_tabs.html id="list_constraints_tabs" shell=shell_2 python=python_2 javascript=javascript_2 java=java_2 rust=rust_2 %}

## Deleting a constraint

See [GRAPH.CONSTRAINT DROP](/commands/graph.constraint-drop)
