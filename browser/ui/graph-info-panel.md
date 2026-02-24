---
title: "Graph Info Panel"
description: "Graph statistics (counts, memory), labels, edge types, property keys, and quick exploration queries."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 6
---

# Graph Info Panel
The Graph Info panel provides quick, clickable insights into the selected graph’s structure.

## What it shows
- **Graph name**
- **Memory usage** (optional; can be toggled via settings)
- **Node count** and **edge count**
- **Node labels**
- **Edge (relationship) types**
- **Property keys**

## Click-to-explore behavior
The panel is designed for exploration:
- Clicking a **label** runs `MATCH (n:Label) RETURN n`.
- Clicking an **edge type** runs `MATCH p=()-[:TYPE]-() RETURN p`.
- Clicking a **property key** runs a query that finds nodes/edges where that key exists.

It also provides “*” shortcuts:
- **All nodes** (`MATCH (n) RETURN n`)
- **All edges** (`MATCH p=()-[]-() RETURN p`)

## Style customization entrypoint
Next to each label, a palette button opens the **Style Settings** panel for that label.

