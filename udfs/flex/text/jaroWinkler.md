# text.jaroWinkler

## Description
Computes the Jaro-Winkler similarity between two strings. This metric is particularly effective for short strings like names and addresses. It gives more favorable ratings to strings that match from the beginning. Returns a value between 0 (no similarity) and 1 (exact match).

## Syntax
```cypher
flex.text.jaroWinkler(string1, string2)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string1` | string | Yes | The first string to compare |
| `string2` | string | Yes | The second string to compare |

## Returns
**Type:** number (float)

A similarity score between 0 and 1:
- `1.0` indicates an exact match
- `0.0` indicates no similarity
- Higher values indicate greater similarity

## Examples

### Example 1: Name Matching
```cypher
// Compare similar names
RETURN flex.text.jaroWinkler('Martha', 'Marhta') AS similarity
```

**Output:**
```
similarity
----------
0.961
```

### Example 2: Fuzzy Name Search
```cypher
// Find people with names similar to "William"
MATCH (p:Person)
WHERE flex.text.jaroWinkler(p.firstName, 'William') > 0.85
RETURN p.firstName, p.lastName, flex.text.jaroWinkler(p.firstName, 'William') AS score
ORDER BY score DESC
```

### Example 3: Deduplication by Company Name
```cypher
// Find potential duplicate company records
MATCH (c1:Company)
MATCH (c2:Company)
WHERE id(c1) < id(c2)
WITH c1, c2, flex.text.jaroWinkler(c1.name, c2.name) AS similarity
WHERE similarity > 0.9
RETURN c1.name, c2.name, similarity
ORDER BY similarity DESC
```

## Notes
- Particularly effective for short strings (names, addresses)
- Gives higher weight to strings that match from the beginning
- Handles `null` values by returning appropriate default values
- Case-sensitive comparison
- More forgiving than exact match but stricter than pure Jaro similarity
- Commonly used in record linkage and deduplication tasks

## See Also
- [text.levenshtein](./levenshtein.md) - Edit distance metric for string comparison
- [sim.jaccard](../similarity/jaccard.md) - Set-based similarity
