---
title: "Query Editor"
description: "Cypher editor: run shortcuts, autocomplete, maximize mode, placeholder behavior, and graph-scoped suggestions."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 9
---

# Query Editor
The query editor is a Monaco-based Cypher editor used to run queries against the selected graph.

## Running queries
- Click **RUN** to execute.
- Keyboard shortcuts:
  - **Enter**: run query (when the suggestion widget is not open)
  - **Cmd/Ctrl + Enter**: run query
  - **Shift + Enter**: insert a newline

## Query history navigation (keyboard)
When your cursor is on the **first line** or **last line** of the editor:
- **Up arrow**: navigate backward through query history
- **Down arrow**: navigate forward through query history

## Autocomplete & syntax highlighting
The editor provides:
- Cypher keyword suggestions
- Function suggestions
- Graph-scoped suggestions (labels, relationship types, property keys) fetched from the server

## Maximize mode
The maximize button opens a full-screen editor dialog with the same Run/Clear controls.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What keyboard shortcuts are available for running queries?"
  a1="Press **Enter** to run a query (only when the autocomplete suggestion widget is closed) or **Cmd/Ctrl + Enter** to run regardless. Use **Shift + Enter** to insert a newline without executing."
  q2="Does the editor support autocomplete?"
  a2="Yes. The Monaco-based editor provides **Cypher keyword suggestions**, **function suggestions**, and **graph-scoped suggestions** (labels, relationship types, property keys) fetched from the server."
  q3="How do I navigate through previous queries using the keyboard?"
  a3="Place your cursor on the **first line** and press **Up arrow** to go back through history, or on the **last line** and press **Down arrow** to go forward."
  q4="Can I expand the editor to full screen?"
  a4="Yes. Click the **maximize button** to open a full-screen editor dialog with the same Run and Clear controls."
%}

