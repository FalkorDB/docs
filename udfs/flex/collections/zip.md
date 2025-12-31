# coll.zip

## Description
Combines two lists element-by-element into a list of pairs. Each pair contains one element from the first list and the corresponding element from the second list. The resulting list has the length of the shorter input list.

## Syntax
```cypher
flex.coll.zip(list1, list2)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `list1` | list | Yes | The first list |
| `list2` | list | Yes | The second list |

## Returns
**Type:** list of lists

A list where each element is a two-element array `[item1, item2]` combining corresponding elements from both lists. Returns an empty list if either input is not an array.

## Examples

### Example 1: Basic Zipping
```cypher
WITH ['a', 'b', 'c'] AS letters, [1, 2, 3] AS numbers
RETURN flex.coll.zip(letters, numbers) AS pairs
```

**Output:**
```
pairs
----------------------------
[["a", 1], ["b", 2], ["c", 3]]
```

### Example 2: Different Length Lists
```cypher
WITH ['x', 'y', 'z'] AS keys, [10, 20] AS values
RETURN flex.coll.zip(keys, values) AS result
```

**Output:**
```
result
--------------------
[["x", 10], ["y", 20]]
```
(Only pairs up to the length of the shorter list)

### Example 3: Creating Key-Value Pairs
```cypher
MATCH (p:Product)
WITH collect(p.name) AS names, collect(p.price) AS prices
RETURN flex.coll.zip(names, prices) AS productData
```

### Example 4: Pairing Related Data
```cypher
WITH ['Mon', 'Tue', 'Wed'] AS days, [120, 135, 98] AS sales
UNWIND flex.coll.zip(days, sales) AS pair
RETURN pair[0] AS day, pair[1] AS salesAmount
```

## Notes
- Returns empty list if either input is not an array or is `null`
- Result length is limited by the shorter of the two input lists
- Excess elements from the longer list are ignored
- Useful for pairing related data or creating key-value associations

## See Also
- [map.fromPairs](../map/fromPairs.md) - Convert pairs to a map
- [coll.union](./union.md) - Combine lists as sets
