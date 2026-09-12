---
title: "User Management"
parent: "Cloud DBaaS"
nav_order: 7
description: "Guide to managing database users on a FalkorDB Cloud instance. Learn how to create, update, and delete users, assign roles, and apply custom Redis ACL rules."
---

# User Management

FalkorDB Cloud lets you manage database users directly from the instance page. You can create additional users, assign them predefined roles or custom Redis ACL rules, update their credentials or permissions, and delete users you no longer need.

> **Prerequisite:** The instance must be in a **running** state before you can manage its users.

---

## Opening the User Access Tab

1. Go to [app.falkordb.cloud](https://app.falkordb.cloud) and sign in.
2. Select your instance from the list.
3. Click the **User Access** tab on the instance detail page.

The tab shows a table of all users configured on the instance, along with their assigned role or ACL rule.

---

## Default User

Every instance has a **default user** that is created automatically during deployment. This user cannot be deleted — its credentials can only be changed by modifying the instance configuration.

---

## Creating a User

1. From the **User Access** tab, click **Add User**.
2. Fill in the required fields:
   - **Username** — the login name for the new user.
   - **Password** — a secure password for the user.
3. Assign permissions using one of the two options:
   - **Predefined role** — select one of the built-in roles from the dropdown:
     - `Admin` — full read/write access and user management.
     - `Read-Write` — full read/write access to graphs.
     - `Read-Only` — read-only access to graphs.
   - **Custom ACL** — enter a Redis ACL rule string directly to define fine-grained access control. See [ACL](/commands/acl) for available rule syntax.
4. Click **Save** to create the user.

---

## Updating a User

1. From the **User Access** tab, locate the user you want to update in the table.
2. Click the **Edit** (pencil) icon next to the user.
3. Modify the **password**, **role**, or **custom ACL** as needed.
4. Click **Save** to apply the changes.

---

## Deleting a User

1. From the **User Access** tab, locate the user you want to remove.
2. Click the **Delete** (trash) icon next to the user.
3. Confirm the deletion in the dialog that appears.

> The **default user** cannot be deleted.

---

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Can I delete the default user?"
  a1="No. The default user is created during deployment and cannot be deleted. Its credentials can only be changed by modifying the instance configuration."
  q2="What predefined roles are available?"
  a2="Three predefined roles are available: **Admin** (full access including user management), **Read-Write** (full graph read/write), and **Read-Only** (graph read access only)."
  q3="How do I apply fine-grained access control?"
  a3="Select **Custom ACL** when creating or editing a user and enter a Redis ACL rule string. See the [ACL command reference](/commands/acl) for the full rule syntax."
  q4="Does the instance need to be running to manage users?"
  a4="Yes. The instance must be in a **running** state before you can open the User Access tab and make changes."
  q5="Can I change a user's password after creation?"
  a5="Yes. Click the **Edit** icon next to the user in the User Access tab, enter a new password, and save."
%}
