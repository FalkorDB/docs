---
title: "Docker and Docker Compose"
nav_order: 11
parent: Operations
description: "Running FalkorDB with Docker and Docker Compose"
---

# Running FalkorDB with Docker and Docker Compose

This guide covers how to run FalkorDB using Docker and Docker Compose, providing flexible deployment options for both development and production environments.

## Docker Images

FalkorDB provides two main Docker images:

### 1. `falkordb/falkordb`
- **Includes**: FalkorDB server + FalkorDB Browser
- **Use case**: Development, quick start, interactive exploration
- **Ports**: 
  - `6379` - Redis/FalkorDB server
  - `3000` - FalkorDB Browser UI

### 2. `falkordb/falkordb-server`
- **Includes**: FalkorDB server only
- **Use case**: Production deployments, lighter footprint
- **Ports**: 
  - `6379` - Redis/FalkorDB server

### 3. `falkordb/falkordb-browser`
- **Includes**: FalkorDB Browser UI only
- **Use case**: Running browser separately from the server, custom deployments
- **Ports**: 
  - `3000` - FalkorDB Browser UI
- **Configuration**: Requires `FALKORDB_URL` environment variable to connect to a FalkorDB server

## Quick Start with Docker

### Running with Browser (Development)

```bash
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:latest
```

