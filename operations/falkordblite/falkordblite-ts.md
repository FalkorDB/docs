---
title: "FalkorDBLite (TypeScript)"
nav_order: 2
parent: "FalkorDBLite"
grand_parent: "Operations"
description: "Embedded FalkorDB runtime for Node.js and TypeScript"
---

# FalkorDBLite for TypeScript

FalkorDBLite for Node.js/TypeScript launches an embedded `redis-server` with the FalkorDB module and returns a connected FalkorDB client. It is ideal for local development, demos, CI jobs, or small apps that want a zero-config graph database that starts and stops with the application.

## Requirements

- Node.js 20 or later
- Ability to download the FalkorDB module during `npm install`
- Linux x64 and macOS arm64 are supported; Windows users should run under WSL2 or use a remote server

## Installation

```bash
npm install falkordblite

# Optional: also install the remote client when you plan to connect to an external server
npm install falkordb
```

## Quick start

```ts
import { FalkorDB } from 'falkordblite';

const db = await FalkorDB.open();
const graph = db.selectGraph('quickstart');

await graph.query('CREATE (p:Person {name: "Ada"})');
const result = await graph.roQuery('MATCH (p:Person) RETURN p.name');
console.log(result.data); // => [ [ 'Ada' ] ]

await db.close();
```

## Persist data between runs

Provide a path to keep data on disk. When set, FalkorDBLite enables periodic snapshots automatically.

```ts
const db = await FalkorDB.open({ path: '/tmp/falkordb-lite' });
const graph = db.selectGraph('inventory');
await graph.query('CREATE (:Product {id: 1, name: \"Laptop\"})');
await db.close();
```

## Work with multiple graphs

Use separate graph IDs to isolate datasets within the same embedded instance.

```ts
const db = await FalkorDB.open();

const users = db.selectGraph('users');
const orders = db.selectGraph('orders');

await users.query('CREATE (:User {id: 1, email: \"a@example.com\"})');
await orders.query('CREATE (:Order {id: 10, total: 99.5})');

await db.close();
```

## Configuration options

Set options on `FalkorDB.open()` to control the embedded server:

| Option | Type | Default | Purpose |
| --- | --- | --- | --- |
| `path` | `string` | temp dir | Data directory; enables persistence and snapshots. |
| `redisServerPath` | `string` | auto | Use a custom `redis-server` binary. |
| `modulePath` | `string` | auto | Use a custom FalkorDB module (`.so`) path. |
| `maxMemory` | `string` | unset | Redis `maxmemory`, e.g. `"256mb"`. |
| `logLevel` | `'debug' \| 'verbose' \| 'notice' \| 'warning'` | unset | Redis log level. |
| `logFile` | `string` | stdout | Where the embedded server logs. |
| `timeout` | `number` | `10000` | Startup timeout in milliseconds. |
| `additionalConfig` | `Record<string, string>` | none | Extra redis.conf entries (e.g. `{ port: '6379' }`). |
| `falkordbVersion` | `string` | `v4.16.3` | FalkorDB module release tag to download. |
| `inheritStdio` | `boolean` | `false` | Pipe `redis-server` output to the parent process. |

The FalkorDB client returned by `selectGraph()` exposes the full FalkorDB Graph API (query, `roQuery`, indexes, constraints, profiling, etc.).

## Migrate to a remote FalkorDB server

Keep your graph logic and swap only the connection line:

```ts
// Embedded
import { FalkorDB } from 'falkordblite';
const db = await FalkorDB.open();

// Remote
import { FalkorDB as RemoteFalkorDB } from 'falkordb';
const remote = await RemoteFalkorDB.connect({
  socket: { host: '127.0.0.1', port: 6379 },
});
```

## Resources

- [falkordblite-ts on GitHub](https://github.com/FalkorDB/falkordblite-ts)
- [Package on npm](https://www.npmjs.com/package/falkordblite)
- [Troubleshooting guide](https://github.com/FalkorDB/falkordblite-ts/blob/main/TROUBLESHOOTING.md)
