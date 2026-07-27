---
title: "Graphs Manager"
description: "Create, delete, duplicate, export, and upload graph data from FalkorDB Browser."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 17
---

# Graphs Manager
Graphs Manager is where you control graph lifecycle actions from one dialog.

## Supported actions

| Action | Description |
| :--- | :--- |
| Create graph | Create a new graph from the UI. |
| Delete graph | Delete one or more selected graphs. |
| Duplicate graph | Create a copy of an existing graph, including data. |
| Export graph | Download a `.dump` file through `/api/graph/{graph}/export`. Replace `{graph}` with the graph identifier. |
| Upload data | Open the Upload Data flow for file-based or query-based imports. |

## Related pages
- [Upload Data dialog](./upload-data.md)
- [Graph page (overall layout)](./graph-page.md)

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Can I export graph data from Graphs Manager?"
  a1="Yes. Select a graph and use Export to download a `.dump` file via `/api/graph/{graph}/export`, replacing `{graph}` with the graph identifier."
  q2="Can I duplicate a graph including all data?"
  a2="Yes. Duplicate creates a new graph copy from the selected source graph."
  q3="Can I remove multiple graphs in one flow?"
  a3="Yes. Graph deletion supports multi-selection when multiple graphs are selected."
%}
