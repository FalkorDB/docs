---
layout: default
title: bitwise.or
description: "Performs a bitwise OR operation on two integers, returning 1 for each bit position where at least one operand has a 1."
parent: Bitwise Functions
grand_parent: FLEX Function Reference
nav_order: 3
---

# bitwise.or

## Description
Performs a bitwise OR operation on two integers. Each bit in the result is 1 if at least one of the corresponding bits in the operands is 1.

## Syntax
```cypher
flex.bitwise.or(a, b)
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `a` | number (integer) | Yes | First operand |
| `b` | number (integer) | Yes | Second operand |

## Returns
**Type:** number (integer)

The result of the bitwise OR operation.

## Examples

### Example 1: Basic OR Operation
```cypher
RETURN flex.bitwise.or(12, 10) AS result
```

**Output:**
```text
result
------
14
```
(Binary: 1100 OR 1010 = 1110 = 14)

### Example 2: Combining Permission Flags
```cypher
WITH 1 AS readFlag, 2 AS writeFlag
RETURN flex.bitwise.or(readFlag, writeFlag) AS readWritePermission
```

**Output:**
```text
readWritePermission
-------------------
3
```
(Binary: 01 OR 10 = 11 = 3)

### Example 3: Setting Multiple Flags
```cypher
MATCH (u:User {id: 123})
SET u.permissions = flex.bitwise.or(u.permissions, 4)  // Add execute permission
```

## Notes
- Operates on 32-bit signed integers in JavaScript
- Both operands are converted to integers if needed
- Commonly used for combining flags and setting bits

## See Also
- [bitwise.and](./and.md) - Bitwise AND operation
- [bitwise.xor](./xor.md) - Bitwise XOR operation
- [bitwise.not](./not.md) - Bitwise NOT operation

{% include faq_accordion.html title="Frequently Asked Questions" q1="What does flex.bitwise.or return?" a1="It returns an integer where each bit is 1 if the corresponding bit in **either** (or both) input operands is 1. For example, `flex.bitwise.or(5, 3)` returns `7`." q2="How can I combine permission flags with bitwise.or?" a2="Use `flex.bitwise.or(existingFlags, newFlag)` to add a permission bit. For example, `flex.bitwise.or(permissions, 4)` sets the third bit." %}
