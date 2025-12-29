# coll.intersection

## Description
Finds the common elements between two lists, returning a new list containing only the elements that appear in both input lists.

## Syntax
```cypher
flex.coll.intersection(list1, list2)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `list1` | list | Yes | The first list |
| `list2` | list | Yes | The second list |

## Returns
**Type:** list

A new list containing only the elements that exist in both input lists. Preserves the order from the first list.

## Examples

### Example 1: Basic Intersection
```cypher
WITH [1, 2, 3, 4] AS a, [3, 4, 5, 6] AS b
RETURN flex.coll.intersection(a, b) AS result
```

**Output:**
```
result
-------
[3, 4]
```

### Example 2: Finding Common Tags
```cypher
MATCH (d1:Document {id: 'doc1'})
MATCH (d2:Document {id: 'doc2'})
WITH flex.coll.intersection(d1.tags, d2.tags) AS commonTags
WHERE size(commonTags) > 0
RETURN commonTags
```

### Example 3: Finding Users with Shared Interests
```cypher
MATCH (u1:User {id: $userId1})
MATCH (u2:User {id: $userId2})
WITH flex.coll.intersection(u1.interests, u2.interests) AS sharedInterests
RETURN u1.name, u2.name, sharedInterests, size(sharedInterests) AS commonCount
```

### Example 4: Filter by Allowed Values
```cypher
WITH ['admin', 'read', 'write', 'delete'] AS allowed
MATCH (u:User)
WITH u, flex.coll.intersection(u.permissions, allowed) AS validPerms
RETURN u.name, validPerms
```

## Notes
- Returns elements that exist in both lists
- Preserves the order from the first list
- If an element appears multiple times in list1, each occurrence is checked against list2
- Efficient implementation using Set for fast lookup
- Equivalent to mathematical set intersection operation

## See Also
- [coll.union](./union.md) - Combine all unique elements from both lists
- [sim.jaccard](../similarity/jaccard.md) - Calculate similarity coefficient using intersection
