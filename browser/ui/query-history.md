---
title: "Query History"
description: "Persistent local query history: open dialog, search/filter by graph, view metadata, delete queries."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 10
---

# Query History
Query History stores previously executed queries in the browser (localStorage) and exposes a dialog to browse them.

## Opening Query History
Click the history button (clock icon) in the selector bar.

If there are no saved queries, the button is disabled.

## What you can do
Inside the Query History dialog:
- **Search** previous queries.
- **Filter by graph name** (toggle one or more graphs).
- **Select a query** to load it into the history editor.
- **View per-query tabs**:
  - Edit Query
  - Profile
  - Metadata
  - Explain

## Deleting history
The dialog supports:
- Delete selected queries (supports multi-select via Ctrl + right-click)
- Delete all queries

Persistence notes:
- Stored under localStorage key: `query history`.

