---
title: "ACL"
nav_order: 100
description: >
    Managing Access Control Lists, enabling administrators to control user permissions at a granular level
parent: "Commands"    
---

# ACL

The ACL command in FalkorDB provides tools for managing Access Control Lists, 
enabling administrators to control user permissions at a granular level. 
This command is crucial for maintaining secure access to your FalkorDB instances.

Usage: `ACL [SUBCOMMAND] [arg1] [arg2] ...`

> **Persisting users:** `ACL SETUSER` only updates the in-memory user table. To make users survive a restart, configure an ACL file and run `ACL SAVE`. See [ACL Persistence on Docker](/operations/durability/acl-persistence) for a complete guide.

## Subcommands

### ACL HELP

Returns a list of all available `ACL` subcommands and their syntax.

Usage: `ACL HELP`

#### Example

```text
> ACL HELP
```

#### Output

```text
1) "GETUSER"
2) "SETUSER"
3) "DELUSER"
4) "LIST"
...
```

### ACL SETUSER

Defines or updates a user's permissions.

Usage: `ACL SETUSER <username> [rule1] [rule2] ...`

#### Rules

    * on / off: Enables or disables the user account.
    * nopass: Allows access without a password.
    * password:<password>: Sets a password for the user.
    * ~<pattern>: Restricts access to graphs matching the given pattern.
    * %<permission>~<pattern>: Restricts access to graphs matching the given pattern with fine-grained read/write permissions. See [Graph permissions](#graph-permissions) below.
    * +<command>: Grants permission to execute specific commands.
    * -<command>: Denies permission to execute specific commands.

#### Graph permissions

In addition to the basic `~<pattern>` rule, ACL supports fine-grained
permissions that restrict how a command is allowed to touch a matching graph.
Graph permission rules take the form `%<permission>~<pattern>`, where
`<permission>` is one or more of the following characters:

* `W` (Write): Data stored within the graph may be updated or deleted (for
  example by `GRAPH.QUERY` running a write Cypher clause, or `GRAPH.DELETE`).
* `R` (Read): Data from the graph is returned to the client (for example by
  `GRAPH.RO_QUERY`, or by `GRAPH.QUERY` running a read-only Cypher clause).
  This does not include graph-level metadata such as the list of existing
  graphs returned by `GRAPH.LIST`.

Permissions can be composed by specifying multiple characters. `%RW~<pattern>`
is full access and is equivalent to plain `~<pattern>`.

##### Example

The basic `~<pattern>` rule grants the same level of access to every matching
graph, so it cannot express different permissions for different graphs that
appear in the same command. For instance, `GRAPH.COPY` reads from a source
graph and writes to a destination graph: with the rules `+@all ~app1:*` alone
there is no way to allow copying from a graph in `app2:*` into `app1:users`
while keeping `app2:*` read-only.

Using graph permissions, the rule set `+@all ~app1:* %R~app2:*` handles this
case: the first pattern matches the destination graph (`app1:users`) with full
access and the second pattern matches the source graph (`app2:users`) with
read-only access.

##### Notes

* Whether a command requires read or write permission on a graph is derived
  from the command's key specifications. Insert, update, and delete flags map
  to the write permission; the access flag maps to the read permission.
  Commands that operate on a graph without a defined logical operation flag
  still require either read or write permission on the graph to execute.
* Side channels to graph data are not considered when evaluating read
  permissions. A command that mutates a graph but only returns metadata about
  the mutation (for example, the count of nodes affected) requires only write
  permission, while a command that mutates a graph and also returns data from
  it requires both read and write permission. If an application must ensure
  that no data is read from a graph, including via side channels, do not
  grant any access to that graph.

#### Example

```text
> ACL SETUSER john on >password123 +GRAPH.LIST +GRAPH.RO_QUERY ~*
```

### ACL GETUSER

Retrieves details about a specific user, including permissions and settings.
Syntax

Usage: `ACL GETUSER <username>`

#### Example

```text
> ACL GETUSER john
```

#### Output

```text
1) "on"
2) ">password123"
3) "+GRAPH.LIST"
4) "+GRAPH.RO_QUERY"
5) "~*"
```

### ACL DELUSER

Deletes a user from the ACL.

Usage: `ACL DELUSER <username>`

#### Example

```text
> ACL DELUSER john
```

### ACL LIST

Lists all users currently configured in the ACL.

Usage: `ACL LIST`

#### Example

```text
> ACL LIST
```

#### Output

```text
1) "admin"
2) "john"
3) "guest"
```

### ACL LOG

Displays a log of recent ACL-related events, such as user authentication attempts or rule changes.

Usage: `ACL LOG [count]`

    * count: (Optional) Limits the number of entries in the log.

#### Example

```text
> ACL LOG 10
```

## Notes

    The ACL command is available only to users with administrative privileges.
    Be cautious when using the nopass rule, as it may compromise security.
    Use specific patterns and commands to enforce the principle of least privilege.

{% include faq_accordion.html title="Frequently Asked Questions" q1="How do I persist ACL users across server restarts?" a1="Use `ACL SAVE` after configuring users with `ACL SETUSER`. You must also configure an ACL file in your server settings. See the [ACL Persistence on Docker](/operations/durability/acl-persistence) guide for details." q2="What is the difference between the ~ and %RW~ key patterns?" a2="The `~<pattern>` rule grants full read-write access to matching graphs. The `%<permission>~<pattern>` syntax allows fine-grained control: `%R~` for read-only, `%W~` for write-only, or `%RW~` for full access (equivalent to `~`)." q3="Can I restrict a user to only run read-only queries?" a3="Yes. Grant only the `GRAPH.RO_QUERY` command and use the `%R~*` permission pattern: `ACL SETUSER reader on >pass +GRAPH.RO_QUERY %R~*`" q4="What happens if a user tries to execute a command they do not have permission for?" a4="The server returns a permission denied error, and the operation is logged in the ACL log (viewable with `ACL LOG`)." q5="Can I grant access to specific graphs only?" a5="Yes. Use key patterns like `~mygraph` for a specific graph or `~app1:*` for all graphs matching a prefix pattern." %}
