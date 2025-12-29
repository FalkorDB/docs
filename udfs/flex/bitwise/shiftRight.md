# bitwise.shiftRight

## Description
Performs a sign-propagating right bit shift operation, moving all bits to the right by the specified number of positions. The sign bit is copied to fill the leftmost positions.

## Syntax
```cypher
flex.bitwise.shiftRight(a, positions)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `a` | number (integer) | Yes | The value to shift |
| `positions` | number (integer) | Yes | Number of positions to shift right |

## Returns
**Type:** number (integer)

The result of shifting the bits right by the specified positions, with sign extension.

## Examples

### Example 1: Basic Right Shift
```cypher
RETURN flex.bitwise.shiftRight(20, 2) AS result
```

**Output:**
```
result
------
5
```
(Binary: 10100 >> 2 = 00101 = 5)

### Example 2: Divide by Power of Two
```cypher
WITH 56 AS value
RETURN 
    flex.bitwise.shiftRight(value, 1) AS div2,
    flex.bitwise.shiftRight(value, 2) AS div4,
    flex.bitwise.shiftRight(value, 3) AS div8
```

**Output:**
```
div2 | div4 | div8
-----|------|-----
28   | 14   | 7
```
(Right shift by n is equivalent to integer division by 2^n)

### Example 3: Sign Extension with Negative Numbers
```cypher
RETURN flex.bitwise.shiftRight(-8, 2) AS result
```

**Output:**
```
result
------
-2
```
(Sign bit is preserved in right shift)

### Example 4: Extracting Higher Bits
```cypher
WITH 255 AS value  // 11111111
RETURN flex.bitwise.shiftRight(value, 4) AS upperNibble
```

**Output:**
```
upperNibble
-----------
15
```
(Extracts upper 4 bits: 00001111 = 15)

## Notes
- Operates on 32-bit signed integers in JavaScript
- Uses arithmetic (sign-propagating) right shift
- Right shift by n is equivalent to integer division by 2^n (truncated toward negative infinity)
- Sign bit is copied to fill vacated positions (sign extension)
- Bits shifted off the right are discarded
- Useful for division by powers of 2 and extracting bit fields

## See Also
- [bitwise.shiftLeft](./shiftLeft.md) - Shift bits to the left
- [bitwise.and](./and.md) - Bitwise AND operation
- [bitwise.or](./or.md) - Bitwise OR operation