Access the browser at [http://localhost:3000](http://localhost:3000)

### Running Server Only (Production)

```bash
docker run -p 6379:6379 -it --rm falkordb/falkordb-server:latest
```

### Running with Authentication

```bash
docker run -p 6379:6379 -p 3000:3000 -it \
  -e REDIS_ARGS="--requirepass yourpassword" \
  --rm falkordb/falkordb:latest
```

### Running with Custom Configuration

```bash
docker run -p 6379:6379 -p 3000:3000 -it \
  -e REDIS_ARGS="--requirepass yourpassword" \
  -e FALKORDB_ARGS="THREAD_COUNT 4 TIMEOUT 5000" \
  --rm falkordb/falkordb:latest
```

## Using Docker Compose

Docker Compose provides a more flexible and maintainable way to run FalkorDB, especially when you need to configure multiple services or manage complex setups.

> **Quick Start**: You can download a ready-to-use docker-compose.yml file from the [FalkorDB repository](https://github.com/FalkorDB/FalkorDB/blob/master/build/docker/docker-compose.yml).

### Basic Docker Compose Setup

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  falkordb:
    image: falkordb/falkordb:latest
    container_name: falkordb
    ports:
      - "6379:6379"
      - "3000:3000"
    environment:
      - REDIS_ARGS=--requirepass falkordb
      - FALKORDB_ARGS=THREAD_COUNT 4
    restart: unless-stopped
```

Start FalkorDB:

```bash
docker-compose up -d
```

Stop FalkorDB:

```bash
docker-compose down
```

### Production Setup with Persistence

For production environments, use the server-only image with data persistence:

```yaml
version: '3.8'

services:
  falkordb:
    image: falkordb/falkordb-server:latest
    container_name: falkordb-server
    ports:
      - "6379:6379"
    environment:
      - REDIS_ARGS=--requirepass ${FALKORDB_PASSWORD:-falkordb} --appendonly yes
      - FALKORDB_ARGS=THREAD_COUNT 8 TIMEOUT_MAX 30000
    volumes:
      - falkordb_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  falkordb_data:
    driver: local
```

Start with custom password:

```bash
FALKORDB_PASSWORD=your-secure-password docker-compose up -d
```

### Separate Server and Browser Setup

Run FalkorDB server and browser as separate containers:

```yaml
version: '3.8'

services:
  falkordb-server:
    image: falkordb/falkordb-server:latest
    container_name: falkordb-server
    ports:
      - "6379:6379"
    environment:
      - REDIS_ARGS=--requirepass falkordb
      - FALKORDB_ARGS=THREAD_COUNT 4
    volumes:
      - falkordb_data:/data
    restart: unless-stopped
    networks:
      - falkordb-network

  falkordb-browser:
    image: falkordb/falkordb-browser:latest
    container_name: falkordb-browser
    ports:
      - "3000:3000"
    environment:
      - FALKORDB_URL=redis://falkordb-server:6379
      - FALKORDB_PASSWORD=falkordb
    depends_on:
      - falkordb-server
    restart: unless-stopped
    networks:
      - falkordb-network

volumes:
  falkordb_data:
    driver: local

networks:
  falkordb-network:
    driver: bridge
```

### Complete Production Setup

A comprehensive production-ready setup with all recommended configurations:

```yaml
version: '3.8'

services:
  falkordb:
    image: falkordb/falkordb-server:latest
    container_name: falkordb-production
    ports:
      - "6379:6379"
    environment:
      # Redis Configuration
      - REDIS_ARGS=--requirepass ${FALKORDB_PASSWORD:-changeme} --appendonly yes --appendfsync everysec --maxmemory 2gb --maxmemory-policy allkeys-lru
      # FalkorDB Configuration
      - FALKORDB_ARGS=THREAD_COUNT 8 CACHE_SIZE 50 TIMEOUT_MAX 60000 TIMEOUT_DEFAULT 30000 QUERY_MEM_CAPACITY 104857600
    volumes:
      - falkordb_data:/data
      - ./falkordb-config:/etc/falkordb
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "$${FALKORDB_PASSWORD:-changeme}", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    networks:
      - falkordb-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

volumes:
  falkordb_data:
    driver: local

networks:
  falkordb-network:
    driver: bridge
```

## Docker Compose Commands

Common Docker Compose commands for managing FalkorDB:

```bash
# Start services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f falkordb

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers with volumes (WARNING: deletes data)
docker-compose down -v

# Restart services
docker-compose restart

# Check service status
docker-compose ps

# Execute commands in running container
docker-compose exec falkordb redis-cli
```

## Environment Variables

### REDIS_ARGS
Pass arguments directly to the Redis server:

```yaml
environment:
  - REDIS_ARGS=--requirepass mypassword --maxmemory 1gb --appendonly yes
```

Common Redis arguments:
- `--requirepass <password>` - Set authentication password
- `--appendonly yes` - Enable AOF persistence
- `--appendfsync everysec` - AOF sync frequency
- `--maxmemory <bytes>` - Maximum memory limit
- `--maxmemory-policy <policy>` - Eviction policy (e.g., `allkeys-lru`)

### FALKORDB_ARGS
Pass configuration to FalkorDB module:

```yaml
environment:
  - FALKORDB_ARGS=THREAD_COUNT 4 CACHE_SIZE 25 TIMEOUT_MAX 10000
```

See the [Configuration](/getting-started/configuration) page for all available FalkorDB parameters.

## Data Persistence

### Using Named Volumes

Named volumes are the recommended approach for data persistence:

```yaml
services:
  falkordb:
    image: falkordb/falkordb-server:latest
    volumes:
      - falkordb_data:/data

volumes:
  falkordb_data:
```

### Using Bind Mounts

For specific host directory mapping:

```yaml
services:
  falkordb:
    image: falkordb/falkordb-server:latest
    volumes:
      - ./falkordb-data:/data
```

Create the directory first:

```bash
mkdir -p ./falkordb-data
```

## Health Checks

Add health checks to ensure FalkorDB is running properly:

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

With authentication:

```yaml
healthcheck:
  test: ["CMD", "redis-cli", "-a", "yourpassword", "ping"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Networking

### Custom Networks

Create isolated networks for better security:

```yaml
networks:
  falkordb-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.25.0.0/16
```

### Expose vs Ports

Use `expose` for internal communication and `ports` for external access:

```yaml
services:
  falkordb:
    image: falkordb/falkordb-server:latest
    expose:
      - "6379"  # Only accessible within Docker network
    # Or use ports for external access:
    # ports:
    #   - "6379:6379"
```

## Best Practices

1. **Use Environment Variables**: Store sensitive information like passwords in `.env` files or environment variables:

   Create a `.env` file:
   ```
   FALKORDB_PASSWORD=your-secure-password
   FALKORDB_THREADS=8
   ```

   Reference in `docker-compose.yml`:
   ```yaml
   environment:
     - REDIS_ARGS=--requirepass ${FALKORDB_PASSWORD}
     - FALKORDB_ARGS=THREAD_COUNT ${FALKORDB_THREADS}
   ```

2. **Enable Persistence**: Always use volumes for production data:
   ```yaml
   volumes:
     - falkordb_data:/data
   ```

3. **Set Resource Limits**: Prevent resource exhaustion:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '4'
         memory: 8G
       reservations:
         cpus: '2'
         memory: 4G
   ```

4. **Use Health Checks**: Ensure automatic recovery:
   ```yaml
   healthcheck:
     test: ["CMD", "redis-cli", "ping"]
     interval: 30s
     timeout: 10s
     retries: 3
   ```

5. **Configure Logging**: Manage log file sizes:
   ```yaml
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```

6. **Separate Concerns**: Use different images for different purposes:
   - Development: `falkordb/falkordb` (with browser)
   - Production: `falkordb/falkordb-server` (server only)

7. **Use Specific Tags**: Pin to specific versions for stability:
   ```yaml
   image: falkordb/falkordb-server:4.0.0
   ```

## Troubleshooting

### Check Container Logs

```bash
docker-compose logs falkordb
```

### Check Container Status

```bash
docker-compose ps
```

### Test Connection

```bash
docker-compose exec falkordb redis-cli ping
```

### Access Redis CLI

```bash
docker-compose exec falkordb redis-cli
```

### View Running Processes

```bash
docker-compose top
```

### Inspect Configuration

```bash
docker-compose config
```

## Next Steps

- Learn about [Persistence](/operations/persistence) for data durability
- Set up [Replication](/operations/replication) for high availability
- Configure a [Cluster](/operations/cluster) for scalability
- Review [Configuration](/getting-started/configuration) options
- Deploy to [Kubernetes](/operations/k8s-support) for orchestration
