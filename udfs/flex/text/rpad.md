# text.rpad

## Description
Pads the end (right side) of a string with a specified character until it reaches the desired length.

## Syntax
```cypher
flex.text.rpad(string, length, padChar)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string/number | Yes | The string to pad (will be converted to string if number) |
| `length` | number | Yes | The target length after padding |
| `padChar` | string | No | The character to use for padding (default: space ' ') |

## Returns
**Type:** string

The padded string. If the original string is already longer than the target length, it is returned unchanged. Returns `null` if input is `null`.

## Examples

### Example 1: Basic Right Padding
```cypher
RETURN flex.text.rpad('test', 8, '-') AS result
```

**Output:**
```
result
----------
test----
```

### Example 2: Creating Fixed-Width Fields
```cypher
MATCH (p:Product)
RETURN flex.text.rpad(p.name, 20, ' ') AS productName, p.price
```

**Output:**
```
productName          | price
---------------------|-------
Laptop               | 999.99
Mouse                | 29.99
```

### Example 3: Building Formatted Tables
```cypher
WITH [['Name', 15], ['Email', 25], ['Role', 10]] AS columns
UNWIND columns AS col
RETURN flex.text.rpad(col[0], col[1], ' ') AS header
```

## Notes
- Returns `null` if input is `null`
- Converts numbers to strings automatically
- Default padding character is a space
- If string is already longer than target length, returns original string
- Useful for creating aligned columns, fixed-width output, or formatted tables

## See Also
- [text.lpad](./lpad.md) - Pad the start (left side) of a string
- [text.repeat](./repeat.md) - Repeat a string multiple times
- [text.format](./format.md) - Format strings with placeholders
