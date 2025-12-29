# bitwise.shiftLeft

## Description
Performs a left bit shift operation, moving all bits to the left by the specified number of positions. Zero bits are shifted in from the right.

## Syntax
```cypher
flex.bitwise.shiftLeft(a, positions)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `a` | number (integer) | Yes | The value to shift |
| `positions` | number (integer) | Yes | Number of positions to shift left |

## Returns
**Type:** number (integer)

The result of shifting the bits left by the specified positions.

## Examples

### Example 1: Basic Left Shift
```cypher
RETURN flex.bitwise.shiftLeft(5, 2) AS result
```

**Output:**
```
result
------
20
```
(Binary: 0101 << 2 = 10100 = 20)

### Example 2: Multiply by Power of Two
```cypher
WITH 7 AS value
RETURN 
    flex.bitwise.shiftLeft(value, 1) AS times2,
    flex.bitwise.shiftLeft(value, 2) AS times4,
    flex.bitwise.shiftLeft(value, 3) AS times8
```

**Output:**
```
times2 | times4 | times8
-------|--------|-------
14     | 28     | 56
```
(Left shift by n is equivalent to multiplying by 2^n)

### Example 3: Creating Bit Masks
```cypher
RETURN flex.bitwise.shiftLeft(1, 3) AS mask
```

**Output:**
```
mask
----
8
```
(Creates mask with bit 3 set: 1000)

## Notes
- Operates on 32-bit signed integers in JavaScript
- Left shift by n is equivalent to multiplying by 2^n
- Bits shifted off the left are discarded
- Zero bits are shifted in from the right
- Useful for multiplication by powers of 2 and creating bit masks

## See Also
- [bitwise.shiftRight](./shiftRight.md) - Shift bits to the right
- [bitwise.and](./and.md) - Bitwise AND operation
- [bitwise.or](./or.md) - Bitwise OR operation
