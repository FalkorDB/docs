---
layout: default
title: Text Functions
description: "FLEX text functions for case conversion, string formatting, padding, searching, and similarity metrics in Cypher queries."
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 70
---

# Text Functions

FLEX text utilities provide comprehensive functions for string manipulation, formatting, and text analysis. These functions enable case conversion, formatting, searching, similarity measurement, and string transformation operations.

## Available Functions

| Function | Description |
|----------|-------------|
| [text.camelCase](./camelCase.md) | Convert string to camelCase format |
| [text.capitalize](./capitalize.md) | Capitalize the first character of a string |
| [text.decapitalize](./decapitalize.md) | Convert the first character to lowercase |
| [text.format](./format.md) | Format a string with placeholders and arguments |
| [text.indexOf](./indexOf.md) | Find the first occurrence of a substring |
| [text.indexesOf](./indexesOf.md) | Find all occurrences of a substring |
| [text.jaroWinkler](./jaroWinkler.md) | Calculate Jaro-Winkler string similarity distance |
| [text.join](./join.md) | Join a list of strings with a separator |
| [text.levenshtein](./levenshtein.md) | Calculate Levenshtein edit distance between strings |
| [text.lpad](./lpad.md) | Pad string on the left to a specified length |
| [text.regexGroups](./regexGroups.md) | Extract regex capture groups from a string |
| [text.repeat](./repeat.md) | Repeat a string a specified number of times |
| [text.replace](./replace.md) | Replace occurrences of a substring with another string |
| [text.rpad](./rpad.md) | Pad string on the right to a specified length |
| [text.snakeCase](./snakeCase.md) | Convert string to snake_case format |
| [text.swapCase](./swapCase.md) | Swap the case of all characters in a string |
| [text.upperCamelCase](./upperCamelCase.md) | Convert string to UpperCamelCase (PascalCase) format |

## Common Use Cases

- **Text Formatting**: Format strings for display, normalize case conventions
- **String Searching**: Find and extract substrings and patterns
- **Fuzzy Matching**: Compare strings and find similar text using distance metrics
- **Data Cleaning**: Normalize and standardize text data
- **Text Transformation**: Convert between naming conventions and formats