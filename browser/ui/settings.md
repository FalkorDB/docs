---
title: "Settings Page"
description: "Browser settings, tutorial replay, personal access tokens, and admin sections (DB configurations, users)."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 3
---

# Settings Page
The Settings page (`/settings`) is where you configure Browser behavior and manage security/admin features.

## Tabs / sections
The Settings page is organized into these sections:
- **Browser Settings** (all users)
- **Personal Access Tokens** (all users)
- **DB Configurations** (Admin only; requires online connection)
- **Users** (Admin only; requires online connection)

If you navigate away from **Browser Settings** while there are unsaved changes, the UI prompts you to **Save** or **Discard** changes.

## Browser Settings
The Browser Settings panel is a page that can be scrolled, with grouped sections (collapsed/expanded in the UI). Common settings include:
- **Query execution**
  - Query timeout
  - Result limits
  - Default query behavior (run a default query when selecting a graph)
- **User experience**
  - Content persistence (restores the last used graph + query from localStorage)
  - Node caption priority keys (controls how node labels/captions are picked)
  - Property-key display options (e.g. prefix behavior)
- **Graph Info**
  - Refresh interval (how often graph info refreshes)
- **Chat**
  - LLM provider API key
  - Model selection
  - How many interactions to store locally

### Replay Tutorial
Browser Settings includes a **Replay Tutorial** action, which re-runs the guided tour overlay.

## Personal Access Tokens
The Tokens section provides a UI to:
- Create tokens (often with optional expiry)
- View/revoke existing tokens

## Admin-only sections
### DB Configurations (Admin)
Allows viewing/updating database configuration values via the server API.

### Users (Admin)
Allows:
- Viewing users
- Changing roles
- Adding/removing users

## Keyboard shortcut
- `Esc` navigates back (with a save/discard prompt if there are unsaved Browser Settings changes).

