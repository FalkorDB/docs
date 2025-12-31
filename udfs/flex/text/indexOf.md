# text.indexOf

## Description
Finds the first occurrence of a substring within a string, optionally starting from a specific offset and ending at a specific position.

## Syntax
```cypher
flex.text.indexOf(string, substring, offset, to)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string | Yes | The string to search in |
| `substring` | string | Yes | The substring to search for |
| `offset` | number | No | Starting position for search (default: 0) |
| `to` | number | No | Ending position for search (default: -1, meaning end of string) |

## Returns
**Type:** number (integer)

The zero-based index of the first occurrence of the substring, or `-1` if not found. Returns `null` if the input string is `null`.

## Examples

### Example 1: Basic Search
```cypher
RETURN flex.text.indexOf('hello world', 'world') AS position
```

**Output:**
```
position
--------
6
```

### Example 2: Search with Offset
```cypher
RETURN flex.text.indexOf('hello hello', 'hello', 3) AS position
```

**Output:**
```
position
--------
6
```
(Finds the second "hello" starting from position 3)

### Example 3: Filtering Nodes by Substring Position
```cypher
MATCH (p:Product)
WHERE flex.text.indexOf(p.description, 'premium') >= 0
RETURN p.name, p.description
```

## Notes
- Returns `null` if input string is `null`
- Returns `-1` if substring is not found
- Uses zero-based indexing
- The `offset` parameter allows starting search from a specific position
- The `to` parameter limits search to a specific range

## See Also
- [text.indexesOf](./indexesOf.md) - Find all occurrences of a substring
- [text.replace](./replace.md) - Replace substring occurrences
