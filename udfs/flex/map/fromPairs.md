# map.fromPairs

## Description
Converts a list of key-value pairs into a map. Each pair should be a two-element array `[key, value]`.

## Syntax
```cypher
flex.map.fromPairs(pairs)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `pairs` | list | Yes | A list of two-element arrays, each containing `[key, value]` |

## Returns
**Type:** map (object)

A map where each key-value pair from the input list becomes a property. Returns an empty map if input is not an array.

## Examples

### Example 1: Basic Conversion
```cypher
WITH [['name', 'Alice'], ['age', 30], ['city', 'NYC']] AS pairs
RETURN flex.map.fromPairs(pairs) AS result
```

**Output:**
```
result
------------------------------------
{name: 'Alice', age: 30, city: 'NYC'}
```

### Example 2: Converting Zipped Data
```cypher
WITH ['name', 'age', 'email'] AS keys,
     ['Bob', 25, 'bob@example.com'] AS values
WITH flex.coll.zip(keys, values) AS pairs
RETURN flex.map.fromPairs(pairs) AS user
```

**Output:**
```
user
------------------------------------------
{name: 'Bob', age: 25, email: 'bob@example.com'}
```

### Example 3: Dynamic Property Creation
```cypher
MATCH (p:Product)
WITH collect([p.id, p.price]) AS pricePairs
RETURN flex.map.fromPairs(pricePairs) AS priceMap
```

### Example 4: Converting Query Results to Lookup Map
```cypher
MATCH (c:Country)
WITH collect([c.code, c.name]) AS countryPairs
WITH flex.map.fromPairs(countryPairs) AS lookup
RETURN lookup['US'] AS usaName, lookup['UK'] AS ukName
```

## Notes
- Returns empty map if input is not an array or is `null`
- Each pair must be a two-element array; invalid pairs are skipped
- If a key is `null` or `undefined`, the pair is ignored
- Duplicate keys result in the last value being used
- Keys are converted to strings as map property names

## See Also
- [coll.zip](../collections/zip.md) - Create pairs from two lists
- [map.submap](./submap.md) - Extract subset of keys from a map
