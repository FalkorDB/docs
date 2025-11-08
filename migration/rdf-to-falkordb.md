---
title: "RDF to FalkorDB"
description: "Migrate from RDF (TTL) to FalkorDB."
parent: "Migration"
---

# RDF to FalkorDB Migration

A comprehensive multi-step process to migrate data from RDF (TTL) based graph data stores into FalkorDB property graph database.

## Overview

RDF data files contain triplets of subject-predicate-object which can specify property assignment to an entity or a relationship assignment to another entity. This migration tool bridges the gap between RDF and FalkorDB by:

1. Extracting the schema from RDF data files
2. Generating a configurable JSON configuration file
3. Exporting nodes and edges to CSV files formatted for FalkorDB
4. Loading the CSV files into FalkorDB

The process ensures complete data migration including all entities, relationships, properties, and metadata.

## Features

* **Schema Extraction**: Automatically extracts ontology from RDF/TTL files
* **Configurable Mapping**: JSON-based configuration for customizing data mapping
* **URI Shortening**: Optional conversion of long URIs to shorter representations
* **CSV Export**: Generates properly formatted CSV files for nodes and edges
* **Flexible Loading**: Multiple loading options with batch processing support
* **Data Preview**: Optional CSV output preview during export

## Prerequisites

* Python 3.6+
* Required Python packages (see requirements.txt in the repository)
* FalkorDB instance (local, Docker, or Cloud)
* RDF/TTL data files

## Installation

1. Clone the migration repository:

```bash
git clone https://github.com/FalkorDB/rdf-to-falkordb.git
cd rdf-to-falkordb
```

2. Install required dependencies:

```bash
pip3 install -r requirements.txt
```

## Step 1: Locating Your RDF (TTL) Data File

Place your TTL file(s) in the import directory. The repository includes several sample files that you can use for testing.

## Step 2: Extracting & Reviewing Ontology

In this step, you will extract the ontology (schema) from the TTL file. The `rdf_to_csv_extractor.py` script handles both ontology extraction and data export.

### Basic Ontology Extraction

```bash
python3 rdf_to_csv_extractor.py import/<rdf-ttl-file.ttl> --extract-ontology config/<your-config.json>
```

### Command Line Options

| Option | Description | Required | Default |
|--------|-------------|----------|---------|
| `ttl_file` | Path to the TTL/RDF file to process | Yes | - |
| `--config` | Path to ontology configuration JSON file | No | - |
| `--extract-ontology` | Extract ontology and save to specified file | No | extracted_ontology_config.json |
| `--output-dir` | Output directory for CSV files | No | csv_output |
| `--shorten-uris` | Convert long URIs to shorter representations | No | False |
| `--uri-prefixes` | JSON file with custom URI prefix mappings | No | - |
| `--csv-output-peek` | Show preview (first 3 lines) of generated CSV files | No | False |

### Review Configuration

After extracting the ontology, review the generated JSON configuration file. You can modify the configuration to customize how RDF triplets are mapped to FalkorDB nodes and relationships.

## Step 3: Extracting Data from TTL File

Once you have reviewed and optionally customized the ontology configuration, export the data to CSV files.

### Basic Data Export

```bash
python3 rdf_to_csv_extractor.py import/<rdf-ttl-file.ttl> --config config/<your-config.json> --output-dir <your-project-subfolder>
```

### Advanced Export with URI Shortening

```bash
python3 rdf_to_csv_extractor.py import/<rdf-ttl-file.ttl> \
  --config config/<your-config.json> \
  --shorten-uris \
  --output-dir <your-project-subfolder> \
  --csv-output-peek
```

### Output Structure

The export script generates the following files:

**Node CSV Files:**
* Format: `nodes_<NodeType>.csv`
* Contains: Entity IDs, labels, and properties
* Example: `nodes_InChIkey.csv`, `nodes_LCMSFeature.csv`

**Edge CSV Files:**
* Format: `edges_<EdgeType>.csv`
* Contains: Source ID, source label, target ID, target label, relationship type
* Example: `edges_HAS_CANOPUS_ANNOTATION.csv`

## Step 4: Loading Data into FalkorDB

You have two options for loading the exported CSV files into FalkorDB:

### Option 1: Using Python Loader (Included in Repository)

The Python loader (`falkordb_csv_loader.py`) provides a straightforward way to load CSV files directly into FalkorDB.

#### Basic Usage

```bash
python3 falkordb_csv_loader.py <graph-name> --csv-dir <your-project-subfolder>
```

#### Advanced Usage

```bash
python3 falkordb_csv_loader.py <graph-name> \
  --host localhost \
  --port 6379 \
  --username myuser \
  --password mypass \
  --csv-dir <your-project-subfolder> \
  --batch-size 5000 \
  --merge-mode \
  --stats
```

#### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `graph_name` | Target graph name in FalkorDB (required) | - |
| `--host` | FalkorDB host | localhost |
| `--port` | FalkorDB port | 6379 |
| `--username` | FalkorDB username (optional) | - |
| `--password` | FalkorDB password (optional) | - |
| `--batch-size` | Batch size for loading | 5000 |
| `--stats` | Show graph statistics after loading | False |
| `--csv-dir` | Directory containing CSV files | csv_output |
| `--merge-mode` | Use MERGE instead of CREATE for upsert behavior | False |

#### Example Output

```
Loading nodes from vgf/nodes_Material.csv...
  Read 1 rows from vgf/nodes_Material.csv
[2025-08-03 13:50:21] Batch complete: Loaded 1 nodes (Duration: 0:00:00.000857)
[2025-08-03 13:50:21] ✅ Loaded 1 Material nodes (Duration: 0:00:00.002075)

Loading edges from vgf/edges_HAS_CANOPUS_ANNOTATION.csv...
  Read 233 rows from vgf/edges_HAS_CANOPUS_ANNOTATION.csv
[2025-08-03 13:51:55] Batch complete: Loaded 233 edges (Duration: 0:00:00.101047)
[2025-08-03 13:51:55] ✅ Loaded 233 HAS_CANOPUS_ANNOTATION relationships (Duration: 0:00:00.102690)

✅ Successfully loaded data into graph 'VGF141'
```

### Option 2: Using FalkorDB Rust Loader (Recommended for Large Datasets)

For better performance with large datasets, use the [FalkorDB Rust Loader](https://github.com/FalkorDB/FalkorDB-Loader-RS).

#### Installation

```bash
git clone https://github.com/FalkorDB/FalkorDB-Loader-RS
cd FalkorDB-Loader-RS
cargo build --release
```

#### Basic Usage

```bash
./target/release/falkordb-loader my_graph --csv-dir <your-project-subfolder>
```

#### Advanced Usage

```bash
./target/release/falkordb-loader my_graph \
  --host localhost \
  --port 6379 \
  --username myuser \
  --password mypass \
  --csv-dir <your-project-subfolder> \
  --batch-size 5000 \
  --merge-mode \
  --stats \
  --progress-interval 1000
```

#### Performance Features

The Rust loader provides significant advantages:

* **Async Operations**: All database operations use async/await for better concurrency
* **Batch Processing**: Processes multiple records per query (configurable batch size)
* **Memory Efficient**: Streams data from CSV files without loading everything into memory
* **Progress Tracking**: Real-time progress updates during loading
* **Error Handling**: Comprehensive error handling with detailed logging

## Example Migration Flow

Here's a complete example migrating a VGF141 dataset:

### 1. Extract Ontology

```bash
python3 rdf_to_csv_extractor.py import/VGF141.ttl --extract-ontology config/vgf141_config.json
```

### 2. Review and Export Data

```bash
python3 rdf_to_csv_extractor.py import/VGF141.ttl \
  --config config/vgf141_config.json \
  --shorten-uris \
  --output-dir vgf \
  --csv-output-peek
```

### 3. Load into FalkorDB

```bash
python3 falkordb_csv_loader.py VGF141 --csv-dir vgf --merge-mode --stats
```

## Data Mapping

### URI Shortening

The tool supports converting long URIs to shorter, more manageable representations. This is particularly useful for:

* Reducing storage requirements
* Improving readability
* Simplifying queries
* Custom prefix mappings via JSON configuration

### Property Handling

The migration process preserves:

* Simple scalar properties (strings, numbers, booleans)
* Complex nested values
* Lists and arrays
* Metadata and annotations

## Troubleshooting

### Common Issues

1. **Missing Dependencies**: Ensure all Python packages from requirements.txt are installed
2. **File Not Found**: Verify the TTL file path is correct and accessible
3. **Memory Issues**: For very large RDF files, consider processing in smaller chunks
4. **URI Format Issues**: Review URI prefix mappings if shortened URIs are not formatted correctly

### Debug Tips

* Use `--csv-output-peek` to preview generated CSV files during export
* Enable verbose logging by modifying the script
* Test with smaller sample datasets first
* Verify the ontology configuration matches your data structure

## Additional Resources

* [rdf-to-falkordb GitHub Repository](https://github.com/FalkorDB-POCs/rdf-to-falkordb)
* [FalkorDB Rust Loader](https://github.com/FalkorDB/FalkorDB-Loader-RS)
* [FalkorDB Bulk Loader](https://github.com/falkordb/falkordb-bulk-loader)

## Next Steps

* Explore [FalkorDB Cypher Language](/cypher) for querying your graph
* Learn about [FalkorDB Operations](/operations) for production deployments
* Check out [FalkorDB Integration](/integration) options
