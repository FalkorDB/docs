---
layout: default
title: JSON Functions
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 40
---

# JSON Functions

FLEX json utilities provide functions for converting between JSON strings and native data structures. These functions enable JSON serialization and deserialization for working with JSON data in Cypher queries.

## Available Functions

| Function | Description |
|----------|-------------|
| [json.fromJsonList](./fromJsonList.md) | Parse a JSON array string into a list |
| [json.fromJsonMap](./fromJsonMap.md) | Parse a JSON object string into a map |
| [json.toJson](./toJson.md) | Convert a value (list, map, etc.) to a JSON string |

## Common Use Cases

- **API Integration**: Parse JSON responses from external APIs
- **Data Import/Export**: Convert between JSON and native graph structures
- **Configuration Storage**: Store and retrieve JSON configuration data
- **Data Serialization**: Convert complex data structures to JSON for storage or transmission