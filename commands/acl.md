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
    * +<command>: Grants permission to execute specific commands.
    * -<command>: Denies permission to execute specific commands.

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

### Key permissions

In addition to the basic `~<pattern>` rule, ACL supports fine-grained per-key
permissions that restrict how a command is allowed to touch a matching key.
Key permission rules take the form `%(<permission>)~<pattern>`, where
`<permission>` is one or more of the following characters:

* `W` (Write): The data stored within the key may be updated or deleted.
* `R` (Read): User-supplied data from the key is processed, copied or returned.
  This does not include metadata such as size information (for example
  `STRLEN`), type information (for example `TYPE`), or whether a value exists
  within a collection (for example `SISMEMBER`).

Permissions can be composed by specifying multiple characters. `%RW~<pattern>`
is full access and is equivalent to plain `~<pattern>`.

#### Example

Consider a user with the rules `+@all ~app1:* (+@read ~app2:*)`. This grants
full access on `app1:*` and read-only access on `app2:*`. However, commands
such as `COPY` read from a source key and write to a destination key, so a
request to copy `app2:user` into `app1:user` would be rejected because neither
the root permission nor the selector fully matches the command. Using key
permissions, the rule set `+@all ~app1:* %R~app2:*` handles this case: the
first pattern matches the destination key with write access and the second
pattern matches the source key with read access.

#### Notes

* Whether a command requires read or write permission on a key is derived from
  the command's key specifications. Insert, update, and delete flags map to
  the write permission; the access flag maps to the read permission. Commands
  with no logical operation flags (for example `EXISTS`) require either read
  or write permission on the key to execute.
* Side channels to user data are not considered when evaluating read
  permissions. For example, `LPUSH key1 data` modifies `key1` but only returns
  metadata (the new list size), so it requires only write permission on
  `key1`. `LPOP key2` modifies `key2` and also returns data from it (the
  left-most item), so it requires both read and write permission on `key2`.
  If an application needs to ensure no data is accessed from a key, including
  via side channels, do not grant any access to the key.

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
