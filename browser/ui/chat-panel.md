---
title: "Chat Panel"
description: "Natural-language to query workflow, prerequisites (API key/model), and persistence limits."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 14
---

# Chat Panel
The Chat panel lets you use English (natural language) to query the graph.

## Prerequisites
Chat requires configuring:
- An LLM provider API key
- A model

These are set in **Settings → Browser Settings → Chat**.

## Opening the panel
On the Graphs page (`/graph`), click **CHAT** in the left sidebar.

When Chat is opened, element selection is cleared (the side panel is dedicated to chat interactions).

## Message retention
The number of saved interactions is configurable in settings (the UI enforces a bounded range).

{% include faq_accordion.html title="Frequently Asked Questions" q1="What do I need to configure before using Chat?" a1="You need to set an **LLM provider API key** and select a **model** in Settings → Browser Settings → Chat before the Chat panel will work." q2="How do I open the Chat panel?" a2="On the Graphs page (`/graph`), click the **CHAT** toggle in the left sidebar. Note that opening Chat clears any element selection." q3="Can I control how many chat messages are saved?" a3="Yes. The number of saved interactions is configurable in **Settings → Browser Settings → Chat**. The UI enforces a bounded range." q4="Does Chat execute queries on the graph?" a4="Yes. Chat translates your **natural language** input into Cypher queries and executes them against the currently selected graph." %}

