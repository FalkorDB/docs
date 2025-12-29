# text.format

## Description
Formats a string by replacing numbered placeholders `{0}`, `{1}`, `{2}`, etc. with corresponding values from a parameters array. Similar to sprintf-style formatting.

## Syntax
```cypher
flex.text.format(template, parameters)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `template` | string | Yes | The format string containing `{0}`, `{1}`, etc. placeholders |
| `parameters` | list | Yes | Array of values to substitute into the template |

## Returns
**Type:** string

The formatted string with placeholders replaced by parameter values. Returns `null` if template is `null`.

## Examples

### Example 1: Basic String Formatting
```cypher
RETURN flex.text.format('Hello {0}, you are {1} years old!', ['Alice', 30]) AS result
```

**Output:**
```
result
--------------------------------
Hello Alice, you are 30 years old!
```

### Example 2: Dynamic Query Messages
```cypher
MATCH (u:User {id: 123})
WITH u, flex.text.format('User {0} ({1}) logged in at {2}', [u.name, u.email, u.lastLogin]) AS message
RETURN message
```

### Example 3: Building URLs or Paths
```cypher
WITH ['users', 'profile', '12345'] AS parts
RETURN flex.text.format('/{0}/{1}/{2}', parts) AS path
```

**Output:**
```
path
------------------------
/users/profile/12345
```

## Notes
- Returns `null` if template is `null`
- Placeholders are zero-indexed: `{0}`, `{1}`, `{2}`, etc.
- Same placeholder can be used multiple times in template
- Parameters are replaced in order of array index
- Useful for building dynamic messages, logs, or formatted output

## See Also
- [text.replace](./replace.md) - Replace text using regex patterns
- [text.join](./join.md) - Join array elements with delimiter
