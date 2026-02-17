---
title: "Full-text Index"
nav_order: 2
description: >
    FalkorDB provides full-text indices through procedure calls.
parent: "Indexing"
grand_parent: "Cypher Language"
---

# Full-text indexing

FalkorDB leverages the indexing capabilities of [RediSearch](https://redis.io/docs/interact/search-and-query/) to provide full-text indices through procedure calls.

## Creating a full-text index for a node label

To construct a full-text index on the `title` property of all nodes with label `Movie`, use the syntax:

{% capture shell_10 %}
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex('Movie', 'title')"
{% endcapture %}

{% capture python_10 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', 'title')")
{% endcapture %}

{% capture javascript_10 %}
await graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', 'title')");
{% endcapture %}

{% capture java_10 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', 'title')");
{% endcapture %}

{% capture rust_10 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', 'title')").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_create_tabs" shell=shell_10 python=python_10 javascript=javascript_10 java=java_10 rust=rust_10 %}

More properties can be added to this index by adding their names to the above set of arguments, or using this syntax again with the additional names.

{% capture shell_11 %}
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex('Person', 'firstName', 'lastName')"
{% endcapture %}

{% capture python_11 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Person', 'firstName', 'lastName')")
{% endcapture %}

{% capture javascript_11 %}
await graph.query("CALL db.idx.fulltext.createNodeIndex('Person', 'firstName', 'lastName')");
{% endcapture %}

{% capture java_11 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Person', 'firstName', 'lastName')");
{% endcapture %}

{% capture rust_11 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Person', 'firstName', 'lastName')").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_multi_property_tabs" shell=shell_11 python=python_11 javascript=javascript_11 java=java_11 rust=rust_11 %}

Index configuration options:

1. Language - Define which language to use for stemming text, which is adding the base form of a word to the index. This allows the query for "going" to also return results for "go" and "gone", for example.
2. Stopwords - These are words that are usually so common that they do not add much information to search, but take up a lot of space and CPU time in the index.

To construct a full-text index on the `title` property using `German` language and using custom stopwords of all nodes with label `Movie`, use the syntax:

{% capture shell_12 %}
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex({ label: 'Movie', language: 'German', stopwords: ['a', 'ab'] }, 'title')"
{% endcapture %}

{% capture python_12 %}
graph.query("CALL db.idx.fulltext.createNodeIndex({ label: 'Movie', language: 'German', stopwords: ['a', 'ab'] }, 'title')")
{% endcapture %}

{% capture javascript_12 %}
await graph.query("CALL db.idx.fulltext.createNodeIndex({ label: 'Movie', language: 'German', stopwords: ['a', 'ab'] }, 'title')");
{% endcapture %}

{% capture java_12 %}
graph.query("CALL db.idx.fulltext.createNodeIndex({ label: 'Movie', language: 'German', stopwords: ['a', 'ab'] }, 'title')");
{% endcapture %}

{% capture rust_12 %}
graph.query("CALL db.idx.fulltext.createNodeIndex({ label: 'Movie', language: 'German', stopwords: ['a', 'ab'] }, 'title')").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_config_tabs" shell=shell_12 python=python_12 javascript=javascript_12 java=java_12 rust=rust_12 %}

Additional field configuration options:

1. Weight - The importance of the text in the field
2. Nostem - Skip stemming when indexing text
3. Phonetic - Enable phonetic search on the text

To construct a full-text index on the `title` property with phonetic search of all nodes with label `Movie`, use the syntax:

{% capture shell_13 %}
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.createNodeIndex('Movie', {field: 'title', phonetic: 'dm:en'})"
{% endcapture %}

{% capture python_13 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', {field: 'title', phonetic: 'dm:en'})")
{% endcapture %}

{% capture javascript_13 %}
await graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', {field: 'title', phonetic: 'dm:en'})");
{% endcapture %}

{% capture java_13 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', {field: 'title', phonetic: 'dm:en'})");
{% endcapture %}

{% capture rust_13 %}
graph.query("CALL db.idx.fulltext.createNodeIndex('Movie', {field: 'title', phonetic: 'dm:en'})").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_phonetic_tabs" shell=shell_13 python=python_13 javascript=javascript_13 java=java_13 rust=rust_13 %}

## Query Syntax and Features

FalkorDB uses [RediSearch query syntax](https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/query_syntax/) which provides powerful search capabilities including fuzzy matching, prefix matching, and tokenization.

### Tokenization

When text is indexed, it is automatically tokenized (split into words). By default, text is split on whitespace and punctuation. This allows you to search for individual words within larger text fields.

For example, if you index a `title` property containing "The Lord of the Rings", you can search for any of the individual words like "Lord" or "Rings".

### Prefix Matching

Prefix matching allows you to search for words that start with a specific prefix using the `*` wildcard. This is useful for autocomplete functionality or when you want to match word variations.

{% capture shell_prefix %}
# Find all movies with titles containing words starting with "Jun"
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.queryNodes('Movie', 'Jun*') YIELD node RETURN node.title"
# This would match "Jungle", "June", "Junior", etc.
{% endcapture %}

{% capture python_prefix %}
# Find all movies with titles containing words starting with "Jun"
result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jun*') YIELD node RETURN node.title")
for record in result:
    print(record["node.title"])
# This would match "Jungle", "June", "Junior", etc.
{% endcapture %}

{% capture javascript_prefix %}
// Find all movies with titles containing words starting with "Jun"
const result = await graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jun*') YIELD node RETURN node.title");
for (const record of result.data) {
    console.log(record["node.title"]);
}
// This would match "Jungle", "June", "Junior", etc.
{% endcapture %}

{% capture java_prefix %}
// Find all movies with titles containing words starting with "Jun"
ResultSet result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jun*') YIELD node RETURN node.title");
for (Record record : result) {
    System.out.println(record.get("node.title"));
}
// This would match "Jungle", "June", "Junior", etc.
{% endcapture %}

{% capture rust_prefix %}
// Find all movies with titles containing words starting with "Jun"
let result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jun*') YIELD node RETURN node.title").execute().await?;
for record in result.data() {
    println!("{}", record["node.title"]);
}
// This would match "Jungle", "June", "Junior", etc.
{% endcapture %}

{% include code_tabs.html id="fulltext_prefix_tabs" shell=shell_prefix python=python_prefix javascript=javascript_prefix java=java_prefix rust=rust_prefix %}

**Note:** Prefix matching only works at the end of a word (e.g., `Jun*`). The wildcard must appear at the end of the search term.

### Fuzzy Matching

Fuzzy matching allows you to find words that are similar to your search term, accounting for typos and spelling variations. Use the `%` symbol followed by the Levenshtein distance (number of character changes allowed).

{% capture shell_fuzzy %}
# Find movies with titles containing words similar to "Jangle" (allowing 1 character difference)
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.queryNodes('Movie', '%Jangle%1') YIELD node RETURN node.title"
# This would match "Jungle" (1 character different)

# Allow up to 2 character differences
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.queryNodes('Movie', '%Jngle%2') YIELD node RETURN node.title"
# This would also match "Jungle" (1 character missing)
{% endcapture %}

{% capture python_fuzzy %}
# Find movies with titles containing words similar to "Jangle" (allowing 1 character difference)
result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', '%Jangle%1') YIELD node RETURN node.title")
for record in result:
    print(record["node.title"])
# This would match "Jungle" (1 character different)

# Allow up to 2 character differences
result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', '%Jngle%2') YIELD node RETURN node.title")
# This would also match "Jungle" (1 character missing)
{% endcapture %}

{% capture javascript_fuzzy %}
// Find movies with titles containing words similar to "Jangle" (allowing 1 character difference)
const result = await graph.query("CALL db.idx.fulltext.queryNodes('Movie', '%Jangle%1') YIELD node RETURN node.title");
for (const record of result.data) {
    console.log(record["node.title"]);
}
// This would match "Jungle" (1 character different)

// Allow up to 2 character differences
const result2 = await graph.query("CALL db.idx.fulltext.queryNodes('Movie', '%Jngle%2') YIELD node RETURN node.title");
// This would also match "Jungle" (1 character missing)
{% endcapture %}

{% capture java_fuzzy %}
// Find movies with titles containing words similar to "Jangle" (allowing 1 character difference)
ResultSet result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', '%Jangle%1') YIELD node RETURN node.title");
for (Record record : result) {
    System.out.println(record.get("node.title"));
}
// This would match "Jungle" (1 character different)

// Allow up to 2 character differences
ResultSet result2 = graph.query("CALL db.idx.fulltext.queryNodes('Movie', '%Jngle%2') YIELD node RETURN node.title");
// This would also match "Jungle" (1 character missing)
{% endcapture %}

{% capture rust_fuzzy %}
// Find movies with titles containing words similar to "Jangle" (allowing 1 character difference)
let result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', '%Jangle%1') YIELD node RETURN node.title").execute().await?;
for record in result.data() {
    println!("{}", record["node.title"]);
}
// This would match "Jungle" (1 character different)

// Allow up to 2 character differences
let result2 = graph.query("CALL db.idx.fulltext.queryNodes('Movie', '%Jngle%2') YIELD node RETURN node.title").execute().await?;
// This would also match "Jungle" (1 character missing)
{% endcapture %}

{% include code_tabs.html id="fulltext_fuzzy_tabs" shell=shell_fuzzy python=python_fuzzy javascript=javascript_fuzzy java=java_fuzzy rust=rust_fuzzy %}

**Fuzzy matching syntax:** `%term%distance` where:
- `term` is the word to match
- `distance` is the maximum Levenshtein distance (1-3, default is 1 if not specified)

**Note:** Fuzzy matching is computationally more expensive than exact or prefix matching, so use it judiciously on large datasets.

### Combining Query Features

You can combine multiple search terms using boolean operators:

- `AND` (or space): All terms must match
- `OR` (`|`): At least one term must match
- `NOT` (`-`): Term must not be present

{% capture shell_combined %}
# Find movies with "Jungle" AND "Book" in the title
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.queryNodes('Movie', 'Jungle Book') YIELD node RETURN node.title"

# Find movies with "Jungle" OR "Forest" in the title
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.queryNodes('Movie', 'Jungle|Forest') YIELD node RETURN node.title"

# Find movies with "Book" but NOT "Jungle"
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.queryNodes('Movie', 'Book -Jungle') YIELD node RETURN node.title"

# Combine prefix and fuzzy matching: Find "Jun*" OR words similar to "Forst"
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.queryNodes('Movie', 'Jun*|%Forst%1') YIELD node RETURN node.title"
{% endcapture %}

{% capture python_combined %}
# Find movies with "Jungle" AND "Book" in the title
result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jungle Book') YIELD node RETURN node.title")

# Find movies with "Jungle" OR "Forest" in the title
result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jungle|Forest') YIELD node RETURN node.title")

# Find movies with "Book" but NOT "Jungle"
result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book -Jungle') YIELD node RETURN node.title")

# Combine prefix and fuzzy matching
result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jun*|%Forst%1') YIELD node RETURN node.title")
{% endcapture %}

{% capture javascript_combined %}
// Find movies with "Jungle" AND "Book" in the title
const result = await graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jungle Book') YIELD node RETURN node.title");

// Find movies with "Jungle" OR "Forest" in the title
const result2 = await graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jungle|Forest') YIELD node RETURN node.title");

// Find movies with "Book" but NOT "Jungle"
const result3 = await graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book -Jungle') YIELD node RETURN node.title");

// Combine prefix and fuzzy matching
const result4 = await graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jun*|%Forst%1') YIELD node RETURN node.title");
{% endcapture %}

{% capture java_combined %}
// Find movies with "Jungle" AND "Book" in the title
ResultSet result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jungle Book') YIELD node RETURN node.title");

// Find movies with "Jungle" OR "Forest" in the title
ResultSet result2 = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jungle|Forest') YIELD node RETURN node.title");

// Find movies with "Book" but NOT "Jungle"
ResultSet result3 = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book -Jungle') YIELD node RETURN node.title");

// Combine prefix and fuzzy matching
ResultSet result4 = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jun*|%Forst%1') YIELD node RETURN node.title");
{% endcapture %}

{% capture rust_combined %}
// Find movies with "Jungle" AND "Book" in the title
let result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jungle Book') YIELD node RETURN node.title").execute().await?;

// Find movies with "Jungle" OR "Forest" in the title
let result2 = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jungle|Forest') YIELD node RETURN node.title").execute().await?;

// Find movies with "Book" but NOT "Jungle"
let result3 = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book -Jungle') YIELD node RETURN node.title").execute().await?;

// Combine prefix and fuzzy matching
let result4 = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Jun*|%Forst%1') YIELD node RETURN node.title").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_combined_tabs" shell=shell_combined python=python_combined javascript=javascript_combined java=java_combined rust=rust_combined %}

For more advanced query syntax features, see the [RediSearch query syntax documentation](https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/query_syntax/).

## Utilizing a full-text index for a node label

An index can be invoked to match any whole words contained within:

{% capture shell_14 %}
GRAPH.QUERY DEMO_GRAPH
"CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node.title"
1) 1) "node.title"
2) 1) 1) "The Jungle Book"
   2) 1) "The Book of Life"
3) 1) "Query internal execution time: 0.927409 milliseconds"
{% endcapture %}

