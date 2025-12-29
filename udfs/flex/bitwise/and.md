# bitwise.and

## Description
Performs a bitwise AND operation on two integers. Each bit in the result is 1 only if the corresponding bits in both operands are 1.

## Syntax
```cypher
flex.bitwise.and(a, b)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `a` | number (integer) | Yes | First operand |
| `b` | number (integer) | Yes | Second operand |

## Returns
**Type:** number (integer)

The result of the bitwise AND operation.

## Examples

### Example 1: Basic AND Operation
```cypher
RETURN flex.bitwise.and(12, 10) AS result
```

**Output:**
```
result
------
8
```
(Binary: 1100 AND 1010 = 1000 = 8)

### Example 2: Checking Permission Flags
```cypher
WITH 7 AS userPermissions  // 0111 (read=1, write=2, execute=4)
WITH userPermissions, 2 AS writeFlag
RETURN flex.bitwise.and(userPermissions, writeFlag) > 0 AS hasWrite
```

### Example 3: Masking Bits
```cypher
MATCH (d:Device)
WITH d, flex.bitwise.and(d.flags, 15) AS lowerNibble
RETURN d.id, lowerNibble
```

## Notes
- Operates on 32-bit signed integers in JavaScript
- Both operands are converted to integers if needed
- Commonly used for flag checking and bit masking

## See Also
- [bitwise.or](./or.md) - Bitwise OR operation
- [bitwise.xor](./xor.md) - Bitwise XOR operation
- [bitwise.not](./not.md) - Bitwise NOT operation
