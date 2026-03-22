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
db = FalkorDB()
help_text = db.connection.acl_help()
print(help_text)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const db = await FalkorDB.connect();
const helpText = await db.connection.aclHelp();
console.log(helpText);
{% endcapture %}

{% capture java_0 %}
Driver driver = FalkorDB.driver("localhost", 6379);
try (Jedis jedis = driver.getConnection()) {
    List<String> helpText = jedis.aclHelp();
    System.out.println(helpText);
}
{% endcapture %}

{% capture rust_0 %}
let client = redis::Client::open("redis://127.0.0.1/")?;
let mut con = client.get_connection()?;
let help: Vec<String> = redis::cmd("ACL").arg("HELP").query(&mut con)?;
println!("{:?}", help);
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
db = FalkorDB()
result = db.connection.acl_setuser(
    'john',
    enabled=True,
    passwords=['password123'],
    commands=['+GRAPH.LIST', '+GRAPH.RO_QUERY'],
    keys=['*']
)
print(result)
{% endcapture %}

{% capture javascript_1 %}
import { FalkorDB } from 'falkordb';
const db = await FalkorDB.connect();
const result = await db.connection.aclSetUser('john', 'on', '>password123', '+GRAPH.LIST', '+GRAPH.RO_QUERY', '~*');
console.log(result);
{% endcapture %}

{% capture java_1 %}
Driver driver = FalkorDB.driver("localhost", 6379);
try (Jedis jedis = driver.getConnection()) {
    String result = jedis.aclSetUser("john", "on", ">password123", "+GRAPH.LIST", "+GRAPH.RO_QUERY", "~*");
    System.out.println(result);
}
{% endcapture %}

{% capture rust_1 %}
let client = redis::Client::open("redis://127.0.0.1/")?;
let mut con = client.get_connection()?;
let result: String = redis::cmd("ACL").arg("SETUSER").arg("john")
    .arg("on").arg(">password123").arg("+GRAPH.LIST").arg("+GRAPH.RO_QUERY").arg("~*")
    .query(&mut con)?;
println!("{}", result);
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
db = FalkorDB()
user_info = db.connection.acl_getuser('john')
print(user_info)
{% endcapture %}

{% capture javascript_2 %}
import { FalkorDB } from 'falkordb';
const db = await FalkorDB.connect();
const userInfo = await db.connection.aclGetUser('john');
console.log(userInfo);
{% endcapture %}

{% capture java_2 %}
Driver driver = FalkorDB.driver("localhost", 6379);
try (Jedis jedis = driver.getConnection()) {
    AccessControlUser userInfo = jedis.aclGetUser("john");
    System.out.println(userInfo);
}
{% endcapture %}

{% capture rust_2 %}
let client = redis::Client::open("redis://127.0.0.1/")?;
let mut con = client.get_connection()?;
let user_info: Vec<String> = redis::cmd("ACL").arg("GETUSER").arg("john").query(&mut con)?;
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
db = FalkorDB()
result = db.connection.acl_deluser('john')
print(result)
{% endcapture %}

{% capture javascript_3 %}
import { FalkorDB } from 'falkordb';
const db = await FalkorDB.connect();
const result = await db.connection.aclDelUser('john');
console.log(result);
{% endcapture %}

{% capture java_3 %}
Driver driver = FalkorDB.driver("localhost", 6379);
try (Jedis jedis = driver.getConnection()) {
    long result = jedis.aclDelUser("john");
    System.out.println(result);
}
{% endcapture %}

{% capture rust_3 %}
let client = redis::Client::open("redis://127.0.0.1/")?;
let mut con = client.get_connection()?;
let result: i64 = redis::cmd("ACL").arg("DELUSER").arg("john").query(&mut con)?;
println!("{}", result);
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
db = FalkorDB()
users = db.connection.acl_list()
print(users)
{% endcapture %}

{% capture javascript_4 %}
import { FalkorDB } from 'falkordb';
const db = await FalkorDB.connect();
const users = await db.connection.aclList();
console.log(users);
{% endcapture %}

{% capture java_4 %}
Driver driver = FalkorDB.driver("localhost", 6379);
try (Jedis jedis = driver.getConnection()) {
    List<String> users = jedis.aclList();
    System.out.println(users);
}
{% endcapture %}

{% capture rust_4 %}
let client = redis::Client::open("redis://127.0.0.1/")?;
let mut con = client.get_connection()?;
let users: Vec<String> = redis::cmd("ACL").arg("LIST").query(&mut con)?;
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
db = FalkorDB()
log_entries = db.connection.acl_log(count=10)
print(log_entries)
{% endcapture %}

{% capture javascript_5 %}
import { FalkorDB } from 'falkordb';
const db = await FalkorDB.connect();
const logEntries = await db.connection.aclLog(10);
console.log(logEntries);
{% endcapture %}

{% capture java_5 %}
Driver driver = FalkorDB.driver("localhost", 6379);
try (Jedis jedis = driver.getConnection()) {
    List<AccessControlLogEntry> logEntries = jedis.aclLog(10);
    System.out.println(logEntries);
}
{% endcapture %}

{% capture rust_5 %}
let client = redis::Client::open("redis://127.0.0.1/")?;
let mut con = client.get_connection()?;
let log_entries: Vec<Vec<String>> = redis::cmd("ACL").arg("LOG").arg("10").query(&mut con)?;
println!("{:?}", log_entries);
{% endcapture %}

{% include code_tabs.html id="log_tabs" shell=shell_5 python=python_5 javascript=javascript_5 java=java_5 rust=rust_5 %}

## Notes

    The ACL command is available only to users with administrative privileges.
    Be cautious when using the nopass rule, as it may compromise security.
    Use specific patterns and commands to enforce the principle of least privilege.