{% capture python_14 %}
result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node.title")
for record in result:
    print(record["node.title"])
# Output:
# The Jungle Book
# The Book of Life
{% endcapture %}

{% capture javascript_14 %}
const result = await graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node.title");
for (const record of result.data) {
    console.log(record["node.title"]);
}
// Output:
// The Jungle Book
// The Book of Life
{% endcapture %}

{% capture java_14 %}
ResultSet result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node.title");
for (Record record : result) {
    System.out.println(record.get("node.title"));
}
// Output:
// The Jungle Book
// The Book of Life
{% endcapture %}

{% capture rust_14 %}
let result = graph.query("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node.title").execute().await?;
for record in result.data() {
    println!("{}", record["node.title"]);
}
// Output:
// The Jungle Book
// The Book of Life
{% endcapture %}

{% include code_tabs.html id="fulltext_query_tabs" shell=shell_14 python=python_14 javascript=javascript_14 java=java_14 rust=rust_14 %}

This CALL clause can be interleaved with other Cypher clauses to perform more elaborate manipulations:

```cypher
CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node AS m
WHERE m.genre = 'Adventure'
RETURN m ORDER BY m.rating
```

```sh
1) 1) "m"
2) 1) 1) 1) 1) "id"
            2) (integer) 1168
         2) 1) "labels"
            2) 1) "Movie"
         3) 1) "properties"
            2) 1) 1) "genre"
                  2) "Adventure"
               2) 1) "rating"
                  2) "7.6"
               3) 1) "votes"
                  2) (integer) 151342
               4) 1) "year"
                  2) (integer) 2016
               5) 1) "title"
                  2) "The Jungle Book"
3) 1) "Query internal execution time: 0.226914 milliseconds"
```

