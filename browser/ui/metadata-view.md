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


{% include faq_accordion.html title="Frequently Asked Questions" q1="What is the difference between Explain and Profile?" a1="**Explain** shows the planned execution steps without running the query. **Profile** actually executes the query and shows real performance data including time spent at each step." q2="When is the Metadata tab available?" a2="The Metadata tab is enabled when the current query has **metadata or explain content** available. It appears alongside the Graph and Table tabs in the results area." q3="Is Profile safe to run on production?" a3="Be cautious — profiling **actually executes the query** and can be intrusive depending on database behavior and query complexity. Use Explain for a non-invasive execution plan." q4="How is the execution plan displayed?" a4="Both Explain and Profile output are rendered as a **nested tree** structure, showing the hierarchy of operations in the query execution plan." %}
