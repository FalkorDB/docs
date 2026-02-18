---
layout: default
title: Bitwise Functions
description: "FLEX bitwise functions for performing AND, OR, XOR, NOT, and bit shift operations on integers in Cypher queries."
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 10
---

# Bitwise Functions

FLEX bitwise utilities provide operations for manipulating integer values at the bit level. These functions are useful for working with flags, permissions, masks, and other low-level data operations.

## Available Functions

| Function | Description |
|----------|-------------|
| [bitwise.and](./and.md) | Performs bitwise AND operation on two integers |
| [bitwise.or](./or.md) | Performs bitwise OR operation on two integers |
| [bitwise.xor](./xor.md) | Performs bitwise XOR (exclusive OR) operation on two integers |
| [bitwise.not](./not.md) | Performs bitwise NOT (complement) operation on an integer |
| [bitwise.shiftLeft](./shiftLeft.md) | Shifts bits to the left by a specified number of positions |
| [bitwise.shiftRight](./shiftRight.md) | Shifts bits to the right by a specified number of positions |

## Common Use Cases

- **Permission Systems**: Check and manipulate user permissions using bit flags
- **Data Compression**: Encode multiple boolean values in a single integer
- **Network Operations**: Work with IP addresses, subnet masks, and network protocols
- **Hardware Interfacing**: Control and read hardware registers and flags
- **Cryptography**: Implement encryption algorithms requiring bit manipulation