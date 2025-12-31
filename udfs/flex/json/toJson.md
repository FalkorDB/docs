# json.toJson

## Description
Serializes a value to a JSON string. Handles various data types including objects, arrays, strings, numbers, booleans, and `null`.

## Syntax
```cypher
flex.json.toJson(value)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `value` | any | Yes | The value to serialize to JSON |

## Returns
**Type:** string

A JSON string representation of the value. Returns `null` if serialization fails or if the input is `undefined`.

## Examples

### Example 1: Serialize a Map
```cypher
WITH {name: 'Alice', age: 30, active: true} AS user
RETURN flex.json.toJson(user) AS json
```

**Output:**
```
json
---------------------------------------
'{"name":"Alice","age":30,"active":true}'
```

### Example 2: Serialize a List
```cypher
WITH [1, 2, 3, 4, 5] AS numbers
RETURN flex.json.toJson(numbers) AS json
```

**Output:**
```
json
-----------
'[1,2,3,4,5]'
```

### Example 3: Preparing Data for Export
```cypher
MATCH (p:Product)
WITH collect({id: p.id, name: p.name, price: p.price}) AS products
RETURN flex.json.toJson(products) AS jsonExport
```

### Example 4: Storing JSON in Properties
```cypher
MATCH (u:User {id: 123})
WITH u, {lastLogin: u.lastLogin, preferences: u.preferences} AS metadata
SET u.metadataJson = flex.json.toJson(metadata)
```

## Notes
- Returns `null` if serialization fails (e.g., circular references)
- `undefined` values are normalized to `null`
- Dates are serialized in ISO format
- Functions and symbols cannot be serialized and will cause `null` return
- Useful for API responses, data export, or storing complex structures

## See Also
- [json.fromJsonMap](./fromJsonMap.md) - Parse JSON string to map
- [json.fromJsonList](./fromJsonList.md) - Parse JSON string to list
