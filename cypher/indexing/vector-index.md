---
title: "Vector Index"
description: >
    FalkorDB supports vector indexes for similarity search on vector embeddings, essential for AI and machine learning applications.
---
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Vector indexing

With the introduction of the `vector` data-type a new type of index was introduced.
A vector index is a dedicated index for indexing and searching through vectors.

To create this type of index use the following syntax:

```cypher
CREATE VECTOR INDEX FOR <entity_pattern> ON <entity_attribute> OPTIONS <options>
```

The options are:
```
{
   dimension: INT, // Required, length of the vector to be indexed
   similarityFunction: STRING, // Required, currently only euclidean or cosine are allowed
   M: INT, // Optional, maximum number of outgoing edges per node. default 16
   efConstruction: INT, // Optional, number of candidates during construction. default 200
   efRuntime: INT // Optional, number of candidates during search. default 10
}
```

For example, to create a vector index over all `Product` nodes `description` attribute
use the following syntax:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
await graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.description) OPTIONS {dimension:128, similarityFunction:'euclidean'}").execute().await?;
```

  </TabItem>
</Tabs>

Similarly to create a vector index over all `Call` relationships `summary` attribute
use the following syntax:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
CREATE VECTOR INDEX FOR ()-[e:Call]->() ON (e.summary) OPTIONS {dimension:128, similarityFunction:'euclidean'}
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query("CREATE VECTOR INDEX FOR ()-[e:Call]->() ON (e.summary) OPTIONS {dimension:128, similarityFunction:'euclidean'}")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
await graph.query("CREATE VECTOR INDEX FOR ()-[e:Call]->() ON (e.summary) OPTIONS {dimension:128, similarityFunction:'euclidean'}");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
graph.query("CREATE VECTOR INDEX FOR ()-[e:Call]->() ON (e.summary) OPTIONS {dimension:128, similarityFunction:'euclidean'}");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
graph.query("CREATE VECTOR INDEX FOR ()-[e:Call]->() ON (e.summary) OPTIONS {dimension:128, similarityFunction:'euclidean'}").execute().await?;
```

  </TabItem>
</Tabs>

**Important**: When creating a vector index, both the vector dimension and similarity function must be provided. Currently, the only supported similarity functions are 'euclidean' or 'cosine'.

## Understanding Vector Index Parameters

### Required Parameters

- **dimension**: The length of the vectors to be indexed. Must match the dimensionality of your embeddings (e.g., 128, 384, 768, 1536).
- **similarityFunction**: The distance metric used for similarity search:
  - `euclidean`: Euclidean distance (L2 norm). Best for embeddings where magnitude matters.
  - `cosine`: Cosine similarity. Best for normalized embeddings where direction matters more than magnitude.

### Optional Parameters

These parameters control the HNSW (Hierarchical Navigable Small World) index structure:

- **M** (default: 16): Maximum number of connections per node in the graph
  - Higher values improve recall but increase memory usage and build time
  - Recommended range: 12-48
  - Use 16-32 for most applications

- **efConstruction** (default: 200): Number of candidates evaluated during index construction
  - Higher values improve index quality but slow down indexing
  - Recommended range: 100-400
  - Use 200-300 for balanced quality/speed

- **efRuntime** (default: 10): Number of candidates evaluated during search
  - Higher values improve recall but slow down queries
  - Can be adjusted per-query for speed/accuracy tradeoffs
  - Recommended: Start with 10, increase if recall is insufficient

## Inserting vectors

