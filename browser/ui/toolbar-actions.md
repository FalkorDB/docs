---
title: "Graph Toolbar & Element Actions"
description: "In-canvas search, selection helpers, add node/edge flows, delete, and related controls."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 13
---

# Graph Toolbar & Element Actions
The Graph toolbar is an overlay shown on the Graph canvas. It’s focused on searching, selecting, and modifying graph elements.

## In-canvas element search
The search input supports matching against:
- Node/edge **property values** (string prefix match)
- **IDs**
- **Relationship type** (edges)
- **Labels** (nodes)

Keyboard behavior:
- `Enter`: jump/select the highlighted suggestion
- `Arrow Up/Down`: move through suggestions
- `Esc`: clear search

Selecting a suggestion zooms/fits the canvas around the matched element.

## Element actions (create / delete)
When the user is not Read-Only, the toolbar supports:
- **Add node**
- **Add edge** (typically only enabled when two nodes are selected)
- **Delete** selected element(s)

These actions open additional UI (e.g., the Add panel) and/or call graph API routes.

## Layout & limit warnings
The toolbar can display warnings when:
- The current query hit a result limit
- The configured limit changed relative to the last query

