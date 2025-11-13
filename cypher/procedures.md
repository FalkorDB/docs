---
title: "Procedures"
nav_order: 19
description: >
    Procedures calling using with CALL and YIELD.
parent: "Cypher Language"
---

# Procedures

Procedures are functions that can be called from within Cypher queries using the `CALL` syntax.

## Syntax

Basic procedure call:

```sh
GRAPH.QUERY social "CALL db.labels()"
```

With explicit `YIELD` to select specific return values:

```sh
GRAPH.QUERY social "CALL db.labels() YIELD label"
```

**Note:** The `YIELD` clause is optional. When omitted, all values listed in the 'Yields' column are returned automatically.

## Available Procedures

| Procedure                       | Arguments                                       | Yields                        | Description                                                                                                                                                                            |
| -------                         | :-------                                        | :-------                      | :-----------                                                                                                                                                                           |
| db.labels                       | none                                            | `label`                       | Yields all node labels in the graph.                                                                                                                                                   |
| db.relationshipTypes            | none                                            | `relationshipType`            | Yields all relationship types in the graph.                                                                                                                                            |
| db.propertyKeys                 | none                                            | `propertyKey`                 | Yields all property keys in the graph.                                                                                                                                                 |
| db.meta.stats                   | none                                            | `labels`, `relTypes`, `relCount`, `nodeCount`, `labelCount`, `relTypeCount`, `propertyKeyCount` | Yield comprehensive graph statistics including maps of labels and relationship types with their counts, total node/relationship counts, and schema metadata counts. |
| db.indexes                      | none                                            | `label`, `properties`, `types`, `options`, `language`, `stopwords`, `entitytype`, `status`, `info` | Yield all indexes in the graph, denoting whether they are of the type of exact-match ("RANGE"), full-text ("FULLTEXT") or vector ("VECTOR") and which label and properties each covers and whether they are indexing node or relationship attributes. |
| db.constraints                  | none                                            | `type`, `label`, `properties`, `entitytype`, `status` | Yield all constraints in the graph, denoting constraint type (UNIQIE/MANDATORY), which label/relationship-type and properties each enforces. |
| db.idx.fulltext.createNodeIndex | `label`, `property` [, `property` ...]          | none                          | Builds a full-text searchable index on a label and the 1 or more specified properties.                                                                                                 |
| db.idx.fulltext.drop            | `label`                                         | none                          | Deletes the full-text index associated with the given label.                                                                                                                           |
| db.idx.fulltext.queryNodes      | `label`, `string`                               | `node`, `score`               | Retrieve all nodes that contain the specified string in the full-text indexes on the given label.                                                                                      |
| algo.pageRank                   | `label`, `relationship-type`                    | `node`, `score`               | Runs the pagerank algorithm over nodes of given label, considering only edges of given relationship type.                                                                              |
| [algo.BFS](#BFS)                | `source-node`, `max-level`, `relationship-type` | `nodes`, `edges`              | Performs BFS to find all nodes connected to the source. A `max level` of 0 indicates unlimited and a non-NULL `relationship-type` defines the relationship type that may be traversed. |
| dbms.procedures()               | none                                            | `name`, `mode`                | List all procedures in the DBMS, yields for every procedure its name and mode (read/write).                                                                                            |
