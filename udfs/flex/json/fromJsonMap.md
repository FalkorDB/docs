# json.fromJsonMap

## Description
Parses a JSON string and returns it as a map (object). Safely handles malformed JSON by returning an empty map on parse errors.

## Syntax
```cypher
flex.json.fromJsonMap(jsonString)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jsonString` | string | Yes | A JSON string representing an object |

## Returns
**Type:** map (object)

A map parsed from the JSON string. Returns an empty map `{}` if parsing fails or if the input is not a valid JSON object.

## Examples

### Example 1: Basic JSON Parsing
```cypher
WITH '{"name":"Alice","age":30,"active":true}' AS json
RETURN flex.json.fromJsonMap(json) AS user
```

**Output:**
```
user
-------------------------------
{name: 'Alice', age: 30, active: true}
```

### Example 2: Parsing Stored JSON Properties
```cypher
MATCH (n:Node)
WHERE n.jsonData IS NOT NULL
WITH n, flex.json.fromJsonMap(n.jsonData) AS parsed
RETURN n.id, parsed.field1, parsed.field2
```

### Example 3: Processing API Responses
```cypher
WITH '{"id":123,"email":"user@example.com","role":"admin"}' AS apiResponse
WITH flex.json.fromJsonMap(apiResponse) AS data
CREATE (u:User {id: data.id, email: data.email, role: data.role})
```

### Example 4: Handling Malformed JSON
```cypher
WITH '{invalid json}' AS badJson
RETURN flex.json.fromJsonMap(badJson) AS result
```

**Output:**
```
result
------
{}
```
(Returns empty map for invalid JSON)

## Notes
- Returns empty map `{}` if input is not valid JSON
- Returns empty map if the JSON represents a non-object value (e.g., array, string)
- Safe to use without error handling as it won't throw exceptions
- Useful for parsing configuration, API responses, or stored JSON data

## See Also
- [json.fromJsonList](./fromJsonList.md) - Parse JSON string to list
- [json.toJson](./toJson.md) - Serialize value to JSON string
