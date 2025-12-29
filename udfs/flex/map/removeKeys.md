# map.removeKeys

## Description
Creates a new map with multiple specified keys removed. The original map is not modified.

## Syntax
```cypher
flex.map.removeKeys(map, keys)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `map` | map | Yes | The map to remove keys from |
| `keys` | list | Yes | An array of key names to remove |

## Returns
**Type:** map (object)

A new map containing all properties from the input map except the specified keys. Returns an empty map if input is not a valid object.

## Examples

### Example 1: Basic Multiple Key Removal
```cypher
WITH {name: 'Alice', age: 30, email: 'alice@example.com', password: 'secret'} AS user
RETURN flex.map.removeKeys(user, ['password', 'email']) AS sanitized
```

**Output:**
```
sanitized
-----------------------
{name: 'Alice', age: 30}
```

### Example 2: Removing Internal Fields
```cypher
MATCH (p:Product)
WITH properties(p) AS props
RETURN flex.map.removeKeys(props, ['internalId', 'createdBy', 'updatedAt']) AS public
```

### Example 3: Filtering Node Properties for API Response
```cypher
MATCH (u:User {id: $userId})
WITH properties(u) AS allProps
WITH flex.map.removeKeys(allProps, ['password', 'salt', 'resetToken']) AS safeProps
RETURN safeProps AS user
```

### Example 4: Removing Non-Existent Keys
```cypher
WITH {a: 1, b: 2, c: 3} AS map
RETURN flex.map.removeKeys(map, ['d', 'e']) AS result
```

**Output:**
```
result
-----------------
{a: 1, b: 2, c: 3}
```
(Non-existent keys are ignored)

## Notes
- Returns empty map if input is not a valid object or is `null`
- `null` values in the keys array are ignored
- Keys that don't exist in the map are silently ignored
- Creates a new map; does not modify the original
- More efficient than calling `removeKey` multiple times
- Useful for bulk removal of sensitive or internal fields

## See Also
- [map.removeKey](./removeKey.md) - Remove a single key
- [map.submap](./submap.md) - Keep only specific keys (inverse operation)
- [map.merge](./merge.md) - Combine multiple maps
