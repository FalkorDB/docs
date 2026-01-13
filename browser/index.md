---
title: "Browser"
description: "FalkorDB Browser web UI documentation"
nav_order: 9
permalink: /browser/
---

# FalkorDB Graph Visualization Tool (Browser)

FalkorDB's Browser provides a web UI for exploring, querying, and managing FalkorDB graphs. It allows developers to interact with graphs loaded to FalkorDB, explore how specific queries behave, and review the current data model. FalkorDB Browser integrates within the main FalkorDB Docker container and through the Cloud service.

![FalkorDB Browser GIF_01-26(1)](https://github.com/user-attachments/assets/af4f4d1c-111a-46a4-8442-8c08c037014f)

---

## Main Features

### Graph exploration (Graph page)

| Feature | Description |
| :--- | :--- |
| Interactive graph canvas | Visualizes query results containing nodes and edges as an interactive graph. Supports pan, zoom, and interaction with nodes and relationships. Toggles visibility by labels and relationship types. |
| Element search (in-canvas search) | Search nodes and edges by node properties (string prefix match), IDs, relationship type, and labels. |
| Data and inspection panel | Selecting an element opens a side panel for inspecting its properties. This panel supports editing workflows (see "Data manipulation"). |
| Entity Creation Tools | Add a node, an edge, or both to the current graph from the canvas view. |

### Querying

| Feature | Description |
| :--- | :--- |
| Cypher query editor (Monaco) | Includes keyboard shortcuts: Run (Enter and Cmd/Ctrl + Enter) and Insert newline (Shift + Enter). Includes Cypher keyword and function completion. |
| Results views | Graph view for node and edge results. Table view for tabular results. |
| Query metadata | The Metadata tab shows query metadata text, explain plan (nested tree), and profile output (nested tree). |

### Query history

| Feature | Description |
| :--- | :--- |
| Persistent query history | Stores in browser localStorage. |
| History browser dialog | Search and filter previous queries by graph name; supports single or multi-select delete. |
| Per-query metadata | Review metadata, explain, and profile for past queries. |

<img width="1419" height="825" alt="query-history-eye-candy" src="https://github.com/user-attachments/assets/be000961-f456-4b04-adf0-96f754b7447a" />

### Data manipulation (nodes/relationships)

| Feature | Description |
| :--- | :--- |
| Create and delete operations | Create node and create relationship flows from the Graph UI. Delete elements (node or relationship) from the Graph UI. |
| Edit labels | Edit labels through API routes (the UI provides label management components). |

### Graph management

| Feature | Description |
| :--- | :--- |
| Create graphs | Create graphs from the UI. |
| Delete graphs | Delete graphs (supports deleting multiple selected graphs). |
| Duplicate graphs | Create a copy of an existing graph (including data). |
| Export graphs | Download a .dump file via the Browser (/api/graph/:graph/export). |
| Upload data | Upload data through the "Upload Data" dialog, which supports drag-and-drop file selection. |

### Graph Info panel

| Feature | Description |
| :--- | :--- |
| Memory Usage tracking | Exposes current memory utilization of the graph in MB. |
| Node Label tracking | Displays all node labels and controls style visualization. Click a label to trigger a query for those nodes. |
| Edge Type tracking | Displays all edge types. Click an edge type to trigger a query showing connected nodes. |
| Property Keys tracking | Displays all property keys. Click a key to see nodes and edges where the property exists. |

<img width="1419" height="825" alt="falkordb-browser-eye-candy" src="https://github.com/user-attachments/assets/74375cd1-c704-40a9-9339-f1f885135a75" />

---

### API Documentation

| Feature | Description |
| :--- | :--- |
| Built-in Swagger UI | Available at `/docs`. Loads the OpenAPI spec from `/api/swagger`. Supports "Try it out" with `X-JWT-Only: true` headers. |

<img width="1419" height="825" alt="browser-api-doc-eye-candy" src="https://github.com/user-attachments/assets/35b0ca72-83f7-4f16-927c-413bf5f65593" />

### Authentication & access control

| Feature | Description |
| :--- | :--- |
| Authentication | Uses NextAuth (credentials-backed) for authentication. |
| Role-aware UI capabilities | Read-Only users cannot create graphs. Admins can access DB config and user management. |

### Settings

| Section | Description |
| :--- | :--- |
| Browser settings | Query timeouts, result limits, content persistence (auto-save), and display-text priority for node captions. |
| DB configurations (Admin) | View and update server configuration values. |
| Users (Admin) | List users, adjust roles, add or delete users. |
| Personal Access Tokens | Generate tokens with optional expiration and revocation management. |

---

## Common Workflows

### Running and visualizing queries

| Step | Action |
| :--- | :--- |
| 1 | Go to Graphs and select a graph. |
| 2 | Write a Cypher query in the editor and run it. |
| 3 | Inspect results in the Graph tab (canvas) or Table tab (rows). |
| 4 | Use Labels and Relationships toggles to focus the canvas. |

### Inspecting and editing elements

| Step | Action |
| :--- | :--- |
| 1 | Click a node or edge in the canvas. |
| 2 | Use the Data panel to inspect properties and apply actions. |

### Working with query history

| Step | Action |
| :--- | :--- |
| 1 | Open Query History and filter by graph or search text. |
| 2 | Select a query and review Metadata, Explain, or Profile. |

### Exporting graph data

| Step | Action |
| :--- | :--- |
| 1 | Open graph management and select a graph. |
| 2 | Click Export Data to download a `.dump` file. |
