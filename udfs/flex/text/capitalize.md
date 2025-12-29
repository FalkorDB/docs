# text.capitalize

## Description
Capitalizes the first character of a string, converting it to uppercase while leaving the rest of the string unchanged.

## Syntax
```cypher
flex.text.capitalize(string)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string | Yes | The string to capitalize |

## Returns
**Type:** string

The input string with its first character converted to uppercase. Returns `null` if the input is `null`, and empty string if input is empty.

## Examples

### Example 1: Basic Usage
```cypher
RETURN flex.text.capitalize('hello world') AS result
```

**Output:**
```
result
-------------
Hello world
```

### Example 2: Capitalizing Node Properties
```cypher
MATCH (p:Person)
RETURN p.id, flex.text.capitalize(p.name) AS capitalizedName
```

## Notes
- Returns `null` for `null` input
- Returns empty string for empty string input
- Only affects the first character
- Does not change the case of subsequent characters

## See Also
- [text.decapitalize](./decapitalize.md) - Lowercase the first character
- [text.camelCase](./camelCase.md) - Convert to camelCase format
- [text.upperCamelCase](./upperCamelCase.md) - Convert to UpperCamelCase format