To create a new vector use the [vecf32](/cypher/functions#vector-functions) function
as follows:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
CREATE (p: Product {description: vecf32([2.1, 0.82, 1.3])})
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query("CREATE (p: Product {description: vecf32([2.1, 0.82, 1.3])})")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
await graph.query("CREATE (p: Product {description: vecf32([2.1, 0.82, 1.3])})");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
graph.query("CREATE (p: Product {description: vecf32([2.1, 0.82, 1.3])})");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
graph.query("CREATE (p: Product {description: vecf32([2.1, 0.82, 1.3])})").execute().await?;
```

  </TabItem>
</Tabs>

The above query creates a new `Product` node with a `description` attribute containing a vector.

## Query vector index

Vector indices are used to search for similar vectors to a given query vector
using the similarity function as a measure of "distance".

To query the index use either `db.idx.vector.queryNodes` for node retrieval or
`db.idx.vector.queryRelationships` for relationships.

```cypher
CALL db.idx.vector.queryNodes(
    label: STRING,
    attribute: STRING,
    k: INTEGER,
    query: VECTOR
) YIELD node, score
```

```cypher
CALL db.idx.vector.queryRelationships(
    relationshipType: STRING,
    attribute: STRING,
    k: INTEGER,
    query: VECTOR
) YIELD relationship, score
```

To query up to 10 similar `Product` descriptions to a given query description vector
issue the following procedure call:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
CALL db.idx.vector.queryNodes(
    'Product',
    'description',
    10,
    vecf32(<array_of_vector_elements>),
    ) YIELD node
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
result = graph.query("CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32(<array_of_vector_elements>)) YIELD node")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
const result = await graph.query("CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32(<array_of_vector_elements>)) YIELD node");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
ResultSet result = graph.query("CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32(<array_of_vector_elements>)) YIELD node");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
let result = graph.query("CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32(<array_of_vector_elements>)) YIELD node").execute().await?;
```

  </TabItem>
</Tabs>

The procedure can yield both the indexed entity assigned to the found similar vector
in addition to a similarity score of that entity.

## Deleting a vector index

To remove a vector index, simply issue the `drop index` command as follows:

```cypher
DROP VECTOR INDEX FOR <entity_pattern> (<entity_attribute>)
```

For example, to drop the vector index over Product description, invoke:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
DROP VECTOR INDEX FOR (p:Product) ON (p.description)
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
graph.query("DROP VECTOR INDEX FOR (p:Product) ON (p.description)")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
await graph.query("DROP VECTOR INDEX FOR (p:Product) ON (p.description)");
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
graph.query("DROP VECTOR INDEX FOR (p:Product) ON (p.description)");
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
graph.query("DROP VECTOR INDEX FOR (p:Product) ON (p.description)").execute().await?;
```

  </TabItem>
</Tabs>

## Index Management

### Listing Vector Indexes

To view all indexes (including vector) in your graph, use:

```cypher
CALL db.indexes()
```

Vector indexes are marked with type `VECTOR` and show the dimension and similarity function in the options field.

## Verifying Vector Index Usage

To verify that a vector index is being used, examine the query execution plan:

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
# Query using vector index
GRAPH.EXPLAIN DEMO_GRAPH "CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32([2.1, 0.82, 1.3])) YIELD node RETURN node"
# Output shows: ProcedureCall | db.idx.vector.queryNodes
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
# Query using vector index
query_vector = [2.1, 0.82, 1.3]
result = graph.explain(f"CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32({query_vector})) YIELD node RETURN node")
print(result)
# Output shows: ProcedureCall | db.idx.vector.queryNodes
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
// Query using vector index
const queryVector = [2.1, 0.82, 1.3];
const result = await graph.explain(`CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32([${queryVector}])) YIELD node RETURN node`);
console.log(result);
// Output shows: ProcedureCall | db.idx.vector.queryNodes
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
// Query using vector index
float[] queryVector = {2.1f, 0.82f, 1.3f};
String result = graph.explain("CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32([2.1, 0.82, 1.3])) YIELD node RETURN node");
System.out.println(result);
// Output shows: ProcedureCall | db.idx.vector.queryNodes
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
// Query using vector index
let result = graph.explain("CALL db.idx.vector.queryNodes('Product', 'description', 10, vecf32([2.1, 0.82, 1.3])) YIELD node RETURN node").execute().await?;
println!("{}", result);
// Output shows: ProcedureCall | db.idx.vector.queryNodes
```

  </TabItem>
</Tabs>

## Performance Tradeoffs and Best Practices

### When to Use Vector Indexes

Vector indexes are essential for:
- **Semantic search**: Finding similar items based on meaning, not just keywords
- **Recommendation systems**: Discovering similar products, content, or users
- **RAG (Retrieval Augmented Generation)**: Retrieving relevant context for LLMs
- **Duplicate detection**: Finding near-duplicate items based on embeddings
- **Image/audio similarity**: When using vision or audio embedding models

### Performance Considerations

**Benefits:**
- Enables efficient approximate nearest neighbor (ANN) search
- Scales to millions of vectors with sub-linear query time
- Supports both node and relationship vectors

**Costs:**
- **Memory usage**: Vector indexes are memory-intensive
  - A 1M vector index with 768 dimensions (float32) requires ~3GB of memory
  - Formula: `vectors × dimensions × 4 bytes + HNSW overhead (~20%)`
- **Build time**: Index construction can be slow for large datasets
- **Approximate results**: Returns approximate (not exact) nearest neighbors
- **No support for filtering**: Vector queries don't combine well with property filters

**Recommendations:**
- Choose appropriate vector dimensions (balance between quality and cost)
- Use cosine similarity for normalized embeddings (e.g., from OpenAI, Sentence Transformers)
- Use euclidean distance for unnormalized data
- Tune M and efConstruction based on your accuracy requirements
- Consider batch indexing for large datasets
- Monitor memory usage carefully

### Similarity Function Tradeoffs

**Cosine Similarity:**
- Best for: Text embeddings, normalized vectors
- Measures: Angular distance between vectors
- Range: -1 to 1 (1 = identical direction)
- Use when: Vector magnitude is not meaningful

**Euclidean Distance:**
- Best for: Unnormalized data, physical measurements
- Measures: Straight-line distance between vectors
- Range: 0 to ∞ (0 = identical)
- Use when: Both direction and magnitude matter

### Example: Realistic Vector Search

