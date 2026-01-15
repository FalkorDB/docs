---
title: Browser
description: FalkorDB Browser web UI documentation
sidebar_position: 9
sidebar_label: Browser
---


# Browser
FalkorDB's Browser provides a web UI for exploring, querying, and managing FalkorDB graphs. It allows developers to interact with graphs loaded to FalkorDB, explore how specific queries behave, and review the current data model. FalkorDB Browser integrates within the main FalkorDB Docker container and through the Cloud service.

![FalkorDB Browser GIF_01-26(1)](https://github.com/user-attachments/assets/af4f4d1c-111a-46a4-8442-8c08c037014f)

---

## Main Features

### Graph exploration (Graph page)

| Feature                           | Description                                                                                                                                                                                         |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Interactive graph canvas          | Visualizes query results containing nodes and edges as an interactive graph. Supports pan, zoom, and interaction with nodes and relationships. Toggles visibility by labels and relationship types. |
| Element search (in-canvas search) | Search nodes and edges by node properties (string prefix match), IDs, relationship type, and labels. Jump to, zoom to, and select the match.                                                        |
| Data and inspection panel         | Selecting an element opens a side panel for inspecting its properties. This panel supports editing workflows (see "Data manipulation").                                                             |
| Entity Creation Tools             | Add a node, an edge, or both to the current graph from the canvas view.                                                                                                                             |

### Querying

| Feature                      | Description                                                                                                                                                                                                                                                                    |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Cypher query editor (Monaco) | The editor-style experience for writing Cypher includes keyboard shortcuts: Run (Enter and Cmd/Ctrl + Enter in the query-history editor) and Insert newline (Shift + Enter). The editor includes Cypher keyword and function completion based on the Browser's built-in lists. |
| Results views                | Graph view for node and edge results. Table view for tabular results.                                                                                                                                                                                                          |
| Query metadata               | The Metadata tab shows query metadata text, explain plan (rendered as a nested tree), and profile output (rendered as a nested tree).                                                                                                                                          |

### Query history

| Feature                  | Description                                                                                                                                    |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Persistent query history | Stores in browser localStorage.                                                                                                                |
| History browser dialog   | Allows you to search and filter previous queries, filter by graph name, and delete single queries, multi-select delete, or delete all queries. |
| Per-query metadata       | Review metadata, explain, and profile for past queries.                                                                                        |

![query-history-eye-candy](https://github.com/user-attachments/assets/be000961-f456-4b04-adf0-96f754b7447a)

### Data manipulation (nodes/relationships)

| Feature                      | Description                                                                                                            |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Create and delete operations | Create node and create relationship flows from the Graph UI. Delete elements (node or relationship) from the Graph UI. |
| Edit labels                  | Edit labels through API routes (the UI provides label management components).                                          |

### Graph management

| Feature          | Description                                                                                              |
| ---------------- | -------------------------------------------------------------------------------------------------------- |
| Create graphs    | Create graphs from the UI.                                                                               |
| Delete graphs    | Delete graphs (supports deleting multiple selected graphs).                                              |
| Duplicate graphs | Create a copy of an existing graph (including data).                                                     |
| Export graphs    | Download a .dump file via the Browser (/api/graph/:graph/export).                                        |
| Upload data      | Upload data through the "Upload Data" dialog, which supports drag-and-drop file selection (Dropzone UI). |

### Graph Info panel

| Feature                | Description                                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Memory Usage tracking  | Exposes current memory utilization of the graph in MB.                                                                                                             |
| Node Label tracking    | Displays all node labels in the graph and controls style visualization for labels. Click on a node label to trigger a query that visualizes nodes from this label. |
| Edge Type tracking     | Displays all edge types in the graph. Click on an edge type to trigger a graph query showing only nodes connected through this edge type.                          |
| Property Keys tracking | Displays all property keys in the graph. Click on a key to issue a query that shows nodes and edges where the property exists (not NULL).                          |

<img width="1419" height="825" alt="falkordb-browser-eye-candy" src="https://github.com/user-attachments/assets/74375cd1-c704-40a9-9339-f1f885135a75" />

---

### API Documentation

| Feature             | Description                                                                                                                                                           |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Built-in Swagger UI | Available at /docs. Loads the Browser's OpenAPI spec from /api/swagger. "Try it out" enabled. Adds an X-JWT-Only: true header when calling endpoints from Swagger UI. |

<img width="1419" height="825" alt="browser-api-doc-eye-candy" src="https://github.com/user-attachments/assets/35b0ca72-83f7-4f16-927c-413bf5f65593" />

### Authentication & access control

| Feature                    | Description                                                                                                                   |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Authentication             | Uses NextAuth (credentials-backed) for authentication.                                                                        |
| Role-aware UI capabilities | Read-Only users cannot create graphs. Admin users can access database configuration and user-management sections in settings. |

### Settings

| Section                   | Description                                                                                                                                                                                                                                                                          |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Browser settings          | Query execution defaults and limits: timeout, result limit, run default query on load. User experience: content persistence (auto-save and restore), display-text priority (controls which node property appears as the node caption). Graph info refresh interval. Tutorial replay. |
| DB configurations (Admin) | View and update server configuration values. Some runtime configurations remain read-only.                                                                                                                                                                                           |
| Users (Admin)             | List users and adjust roles. Add and delete users.                                                                                                                                                                                                                                   |
| Personal Access Tokens    | Generate tokens (with optional expiration). Tokens appear once at creation (copy-to-clipboard UX). Revoke existing tokens.                                                                                                                                                           |
<!--
### Optional “Chat” (English → Cypher)
If enabled, the Browser includes a **Chat panel** that streams responses from a text-to-cypher service.
- The UI sends messages to `/api/chat` and processes server-sent events.
- Chat configuration lives in Settings (model + secret key).
- The chat backend URL is controlled by `CHAT_URL`.
-->

---

## Common Workflows

### Running and visualizing queries

| Step | Action                                                                                 |
| ---- | -------------------------------------------------------------------------------------- |
| 1    | Go to Graphs and select a graph.                                                       |
| 2    | Write a Cypher query in the editor and run it.                                         |
| 3    | Inspect results in the Graph tab (interactive canvas) or Table tab (rows and columns). |
| 4    | Use Labels and Relationships toggles to focus the canvas.                              |

[NEED GIF HERE]

### Inspecting and editing elements

| Step | Action                                                                                 |
| ---- | -------------------------------------------------------------------------------------- |
| 1    | Click a node or edge in the canvas.                                                    |
| 2    | Use the Data panel to inspect properties and apply create or delete actions as needed. |

### Working with query history

| Step | Action                                                                 |
| ---- | ---------------------------------------------------------------------- |
| 1    | Open Query History and filter by graph or search for a previous query. |
| 2    | Select a query and review Metadata, Explain, or Profile.               |

[NEED GIF HERE]

### Exporting graph data

| Step | Action                                          |
| ---- | ----------------------------------------------- |
| 1    | Open graph management and select a graph.       |
| 2    | Click Export Data to download a `.dump` file.   |

[NEED GIF HERE]

