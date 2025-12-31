# coll.frequencies

## Description
Counts the frequency of each element in a list, returning a map where keys are the unique elements and values are their occurrence counts.

## Syntax
```cypher
flex.coll.frequencies(list)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `list` | list | Yes | The list to analyze |

## Returns
**Type:** map (object)

A map where each key is a unique element from the list and each value is the count of how many times that element appears. Returns an empty map if input is not an array.

## Examples

### Example 1: Basic Frequency Count
```cypher
WITH ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple'] AS fruits
RETURN flex.coll.frequencies(fruits) AS counts
```

**Output:**
```
counts
---------------------------------------
{apple: 3, banana: 2, cherry: 1}
```

### Example 2: Tag Analysis
```cypher
MATCH (d:Document)
WITH collect(d.tags) AS allTagLists
UNWIND allTagLists AS tags
UNWIND tags AS tag
WITH collect(tag) AS flatTags
RETURN flex.coll.frequencies(flatTags) AS tagCounts
```

### Example 3: Finding Most Common Values
```cypher
MATCH (u:User)
WITH collect(u.country) AS countries
WITH flex.coll.frequencies(countries) AS freq
UNWIND keys(freq) AS country
RETURN country, freq[country] AS count
ORDER BY count DESC
LIMIT 10
```

### Example 4: Word Frequency Analysis
```cypher
MATCH (doc:Document)
WITH split(toLower(doc.content), ' ') AS words
WITH flex.coll.frequencies(words) AS wordCounts
UNWIND keys(wordCounts) AS word
WHERE wordCounts[word] > 5
RETURN word, wordCounts[word] AS frequency
ORDER BY frequency DESC
```

## Notes
- Returns empty map if input is not an array or is `null`
- `null` and `undefined` values are stored with key `"null"`
- All elements are converted to string keys in the result map
- Useful for analytics, statistics, and data exploration
- Can be combined with `keys()` and sorting for top-N analysis

## See Also
- [coll.union](./union.md) - Get unique elements (keys would give unique items)
- [coll.intersection](./intersection.md) - Find common elements
