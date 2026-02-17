---
layout: default
title: Map Functions
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 50
---

# Map Functions

FLEX map utilities provide functions for working with key-value maps (objects). These functions enable map manipulation, merging, filtering, and transformation operations.

## Available Functions

| Function | Description |
|----------|-------------|
| [map.fromPairs](./fromPairs.md) | Create a map from a list of key-value pairs |
| [map.merge](./merge.md) | Merge multiple maps into a single map |
| [map.removeKey](./removeKey.md) | Remove a single key from a map |
| [map.removeKeys](./removeKeys.md) | Remove multiple keys from a map |
| [map.submap](./submap.md) | Extract a subset of a map by selecting specific keys |

## Common Use Cases

- **Data Transformation**: Restructure and transform map data
- **Property Management**: Add, remove, or update node/relationship properties
- **Configuration Merging**: Combine default and custom configuration maps
- **Data Filtering**: Extract only needed fields from complex data structures