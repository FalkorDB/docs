---
title: "API Docs (Swagger)"
description: "Use the built-in Swagger UI in FalkorDB Browser to explore and test REST API endpoints."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 18
---

# API Docs (Swagger)
FalkorDB Browser includes built-in API documentation at `/docs`.

Use the Authorize flow before running protected endpoints.

## Swagger capabilities

| Feature | Description |
| :--- | :--- |
| Built-in docs | Available at `/docs`. |
| OpenAPI source | Loaded from `/api/swagger`. |
| Interactive testing | Supports authenticated "Try it out" requests. |

## Typical workflow

| Step | Action |
| :--- | :--- |
| 1 | Open `/docs` from the Browser. |
| 2 | Expand the endpoint group and choose an endpoint. |
| 3 | Use Authorize when needed, then run "Try it out". |

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Where are Browser API docs located?"
  a1="Open `/docs` in the Browser app to view Swagger UI."
  q2="Where does Swagger load its schema from?"
  a2="Swagger loads the OpenAPI document from `/api/swagger`."
  q3="Can I test endpoints from the docs page?"
  a3="Yes. Use the built-in interactive execution flow in Swagger."
%}
