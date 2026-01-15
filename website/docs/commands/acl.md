---
title: ACL
description: >
sidebar_position: 100
sidebar_label: ACL
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

```
> ACL HELP
```

#### Output

```
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
    * password:`<password>`: Sets a password for the user.
    * ~`<pattern>`: Restricts access to graphs matching the given pattern.
    * +`<command>`: Grants permission to execute specific commands.
    * -`<command>`: Denies permission to execute specific commands.

#### Example

```
> ACL SETUSER john on >password123 +GRAPH.LIST +GRAPH.RO_QUERY ~*
```

### ACL GETUSER

Retrieves details about a specific user, including permissions and settings.
Syntax

Usage: `ACL GETUSER <username>`

#### Example

```
> ACL GETUSER john
```

#### Output

```
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

```
> ACL DELUSER john
```

### ACL LIST

Lists all users currently configured in the ACL.

Usage: `ACL LIST`

#### Example

```
> ACL LIST
```

#### Output

```
1) "admin"
2) "john"
3) "guest"
```

### ACL LOG

Displays a log of recent ACL-related events, such as user authentication attempts or rule changes.

Usage: `ACL LOG [count]`

    * count: (Optional) Limits the number of entries in the log.

#### Example

```
> ACL LOG 10
```

## Notes

    The ACL command is available only to users with administrative privileges.
    Be cautious when using the nopass rule, as it may compromise security.
    Use specific patterns and commands to enforce the principle of least privilege.
