---
title: "Data / Property Panel"
description: "Inspect and edit node/edge details: ID, labels/relationship type, and property table editing."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 8
---

# Data / Property Panel
The Data panel opens when you select a node or edge in the graph. It’s used to inspect properties and perform edit operations.

## What it shows
For the selected element:
- **ID**
- **Attributes count**
- **Labels** (nodes) or **Relationship type** (edges)
- A **properties table** (key/value) for viewing and editing attributes

## Node label management
For nodes (and when the user role is not Read-Only):
- **Add Label**
- **Remove Label** (except the “default” empty label)

Label changes are immediately reflected in:
- The in-app graph model
- The visible canvas node styling
- The graph info panel counts/listing

## Editing properties
Properties are managed via the embedded table component. Typical operations include:
- Editing existing values
- Adding/removing properties

(Exact editing affordances depend on the table component implementation.)

## Keyboard shortcut
- `Esc` closes the Data panel.

