# sim.jaccard

## Description
Computes the Jaccard similarity coefficient between two sets (lists). The Jaccard index measures the similarity between two sets by dividing the size of their intersection by the size of their union. It returns a value between 0 (no similarity) and 1 (identical sets).

## Syntax
```cypher
flex.sim.jaccard(list1, list2)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `list1` | list | Yes | The first list to compare |
| `list2` | list | Yes | The second list to compare |

## Returns
**Type:** number (float)

A value between 0 and 1 representing the Jaccard similarity coefficient:
- `1.0` indicates identical sets
- `0.0` indicates no common elements
- Returns `null` for invalid inputs

## Examples

### Example 1: Basic Set Similarity
```cypher
// Compare two tag lists
RETURN flex.sim.jaccard(['tag1', 'tag2', 'tag3'], ['tag2', 'tag3', 'tag4']) AS similarity
```

**Output:**
```
similarity
----------
0.5
```
(2 common elements / 4 total unique elements = 0.5)

### Example 2: Finding Similar Documents by Tags
```cypher
// Find documents with similar tags to a reference document
MATCH (ref:Document {id: 'doc123'})
MATCH (other:Document)
WHERE other.id <> ref.id
WITH ref, other, flex.sim.jaccard(ref.tags, other.tags) AS similarity
WHERE similarity > 0.3
RETURN other.title, similarity
ORDER BY similarity DESC
LIMIT 10
```

### Example 3: User Interest Matching
```cypher
// Find users with similar interests
MATCH (u1:User {id: $userId})
MATCH (u2:User)
WHERE u1 <> u2
WITH u1, u2, flex.sim.jaccard(u1.interests, u2.interests) AS match_score
WHERE match_score > 0.5
RETURN u2.name, u2.interests, match_score
ORDER BY match_score DESC
```

## Notes
- Treats input lists as sets (duplicates within each list don't affect the result)
- Returns `null` if either input is not an array
- Order of elements doesn't matter
- Works with any comparable data types (strings, numbers, etc.)
- Ideal for comparing categorical attributes, tags, or interest lists

## See Also
- [text.levenshtein](../text/levenshtein.md) - Edit distance for string comparison
- [coll.intersection](../collections/intersection.md) - Get common elements between sets
- [coll.union](../collections/union.md) - Combine sets
