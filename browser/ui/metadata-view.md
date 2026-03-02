---
title: "Metadata View"
description: "Query execution details: metadata text, explain plan tree, and profile output."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 12
---

# Metadata View
The Metadata tab provides query execution details for the current query.

## Sections
The UI is split into three main panels:
- **Profile**
  - Runs a profiling request and renders the output as a nested tree.
  - Warning: profiling can be intrusive depending on the database behavior.
- **Metadata**
  - Displays metadata text lines.
- **Explain**
  - Displays explain-plan output as a nested tree.

## When it’s enabled
The Metadata tab is enabled when the current query has metadata/explain content.

