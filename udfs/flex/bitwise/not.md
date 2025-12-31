# bitwise.not

## Description
Performs a bitwise NOT operation (one's complement) on an integer, inverting all bits.

## Syntax
```cypher
flex.bitwise.not(a)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `a` | number (integer) | Yes | The operand to invert |

## Returns
**Type:** number (integer)

The result of the bitwise NOT operation (one's complement).

## Examples

### Example 1: Basic NOT Operation
```cypher
RETURN flex.bitwise.not(5) AS result
```

**Output:**
```
result
------
-6
```
(Binary: NOT 0101 = ...11111010 in 32-bit two's complement = -6)

### Example 2: Inverting All Bits
```cypher
RETURN flex.bitwise.not(0) AS result
```

**Output:**
```
result
------
-1
```
(All bits become 1 in two's complement = -1)

### Example 3: Double NOT Returns Original
```cypher
WITH 42 AS value
RETURN flex.bitwise.not(flex.bitwise.not(value)) AS restored
```

**Output:**
```
restored
--------
42
```

## Notes
- Operates on 32-bit signed integers in JavaScript
- Result uses two's complement representation
- NOT operation inverts all bits including sign bit
- Formula: `~n = -(n + 1)`
- Less commonly used than AND, OR, XOR in typical applications

## See Also
- [bitwise.and](./and.md) - Bitwise AND operation
- [bitwise.or](./or.md) - Bitwise OR operation
- [bitwise.xor](./xor.md) - Bitwise XOR operation
