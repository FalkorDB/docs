# text.camelCase

## Description
Converts a string to camelCase format by removing non-alphanumeric characters and capitalizing the first letter of each word except the first.

## Syntax
```cypher
flex.text.camelCase(string)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string | Yes | The string to convert to camelCase |

## Returns
**Type:** string

The input string converted to camelCase format. Returns `null` if input is `null`.

## Examples

### Example 1: Basic Usage
```cypher
RETURN flex.text.camelCase('hello world') AS result
```

**Output:**
```
result
----------
helloWorld
```

### Example 2: Converting Field Names
```cypher
RETURN flex.text.camelCase('user_first_name') AS result
```

**Output:**
```
result
-------------
userFirstName
```

### Example 3: Normalizing Property Names
```cypher
WITH ['first-name', 'last_name', 'Email Address'] AS fields
UNWIND fields AS field
RETURN field AS original, flex.text.camelCase(field) AS camelCase
```

## Notes
- Returns `null` for `null` input
- Removes all non-alphanumeric characters
- First character is always lowercase
- Subsequent words start with uppercase
- Useful for normalizing field names to JavaScript/JSON conventions

## See Also
- [text.upperCamelCase](./upperCamelCase.md) - Convert to UpperCamelCase (PascalCase)
- [text.snakeCase](./snakeCase.md) - Convert to snake_case format
- [text.capitalize](./capitalize.md) - Capitalize first character only
