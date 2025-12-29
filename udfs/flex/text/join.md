# text.join

## Description
Joins an array of strings into a single string using a specified delimiter.

## Syntax
```cypher
flex.text.join(array, delimiter)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `array` | list | Yes | The array of strings to join |
| `delimiter` | string | Yes | The separator to insert between elements |

## Returns
**Type:** string

A single string with all array elements concatenated, separated by the delimiter. Returns `null` if the array is `null` or undefined.

## Examples

### Example 1: Basic String Joining
```cypher
RETURN flex.text.join(['apple', 'banana', 'cherry'], ', ') AS result
```

**Output:**
```
result
----------------------
apple, banana, cherry
```

### Example 2: Building CSV Lines
```cypher
MATCH (u:User)
WITH [u.id, u.name, u.email] AS fields
RETURN flex.text.join(fields, ',') AS csvLine
```

### Example 3: Creating Tags String
```cypher
MATCH (p:Post)
RETURN p.title, flex.text.join(p.tags, ' #') AS hashtags
```

**Output:**
```
title           | hashtags
----------------|------------------
My First Post   | tech #coding #js
```

### Example 4: Building Paths
```cypher
WITH ['home', 'user', 'documents', 'file.txt'] AS parts
RETURN flex.text.join(parts, '/') AS path
```

**Output:**
```
path
--------------------------
home/user/documents/file.txt
```

## Notes
- Returns `null` if input array is `null`
- Empty strings in the array are included in the output
- Delimiter can be any string, including empty string
- Commonly used for CSV generation, path building, or tag formatting

## See Also
- [text.format](./format.md) - Format strings with placeholders
- [coll.zip](../collections/zip.md) - Combine two lists
