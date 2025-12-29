# text.repeat

## Description
Repeats a string a specified number of times.

## Syntax
```cypher
flex.text.repeat(string, count)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string | Yes | The string to repeat |
| `count` | number | Yes | The number of times to repeat the string |

## Returns
**Type:** string

A new string consisting of the input string repeated the specified number of times. Returns `null` if input is `null`.

## Examples

### Example 1: Basic Repetition
```cypher
RETURN flex.text.repeat('Ha', 3) AS result
```

**Output:**
```
result
------
HaHaHa
```

### Example 2: Creating Separators
```cypher
RETURN flex.text.repeat('-', 40) AS separator
```

**Output:**
```
separator
----------------------------------------
----------------------------------------
```

### Example 3: Building Star Ratings
```cypher
MATCH (r:Review)
RETURN r.product, flex.text.repeat('★', r.rating) AS stars
```

**Output:**
```
product     | stars
------------|-------
Laptop      | ★★★★★
Mouse       | ★★★★
Keyboard    | ★★★
```

### Example 4: Indentation
```cypher
WITH 2 AS level
RETURN flex.text.repeat('  ', level) + 'Nested Item' AS indented
```

**Output:**
```
indented
----------------
    Nested Item
```

## Notes
- Returns `null` if input is `null`
- Count must be a non-negative integer
- Useful for creating visual elements, separators, or formatting
- Can be combined with other text functions for complex formatting

## See Also
- [text.lpad](./lpad.md) - Pad the start of a string
- [text.rpad](./rpad.md) - Pad the end of a string
- [text.format](./format.md) - Format strings with placeholders
