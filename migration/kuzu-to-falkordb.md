---
title: "Kuzu to FalkorDB"
description: "Migrate from Kuzu to FalkorDB."
parent: "Migration"
---

# Kuzu to FalkorDB Migration

A streamlined 2-step process to migrate data from Kuzu graph database into FalkorDB using automated schema discovery and CSV export.

## Overview

This migration tool bridges the gap between Kuzu and FalkorDB by:
1. Automatically discovering your Kuzu database schema
2. Exporting all nodes and relationships to properly formatted CSV files
3. Loading these CSV files into FalkorDB using the FalkorDB Rust loader

The process ensures complete data migration including nodes, relationships, properties, and metadata.

## Features

- **Automatic Schema Discovery**: Dynamically discovers all node types and relationship types in your Kuzu database
- **FalkorDB Compatibility**: Generates CSV files in the exact format expected by FalkorDB
- **Intelligent Label Mapping**: Maps Kuzu relationship names to standardized FalkorDB edge types
- **Complex Property Handling**: Properly handles lists, nested values, and various data types
- **Comprehensive Export**: Exports both nodes and relationships with full metadata
- **Schema Documentation**: Optional JSON schema file generation for documentation purposes

## Prerequisites

- Python 3.6+
- `kuzu` Python package
- FalkorDB instance (local, Docker, or Cloud)
- [FalkorDB Rust Loader](https://github.com/FalkorDB/FalkorDB-Loader-RS)

## Installation

1. Install the required dependencies:

```bash
pip3 install kuzu
```

2. Download the migration script:

```bash
git clone https://github.com/FalkorDB-POCs/Kuzu-to-FalkorDB.git
cd Kuzu-to-FalkorDB
```

## Step 1: Exporting from Kuzu

### Basic Usage

Export all data from a Kuzu database:

```bash
python3 kuzu_to_falkordb_export.py --db path/to/your/database
```

### Advanced Usage

```bash
# Export with schema documentation
python3 kuzu_to_falkordb_export.py --db network_it_smart_db --schema schema.json

# Export to custom directory
python3 kuzu_to_falkordb_export.py --db network_it_smart_db --output my_csv_export

# Full example with all options
python3 kuzu_to_falkordb_export.py --db network_it_smart_db --schema schema.json --output falkordb_import
```

### Command Line Options

| Option | Description | Required | Default |
|--------|-------------|----------|---------|
| `--db`, `--database` | Path to Kuzu database file/directory | Yes | - |
| `--schema` | Path to output schema JSON file | No | None |
| `--output` | Output directory for CSV files | No | `_csv_` |

### Output Structure

The export script generates the following files:

**Node CSV Files:**
- Format: `nodes_<NodeType>.csv`
- Structure: `id,labels,property1,property2,...`
- Example: `nodes_Application.csv`, `nodes_Machine.csv`

**Edge CSV Files:**
- Format: `edges_<EdgeType>.csv`
- Structure: `source,source_label,target,target_label,type`
- Example: `edges_CONNECTS.csv`, `edges_CONTAINS.csv`

**Schema File (Optional):**
- File: `schema.json`
- Contains: Export metadata, node types, relationship types, and file mappings

### Example Export Output

```
🚀 Kuzu to FalkorDB CSV Exporter
==================================================
Database: network_it_smart_db
Output: _csv_
Schema: schema.json
==================================================

🔍 Discovering database schema...
  📦 Found node table: Application
  📦 Found node table: Machine
  🔗 Found relationship table: CONNECTS -> CONNECTS
  🔗 Found relationship table: INSTANCE_APP_SW -> INSTANCE
  ✓ Discovered 8 node types and 15 relationship types

📤 Exporting 8 node types...
  📦 Exporting Application...
    ✓ Exported 1,234 Application nodes to nodes_Application.csv

🔗 Exporting 15 relationship types...
  🔗 Exporting CONNECTS (from 3 Kuzu tables)...
    ✓ Exported 5,678 CONNECTS relationships to edges_CONNECTS.csv

🎉 Export completed successfully!
📁 Output files in: _csv_
📊 Exported: 8 node types, 15 relationship types
```

## Step 2: Loading into FalkorDB

Use the [FalkorDB Rust Loader](https://github.com/FalkorDB/FalkorDB-Loader-RS) to load the exported CSV files directly into FalkorDB.

Follow the loader documentation for installation and usage instructions. The loader provides high-performance bulk loading of graph data from CSV files.

## Data Mapping Features

### Relationship Mapping

The script intelligently maps Kuzu relationship names to standardized FalkorDB edge types, ensuring consistent naming conventions.

### Label Enhancement

The script enhances node labels with context for better FalkorDB compatibility:

- Process nodes in different contexts: `Application:Process`, `Service:Process`, or `OS:Process`
- Network zones: `Network:Zone`
- Service software: `Software:Service`

## Error Handling

The migration script includes robust error handling:

- Validates database path exists
- Handles missing relationship types gracefully
- Continues export even if individual tables fail
- Provides detailed progress and error messages

## Troubleshooting

### Common Issues

1. **Database not found**: Ensure the database path is correct and accessible
2. **Permission errors**: Check write permissions for the output directory
3. **Memory issues**: For very large databases, consider adjusting batch sizes or processing in chunks

### Debug Mode

For additional debugging information, you can modify the script to include more verbose logging or add print statements to track the export process.

## Additional Resources

- [Kuzu-to-FalkorDB GitHub Repository](https://github.com/FalkorDB-POCs/Kuzu-to-FalkorDB)
- [FalkorDB Rust Loader](https://github.com/FalkorDB/FalkorDB-Loader-RS)
- [FalkorDB Bulk Loader](https://github.com/falkordb/falkordb-bulk-loader)

## Next Steps

- Explore [FalkorDB Cypher Language](/cypher) for querying your graph
- Learn about [FalkorDB Operations](/operations) for production deployments
- Check out [FalkorDB Integration](/integration) options

