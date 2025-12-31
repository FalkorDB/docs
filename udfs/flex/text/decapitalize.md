# text.decapitalize

## Description
Converts the first character of a string to lowercase while leaving the rest of the string unchanged.

## Syntax
```cypher
flex.text.decapitalize(string)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string | Yes | The string to decapitalize |

## Returns
**Type:** string

The input string with its first character converted to lowercase. Returns `null` if the input is `null`, and empty string if input is empty.

## Examples

### Example 1: Basic Usage
```cypher
RETURN flex.text.decapitalize('Hello World') AS result
```

**Output:**
```
result
-------------
hello World
```

### Example 2: Processing Field Names
```cypher
WITH ['FirstName', 'LastName', 'Email'] AS fields
UNWIND fields AS field
RETURN flex.text.decapitalize(field) AS jsonKey
```

## Notes
- Returns `null` for `null` input
- Returns empty string for empty string input
- Only affects the first character
- Does not change the case of subsequent characters

## See Also
- [text.capitalize](./capitalize.md) - Uppercase the first character
- [text.camelCase](./camelCase.md) - Convert to camelCase format
