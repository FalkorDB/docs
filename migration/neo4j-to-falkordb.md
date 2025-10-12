---
title: "Neo4j to FalkorDB"
description: "Migrate from Neo4j to FalkorDB."
parent: "Migration"
---

# Neo4j to FalkorDB Migration

Migrating graph database contents from Neo4j to FalkorDB is straightforward using standard Cypher queries to extract data, transform labels and properties as needed, and load CSV files into FalkorDB. This process migrates nodes, edges, constraints, and indexes.

## Overview

The migration process consists of the following steps:

1. Set up Neo4j and prepare your data
2. Review and configure mapping settings
3. Extract data from Neo4j to CSV files
4. Load CSV data into FalkorDB
5. Validate the migrated data

## Prerequisites

- Neo4j instance (local or remote)
- FalkorDB instance (local, Docker, or Cloud)
- Python 3.6+
- Migration tools from the [Neo4j-to-FalkorDB repository](https://github.com/FalkorDB/Neo4j-to-FalkorDB)

## Step 1: Setting Up Neo4j

Follow the [Neo4j documentation](https://neo4j.com/docs/operations-manual/current/installation/) to set up a locally run Neo4j database.

For testing purposes, you can load the Movies sample dataset by following the `:guide movies` command in the Neo4j browser. More details are available in the [Neo4j Getting Started guide](https://neo4j.com/docs/getting-started/appendix/example-data/).

## Step 2: Reviewing and Updating Mapping Configuration

The configuration file `migrate_config.json` allows you to modify how labels and properties are represented in FalkorDB.

### Generating a Configuration Template

To extract the ontology from your Neo4j database and generate a template config file:

```bash
python3 neo4j_to_csv_extractor.py --password <your-neo4j-password> --generate-template <your-template>.json --analyze-only
```

### Extractor Usage

```bash
python3 neo4j_to_csv_extractor.py [-h] [--uri URI] [--username USERNAME] --password PASSWORD 
                                  [--database DATABASE] [--batch-size BATCH_SIZE]
                                  [--nodes-only] [--edges-only] [--indexes-only] 
                                  [--config CONFIG] [--generate-template GENERATE_TEMPLATE]
                                  [--analyze-only]
```

**Options:**
- `--uri URI`: Neo4j URI (default: bolt://localhost:7687)
- `--username USERNAME`: Neo4j username (default: neo4j)
- `--password PASSWORD`: Neo4j password (required)
- `--database DATABASE`: Neo4j database name
- `--batch-size BATCH_SIZE`: Batch size for extraction
- `--nodes-only`: Extract only nodes
- `--edges-only`: Extract only relationships
- `--indexes-only`: Extract only indexes and constraints
- `--config CONFIG`: Path to migration configuration JSON file
- `--generate-template GENERATE_TEMPLATE`: Generate template migration config file
- `--analyze-only`: Only analyze topology, do not extract data

### Example Output

When analyzing a database, you'll see output similar to:

```
Connecting to Neo4j at bolt://localhost:7687 with username 'neo4j'...
✅ Loaded configuration from migrate_config.json
✅ Successfully connected to Neo4j!
🔍 Analyzing Neo4j database topology...
  Found 2 node labels: ['Movie', 'Person']
  Found 6 relationship types: ['ACTED_IN', 'DIRECTED', 'PRODUCED', 'WROTE', 'FOLLOWS', 'REVIEWED']

📊 Analyzing node properties...
  Analyzing Movie properties...
    Found 3 properties: ['released', 'tagline', 'title']
  Analyzing Person properties...
    Found 2 properties: ['born', 'name']

🔗 Analyzing relationship properties...
  Analyzing ACTED_IN properties...
    Found 1 properties: ['roles']
  ...

📈 Gathering database statistics...
  Movie: 38 nodes
  Person: 133 nodes
  ACTED_IN: 172 relationships
  ...
```

## Step 3: Extracting Data from Neo4j

To extract data from Neo4j and generate CSV files:

```bash
python3 neo4j_to_csv_extractor.py --password <your-neo4j-password> --config migrate_config.json
```

The script will:
- Read data from Neo4j
- Create CSV files in the `csv_output` subfolder
- Generate headers and content based on the configuration
- Create both nodes and edges CSV files
- Export indexes and constraints
- Generate FalkorDB load scripts

### Output Files

The extraction creates the following files in the `csv_output` directory:

- `nodes_<label>.csv`: One file per node label
- `edges_<type>.csv`: One file per relationship type
- `indexes.csv`: Database indexes
- `constraints.csv`: Database constraints
- `load_to_falkordb.cypher`: FalkorDB load script
- `create_indexes_falkordb.cypher`: Index creation script

## Step 4: Loading CSV Data into FalkorDB

### Setting Up FalkorDB

Set up FalkorDB on your local machine following the [Getting Started guide](https://docs.falkordb.com/getting_started.html).

You can use either:
- The full deployment with browser (port 3000)
- The server-only option (port 6379)

### Loading Data

Load the CSV data into FalkorDB using the Python loader:

```bash
python3 falkordb_csv_loader.py MOVIES --port 6379 --stats
```

**Options:**
- `graph_name`: Target graph name in FalkorDB (required)
- `--host HOST`: FalkorDB host (default: localhost)
- `--port PORT`: FalkorDB port (default: 6379)
- `--username USERNAME`: FalkorDB username (optional)
- `--password PASSWORD`: FalkorDB password (optional)
- `--batch-size BATCH_SIZE`: Batch size for loading (default: 5000)
- `--stats`: Show graph statistics after loading
- `--csv-dir CSV_DIR`: Directory containing CSV files (default: csv_output)
- `--merge-mode`: Use MERGE instead of CREATE for upsert behavior

### Using FalkorDB-Loader-RS (Recommended for Large Datasets)

For significantly improved loading speed and performance, especially with large datasets, we recommend using the Rust-based FalkorDB CSV Loader.

#### Features

- **High Performance**: Built with Rust and async/await for optimal speed
- **Batch Processing**: Configurable batch sizes (default: 5000 records)
- **Memory Efficient**: Streams data without loading everything into memory
- **Automatic Schema Management**: Creates indexes and constraints automatically
- **Merge Mode**: Support for upsert operations using MERGE instead of CREATE
- **Progress Reporting**: Real-time progress tracking during loading

#### Installation

```bash
git clone https://github.com/FalkorDB/FalkorDB-Loader-RS
cd FalkorDB-Loader-RS
cargo build --release
```

The binary will be available at `target/release/falkordb-loader`.

#### Basic Usage

```bash
./target/release/falkordb-loader MOVIES
```

#### Advanced Usage

```bash
./target/release/falkordb-loader MOVIES \
  --host localhost \
  --port 6379 \
  --username myuser \
  --password mypass \
  --csv-dir ./csv_output \
  --batch-size 1000 \
  --merge-mode \
  --stats \
  --progress-interval 500
```

#### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `graph_name` | Target graph name in FalkorDB (required) | - |
| `--host` | FalkorDB host | localhost |
| `--port` | FalkorDB port | 6379 |
| `--username` | FalkorDB username (optional) | - |
| `--password` | FalkorDB password (optional) | - |
| `--csv-dir` | Directory containing CSV files | csv_output |
| `--batch-size` | Batch size for loading | 5000 |
| `--merge-mode` | Use MERGE instead of CREATE for upsert | false |
| `--stats` | Show graph statistics after loading | false |
| `--progress-interval` | Report progress every N records (0 to disable) | 1000 |

#### Performance Tips

1. **Adjust batch size** based on your data and available memory
2. **Enable progress reporting** for long-running imports: `--progress-interval 1000`
3. **Use merge mode** if you need to update existing data: `--merge-mode`
4. **Set log level** for debugging: `RUST_LOG=info ./target/release/falkordb-loader MOVIES`

For more details, see the [FalkorDB-Loader-RS repository](https://github.com/FalkorDB/FalkorDB-Loader-RS).

### Example Output

```
Connecting to FalkorDB at localhost:6379...
✅ Connected to FalkorDB graph 'MOVIES'
Found 2 node files and 6 edge files

🗼️ Setting up database schema...
🔧 Creating ID indexes for all node labels...
  Creating ID index: CREATE INDEX ON :Movie(id)
  Creating ID index: CREATE INDEX ON :Person(id)
✅ Created 2 ID indexes

🔧 Creating indexes from CSV...
  ...
✅ Created 2 indexes from CSV

🔒 Creating constraints...
  ...
✅ Created 2 constraints

📥 Loading nodes...
  Loading nodes from csv_output/nodes_movie.csv...
  ✅ Loaded 38 Movie nodes

🔗 Loading edges...
  Loading edges from csv_output/edges_acted_in.csv...
  ✅ Loaded 172 ACTED_IN relationships

✅ Successfully loaded data into graph 'MOVIES'

📊 Graph Statistics:
Nodes:
  ['Movie']: 38
  ['Person']: 133
Relationships:
  ACTED_IN: 172
  DIRECTED: 44
  ...
```

## Step 5: Validating Content

Validate that your data has been successfully migrated by running queries in both Neo4j and FalkorDB. Compare the results to ensure data integrity.

Example query:

```cypher
MATCH p=()-[:REVIEWED]->() RETURN p LIMIT 25;
```

You can visualize and compare the results in both the Neo4j Browser and FalkorDB Browser to ensure the migration was successful.

## Additional Resources

- [Neo4j-to-FalkorDB GitHub Repository](https://github.com/FalkorDB/Neo4j-to-FalkorDB)
- [FalkorDB Bulk Loader](https://github.com/falkordb/falkordb-bulk-loader)
- [FalkorDB Rust Loader](https://github.com/FalkorDB/FalkorDB-Loader-RS)

## Next Steps

- Explore [FalkorDB Cypher Language](/cypher) for querying your graph
- Learn about [FalkorDB Operations](/operations) for production deployments
- Check out [FalkorDB Integration](/integration) options

