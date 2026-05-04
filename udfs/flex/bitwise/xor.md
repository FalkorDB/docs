---
layout: default
title: bitwise.xor
description: "Performs a bitwise XOR operation on two integers, returning 1 for each bit position where the operands differ."
parent: Bitwise Functions
grand_parent: FLEX Function Reference
nav_order: 6
---

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
```text
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
```text
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
```text
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

{% include faq_accordion.html title="Frequently Asked Questions" q1="What does flex.bitwise.xor return?" a1="It returns an integer where each bit is 1 only if the corresponding bits in the two operands differ. For example, `flex.bitwise.xor(5, 3)` returns `6`." q2="What is XOR commonly used for?" a2="XOR is useful for toggling flags, simple checksums, and detecting differences between two bitmasks." %}
