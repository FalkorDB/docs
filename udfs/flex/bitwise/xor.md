# bitwise.xor

## Description
Performs a bitwise XOR (exclusive OR) operation on two integers. Each bit in the result is 1 if the corresponding bits in the operands are different.

## Syntax
```cypher
flex.bitwise.xor(a, b)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `a` | number (integer) | Yes | First operand |
| `b` | number (integer) | Yes | Second operand |

## Returns
**Type:** number (integer)

The result of the bitwise XOR operation.

## Examples

### Example 1: Basic XOR Operation
```cypher
RETURN flex.bitwise.xor(12, 10) AS result
```

**Output:**
```
result
------
6
```
(Binary: 1100 XOR 1010 = 0110 = 6)

### Example 2: Toggling Bits
```cypher
WITH 5 AS value, 3 AS toggleMask
RETURN flex.bitwise.xor(value, toggleMask) AS toggled
```

**Output:**
```
toggled
-------
6
```
(Binary: 0101 XOR 0011 = 0110)

### Example 3: Simple Encryption/Decryption
```cypher
WITH 42 AS data, 17 AS key
WITH flex.bitwise.xor(data, key) AS encrypted
RETURN flex.bitwise.xor(encrypted, key) AS decrypted
```

**Output:**
```
decrypted
---------
42
```
(XOR with same key twice returns original value)

## Notes
- Operates on 32-bit signed integers in JavaScript
- Both operands are converted to integers if needed
- XOR with same value twice returns the original value
- Commonly used for toggling flags and simple encryption

## See Also
- [bitwise.and](./and.md) - Bitwise AND operation
- [bitwise.or](./or.md) - Bitwise OR operation
- [bitwise.not](./not.md) - Bitwise NOT operation
