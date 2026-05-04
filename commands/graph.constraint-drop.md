---
title: "GRAPH.CONSTRAINT DROP"
description: >
    Deletes a constraint from specified graph
parent: "Commands"
nav_order: 8
---

# GRAPH.CONSTRAINT DROP

---
syntax: |
  GRAPH.CONSTRAINT DROP key 
    MANDATORY|UNIQUE
    NODE label | RELATIONSHIP reltype
    PROPERTIES propCount prop [prop...]  
---

Deleted a graph constraint.

[Examples](#examples)

For an introduction to constraints see [GRAPH.CONSTRAINT CREATE](/commands/graph.constraint-create)

## Required arguments

<details open><summary><code>key</code></summary>

is key name for the graph.
</details>

<details open><summary><code>constraintType</code></summary>

is the constraint type: either `MANDATORY` or `UNIQUE`.

</details>

<details open><summary><code>NODE label | RELATIONSHIP reltype</code></summary>
  
is the graph entity type (`NODE` or `RELATIONSHIP`) and the name of the node label or relationship type on which the constraint is enforced.

</details>

<details open><summary><code>propCount</code></summary>

is the number of properties following. Valid values are between 1 and 255.

</details>

<details open><summary><code>prop...</code></summary>

is a list of `propCount` property names.

</details>

## Return value

@simple-string-reply - `OK` if executed correctly, or @error-reply otherwise.

## Examples

To delete a unique constraint for all nodes with label `Person` enforcing uniqueness on the combination of values of attributes `first_name` and `last_name`, issue the following command:

{% capture shell_0 %}
redis> GRAPH.CONSTRAINT DROP g UNIQUE NODE Person PROPERTIES 2 first_name last_name
# Output: OK
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
result = client.drop_constraint('g', 'UNIQUE', 'NODE', 'Person', ['first_name', 'last_name'])
print(result)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const result = await client.dropConstraint('g', 'UNIQUE', 'NODE', 'Person', ['first_name', 'last_name']);
console.log(result);
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
String result = client.dropConstraint("g", "UNIQUE", "NODE", "Person", Arrays.asList("first_name", "last_name"));
System.out.println(result);
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
let result = client.drop_constraint("g", "UNIQUE", "NODE", "Person", &["first_name", "last_name"])?;
println!("{}", result);
{% endcapture %}

{% include code_tabs.html id="drop_constraint_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

{% include faq_accordion.html title="Frequently Asked Questions" q1="Is dropping a constraint synchronous or asynchronous?" a1="Unlike constraint creation, dropping a constraint is **synchronous**. The command returns `OK` immediately upon successful removal." q2="Do I need to drop the supporting index after dropping a unique constraint?" a2="No, the supporting index is not automatically removed. You can drop it separately if it is no longer needed, but it may still be useful for query performance." q3="What happens if I try to drop a constraint that does not exist?" a3="The command will return an error indicating that the specified constraint was not found." q4="Does dropping a constraint affect existing data?" a4="No. Dropping a constraint only removes the enforcement rule. Existing data remains unchanged; it simply will no longer be validated against that constraint." %}
