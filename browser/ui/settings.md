---
title: "Settings Page"
description: "Browser settings, tutorial replay, personal access tokens, and admin sections (DB configurations, users)."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 3
---

# Settings Page

Settings (`/settings`) manages Browser behavior and security/admin tools.

## Tabs

- Browser Settings
- Personal Access Tokens
- DB Configurations (admin only, online)
- Users (admin only, online)

Unsaved Browser Settings changes trigger save/discard confirmation on tab change or navigation.

## Browser Settings sections

### Query Execution

- Timeout
- Result limit
- Run default query
- Default query text

### User Experience

- Content persistence
- Caption key priority and property key prefix display
- Table sizing settings

### Graph Info

- Refresh interval
- Search threshold behavior

### Chat

- Model source: API key or local
- Local provider: Ollama or LM Studio
- Local endpoint
- Model selection
- Message retention count
- Cypher-only mode

### Replay Tutorial

- Re-runs onboarding tutorial flow.

## Personal Access Tokens

- Create token with optional expiration
- One-time token reveal/copy
- List and revoke active tokens

## DB Configurations (Admin)

- View and update supported DB config values

## Users (Admin)

- Add, edit, and delete users
- Role and key/graph permission management
