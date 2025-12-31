# map.submap

## Description
Creates a new map containing only the specified keys from the input map. This is the inverse of `removeKeys`.

## Syntax
```cypher
flex.map.submap(map, keys)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `map` | map | Yes | The source map to extract keys from |
| `keys` | list | Yes | An array of key names to include in the result |

## Returns
**Type:** map (object)

A new map containing only the specified keys and their values from the input map. Returns an empty map if input is not a valid object or keys is not an array.

## Examples

### Example 1: Basic Submap Extraction
```cypher
WITH {name: 'Alice', age: 30, email: 'alice@example.com', city: 'NYC'} AS user
RETURN flex.map.submap(user, ['name', 'email']) AS contact
```

**Output:**
```
contact
---------------------------------
{name: 'Alice', email: 'alice@example.com'}
```

### Example 2: Selecting Specific Node Properties
```cypher
MATCH (p:Product)
RETURN flex.map.submap(properties(p), ['id', 'name', 'price']) AS summary
```

### Example 3: Building API Response with Selected Fields
```cypher
MATCH (u:User {id: $userId})
WITH properties(u) AS allProps
RETURN flex.map.submap(allProps, ['id', 'name', 'email', 'role']) AS userInfo
```

### Example 4: Handling Non-Existent Keys
```cypher
WITH {a: 1, b: 2} AS map
RETURN flex.map.submap(map, ['a', 'c', 'd']) AS result
```

**Output:**
```
result
------
{a: 1}
```
(Only existing keys are included)

### Example 5: Dynamic Field Selection
```cypher
WITH ['name', 'price', 'category'] AS requestedFields
MATCH (p:Product {id: 123})
RETURN flex.map.submap(properties(p), requestedFields) AS response
```

## Notes
- Returns empty map if input is not a valid object or keys is not an array
- `null` values in the keys array are ignored
- Non-existent keys are silently skipped
- Creates a new map; does not modify the original
- Useful for selecting specific fields, building API responses, or data projection
- More efficient than manually picking each field

## See Also
- [map.removeKeys](./removeKeys.md) - Remove specific keys (inverse operation)
- [map.removeKey](./removeKey.md) - Remove a single key
- [map.merge](./merge.md) - Combine multiple maps
