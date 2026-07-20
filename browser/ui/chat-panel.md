---
title: "Chat Panel"
description: "Natural-language to query workflow, LLM connection setup, and persistence limits."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 14
---

# Chat Panel

Chat panel supports natural-language interaction for graph querying workflows.

## Requirements

- Active graph selected
- Chat model configured in Settings
- Valid API key or reachable local LLM endpoint

## Features

- Markdown-rendered assistant messages
- Generated Cypher snippets and execution actions
- Message status/result events
- Confidence badge rendering when provided
- Per-graph chat history persistence

## Model sources

- API key providers
- Local providers (Ollama, LM Studio)
- Optional cypher-only mode
