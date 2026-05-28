---
title: "PyTorch Geometric"
nav_order: 7
description: "Train Graph Neural Networks on FalkorDB using the PyTorch Geometric remote backend."
parent: "Integration"
---

# PyTorch Geometric Integration

This page describes how to integrate FalkorDB with [PyTorch Geometric (PyG)](https://pytorch-geometric.readthedocs.io/) using the [falkordb-pyg](https://github.com/FalkorDB/falkordb-pyg) package.

## Overview

`falkordb-pyg` implements PyG's [Remote Backend interface](https://pytorch-geometric.readthedocs.io/en/latest/advanced/remote.html) (`FeatureStore` + `GraphStore`) for FalkorDB. Once connected, you can plug the backend directly into `NeighborLoader`, `LinkNeighborLoader`, and other standard PyG data loaders — no changes to your model or training code required.

**Key features:**

- **Zero-copy lazy loading** — features and topology are fetched on demand and cached locally
- **Heterogeneous graph support** — multiple node and edge types
- **Automatic ID remapping** — non-contiguous FalkorDB node IDs are mapped to contiguous PyG indices transparently
- **Drop-in replacement** — works with any PyG workflow that accepts a remote backend

## Installation

> **Prerequisite:** PyTorch and PyTorch Geometric must be installed first.
> Follow the [PyTorch](https://pytorch.org/get-started/locally/) and
> [PyG](https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html)
> installation guides for your platform and CUDA version.

```bash
pip install falkordb-pyg
```

Or install with PyTorch and PyG included (CPU-only defaults):

```bash
pip install 'falkordb-pyg[torch]'
```

> **Requires:** Python ≥ 3.10, PyTorch ≥ 2.0, PyTorch Geometric ≥ 2.4, FalkorDB Python client ≥ 1.0.

## Quick Start

### 1. Start FalkorDB

```bash
docker run -p 6379:6379 falkordb/falkordb:latest
```

### 2. Load data into FalkorDB

```python
from falkordb import FalkorDB

db = FalkorDB(host="localhost", port=6379)
graph = db.select_graph("papers")

# Create nodes with features and labels
graph.query("CREATE (:paper {x: [1.0, 0.0, 1.0], y: 0})")
graph.query("CREATE (:paper {x: [0.0, 1.0, 0.5], y: 1})")

# Create edges
graph.query(
    "MATCH (a:paper), (b:paper) "
    "WHERE ID(a) = 0 AND ID(b) = 1 "
    "CREATE (a)-[:cites]->(b)"
)
```

### 3. Create the remote backend

```python
from falkordb_pyg import get_remote_backend

feature_store, graph_store = get_remote_backend(
    host="localhost",
    port=6379,
    graph_name="papers",
)
```

### 4. Use with NeighborLoader

```python
from torch_geometric.loader import NeighborLoader
import torch

train_nodes = torch.tensor([0])

loader = NeighborLoader(
    data=(feature_store, graph_store),
    num_neighbors={("paper", "cites", "paper"): [10, 10]},
    batch_size=32,
    input_nodes=("paper", train_nodes),
)

for batch in loader:
    paper_x = batch["paper"].x
    paper_y = batch["paper"].y
    edge_index = batch["paper", "cites", "paper"].edge_index
    # ... forward pass, loss, backward ...
```

## API Reference

### `get_remote_backend`

```python
from falkordb_pyg import get_remote_backend

feature_store, graph_store = get_remote_backend(
    host="localhost",           # FalkorDB / Redis hostname
    port=6379,                  # FalkorDB / Redis port
    graph_name="default",       # Graph name in FalkorDB
    node_type_to_label=None,    # Dict[str, str] — PyG type → FalkorDB label
    edge_type_to_rel=None,      # Dict[Tuple, str] — PyG edge triple → rel type
)
```

Returns a `(FalkorDBFeatureStore, FalkorDBGraphStore)` tuple.

### `FalkorDBFeatureStore`

Implements [`torch_geometric.data.FeatureStore`](https://pytorch-geometric.readthedocs.io/en/latest/modules/data.html#torch_geometric.data.FeatureStore).

| Method | Description |
|---|---|
| `_get_tensor(attr)` | Fetch a node-feature tensor (lazy, cached) |
| `_put_tensor(tensor, attr)` | Store a tensor in the local cache |
| `_remove_tensor(attr)` | Remove a cached tensor |
| `_get_tensor_size(attr)` | Return the shape of a tensor |
| `get_all_tensor_attrs()` | List all registered `TensorAttr` objects |

**Constructor:**

```python
FalkorDBFeatureStore(
    graph,                     # falkordb.Graph instance
    node_type_to_label=None,   # Optional Dict[str, str]
)
```

### `FalkorDBGraphStore`

Implements [`torch_geometric.data.GraphStore`](https://pytorch-geometric.readthedocs.io/en/latest/modules/data.html#torch_geometric.data.GraphStore).

| Method | Description |
|---|---|
| `_get_edge_index(attr)` | Fetch a COO edge index (lazy, cached) |
| `_put_edge_index(edge_index, attr)` | Store a COO edge index in the local cache |
| `_remove_edge_index(attr)` | Remove a cached edge index |
| `get_all_edge_attrs()` | List all registered `EdgeAttr` objects |

**Constructor:**

```python
FalkorDBGraphStore(
    graph,                     # falkordb.Graph instance
    node_type_to_label=None,   # Optional Dict[str, str]
    edge_type_to_rel=None,     # Optional Dict[Tuple[str,str,str], str]
)
```

### `NodeIDMapper`

Bidirectional mapping between FalkorDB internal node IDs and contiguous 0-based PyG indices.

```python
from falkordb_pyg.utils import NodeIDMapper

mapper = NodeIDMapper(falkordb_ids=[100, 200, 300])
mapper.falkor_to_pyg(200)  # -> 1
mapper.pyg_to_falkor(1)    # -> 200
mapper.num_nodes            # -> 3
```

## Node ID Remapping

FalkorDB assigns internal integer IDs to nodes that may not be contiguous or start at zero. `falkordb-pyg` transparently builds a `NodeIDMapper` for each node type on first access, converting FalkorDB IDs to contiguous PyG indices. Edges referencing IDs not present in the mapper are silently dropped.

## Example: Training GraphSAGE

See [`examples/train_example.py`](https://github.com/FalkorDB/falkordb-pyg/blob/main/examples/train_example.py) for a complete GraphSAGE training script that:

1. Populates FalkorDB with a synthetic paper-citation graph
2. Creates a remote backend with `get_remote_backend`
3. Fetches features and edge indices lazily
4. Trains a two-layer GraphSAGE classifier

## Reference

- [falkordb-pyg on GitHub](https://github.com/FalkorDB/falkordb-pyg)
- [falkordb-pyg on PyPI](https://pypi.org/project/falkordb-pyg/)
- [PyG Remote Backend documentation](https://pytorch-geometric.readthedocs.io/en/latest/advanced/remote.html)
- [FalkorDB Python client](https://github.com/FalkorDB/falkordb-py)

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What is falkordb-pyg used for?"
  a1="It enables you to train **Graph Neural Networks** (GNNs) directly on graphs stored in FalkorDB using PyTorch Geometric's remote backend interface, without exporting data to files first."
  q2="What are the minimum version requirements?"
  a2="You need **Python >= 3.10**, **PyTorch >= 2.0**, **PyTorch Geometric >= 2.4**, and **FalkorDB Python client >= 1.0**. Install with `pip install falkordb-pyg` or `pip install 'falkordb-pyg[torch]'` for bundled PyTorch."
  q3="Does falkordb-pyg support heterogeneous graphs?"
  a3="Yes, it fully supports **heterogeneous graphs** with multiple node and edge types. Use the `node_type_to_label` and `edge_type_to_rel` parameters in `get_remote_backend` to map PyG types to FalkorDB labels."
  q4="How does node ID remapping work?"
  a4="FalkorDB assigns internal integer IDs that may not be contiguous. The `NodeIDMapper` automatically builds a bidirectional mapping between FalkorDB IDs and contiguous 0-based PyG indices on first access."
  q5="Can I use standard PyG data loaders with this backend?"
  a5="Yes, the remote backend works as a **drop-in replacement** with `NeighborLoader`, `LinkNeighborLoader`, and any other PyG data loader that accepts a `(FeatureStore, GraphStore)` tuple."
%}
