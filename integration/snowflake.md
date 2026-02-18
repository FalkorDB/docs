---
title: "Snowflake Integration"
nav_order: 6
description: "Run graph database operations directly within your Snowflake environment using the FalkorDB Native App."
parent: "Integration"
---

# FalkorDB Snowflake Integration Guide

## Overview

FalkorDB is available as a [Snowflake Native App](https://app.snowflake.com/marketplace/listing/GZT1Z2XCTHL/falkordb-falkordb-graph-database?search=falkordb), allowing you to run graph database operations directly within your Snowflake environment. This integration enables you to:

- Load data from Snowflake tables into graph structures
- Query relationships using Cypher query language
- Analyze connected data without moving it outside Snowflake
- Leverage graph algorithms on your existing data warehouse

## Installation

### From Snowflake Marketplace

1. Navigate to **Snowflake Marketplace**
2. Search for **"FalkorDB"**
3. Click **Get** to install the app
4. Select your target database and warehouse
5. Click **Get** to complete installation

<img width="1333" height="299" alt="image" src="https://github.com/user-attachments/assets/a7b321a1-805f-4569-9802-c8e663ecb0ed" />


### Initial Setup

After installation, start the FalkorDB service:

```sql
-- Start the service (creates compute pool and warehouse)
-- Replace <app_instance_name> with your installed app name
CALL <app_instance_name>.app_public.start_app('FALKORDB_POOL', 'FALKORDB_WH');

-- Check service status
CALL <app_instance_name>.app_public.get_service_status();
```

**Note**: Replace `<app_instance_name>` with the name you chose during installation.

Wait for the service status to show `READY` before proceeding (typically 2-3 minutes).

## Basic Usage

### Creating a Graph from Direct Queries

The simplest way to create a graph is using direct Cypher queries:

```sql
-- Create nodes
CALL <app_instance_name>.app_public.graph_query('my_graph',
  'CREATE (:Person {name: ''Alice'', age: 30}),
          (:Person {name: ''Bob'', age: 25})'
);

-- Create relationships
CALL <app_instance_name>.app_public.graph_query('my_graph',
  'MATCH (a:Person {name: ''Alice''}), (b:Person {name: ''Bob''})
   CREATE (a)-[:KNOWS {since: 2020}]->(b)'
);

-- Query the graph
CALL <app_instance_name>.app_public.graph_query('my_graph',
  'MATCH (p:Person) RETURN p.name, p.age'
);
```

### Loading Data from Snowflake Tables

To load data from your existing Snowflake tables, you need to bind a table reference:

#### Step 1: Bind Your Table

1. In Snowflake UI, go to **Data Products** → **Apps**
2. Find and click on **FalkorDB**
3. Go to **Security** → **References**
4. Click **+ Add** next to "Consumer Data Table"
5. Select your database, schema, and table
6. Click **Save**

**Important**: Your table must have a header row or column names. CSV headers will be converted to UPPERCASE by Snowflake.

#### Step 2: Load Data Using CSV

```sql
-- Example: Load customer data
-- Assumes your bound table has columns: ID, NAME, EMAIL, CITY
CALL <app_instance_name>.app_public.load_csv(
  'customer_graph',
  'LOAD CSV FROM ''file://consumer_data.csv'' AS row 
   CREATE (:Customer {
     id: row[0],
     name: row[1],
     email: row[2],
     city: row[3]
   })'
);
```

**Note**: 
- The table is automatically retrieved from your Config UI binding—no need to specify it as a parameter
- The Cypher query must include `LOAD CSV FROM 'file://consumer_data.csv' AS row` to access the CSV data
- Access columns using `row[0]`, `row[1]`, `row[2]`, etc. (0-indexed)

### Querying Graphs

Use `graph_query()` to run Cypher queries:

```sql
-- Find all customers
CALL <app_instance_name>.app_public.graph_query('customer_graph',
  'MATCH (c:Customer) RETURN c.name, c.email LIMIT 10'
);

-- Find relationships
CALL <app_instance_name>.app_public.graph_query('social_graph',
  'MATCH (a:Person)-[r:KNOWS]->(b:Person) 
   RETURN a.name, r.since, b.name'
);

-- Pathfinding
CALL <app_instance_name>.app_public.graph_query('social_graph',
  'MATCH path = (a:Person {name: ''Alice''})-[:KNOWS*1..3]-(b:Person {name: ''Eve''})
   RETURN path'
);
```

### Managing Graphs

```sql
-- List all graphs
CALL <app_instance_name>.app_public.graph_list();

-- Delete a graph
CALL <app_instance_name>.app_public.graph_delete('my_graph');
```

## Complete Example: Social Network

### Step 1: Create Sample Data Table

```sql
-- Create a table with social network data
CREATE OR REPLACE TABLE social_data (
  person_id INT,
  name VARCHAR,
  age INT,
  city VARCHAR,
  knows_id INT,
  knows_since INT
);

-- Insert sample data
INSERT INTO social_data VALUES
  (1, 'Alice', 30, 'New York', 2, 2020),
  (2, 'Bob', 25, 'San Francisco', 3, 2019),
  (3, 'Carol', 35, 'Seattle', 5, 2018),
  (4, 'David', 28, 'Boston', 5, 2022),
  (5, 'Eve', 32, 'Chicago', NULL, NULL);
```

### Step 2: Bind the Table

Follow the UI steps above to bind `social_data` table to FalkorDB.

### Step 3: Load Nodes

```sql
-- Load person nodes
CALL <app_instance_name>.app_public.load_csv(
  'social_network',
  'LOAD CSV FROM ''file://consumer_data.csv'' AS row 
   CREATE (:Person {
     id: toInteger(row[0]),
     name: row[1],
     age: toInteger(row[2]),
     city: row[3]
   })'
);
```

**Note**: Columns are accessed by index: `row[0]` = person_id, `row[1]` = name, `row[2]` = age, `row[3]` = city

### Step 4: Load Relationships

For relationships, you'll need to bind a table that represents edges:

```sql
-- Create relationships table
CREATE OR REPLACE TABLE social_relationships AS
SELECT person_id, knows_id, knows_since
FROM social_data
WHERE knows_id IS NOT NULL;
```

Bind `social_relationships` and load:

```sql
CALL <app_instance_name>.app_public.load_csv(
  'social_network',
  'LOAD CSV FROM ''file://consumer_data.csv'' AS row 
   MATCH (a:Person {id: toInteger(row[0])})
   MATCH (b:Person {id: toInteger(row[1])})
   CREATE (a)-[:KNOWS {since: toInteger(row[2])}]->(b)'
);
```

**Note**: For relationships table: `row[0]` = person_id, `row[1]` = knows_id, `row[2]` = knows_since

### Step 5: Query the Graph

```sql
-- Find all friends of Alice
CALL <app_instance_name>.app_public.graph_query('social_network',
  'MATCH (a:Person {name: ''Alice''})-[:KNOWS]->(friend)
   RETURN friend.name, friend.city'
);

-- Find friend-of-friend connections
CALL <app_instance_name>.app_public.graph_query('social_network',
  'MATCH (a:Person {name: ''Alice''})-[:KNOWS*2]-(fof)
   WHERE fof.name <> ''Alice''
   RETURN DISTINCT fof.name, fof.city'
);

-- Find shortest path between two people
CALL <app_instance_name>.app_public.graph_query('social_network',
  'MATCH path = shortestPath(
     (a:Person {name: ''Alice''})-[:KNOWS*]-(b:Person {name: ''Eve''})
   )
   RETURN path'
);
```

## Quick Start with Sample Data

FalkorDB includes a sample data loader for testing:

```sql
-- 1. Make sure the service is running
CALL <app_instance_name>.app_public.get_service_status();

-- 2. Load built-in sample social network (5 people with relationships)
CALL <app_instance_name>.app_public.load_sample_social_network();

-- 3. Query the sample data
CALL <app_instance_name>.app_public.graph_query('demo_social_network',
  'MATCH (p:Person) RETURN p.name, p.age, p.city'
);

-- 4. Find relationships in the sample network
CALL <app_instance_name>.app_public.graph_query('demo_social_network',
  'MATCH (a:Person)-[r:KNOWS]->(b:Person) 
   RETURN a.name, b.name, r.since'
);
```

## Important Notes

### Data Updates and Duplicates

**Current Limitation**: Running `load_csv()` multiple times will create duplicate nodes. FalkorDB currently uses `CREATE` statements which always insert new data.

**Workaround**: Delete and recreate the graph for updates:

```sql
-- Delete existing graph
CALL <app_instance_name>.app_public.graph_delete('my_graph');

-- Reload with updated data
CALL <app_instance_name>.app_public.load_csv('my_graph', '...');
```

**Future**: We're working on MERGE/upsert support for incremental updates.

### CSV Data Access

When using `load_csv`, access CSV columns by index using `row[0]`, `row[1]`, `row[2]`, etc.:

```cypher
-- Example: First column is ID, second is NAME, third is EMAIL
LOAD CSV FROM 'file://consumer_data.csv' AS row 
CREATE (:Person {id: row[0], name: row[1], email: row[2]})
```

The CSV data comes from your bound table (configured in the app's Permissions tab).

### Cost Management

FalkorDB runs on Snowflake Compute Pools, which charge based on usage:

- **ACTIVE** pools charge continuously (even when idle)
- **SUSPENDED** pools don't charge

**Always suspend when not in use:**

```sql
-- Outside the app, using ACCOUNTADMIN
USE ROLE ACCOUNTADMIN;
SHOW COMPUTE POOLS;
ALTER COMPUTE POOL falkordb_pool SUSPEND;

-- Resume when needed
ALTER COMPUTE POOL falkordb_pool RESUME;
```

### Service Management

```sql
-- Stop the service (doesn't delete compute pool)
CALL <app_instance_name>.app_public.stop_app();

-- Restart the service
CALL <app_instance_name>.app_public.start_app('FALKORDB_POOL', 'FALKORDB_WH');

-- Check logs (if issues occur)
CALL <app_instance_name>.app_public.get_service_logs('0', 'falkordb', 100);

-- List containers
CALL <app_instance_name>.app_public.get_service_containers();
```

## Cypher Query Language Basics

### Creating Nodes

```cypher
-- Simple node
CREATE (:Label {property: 'value'})

-- Multiple properties
CREATE (:Person {name: 'Alice', age: 30, city: 'NYC'})

-- Multiple nodes
CREATE (:Person {name: 'Alice'}), (:Person {name: 'Bob'})
```

### Creating Relationships

```cypher
-- Match existing nodes and create relationship
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:KNOWS {since: 2020}]->(b)

-- Bidirectional (two relationships)
MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'})
CREATE (a)-[:KNOWS]->(b), (b)-[:KNOWS]->(a)
```

### Querying

```cypher
-- Match all nodes with label
MATCH (p:Person) RETURN p

-- Match with filter
MATCH (p:Person {city: 'NYC'}) RETURN p.name, p.age

-- Match relationships
MATCH (a:Person)-[r:KNOWS]->(b:Person) RETURN a.name, b.name

-- Pattern matching
MATCH (a:Person)-[:KNOWS]->(b:Person)-[:KNOWS]->(c:Person)
RETURN a.name, b.name, c.name
```

### Advanced Queries

```cypher
-- Shortest path
MATCH path = shortestPath((a:Person {name: 'Alice'})-[:KNOWS*]-(b:Person {name: 'Eve'}))
RETURN path

-- Variable length paths
MATCH (a:Person)-[:KNOWS*1..3]-(b:Person)
RETURN DISTINCT a.name, b.name

-- Aggregation
MATCH (p:Person)-[:KNOWS]->(friend)
RETURN p.name, COUNT(friend) AS friend_count
ORDER BY friend_count DESC
```

## Troubleshooting

### "Reference NOT bound" Error

**Problem**: `load_csv()` fails with reference error.

**Solution**: Ensure you've bound a table via the UI (Apps → FalkorDB → Security → References → Add).

### Service Not Starting

**Problem**: `get_service_status()` shows error state.

**Solution**: 
```sql
-- Check logs
CALL <app_instance_name>.app_public.get_service_logs('0', 'falkordb', 200);

-- Restart service
CALL <app_instance_name>.app_public.stop_app();
CALL <app_instance_name>.app_public.start_app('FALKORDB_POOL', 'FALKORDB_WH');
```

### Duplicate Nodes After Reload

**Problem**: Running `load_csv()` twice creates duplicate nodes.

**Solution**: Delete graph before reloading:
```sql
CALL <app_instance_name>.app_public.graph_delete('my_graph');
CALL <app_instance_name>.app_public.load_csv('my_graph', 
  'LOAD CSV FROM ''file://consumer_data.csv'' AS row CREATE (:Node {id: row[0]})');
```

### Column Not Found in CSV

**Problem**: Cypher query can't access CSV columns.

**Solution**: Use index-based access: `row[0]`, `row[1]`, `row[2]`, etc. (not `row.COLUMNNAME`)

```cypher
-- Correct
LOAD CSV FROM 'file://consumer_data.csv' AS row CREATE (:Person {id: row[0], name: row[1]})

-- Incorrect
CREATE (:Person {id: row.ID, name: row.NAME})
```

## Performance Tips

1. **Create indexes** on frequently queried properties
2. **Use specific labels** in MATCH clauses to reduce search space
3. **Limit result sets** for exploration: `RETURN ... LIMIT 100`
4. **Batch large loads** into smaller transactions if timeouts occur

## Additional Resources

- **Cypher Query Language**: [OpenCypher Documentation](https://opencypher.org/)
- **FalkorDB GitHub**: [github.com/FalkorDB/FalkorDB](https://github.com/FalkorDB/FalkorDB)
- **Snowflake Native Apps**: [Snowflake Documentation](https://docs.snowflake.com/en/developer-guide/native-apps/native-apps-about)

## Support

For issues, questions, or feature requests:
- **GitHub Issues**: [FalkorDB Snowflake Integration](https://github.com/FalkorDB/snowflake-integration/issues)
- **Community**: FalkorDB Discord/Slack (check GitHub README for links)

---

**Last Updated**: February 2026  
**Version**: 2.0 (Patch 17)
