---
title: "Indexing"
nav_order: 21
description: >
    FalkorDB supports single-property indexes for node labels and for relationship type. String, numeric, and geospatial data types can be indexed.
parent: "Cypher Language"
has_children: true
redirect_from:
  - /cypher/indexing.html
---

# Indexing

FalkorDB provides multiple types of indexes to optimize query performance and enable efficient data retrieval. Each index type is designed for specific use cases and data patterns.

## Index Types

FalkorDB supports the following index types:

### [Range Index](./range-index.md)

Range indexes support single-property indexes for node labels and relationship types. String, numeric, and geospatial data types can be indexed. These indexes automatically optimize queries with filters on indexed properties.

### [Full-text Index](./fulltext-index.md)

Full-text indexes leverage RediSearch capabilities to provide powerful text search functionality. They support features like stemming, stopwords, phonetic search, and scoring based on TF-IDF.

### [Vector Index](./vector-index.md)

Vector indexes enable similarity search on vector embeddings. These indexes are essential for AI and machine learning applications, supporting operations like nearest neighbor search with configurable similarity functions (euclidean or cosine).

---

Choose an index type from the navigation menu to learn more about creating, querying, and managing that specific type of index.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What types of indexes does FalkorDB support?"
  a1="FalkorDB supports three index types: **Range indexes** for exact-match and comparison queries, **Full-text indexes** for text search with stemming and scoring, and **Vector indexes** for similarity search on embeddings."
  q2="When should I create an index?"
  a2="Create indexes on properties frequently used in WHERE clause filters. Indexes accelerate lookups but add write overhead, so avoid indexing properties that are rarely queried or have very high write frequency."
  q3="Can I index relationship properties?"
  a3="Yes. FalkorDB supports indexing both node label properties and relationship type properties with range and full-text indexes."
  q4="How do I check which indexes exist in my graph?"
  a4="Use the procedure `CALL db.indexes()` which yields all indexes with their label, properties, type (RANGE, FULLTEXT, or VECTOR), entity type, and status."
%}
