# text.regexGroups

## Description
Extracts all matches and capture groups from a string using a regular expression pattern. Returns a nested array where each match contains the full match and any captured groups.

## Syntax
```cypher
flex.text.regexGroups(string, regex)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string | Yes | The string to search in |
| `regex` | string | Yes | The regular expression pattern (applied globally) |

## Returns
**Type:** list of lists

A nested array where each inner array represents one match and contains the full match followed by any capture groups. Returns `null` if input string is `null`.

## Examples

### Example 1: Extract Email Components
```cypher
WITH 'Contact: john@example.com or jane@test.org' AS text
RETURN flex.text.regexGroups(text, '(\\w+)@(\\w+\\.\\w+)') AS matches
```

**Output:**
```
matches
----------------------------------------------------
[["john@example.com", "john", "example.com"], 
 ["jane@test.org", "jane", "test.org"]]
```

### Example 2: Parse Date Components
```cypher
WITH '2024-01-15 and 2024-12-25' AS dates
RETURN flex.text.regexGroups(dates, '(\\d{4})-(\\d{2})-(\\d{2})') AS parsed
```

**Output:**
```
parsed
-------------------------------------------------
[["2024-01-15", "2024", "01", "15"],
 ["2024-12-25", "2024", "12", "25"]]
```

### Example 3: Extract URLs and Protocol
```cypher
MATCH (d:Document)
WITH d, flex.text.regexGroups(d.content, '(https?)://([\\w.]+)') AS urls
WHERE size(urls) > 0
RETURN d.title, urls
```

## Notes
- Returns `null` if input string is `null`
- The regex is applied globally (finds all matches)
- Each match array contains: [fullMatch, group1, group2, ...]
- Useful for parsing structured text, extracting data patterns
- More powerful than simple string search for complex patterns

## See Also
- [text.replace](./replace.md) - Replace text using regex
- [text.indexOf](./indexOf.md) - Find simple substring position
- [text.indexesOf](./indexesOf.md) - Find all substring positions
