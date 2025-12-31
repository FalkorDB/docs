# json.fromJsonList

## Description
Parses a JSON string and returns it as a list (array). Safely handles malformed JSON by returning an empty list on parse errors.

## Syntax
```cypher
flex.json.fromJsonList(jsonString)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jsonString` | string | Yes | A JSON string representing an array |

## Returns
**Type:** list

A list parsed from the JSON string. Returns an empty list `[]` if parsing fails or if the input is not a valid JSON array.

## Examples

### Example 1: Basic JSON Array Parsing
```cypher
WITH '[1, 2, 3, 4, 5]' AS json
RETURN flex.json.fromJsonList(json) AS numbers
```

**Output:**
```
numbers
-----------
[1, 2, 3, 4, 5]
```

### Example 2: Parsing Complex Arrays
```cypher
WITH '[{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]' AS json
WITH flex.json.fromJsonList(json) AS users
UNWIND users AS user
RETURN user.id, user.name
```

### Example 3: Processing Stored List Data
```cypher
MATCH (p:Product)
WHERE p.tagsJson IS NOT NULL
WITH p, flex.json.fromJsonList(p.tagsJson) AS tags
UNWIND tags AS tag
RETURN p.name, tag
```

### Example 4: Handling Malformed JSON
```cypher
WITH '[invalid, json]' AS badJson
RETURN flex.json.fromJsonList(badJson) AS result
```

**Output:**
```
result
------
[]
```
(Returns empty list for invalid JSON)

## Notes
- Returns empty list `[]` if input is not valid JSON
- Returns empty list if the JSON represents a non-array value (e.g., object, string)
- Safe to use without error handling as it won't throw exceptions
- Useful for parsing list data, batch imports, or stored JSON arrays

## See Also
- [json.fromJsonMap](./fromJsonMap.md) - Parse JSON string to map
- [json.toJson](./toJson.md) - Serialize value to JSON string
