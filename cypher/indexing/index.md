---
title: "Indexing"
nav_order: 21
description: >
    FalkorDB supports single-property indexes for node labels and for relationship type. String, numeric, and geospatial data types can be indexed.
parent: "Cypher Language"
has_children: true
---

# Indexing

FalkorDB provides multiple types of indexes to optimize query performance and enable efficient data retrieval. Each index type is designed for specific use cases and data patterns.

## Index Types

FalkorDB supports the following index types:

### [Range Index](./range-index)

Range indexes support single-property indexes for node labels and relationship types. String, numeric, and geospatial data types can be indexed. These indexes automatically optimize queries with filters on indexed properties.

### [Full-text Index](./fulltext-index)

Full-text indexes leverage RediSearch capabilities to provide powerful text search functionality. They support features like stemming, stopwords, phonetic search, and scoring based on TF-IDF.

### [Vector Index](./vector-index)

Vector indexes enable similarity search on vector embeddings. These indexes are essential for AI and machine learning applications, supporting operations like nearest neighbor search with configurable similarity functions (euclidean or cosine).

---

Choose an index type from the navigation menu to learn more about creating, querying, and managing that specific type of index.
