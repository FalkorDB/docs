---
title: "Graph Info Panel"
description: "Graph statistics (counts, memory), labels, edge types, property keys, and quick exploration queries."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 6
---

# Graph Info Panel
The Graph Info panel provides quick, clickable insights into the selected graph’s structure.

## What it shows
- **Graph name**
- **Memory usage** (optional; can be toggled via settings)
- **Node count** and **edge count**
- **Node labels**
- **Edge (relationship) types**
- **Property keys**

## Click-to-explore behavior
The panel is designed for exploration:
- Clicking a **label** runs `MATCH (n:Label) RETURN n`.
- Clicking an **edge type** runs `MATCH p=()-[:TYPE]-() RETURN p`.
- Clicking a **property key** runs a query that finds nodes/edges where that key exists.

It also provides “*” shortcuts:
- **All nodes** (`MATCH (n) RETURN n`)
- **All edges** (`MATCH p=()-[]-() RETURN p`)

## Style customization entrypoint
Next to each label, a palette button opens the **Style Settings** panel for that label.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="How do I explore nodes of a specific label?"
  a1="Click a **label name** in the Graph Info panel. This automatically runs `MATCH (n:Label) RETURN n` and displays the results on the canvas."
  q2="Can I see all edges of a specific relationship type?"
  a2="Yes. Click an **edge type** in the Graph Info panel to run `MATCH p=()-[:TYPE]-() RETURN p` and visualize all relationships of that type."
  q3="What does the memory usage indicator show?"
  a3="It shows the current **memory utilization** of the selected graph in MB. This can be toggled on/off in Browser Settings."
  q4="How do I change the visual style of a label?"
  a4="Click the **palette icon** next to a label in the Graph Info panel to open the Style Settings panel where you can change color and size."
%}

