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
