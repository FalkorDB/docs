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

{% capture shell_0 %}
ACL HELP
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
help_text = client.execute_command('ACL', 'HELP')
print(help_text)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const helpText = await client.sendCommand(['ACL', 'HELP']);
console.log(helpText);
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
Object helpText = client.sendCommand("ACL", "HELP");
System.out.println(helpText);
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
let help_text = client.execute_command(&["ACL", "HELP"])?;
println!("{:?}", help_text);
{% endcapture %}

{% include code_tabs.html id="acl_help_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}

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
    * password:<password>: Sets a password for the user.
    * ~<pattern>: Restricts access to graphs matching the given pattern.
    * +<command>: Grants permission to execute specific commands.
    * -<command>: Denies permission to execute specific commands.

#### Example

{% capture shell_1 %}
ACL SETUSER john on >password123 +GRAPH.LIST +GRAPH.RO_QUERY ~*
{% endcapture %}

{% capture python_1 %}
from falkordb import FalkorDB
client = FalkorDB()
result = client.execute_command('ACL', 'SETUSER', 'john', 'on', '>password123', '+GRAPH.LIST', '+GRAPH.RO_QUERY', '~*')
print(result)
{% endcapture %}

{% capture javascript_1 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const result = await client.sendCommand(['ACL', 'SETUSER', 'john', 'on', '>password123', '+GRAPH.LIST', '+GRAPH.RO_QUERY', '~*']);
console.log(result);
{% endcapture %}

{% capture java_1 %}
FalkorDB client = new FalkorDB();
Object result = client.sendCommand("ACL", "SETUSER", "john", "on", ">password123", "+GRAPH.LIST", "+GRAPH.RO_QUERY", "~*");
System.out.println(result);
{% endcapture %}

{% capture rust_1 %}
let client = FalkorDB::connect_default();
let result = client.execute_command(&["ACL", "SETUSER", "john", "on", ">password123", "+GRAPH.LIST", "+GRAPH.RO_QUERY", "~*"])?;
println!("{:?}", result);
{% endcapture %}

{% include code_tabs.html id="setuser_tabs" shell=shell_1 python=python_1 javascript=javascript_1 java=java_1 rust=rust_1 %}

### ACL GETUSER

Retrieves details about a specific user, including permissions and settings.
Syntax

Usage: `ACL GETUSER <username>`

#### Example

{% capture shell_2 %}
ACL GETUSER john
{% endcapture %}

{% capture python_2 %}
from falkordb import FalkorDB
client = FalkorDB()
user_info = client.execute_command('ACL', 'GETUSER', 'john')
print(user_info)
{% endcapture %}

{% capture javascript_2 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const userInfo = await client.sendCommand(['ACL', 'GETUSER', 'john']);
console.log(userInfo);
{% endcapture %}

{% capture java_2 %}
FalkorDB client = new FalkorDB();
Object userInfo = client.sendCommand("ACL", "GETUSER", "john");
System.out.println(userInfo);
{% endcapture %}

{% capture rust_2 %}
let client = FalkorDB::connect_default();
let user_info = client.execute_command(&["ACL", "GETUSER", "john"])?;
println!("{:?}", user_info);
{% endcapture %}

{% include code_tabs.html id="getuser_tabs" shell=shell_2 python=python_2 javascript=javascript_2 java=java_2 rust=rust_2 %}

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

{% capture shell_3 %}
ACL DELUSER john
{% endcapture %}

{% capture python_3 %}
from falkordb import FalkorDB
client = FalkorDB()
result = client.execute_command('ACL', 'DELUSER', 'john')
print(result)
{% endcapture %}

{% capture javascript_3 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const result = await client.sendCommand(['ACL', 'DELUSER', 'john']);
console.log(result);
{% endcapture %}

{% capture java_3 %}
FalkorDB client = new FalkorDB();
Object result = client.sendCommand("ACL", "DELUSER", "john");
System.out.println(result);
{% endcapture %}

{% capture rust_3 %}
let client = FalkorDB::connect_default();
let result = client.execute_command(&["ACL", "DELUSER", "john"])?;
println!("{:?}", result);
{% endcapture %}

{% include code_tabs.html id="deluser_tabs" shell=shell_3 python=python_3 javascript=javascript_3 java=java_3 rust=rust_3 %}

### ACL LIST

Lists all users currently configured in the ACL.

Usage: `ACL LIST`

#### Example

{% capture shell_4 %}
ACL LIST
{% endcapture %}

{% capture python_4 %}
from falkordb import FalkorDB
client = FalkorDB()
users = client.execute_command('ACL', 'LIST')
print(users)
{% endcapture %}

{% capture javascript_4 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const users = await client.sendCommand(['ACL', 'LIST']);
console.log(users);
{% endcapture %}

{% capture java_4 %}
FalkorDB client = new FalkorDB();
Object users = client.sendCommand("ACL", "LIST");
System.out.println(users);
{% endcapture %}

{% capture rust_4 %}
let client = FalkorDB::connect_default();
let users = client.execute_command(&["ACL", "LIST"])?;
println!("{:?}", users);
{% endcapture %}

{% include code_tabs.html id="list_tabs" shell=shell_4 python=python_4 javascript=javascript_4 java=java_4 rust=rust_4 %}

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

{% capture shell_5 %}
ACL LOG 10
{% endcapture %}

{% capture python_5 %}
from falkordb import FalkorDB
client = FalkorDB()
log_entries = client.execute_command('ACL', 'LOG', '10')
print(log_entries)
{% endcapture %}

{% capture javascript_5 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const logEntries = await client.sendCommand(['ACL', 'LOG', '10']);
console.log(logEntries);
{% endcapture %}

{% capture java_5 %}
FalkorDB client = new FalkorDB();
Object logEntries = client.sendCommand("ACL", "LOG", "10");
System.out.println(logEntries);
{% endcapture %}

{% capture rust_5 %}
let client = FalkorDB::connect_default();
let log_entries = client.execute_command(&["ACL", "LOG", "10"])?;
println!("{:?}", log_entries);
{% endcapture %}

{% include code_tabs.html id="log_tabs" shell=shell_5 python=python_5 javascript=javascript_5 java=java_5 rust=rust_5 %}

## Notes

    The ACL command is available only to users with administrative privileges.
    Be cautious when using the nopass rule, as it may compromise security.
    Use specific patterns and commands to enforce the principle of least privilege.
