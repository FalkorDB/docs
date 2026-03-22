---
title: "Query Editor"
description: "Cypher editor: run shortcuts, autocomplete, maximize mode, placeholder behavior, and graph-scoped suggestions."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 9
---

# Query Editor
The query editor is a Monaco-based Cypher editor used to run queries against the selected graph.

## Running queries
- Click **RUN** to execute.
- Keyboard shortcuts:
  - **Enter**: run query (when the suggestion widget is not open)
  - **Cmd/Ctrl + Enter**: run query
  - **Shift + Enter**: insert a newline

## Query history navigation (keyboard)
When your cursor is on the **first line** or **last line** of the editor:
- **Up arrow**: navigate backward through query history
- **Down arrow**: navigate forward through query history

## Autocomplete & syntax highlighting
The editor provides:
- Cypher keyword suggestions
- Function suggestions
- Graph-scoped suggestions (labels, relationship types, property keys) fetched from the server

## Maximize mode
The maximize button opens a full-screen editor dialog with the same Run/Clear controls.

