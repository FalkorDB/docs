---
title: "OPTIONAL MATCH"
nav_order: 2
description: >
    The OPTIONAL MATCH clause is a MATCH variant that produces null values for elements that do not match successfully, rather than the all-or-nothing logic for patterns in MATCH clauses.
parent: "Cypher Language"
redirect_from:
  - /cypher/optional_match.html
  - /cypher/optional_match
---

# OPTIONAL MATCH

The OPTIONAL MATCH clause is a MATCH variant that produces null values for elements that do not match successfully, rather than the all-or-nothing logic for patterns in MATCH clauses.

It can be considered to fill the same role as LEFT/RIGHT JOIN does in SQL, as MATCH entities must be resolved but nodes and edges introduced in OPTIONAL MATCH will be returned as nulls if they cannot be found.

OPTIONAL MATCH clauses accept the same patterns as standard MATCH clauses, and may similarly be modified by WHERE clauses.

Multiple MATCH and OPTIONAL MATCH clauses can be chained together, though a mandatory MATCH cannot follow an optional one.

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (p:Person) OPTIONAL MATCH (p)-[w:WORKS_AT]->(c:Company)
WHERE w.start_date > 2016
RETURN p, w, c"
```

All `Person` nodes are returned, as well as any `WORKS_AT` relations and `Company` nodes that can be resolved and satisfy the `start_date` constraint. For each `Person` that does not resolve the optional pattern, the person will be returned as normal and the non-matching elements will be returned as null.

Cypher is lenient in its handling of null values, so actions like property accesses and function calls on null values will return null values rather than emit errors.

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (p:Person) OPTIONAL MATCH (p)-[w:WORKS_AT]->(c:Company)
RETURN p, w.department, ID(c) as ID"
```

In this case, `w.department` and `ID` will be returned if the OPTIONAL MATCH was successful, and will be null otherwise.

Clauses like SET, CREATE, MERGE, and DELETE will ignore null inputs and perform the expected updates on real inputs. One exception to this is that attempting to create a relation with a null endpoint will cause an error:

```sh
GRAPH.QUERY DEMO_GRAPH
"MATCH (p:Person) OPTIONAL MATCH (p)-[w:WORKS_AT]->(c:Company)
CREATE (c)-[:NEW_RELATION]->(:NEW_NODE)"
```

If `c` is null for any record, this query will emit an error. In this case, no changes to the graph are committed, even if some values for `c` were resolved.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What is the difference between MATCH and OPTIONAL MATCH?"
  a1="**MATCH** requires all patterns to be satisfied or the entire row is excluded. **OPTIONAL MATCH** returns null values for pattern elements that cannot be found, similar to a LEFT JOIN in SQL."
  q2="Can I chain multiple OPTIONAL MATCH clauses?"
  a2="Yes. You can chain multiple MATCH and OPTIONAL MATCH clauses together. However, a mandatory MATCH cannot follow an OPTIONAL MATCH in the same query."
  q3="How does FalkorDB handle null values from OPTIONAL MATCH?"
  a3="FalkorDB is lenient with nulls: property accesses and function calls on null values return null rather than errors. Clauses like SET, CREATE, and DELETE will ignore null inputs gracefully."
  q4="Can I use WHERE with OPTIONAL MATCH?"
  a4="Yes. OPTIONAL MATCH clauses accept the same WHERE predicates as standard MATCH clauses to further filter the optional pattern."
%}
