# coll.union

## Description
Combines two lists and returns a new list containing all unique elements from both lists. Duplicates are automatically removed, treating the inputs as sets.

## Syntax
```cypher
flex.coll.union(list1, list2)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `list1` | list | Yes | The first list |
| `list2` | list | Yes | The second list |

## Returns
**Type:** list

A new list containing all unique elements from both input lists. The order is not guaranteed.

## Examples

### Example 1: Basic Union
```cypher
WITH [1, 2, 3] AS a, [3, 4, 5] AS b
RETURN flex.coll.union(a, b) AS result
```

**Output:**
```
result
--------------
[1, 2, 3, 4, 5]
```

### Example 2: Combining Tags from Multiple Nodes
```cypher
MATCH (d1:Document {id: 'doc1'})
MATCH (d2:Document {id: 'doc2'})
RETURN flex.coll.union(d1.tags, d2.tags) AS allTags
```

### Example 3: Merging User Interests
```cypher
MATCH (u:User)
WITH collect(u.interests) AS interestLists
RETURN reduce(result = [], list IN interestLists | 
    flex.coll.union(result, list)
) AS allUniqueInterests
```

### Example 4: Finding All Related Categories
```cypher
MATCH (p:Product {id: 123})
MATCH (similar:Product)-[:SIMILAR_TO]-(p)
RETURN flex.coll.union(p.categories, similar.categories) AS combinedCategories
```

## Notes
- Automatically removes duplicates from the result
- Works with any comparable data types
- Order of elements in the result is not guaranteed
- Equivalent to mathematical set union operation
- Both lists are spread and deduplicated using Set

## See Also
- [coll.intersection](./intersection.md) - Find common elements between lists
- [sim.jaccard](../similarity/jaccard.md) - Calculate similarity between sets