<Tabs groupId="programming-language">
  <TabItem value="shell" label="Shell">

```bash
# Create vector index for product embeddings
GRAPH.QUERY DEMO_GRAPH "CREATE VECTOR INDEX FOR (p:Product) ON (p.embedding) OPTIONS {dimension:768, similarityFunction:'cosine', M:32, efConstruction:200}"

# Insert products with embeddings (embeddings would come from your model)
GRAPH.QUERY DEMO_GRAPH "CREATE (p:Product {name: 'Laptop', embedding: vecf32([0.1, 0.2, ...])})"

# Search for similar products
GRAPH.QUERY DEMO_GRAPH "CALL db.idx.vector.queryNodes('Product', 'embedding', 5, vecf32([0.15, 0.18, ...])) YIELD node, score RETURN node.name, score ORDER BY score DESC"
```

  </TabItem>
  <TabItem value="python" label="Python">

```python
# Create vector index for product embeddings
graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.embedding) OPTIONS {dimension:768, similarityFunction:'cosine', M:32, efConstruction:200}")

# Insert products with embeddings (embeddings would come from your model)
embedding = model.encode("laptop computer")  # Your embedding model
graph.query(f"CREATE (p:Product {name: 'Laptop', embedding: vecf32({embedding.tolist()})})")

# Search for similar products
query_embedding = model.encode("notebook pc")
result = graph.query(f"CALL db.idx.vector.queryNodes('Product', 'embedding', 5, vecf32({query_embedding.tolist()})) YIELD node, score RETURN node.name, score ORDER BY score DESC")
for record in result.result_set:
    print(f"Product: {record[0]}, Similarity: {record[1]}")
```

  </TabItem>
  <TabItem value="javascript" label="JavaScript">

```javascript
// Create vector index for product embeddings
await graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.embedding) OPTIONS {dimension:768, similarityFunction:'cosine', M:32, efConstruction:200}");

// Insert products with embeddings (embeddings would come from your model)
const embedding = await model.encode("laptop computer");  // Your embedding model
await graph.query(`CREATE (p:Product {name: 'Laptop', embedding: vecf32([${embedding}])})`);

// Search for similar products
const queryEmbedding = await model.encode("notebook pc");
const result = await graph.query(`CALL db.idx.vector.queryNodes('Product', 'embedding', 5, vecf32([${queryEmbedding}])) YIELD node, score RETURN node.name, score ORDER BY score DESC`);
for (const record of result.data) {
    console.log(`Product: ${record['node.name']}, Similarity: ${record['score']}`);
}
```

  </TabItem>
  <TabItem value="java" label="Java">

```java
// Create vector index for product embeddings
graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.embedding) OPTIONS {dimension:768, similarityFunction:'cosine', M:32, efConstruction:200}");

// Insert products with embeddings (embeddings would come from your model)
float[] embedding = model.encode("laptop computer");  // Your embedding model
graph.query(String.format("CREATE (p:Product {name: 'Laptop', embedding: vecf32(%s)})", Arrays.toString(embedding)));

// Search for similar products
float[] queryEmbedding = model.encode("notebook pc");
ResultSet result = graph.query(String.format("CALL db.idx.vector.queryNodes('Product', 'embedding', 5, vecf32(%s)) YIELD node, score RETURN node.name, score ORDER BY score DESC", Arrays.toString(queryEmbedding)));
for (Record record : result) {
    System.out.printf("Product: %s, Similarity: %s%n", record.get("node.name"), record.get("score"));
}
```

  </TabItem>
  <TabItem value="rust" label="Rust">

```rust
// Create vector index for product embeddings
graph.query("CREATE VECTOR INDEX FOR (p:Product) ON (p.embedding) OPTIONS {dimension:768, similarityFunction:'cosine', M:32, efConstruction:200}").execute().await?;

// Insert products with embeddings (embeddings would come from your model)
let embedding = model.encode("laptop computer");  // Your embedding model
graph.query(&format!("CREATE (p:Product {name: 'Laptop', embedding: vecf32({:?})})", embedding)).execute().await?;

// Search for similar products
let query_embedding = model.encode("notebook pc");
let result = graph.query(&format!("CALL db.idx.vector.queryNodes('Product', 'embedding', 5, vecf32({:?})) YIELD node, score RETURN node.name, score ORDER BY score DESC", query_embedding)).execute().await?;
for record in result.data() {
    println!("Product: {}, Similarity: {}", record["node.name"], record["score"]);
}
```

  </TabItem>
</Tabs>

### Troubleshooting

**Common Issues:**

1. **Dimension mismatch**: Ensure all vectors have the same dimension as specified in the index
2. **Wrong similarity function**: Use cosine for normalized vectors, euclidean for unnormalized
3. **Poor recall**: Increase efRuntime or efConstruction parameters
4. **Slow queries**: Decrease efRuntime or reduce k (number of results)
5. **High memory usage**: Reduce M parameter or use lower-dimensional embeddings
