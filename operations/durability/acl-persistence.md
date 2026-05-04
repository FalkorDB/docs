---
title: "ACL Persistence on Docker"
nav_order: 2
description: "Run FalkorDB in Docker with persistent Access Control List (ACL) users by mounting an external ACL file so users, passwords, and permissions survive container restarts and recreations."
parent: "Durability"
grand_parent: "Operations"
---

# Persisting ACL Users in FalkorDB on Docker

By default, ACL users you create with `ACL SETUSER` live only in memory. As soon as you restart the container — and certainly if you `docker rm` it — the users are gone and only the `default` user remains.

This guide shows how to configure FalkorDB so that ACL users, hashed passwords, and permissions are stored on disk and reloaded automatically on every restart.

## How It Works

Redis (and therefore FalkorDB) supports two ways of storing ACL users:

1. Inline in `redis.conf` (rewritten with `CONFIG REWRITE`).
2. In a dedicated **ACL file** referenced by the `aclfile` directive, written with `ACL SAVE`.

When `aclfile` is set, Redis uses the file as the single source of truth for users at startup, and `ACL SAVE` will persist any in-memory changes back to it. This is the approach we use here, because it works cleanly with the FalkorDB Docker image (which doesn't ship a writable `redis.conf`).

## Prerequisites

* Docker installed.
* The `falkordb/falkordb` (or `falkordb/falkordb-server`) image.
* `redis-cli` available locally for testing.

## Step 1: Prepare the Host Directory and ACL File

Create a directory on the host that will be bind-mounted into the container, and create an empty ACL file inside it. The file must exist before the container starts — Redis will refuse to start if `aclfile` points to a missing file.

```bash
mkdir -p ~/falkordb/data
touch ~/falkordb/data/users.acl
```

## Step 2: Start FalkorDB With an ACL File

Pass `--aclfile` (and optionally `--appendonly yes` for data persistence) through the `REDIS_ARGS` environment variable. The FalkorDB entrypoint forwards `REDIS_ARGS` to `redis-server`.

```bash
docker run -d --name falkordb \
  -p 6379:6379 \
  -v ~/falkordb/data:/var/lib/falkordb/data \
  -e REDIS_ARGS="--appendonly yes --aclfile /var/lib/falkordb/data/users.acl" \
  falkordb/falkordb:latest
```

**Why this works:**

- `-v ~/falkordb/data:/var/lib/falkordb/data` bind-mounts the host directory into FalkorDB's default data directory, so both the AOF/RDB files and `users.acl` live on the host.
- `--aclfile /var/lib/falkordb/data/users.acl` tells Redis to load users from — and `ACL SAVE` to write users to — that file.
- `--appendonly yes` enables AOF so that the graph data is also durable. See [Data Durability](/operations/durability) for the full set of options.

Verify the container picked up the configuration:

```bash
redis-cli CONFIG GET aclfile
# 1) "aclfile"
# 2) "/var/lib/falkordb/data/users.acl"
```

## Step 3: Create ACL Users and Save Them

Connect with `redis-cli` and create some users:

```bash
redis-cli ACL SETUSER alice on '>secret123' '~*' '&*' '+@all'
redis-cli ACL SETUSER bob   on '>bobpass'   '~bob:*' '+@read' '+GRAPH.QUERY' '+GRAPH.RO_QUERY'
```

> **Important:** `ACL SETUSER` only updates the in-memory user table. You must run `ACL SAVE` to write the changes to the ACL file. If `aclfile` is not configured, `ACL SAVE` returns a clear error:
>
> ```text
> (error) ERR This Redis instance is not configured to use an ACL file. You may want to
> specify users via the ACL SETUSER command and then issue a CONFIG REWRITE (assuming you
> have a Redis configuration file set) in order to store users in the Redis configuration.
> ```
>
> If you see this error, check that `--aclfile` was passed (e.g. via `REDIS_ARGS`) and that the file existed on disk before the container started.

Persist the users to disk:

```bash
redis-cli ACL SAVE
# OK
```

Inspect the file on the host:

```bash
cat ~/falkordb/data/users.acl
# user alice on sanitize-payload #fcf730b6...e4 ~* &* +@all
# user bob   on sanitize-payload #da7655b5...a1 ~bob:* resetchannels -@all +@read +graph.query +graph.ro_query
# user default on nopass sanitize-payload ~* &* +@all
```

## Step 4: Verify Persistence Across Restarts

Restart — or even fully recreate — the container, then confirm the users are still there:

```bash
docker restart falkordb
sleep 2

redis-cli ACL LIST
# 1) "user alice on sanitize-payload #... ~* &* +@all"
# 2) "user bob on sanitize-payload #... ~bob:* resetchannels -@all +@read +graph.query +graph.ro_query"
# 3) "user default on nopass sanitize-payload ~* &* +@all"

redis-cli --user alice --pass secret123 --no-auth-warning PING
# PONG
```

To prove the users survive a full container removal, not just a restart:

```bash
docker rm -f falkordb

docker run -d --name falkordb \
  -p 6379:6379 \
  -v ~/falkordb/data:/var/lib/falkordb/data \
  -e REDIS_ARGS="--appendonly yes --aclfile /var/lib/falkordb/data/users.acl" \
  falkordb/falkordb:latest

sleep 2
redis-cli ACL LIST
```

The `alice` and `bob` users (along with their hashed passwords and rules) are reloaded from `users.acl`.

## Docker Compose Example

```yaml
services:
  falkordb:
    image: falkordb/falkordb:latest
    container_name: falkordb
    ports:
      - "6379:6379"
    volumes:
      - ./data:/var/lib/falkordb/data
    environment:
      REDIS_ARGS: "--appendonly yes --aclfile /var/lib/falkordb/data/users.acl"
    restart: unless-stopped
```

Before the first `docker compose up`, create the ACL file so Redis can open it:

```bash
mkdir -p ./data && touch ./data/users.acl
docker compose up -d
```

## Operational Notes

- **Always run `ACL SAVE` after changes.** `ACL SETUSER`, `ACL DELUSER`, and `ACL SETUSER ... reset` only affect memory until you persist them.
- **Disable the `default` user in production.** Once your real users exist, lock it down: `ACL SETUSER default off`. Make sure at least one administrative user with `+@all` permissions remains enabled.
- **Protect the ACL file.** It contains password hashes. Restrict host filesystem permissions: `chmod 600 ~/falkordb/data/users.acl`.
- **Snap-installed Docker.** If your Docker Engine was installed via Snap, bind mounts only work under your home directory — paths like `/tmp/...` will appear empty inside the container.
- **Mixing inline and file-based ACLs.** When `aclfile` is set, you cannot also set `user` directives in `redis.conf`. Choose one mechanism.

## Related

- [Persistence on Docker](/operations/durability/persistence) — persisting graph data with volumes and verifying data durability.
- [Data Durability](/operations/durability) — RDB/AOF configuration.
- [ACL command reference](/commands/acl) — all ACL subcommands.
- [Redis ACL documentation](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/) — full rule syntax.

{% include faq_accordion.html title="Frequently Asked Questions" q1="Why do my ACL users disappear after restarting the container?" a1="By default, ACL users live only in memory. You must configure `--aclfile /path/to/users.acl` via `REDIS_ARGS` and run `ACL SAVE` after creating users to persist them to disk." q2="Do I need to create the ACL file before starting the container?" a2="Yes. Redis will refuse to start if the `aclfile` directive points to a non-existent file. Create an empty file first: `touch ~/falkordb/data/users.acl`." q3="Can I mix inline ACL users in redis.conf with an ACL file?" a3="No. When `aclfile` is set, you cannot also define `user` directives in `redis.conf`. Choose one mechanism for managing ACL users." q4="How do I secure the ACL file on the host?" a4="Restrict filesystem permissions since the file contains password hashes: `chmod 600 ~/falkordb/data/users.acl`. Ensure only the Docker process and administrators can read it." q5="What happens if I forget to run ACL SAVE?" a5="Any users created with `ACL SETUSER` remain only in memory. They will be lost on the next container restart. Always run `ACL SAVE` after making ACL changes." %}
