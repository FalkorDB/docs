---
title: "Main Graph Canvas"
description: "Interactive graph visualization: pan/zoom, selection, label/relationship toggles, and layout controls."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 5
---

# Main Graph Canvas
The **Graph** results tab renders your query results as an interactive node/edge visualization.

## Core interactions
- **Pan/zoom** the canvas to explore results.
- **Select** nodes/edges to inspect them (opens the Data panel).
- **Right-click / context menu** is used in the tutorial flow to open element details.

## Labels & Relationships filters
When you have results, the overlay includes:
- **Labels** list: toggle visibility of nodes by label.
- **Relationships** list: toggle visibility of edges by relationship type.

These toggles update visibility on the canvas without re-running the query.

## Canvas controls
The controls area includes:
- **Animation control** (play/pause force-layout delay)
- **Zoom in / Zoom out**
- **Center / fit to screen**

## Tabs around the canvas
From the same results region you can switch to:
- **Table** view (when tabular data exists)
- **Metadata** view (when metadata/explain exists)

{% include faq_accordion.html title="Frequently Asked Questions" q1="How do I pan and zoom the graph canvas?" a1="Use your mouse or trackpad to **pan** (click and drag the background) and **zoom** (scroll wheel or pinch gesture). You can also use the zoom in/out buttons in the canvas controls." q2="Can I hide certain node labels or relationship types?" a2="Yes. Use the **Labels** and **Relationships** filter lists overlaid on the canvas to toggle visibility of specific node labels or edge types without re-running the query." q3="How do I center the graph on screen?" a3="Click the **Center / fit to screen** button in the canvas controls area to automatically fit all visible elements within the viewport." q4="What does the animation control do?" a4="The play/pause button controls the **force-layout animation** which arranges nodes dynamically. Pausing it freezes the layout in its current position." %}