In addition to yielding matching nodes, full-text index scans will return the score of each node. This is the [TF-IDF](https://redis.io/docs/interact/search-and-query/advanced-concepts/scoring/#tfidf-default) score of the node, which is informed by how many times the search terms appear in the node and how closely grouped they are. This can be observed in the example:

```cypher
CALL db.idx.fulltext.queryNodes('Node', 'hello world') YIELD node, score RETURN score, node.val
```

```sh
1) 1) "score"
   2) "node.val"
2) 1) 1) "2"
      2) "hello world"
   2) 1) "1"
      2) "hello to a different world"
3) 1) "Cached execution: 1"
   2) "Query internal execution time: 0.335401 milliseconds"
```

## Deleting a full-text index for a node label

For a node label, the full-text index deletion syntax is:

{% capture shell_15 %}
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.fulltext.drop('Movie')"
{% endcapture %}

{% capture python_15 %}
graph.query("CALL db.idx.fulltext.drop('Movie')")
{% endcapture %}

{% capture javascript_15 %}
await graph.query("CALL db.idx.fulltext.drop('Movie')");
{% endcapture %}

{% capture java_15 %}
graph.query("CALL db.idx.fulltext.drop('Movie')");
{% endcapture %}

{% capture rust_15 %}
graph.query("CALL db.idx.fulltext.drop('Movie')").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_drop_tabs" shell=shell_15 python=python_15 javascript=javascript_15 java=java_15 rust=rust_15 %}

## Creating Full-Text indexing for Relation Labels
To create a full-text index on the name property of all relations with the label Manager and enable phonetic search, use the following syntax:

{% capture shell_16 %}
GRAPH.QUERY DEMO_GRAPH "CREATE FULLTEXT INDEX FOR ()-[m:Manager]-() on (m.name)"
{% endcapture %}

{% capture python_16 %}
graph.query("CREATE FULLTEXT INDEX FOR ()-[m:Manager]-() on (m.name)")
{% endcapture %}

{% capture javascript_16 %}
await graph.query("CREATE FULLTEXT INDEX FOR ()-[m:Manager]-() on (m.name)");
{% endcapture %}

{% capture java_16 %}
graph.query("CREATE FULLTEXT INDEX FOR ()-[m:Manager]-() on (m.name)");
{% endcapture %}

{% capture rust_16 %}
graph.query("CREATE FULLTEXT INDEX FOR ()-[m:Manager]-() on (m.name)").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_relation_create_tabs" shell=shell_16 python=python_16 javascript=javascript_16 java=java_16 rust=rust_16 %}
## Querying with a Full-Text Index
To search for specific words within the indexed relations, use:

{% capture shell_17 %}
GRAPH.QUERY DEMO_GRAPH
"CALL db.idx.fulltext.queryRelationships('Manager', 'Charlie Munger') YIELD relationship RETURN relationship.name"
{% endcapture %}

{% capture python_17 %}
result = graph.query("CALL db.idx.fulltext.queryRelationships('Manager', 'Charlie Munger') YIELD relationship RETURN relationship.name")
{% endcapture %}

{% capture javascript_17 %}
const result = await graph.query("CALL db.idx.fulltext.queryRelationships('Manager', 'Charlie Munger') YIELD relationship RETURN relationship.name");
{% endcapture %}

{% capture java_17 %}
ResultSet result = graph.query("CALL db.idx.fulltext.queryRelationships('Manager', 'Charlie Munger') YIELD relationship RETURN relationship.name");
{% endcapture %}

{% capture rust_17 %}
let result = graph.query("CALL db.idx.fulltext.queryRelationships('Manager', 'Charlie Munger') YIELD relationship RETURN relationship.name").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_relation_query_tabs" shell=shell_17 python=python_17 javascript=javascript_17 java=java_17 rust=rust_17 %}

## Deleting a Full-Text Index
To delete the full-text index for a specific relation label, use:

{% capture shell_18 %}
GRAPH.QUERY DEMO_GRAPH "DROP FULLTEXT INDEX FOR ()-[m:Manager]-() ON (m.name)"
{% endcapture %}

{% capture python_18 %}
graph.query("DROP FULLTEXT INDEX FOR ()-[m:Manager]-() ON (m.name)")
{% endcapture %}

{% capture javascript_18 %}
await graph.query("DROP FULLTEXT INDEX FOR ()-[m:Manager]-() ON (m.name)");
{% endcapture %}

{% capture java_18 %}
graph.query("DROP FULLTEXT INDEX FOR ()-[m:Manager]-() ON (m.name)");
{% endcapture %}

{% capture rust_18 %}
graph.query("DROP FULLTEXT INDEX FOR ()-[m:Manager]-() ON (m.name)").execute().await?;
{% endcapture %}

{% include code_tabs.html id="fulltext_relation_drop_tabs" shell=shell_18 python=python_18 javascript=javascript_18 java=java_18 rust=rust_18 %}

## Index Management

### Listing Full-text Indexes

To view all indexes (including full-text) in your graph, use:

```cypher
CALL db.indexes()
```

This returns information about all indexes, with full-text indexes marked with type `FULLTEXT`.

## Performance Tradeoffs and Best Practices

### When to Use Full-text Indexes

Full-text indexes are ideal for:
- **Text-heavy search**: Searching within large text fields like descriptions, articles, or comments
- **Partial word matching**: When users might not know the exact text
- **Fuzzy search**: Handling typos and spelling variations
- **Multi-word queries**: Searching for multiple terms with boolean logic

### When NOT to Use Full-text Indexes

Full-text indexes are not optimal for:
- **Exact numeric filtering**: Use range indexes instead for numeric comparisons
- **Exact-match queries**: Range indexes are more efficient for exact property matches
- **Small or structured data**: For short, well-defined strings, range indexes may be sufficient

### Performance Considerations

**Benefits:**
- Enables sophisticated text search capabilities (fuzzy, prefix, phonetic)
- Supports stemming and language-specific optimizations
- Returns relevance scores (TF-IDF) for ranking results

**Costs:**
- **Write overhead**: Text must be tokenized and indexed on write
- **Storage**: Requires more space than range indexes due to tokenization and inverted indices
- **Configuration complexity**: Language, stopwords, and stemming settings affect results
- **Query performance**: Fuzzy matching is more expensive than exact matching

**Recommendations:**
- Choose the correct language setting for proper stemming
- Configure appropriate stopwords for your use case
- Use prefix matching (`*`) for autocomplete rather than full fuzzy search when possible
- Test query performance with realistic data volumes
- Consider the tradeoff between index configurability and query performance

### Configuration Best Practices

**Language Selection:**
- Wrong language settings can produce poor stemming results
- Example: Searching "running" with English stemming finds "run", but German stemming won't

**Stopwords:**
- Default stopwords are optimized for general text
- Customize stopwords for domain-specific applications (e.g., legal, medical, technical documents)
- Too many stopwords can hurt precision; too few increase index size

**Phonetic Search:**
- Useful for name searches and when spelling variations are common
- Increases index size and query time
- Double Metaphone (`dm:en`) is recommended for English

## Verifying Full-text Index Usage

Use `GRAPH.EXPLAIN` to verify that full-text queries use the index:

{% capture shell_ft_verify %}
# Check if full-text index is used
GRAPH.EXPLAIN DEMO_GRAPH "CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node"
# Output shows: ProcedureCall | db.idx.fulltext.queryNodes
{% endcapture %}

{% capture python_ft_verify %}
# Check if full-text index is used
result = graph.explain("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node")
print(result)
# Output shows: ProcedureCall | db.idx.fulltext.queryNodes
{% endcapture %}

{% capture javascript_ft_verify %}
// Check if full-text index is used
const result = await graph.explain("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node");
console.log(result);
// Output shows: ProcedureCall | db.idx.fulltext.queryNodes
{% endcapture %}

{% capture java_ft_verify %}
// Check if full-text index is used
String result = graph.explain("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node");
System.out.println(result);
// Output shows: ProcedureCall | db.idx.fulltext.queryNodes
{% endcapture %}

{% capture rust_ft_verify %}
// Check if full-text index is used
let result = graph.explain("CALL db.idx.fulltext.queryNodes('Movie', 'Book') YIELD node RETURN node").execute().await?;
println!("{}", result);
// Output shows: ProcedureCall | db.idx.fulltext.queryNodes
{% endcapture %}

{% include code_tabs.html id="fulltext_verify_tabs" shell=shell_ft_verify python=python_ft_verify javascript=javascript_ft_verify java=java_ft_verify rust=rust_ft_verify %}
