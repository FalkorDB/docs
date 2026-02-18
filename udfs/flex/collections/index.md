---
layout: default
title: Collection Functions
description: "FLEX collection functions for set operations, frequency analysis, and list manipulation in Cypher queries."
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 20
---

# Collection Functions

FLEX collections utilities provide functions for working with lists and arrays. These functions enable advanced list manipulation, set operations, and data transformation operations.

## Available Functions

| Function | Description |
|----------|-------------|
| [collections.frequencies](./frequencies.md) | Count occurrences of each element in a collection |
| [collections.intersection](./intersection.md) | Find common elements between two collections |
| [collections.shuffle](./shuffle.md) | Randomly shuffle elements in a collection |
| [collections.union](./union.md) | Combine two collections, removing duplicates |
| [collections.zip](./zip.md) | Combine two collections into pairs |

## Common Use Cases

- **Set Operations**: Perform union, intersection, and other set-like operations on lists
- **Data Analysis**: Count element frequencies and find patterns in data
- **Randomization**: Shuffle data for sampling or randomization purposes
- **Data Transformation**: Combine and restructure collections for processing