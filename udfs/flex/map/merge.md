# map.merge

## Description
Performs a shallow merge of multiple maps into a new map. When keys conflict, values from later maps override earlier ones. Non-object inputs are ignored.

## Syntax
```cypher
flex.map.merge(map1, map2, ...)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `map1` | map | No | First map to merge |
| `map2` | map | No | Second map to merge |
| `...` | map | No | Additional maps to merge |

## Returns
**Type:** map (object)

A new map containing all keys and values from the input maps. Later maps override earlier ones for duplicate keys.

## Examples

### Example 1: Basic Merge
```cypher
WITH {a: 1, b: 2} AS map1, {b: 3, c: 4} AS map2
RETURN flex.map.merge(map1, map2) AS result
```

**Output:**
```
result
------------------
{a: 1, b: 3, c: 4}
```
(Note: `b` from map2 overrides `b` from map1)

### Example 2: Merging Node Properties
```cypher
MATCH (u:User {id: 123})
WITH {role: 'admin', status: 'active'} AS defaults
RETURN flex.map.merge(defaults, properties(u)) AS userWithDefaults
```

### Example 3: Combining Configuration
```cypher
WITH {host: 'localhost', port: 6379} AS defaults,
     {port: 7000, password: 'secret'} AS config
RETURN flex.map.merge(defaults, config) AS finalConfig
```

**Output:**
```
finalConfig
--------------------------------------------------
{host: 'localhost', port: 7000, password: 'secret'}
```

### Example 4: Merging Multiple Maps
```cypher
WITH {a: 1} AS base, {b: 2} AS extra1, {c: 3} AS extra2
RETURN flex.map.merge(base, extra1, extra2) AS combined
```

## Notes
- Non-object inputs are silently ignored
- Performs shallow merge (nested objects are not deeply merged)
- Later maps take precedence for duplicate keys
- Returns a new map; does not modify input maps
- Useful for applying defaults, combining configuration, or merging properties

## See Also
- [map.submap](./submap.md) - Extract specific keys from a map
- [map.removeKeys](./removeKeys.md) - Remove keys from a map
