# text.levenshtein

## Description
Computes the Levenshtein edit distance between two strings. The edit distance is the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one string into another. This is useful for fuzzy string matching, spell checking, and finding similar records.

## Syntax
```cypher
flex.text.levenshtein(string1, string2)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string1` | string | Yes | The first string to compare |
| `string2` | string | Yes | The second string to compare |

## Returns
**Type:** number (integer)

The minimum number of single-character edits needed to transform `string1` into `string2`. Returns `0` if the strings are identical.

## Examples

### Example 1: Basic String Comparison
```cypher
// Compare two similar strings
RETURN flex.text.levenshtein('kitten', 'sitting') AS distance
```

**Output:**
```
distance
--------
3
```

### Example 2: Finding Similar User Names
```cypher
// Find users with names similar to "Sarah" within edit distance of 2
MATCH (u:User)
WHERE flex.text.levenshtein(u.name, 'Sarah') <= 2
RETURN u.name, u.email, flex.text.levenshtein(u.name, 'Sarah') AS distance
ORDER BY distance
```

### Example 3: Fuzzy Matching with Multiple Candidates
```cypher
// Find the closest matching product name
WITH 'iPhone' AS search_term
MATCH (p:Product)
WITH p, flex.text.levenshtein(p.name, search_term) AS distance
WHERE distance <= 3
RETURN p.name, distance
ORDER BY distance
LIMIT 5
```

## Notes
- Handles `null` values gracefully by treating them as empty strings
- The function is symmetric: `levenshtein(a, b) = levenshtein(b, a)`
- Empty strings return the length of the non-empty string as distance
- Two `null` values return distance of `0`
- Optimized for performance with memory-efficient implementation
- Case-sensitive comparison (use `toLower()` if case-insensitive matching is needed)

## See Also
- [sim.jaccard](../similarity/jaccard.md) - Set-based similarity for collections
- [text.jaroWinkler](./jaroWinkler.md) - Alternative string similarity metric
