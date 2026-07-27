---
title: "UI Elements"
description: "Detailed documentation for FalkorDB Browser UI screens, panels, and interactions."
parent: "Browser"
nav_order: 1
has_children: true
---

# UI Elements
This section breaks down FalkorDB Browser’s UI into focused pages so you can quickly learn what each screen/panel does and how to use it.

The screenshots across this section use the same demo graph so the pages line up with one another.

## Screenshot set
- [Login screen](../../images/browser/login-screen.png)
- [Main graph overview](../../images/browser/overview.png)
- [Graph info panel](../../images/browser/graph-info.png)
- [Query editor](../../images/browser/query-editor.png)
- [Query history](../../images/browser/query-history.png)
- [Upload Data (Load CSV - step 1)](../../images/browser/upload-data-load-csv-step1.png)
- [Upload Data (Load CSV - step 2)](../../images/browser/upload-data-load-csv-step2.png)
- [Upload Data (Cypher batch)](../../images/browser/upload-data-cypher-batch.png)
- [Table view](../../images/browser/table-view.png)
- [Metadata view](../../images/browser/metadata-view.png)
- [Data / property panel](../../images/browser/data-panel.png)
- [Style panel](../../images/browser/style-panel.png)
- [Chat panel](../../images/browser/chat-panel.png)
- [Settings page](../../images/browser/settings-page.png)
- [UDF Libraries page](../../images/browser/udf-libraries.png)

## Authentication
- [Login Screen](./login.md)

## Navigation & global controls
- [Navigation, theme toggle, and header](./navigation.md)

## Settings
- [Settings page (Browser settings, admin tools, tokens, tutorial)](./settings.md)

## UDF management
- [UDF Libraries page](./udf-libraries.md)

## Graph workspace
- [Graph page (overall layout)](./graph-page.md)
- [Main graph canvas](./graph-canvas.md)
- [Graph Info panel](./graph-info-panel.md)
- [Style panel (Customize label styles)](./style-panel.md)
- [Data / Property panel](./data-panel.md)
- [Graph toolbar & element actions](./toolbar-actions.md)
- [Chat panel (natural-language to Cypher)](./chat-panel.md)

## Querying & results
- [Query editor](./query-editor.md)
- [Query history](./query-history.md)
- [Upload Data dialog](./upload-data.md)
- [Table view](./table-view.md)
- [Metadata view (Explain/Profile/Metadata)](./metadata-view.md)

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What are the main sections of the FalkorDB Browser UI?"
  a1="The UI is organized into **Authentication** (login), **Navigation & global controls**, **Settings**, **Graph workspace** (canvas, panels, toolbar, chat), and **Querying & results** (editor, history, table, metadata)."
  q2="Where do I find graph visualization controls?"
  a2="Graph visualization controls are on the **Graph page**. See the [Main graph canvas](./graph-canvas.md) and [Graph toolbar](./toolbar-actions.md) pages for details on pan/zoom, selection, and element actions."
  q3="How do I customize the appearance of nodes?"
  a3="Use the [Style panel](./style-panel.md) to change node colors and sizes per label. Open it from the Graph Info panel by clicking the palette icon next to a label."
%}
