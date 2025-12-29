# map.removeKey

## Description
Creates a new map with a single specified key removed. The original map is not modified.

## Syntax
```cypher
flex.map.removeKey(map, key)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `map` | map | Yes | The map to remove the key from |
| `key` | string | Yes | The key to remove |

## Returns
**Type:** map (object)

A new map containing all properties from the input map except the specified key. Returns an empty map if input is not a valid object.

## Examples

### Example 1: Basic Key Removal
```cypher
WITH {name: 'Alice', age: 30, email: 'alice@example.com'} AS user
RETURN flex.map.removeKey(user, 'email') AS sanitized
```

**Output:**
```
sanitized
-----------------------
{name: 'Alice', age: 30}
```

### Example 2: Removing Sensitive Data
```cypher
MATCH (u:User)
WITH properties(u) AS userProps
RETURN u.id, flex.map.removeKey(userProps, 'password') AS safeProps
```

### Example 3: Cleaning Response Data
```cypher
MATCH (p:Product {id: 123})
WITH properties(p) AS props
WITH flex.map.removeKey(props, 'internalId') AS cleaned
RETURN cleaned AS product
```

### Example 4: Removing Non-Existent Key
```cypher
WITH {a: 1, b: 2} AS map
RETURN flex.map.removeKey(map, 'c') AS result
```

**Output:**
```
result
---------
{a: 1, b: 2}
```
(Key doesn't exist, so map is returned unchanged)

## Notes
- Returns empty map if input is not a valid object or is `null`
- If key is `null`, returns a shallow copy of the map
- If the key doesn't exist, returns a copy with all original properties
- Creates a new map; does not modify the original
- Useful for sanitizing data, removing sensitive fields, or filtering properties

## See Also
- [map.removeKeys](./removeKeys.md) - Remove multiple keys at once
- [map.submap](./submap.md) - Keep only specific keys (inverse operation)
- [map.merge](./merge.md) - Combine multiple maps
