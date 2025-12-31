# text.snakeCase

## Description
Converts a string to snake_case format by separating words with underscores and converting all characters to lowercase.

## Syntax
```cypher
flex.text.snakeCase(string)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string | Yes | The string to convert to snake_case |

## Returns
**Type:** string

The input string converted to snake_case format. Returns the original string if no matches are found. Returns `null` if input is `null`.

## Examples

### Example 1: Basic Usage
```cypher
RETURN flex.text.snakeCase('HelloWorld') AS result
```

**Output:**
```
result
-----------
hello_world
```

### Example 2: Converting Multiple Formats
```cypher
WITH ['camelCase', 'PascalCase', 'kebab-case', 'space separated'] AS inputs
UNWIND inputs AS input
RETURN input AS original, flex.text.snakeCase(input) AS snake
```

**Output:**
```
original        | snake
----------------|------------------
camelCase       | camel_case
PascalCase      | pascal_case
kebab-case      | kebab_case
space separated | space_separated
```

### Example 3: Database Column Naming
```cypher
MATCH (u:User)
WITH u, keys(u) AS properties
UNWIND properties AS prop
RETURN prop AS camelCase, flex.text.snakeCase(prop) AS dbColumn
```

## Notes
- Returns `null` for `null` input
- Handles multiple word boundary detection patterns
- All characters are converted to lowercase
- Words are separated by underscores
- Common for database column names and Python conventions
- Returns the original string if no word boundaries are detected

## See Also
- [text.camelCase](./camelCase.md) - Convert to camelCase format
- [text.upperCamelCase](./upperCamelCase.md) - Convert to UpperCamelCase format
