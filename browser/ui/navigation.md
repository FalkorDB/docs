---
title: "Navigation & Header"
description: "Left sidebar navigation (Graphs/Settings), graph-side panel toggles, help menu, theme toggle, logout."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 2
---

# Navigation & Header
FalkorDB Browser uses a left sidebar (header) for navigation and global actions.

## Main navigation buttons
Located in the sidebar under the user name/version block:
- **SETTINGS** → opens `/settings`
- **GRAPHS** → opens `/graph`

## Contextual graph controls (Graphs page)
When you are on **Graphs** (`/graph`) and a graph is selected:
- **Graph Info toggle** (database icon) opens/closes the Graph Info panel.
- **CHAT** toggle opens/closes the Chat side panel (requires API key/model configured in Settings).

## Create graph
For non–Read-Only users, the sidebar can expose **Create Graph** (depending on the current route).

## Help menu
The “Help” button (file/code icon) opens a menu with:
- Documentation (external)
- API Documentation (`/docs`)
- Support (Discord)
- About drawer

## Theme toggle
The theme toggle cycles through:
- Dark → Light → System → Dark

## Connection indicators
The sidebar may show connection “mode” badges (e.g. Single/Sentinel/Cluster) and an **Offline** indicator when the backend is unreachable.

## Logout
The logout button signs out and redirects to `/login`.

