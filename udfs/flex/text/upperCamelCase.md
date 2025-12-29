# text.upperCamelCase

## Description
Converts a string to UpperCamelCase (also known as PascalCase) format by removing non-alphanumeric characters and capitalizing the first letter of each word including the first.

## Syntax
```cypher
flex.text.upperCamelCase(string)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string | Yes | The string to convert to UpperCamelCase |

## Returns
**Type:** string

The input string converted to UpperCamelCase format. Returns `null` if input is `null`.

## Examples

### Example 1: Basic Usage
```cypher
RETURN flex.text.upperCamelCase('hello world') AS result
```

**Output:**
```
result
----------
HelloWorld
```

### Example 2: Converting Class Names
```cypher
RETURN flex.text.upperCamelCase('user_account') AS result
```

**Output:**
```
result
-----------
UserAccount
```

### Example 3: Normalizing Entity Names
```cypher
MATCH (e:Entity)
RETURN e.rawName, flex.text.upperCamelCase(e.rawName) AS className
```

## Notes
- Returns `null` for `null` input
- Removes all non-alphanumeric characters
- First character is always uppercase (unlike camelCase)
- Also known as PascalCase
- Useful for class names, type names, and entity naming conventions

## See Also
- [text.camelCase](./camelCase.md) - Convert to camelCase (first letter lowercase)
- [text.snakeCase](./snakeCase.md) - Convert to snake_case format
- [text.capitalize](./capitalize.md) - Capitalize first character only
