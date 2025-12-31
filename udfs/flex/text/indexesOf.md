# text.indexesOf

## Description
Finds all occurrences of a substring within a string, returning an array of all matching positions. Optionally search within a specific range.

## Syntax
```cypher
flex.text.indexesOf(string, substring, from, to)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string | Yes | The string to search in |
| `substring` | string | Yes | The substring to search for |
| `from` | number | No | Starting position for search (default: 0) |
| `to` | number | No | Ending position for search (default: -1, meaning end of string) |

## Returns
**Type:** list of numbers

An array containing the zero-based indices of all occurrences of the substring. Returns an empty array if no matches are found. Returns `null` if the input string is `null`.

## Examples

### Example 1: Find All Occurrences
```cypher
RETURN flex.text.indexesOf('hello hello hello', 'hello') AS positions
```

**Output:**
```
positions
-----------
[0, 6, 12]
```

### Example 2: Find Occurrences in Range
```cypher
RETURN flex.text.indexesOf('abcabcabc', 'abc', 1, 9) AS positions
```

**Output:**
```
positions
---------
[3, 6]
```
(Skips first 'abc' at position 0, finds those within range)

### Example 3: Count Keyword Occurrences
```cypher
MATCH (d:Document)
WITH d, flex.text.indexesOf(d.content, 'important') AS occurrences
WHERE size(occurrences) > 2
RETURN d.title, size(occurrences) AS importanceScore
ORDER BY importanceScore DESC
```

## Notes
- Returns `null` if input string is `null`
- Returns empty array if substring is not found
- Uses zero-based indexing
- The `from` parameter allows starting search from a specific position
- The `to` parameter limits search to a specific range
- Useful for counting occurrences or analyzing text patterns

## See Also
- [text.indexOf](./indexOf.md) - Find first occurrence only
- [text.replace](./replace.md) - Replace substring occurrences
- [text.regexGroups](./regexGroups.md) - Find matches using regex patterns
