---
layout: default
title: text.swapCase
description: "Swaps the case of every character in a string — uppercase becomes lowercase and vice versa."
parent: Text Functions
grand_parent: FLEX Function Reference
nav_order: 16
---

# text.swapCase

## Description
Swaps the case of each character in a string - uppercase characters become lowercase and vice versa.

## Syntax
```cypher
flex.text.swapCase(string)
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `string` | string | Yes | The string to swap case |

## Returns
**Type:** string

A new string with all uppercase characters converted to lowercase and all lowercase characters converted to uppercase. Returns `null` if input is `null`.

## Examples

### Example 1: Basic Usage
```cypher
RETURN flex.text.swapCase('Hello World') AS result
```

**Output:**
```text
result
-------------
hELLO wORLD
```

### Example 2: Swapping Mixed Case
```cypher
RETURN flex.text.swapCase('aBc123XyZ') AS result
```

**Output:**
```text
result
----------
AbC123xYz
```

## Notes
- Returns `null` for `null` input
- Non-alphabetic characters remain unchanged
- Applies to all characters in the string, not just the first

## See Also
- [text.capitalize](./capitalize.md) - Uppercase the first character
- [text.camelCase](./camelCase.md) - Convert to camelCase format
- [text.snakeCase](./snakeCase.md) - Convert to snake_case format

{% include faq_accordion.html title="Frequently Asked Questions" q1="Does flex.text.swapCase affect non-alphabetic characters?" a1="No. Numbers, punctuation, and other non-alphabetic characters remain unchanged." q2="Is swapCase applied to all characters or just the first?" a2="It is applied to **every** character in the string — each uppercase letter becomes lowercase and vice versa." %}
