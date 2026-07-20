---
title: "Query Editor"
description: "Cypher editor: run shortcuts, autocomplete, maximize mode, placeholder behavior, and graph-scoped suggestions."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 9
---

# Query Editor

Browser uses a Monaco-based Cypher editor.

## Shortcuts

- Enter: run query (when suggestions are closed)
- Ctrl/Cmd + Enter: run query
- Shift + Enter: newline

## Suggestions

Editor suggestions include:

- Cypher keywords
- Built-in functions
- Procedure names
- Graph metadata terms
- UDF function names

## Diagnostics

Backend diagnostics are rendered as Monaco markers with hover details and supported quick actions.

## Maximize mode

Maximize opens a larger editor dialog with the same execution semantics.
