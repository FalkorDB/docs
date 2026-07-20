---
title: "Login Screen"
description: "How to connect FalkorDB Browser to a FalkorDB server (manual fields, URL mode, TLS/CA)."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 1
---

# Login Screen

Login creates a Browser session and connects to a FalkorDB instance.

## Connection modes

- Manual Configuration
- FalkorDB URL

## Manual Configuration fields

- Host
- Port
- Username (optional)
- Password (optional)
- TLS toggle
- CA certificate upload (when TLS is enabled)

## URL mode

URL mode parses host, port, credentials, and TLS from a connection URL.

## Behavior

- Success: navigates to `/graph`
- Failure: shows inline credentials/connection error
- Login page also links to built-in API docs at `/docs`
