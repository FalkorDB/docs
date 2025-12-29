# text.lpad

## Description
Pads the start (left side) of a string with a specified character until it reaches the desired length.

## Syntax
```cypher
flex.text.lpad(string, length, padChar)
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

### Example 1: Basic Left Padding
```cypher
RETURN flex.text.lpad('5', 3, '0') AS result
```

**Output:**
```
result
------
005
```

### Example 2: Formatting Numbers with Leading Zeros
```cypher
MATCH (o:Order)
RETURN flex.text.lpad(toString(o.id), 8, '0') AS orderId
```

**Output:**
```
orderId
--------
00000123
00000456
```

### Example 3: Aligning Text
```cypher
WITH ['Total:', 'Subtotal:', 'Tax:'] AS labels
UNWIND labels AS label
RETURN flex.text.lpad(label, 12, ' ') AS aligned
```

**Output:**
```
aligned
--------------
      Total:
   Subtotal:
        Tax:
```

## Notes
- Returns `null` if input is `null`
- Converts numbers to strings automatically
- Default padding character is a space
- If string is already longer than target length, returns original string
- Useful for formatting IDs, aligning columns, or creating fixed-width output

## See Also
- [text.rpad](./rpad.md) - Pad the end (right side) of a string
- [text.repeat](./repeat.md) - Repeat a string multiple times
- [text.format](./format.md) - Format strings with placeholders
