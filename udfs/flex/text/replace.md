# text.replace

## Description
Replaces all occurrences of a substring matching a regular expression pattern with a replacement string.

## Syntax
```cypher
flex.text.replace(string, regex, replacement)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string | Yes | The string to perform replacements on |
| `regex` | string | Yes | The regular expression pattern to match (applied globally) |
| `replacement` | string | Yes | The string to replace matches with |

## Returns
**Type:** string

A new string with all pattern matches replaced by the replacement string. Returns `null` if input string is `null`.

## Examples

### Example 1: Basic Text Replacement
```cypher
RETURN flex.text.replace('hello world', 'world', 'universe') AS result
```

**Output:**
```
result
--------------
hello universe
```

### Example 2: Remove Non-Numeric Characters
```cypher
WITH 'Phone: (555) 123-4567' AS phone
RETURN flex.text.replace(phone, '[^0-9]', '') AS cleaned
```

**Output:**
```
cleaned
-----------
5551234567
```

### Example 3: Sanitize User Input
```cypher
MATCH (c:Comment)
WITH c, flex.text.replace(c.text, '<[^>]+>', '') AS sanitized
RETURN sanitized AS cleanComment
```

### Example 4: Normalize Whitespace
```cypher
WITH '  Multiple   spaces   here  ' AS text
RETURN flex.text.replace(text, '\\s+', ' ') AS normalized
```

**Output:**
```
normalized
-------------------------
 Multiple spaces here
```

## Notes
- Returns `null` if input string is `null`
- Uses global replacement (replaces all occurrences)
- Pattern is treated as a regular expression
- Useful for data cleaning, sanitization, and text transformation
- Can use regex patterns for complex replacements

## See Also
- [text.regexGroups](./regexGroups.md) - Extract matches with capture groups
- [text.indexOf](./indexOf.md) - Find substring position
- [text.format](./format.md) - Format strings with placeholders
