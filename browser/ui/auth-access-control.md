---
title: "Roles & Access"
description: "How authentication and role-based permissions affect FalkorDB Browser features."
parent: "UI Elements"
grand_parent: "Browser"
nav_order: 16
---

# Roles & Access
Browser authentication and authorization control which actions are available to each user.

![Read-only user connected](../../images/browser/read-only-user-connected.png)

## Authentication model

| Feature | Description |
| :--- | :--- |
| Authentication | Uses NextAuth (credentials-backed authentication flow). |
| Session-based access | UI and API capabilities are enabled based on user role. |

## Role-aware behavior

| Role capability | Description |
| :--- | :--- |
| Read-Only restrictions | Read-Only users cannot create graphs. |
| Admin-only settings | Admin users can access DB Configurations and Users management. |

For login details, see [Login Screen](./login.md).

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Can Read-Only users create graphs?"
  a1="No. Graph creation actions are not available to Read-Only users."
  q2="What is Admin-only in the Browser UI?"
  a2="Admins can manage DB configurations and users from Settings."
  q3="Is Browser access role-based?"
  a3="Yes. The UI exposes actions according to the authenticated user's role."
%}
