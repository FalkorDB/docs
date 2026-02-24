---
title: "Table View"
description: "Tabular query results view, search/expand behaviors, and CSV export."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 11
---

# Table View
The Table tab displays query results as rows/columns when the query returns tabular data.

## When it appears
The **Table** tab is enabled when the current query produced `graph.Data` (i.e., non-empty tabular results).

## Features
- Automatic header extraction (union of keys across returned rows).
- Table UI capabilities provided by the shared Table component:
  - Search
  - Expand/collapse nested values (when applicable)
  - Scroll position persistence within the session

## Export to CSV
Click **Export** to download the current table results as a CSV file.

Notes:
- Complex values (objects) are JSON-stringified.
- The output filename includes the graph ID (e.g., `<graph>_table_export.csv`).

