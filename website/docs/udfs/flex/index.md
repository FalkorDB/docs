---
title: FLEX Function Reference
sidebar_label: FLEX Function Reference
---

# FLEX Function Reference

FLEX is FalkorDB's open source community UDF package, available at [github.com/FalkorDB/flex](https://github.com/FalkorDB/flex).  
It contains a variety of useful functionality, including:

- String and set similarity metrics for fuzzy matching and comparison  
- Date and time manipulation, formatting, and parsing  
- Low-level bitwise operations on integers  

We welcome contributions to extend this library with additional functionality.

The following sections document all FLEX (FalkorDB Library for Extensions) functions.

## Function Categories

### Similarity Functions (`flex.sim.*`)

Set similarity metrics for fuzzy matching and comparison.

| Function | Description |
|----------|-------------|
| [sim.jaccard](./similarity/jaccard.md) | Calculate Jaccard similarity coefficient between sets |

### Text Functions (`flex.text.*`)

String manipulation, formatting, case conversion utilities, and string similarity metrics.

| Function | Description |
|----------|-------------|
| [text.capitalize](./text/capitalize.md) | Capitalize the first character of a string |
| [text.decapitalize](./text/decapitalize.md) | Lowercase the first character of a string |
| [text.swapCase](./text/swapCase.md) | Swap the case of all characters in a string |
| [text.camelCase](./text/camelCase.md) | Convert string to camelCase format |
| [text.upperCamelCase](./text/upperCamelCase.md) | Convert string to UpperCamelCase (PascalCase) |
| [text.snakeCase](./text/snakeCase.md) | Convert string to snake_case format |
| [text.format](./text/format.md) | Format string with placeholder substitution |
| [text.indexOf](./text/indexOf.md) | Find first occurrence of substring |
| [text.indexesOf](./text/indexesOf.md) | Find all occurrences of substring |
| [text.join](./text/join.md) | Join array elements with delimiter |
| [text.lpad](./text/lpad.md) | Pad string on the left to target length |
| [text.rpad](./text/rpad.md) | Pad string on the right to target length |
| [text.regexGroups](./text/regexGroups.md) | Extract regex matches and capture groups |
| [text.repeat](./text/repeat.md) | Repeat string multiple times |
| [text.replace](./text/replace.md) | Replace text using regex pattern |
| [text.jaroWinkler](./text/jaroWinkler.md) | Compute Jaro-Winkler similarity for short strings |
| [text.levenshtein](./text/levenshtein.md) | Compute Levenshtein edit distance between strings |

### Collection Functions (`flex.coll.*`)

Operations on lists and arrays including set operations and transformations.

| Function | Description |
|----------|-------------|
| [coll.zip](./collections/zip.md) | Combine two lists element-by-element into pairs |
| [coll.union](./collections/union.md) | Combine lists and return unique elements |
| [coll.intersection](./collections/intersection.md) | Find common elements between lists |
| [coll.shuffle](./collections/shuffle.md) | Randomly shuffle list elements |
| [coll.frequencies](./collections/frequencies.md) | Count frequency of each element in list |

### Map Functions (`flex.map.*`)

Map/object manipulation for property management and transformation.

| Function | Description |
|----------|-------------|
| [map.merge](./map/merge.md) | Shallow merge multiple maps |
| [map.fromPairs](./map/fromPairs.md) | Convert list of key-value pairs to map |
| [map.submap](./map/submap.md) | Extract subset of keys from map |
| [map.removeKey](./map/removeKey.md) | Remove single key from map |
| [map.removeKeys](./map/removeKeys.md) | Remove multiple keys from map |

### JSON Functions (`flex.json.*`)

JSON serialization and parsing utilities.

| Function | Description |
|----------|-------------|
| [json.toJson](./json/toJson.md) | Serialize value to JSON string |
| [json.fromJsonMap](./json/fromJsonMap.md) | Parse JSON string to map |
| [json.fromJsonList](./json/fromJsonList.md) | Parse JSON string to list |

### Date Functions (`flex.date.*`)

Date and time manipulation, formatting, and parsing.

| Function | Description |
|----------|-------------|
| [date.format](./date/format.md) | Format date/time with pattern and timezone |
| [date.parse](./date/parse.md) | Parse date/time string with optional pattern |
| [date.truncate](./date/truncate.md) | Truncate date to specific unit (day, month, etc.) |
| [date.toTimeZone](./date/toTimeZone.md) | Convert date to timezone offset |

### Bitwise Functions (`flex.bitwise.*`)

Low-level bitwise operations on integers.

| Function | Description |
|----------|-------------|
| [bitwise.and](./bitwise/and.md) | Bitwise AND operation |
| [bitwise.or](./bitwise/or.md) | Bitwise OR operation |
| [bitwise.xor](./bitwise/xor.md) | Bitwise XOR (exclusive OR) operation |
| [bitwise.not](./bitwise/not.md) | Bitwise NOT (one's complement) operation |
| [bitwise.shiftLeft](./bitwise/shiftLeft.md) | Left bit shift operation |
| [bitwise.shiftRight](./bitwise/shiftRight.md) | Right bit shift with sign extension |

## Common Use Cases

### Data Cleaning and Normalization
- `text.camelCase`, `text.snakeCase` - Normalize field names
- `text.replace` - Remove or sanitize unwanted characters
- `coll.union` - Deduplicate lists

### Fuzzy Matching and Search
- `text.levenshtein` - Find similar strings with edit distance
- `text.jaroWinkler` - Match names and short strings
- `sim.jaccard` - Compare sets and tag similarity

### Data Aggregation and Analysis
- `date.truncate` - Group by time periods
- `coll.frequencies` - Count occurrences
- `map.submap` - Select relevant fields

### API and Data Exchange
- `json.toJson`, `json.fromJsonMap` - JSON serialization
- `map.removeKeys` - Filter sensitive data
- `text.format` - Build formatted messages

### Permission and Flag Management
- `bitwise.and`, `bitwise.or` - Check and set permission flags
- `bitwise.xor` - Toggle flags
