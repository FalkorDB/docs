---
layout: default
title: Home
nav_order: 1
description: "The fastest way to your knowledge"
permalink: /
---

# FalkorDB

[![Docker Hub](https://img.shields.io/docker/pulls/falkordb/falkordb?label=Docker)](https://hub.docker.com/r/falkordb/falkordb/)
[![Discord](https://img.shields.io/discord/1146782921294884966?style=flat-square)](https://discord.gg/ErBEqN9E)

[![Try Free](https://img.shields.io/badge/Try%20Free-FalkorDB%20Cloud-FF8101?labelColor=FDE900&style=for-the-badge&link=https://app.falkordb.cloud)](https://app.falkordb.cloud)


FalkorDB is a blazing fast graph database used for low latency & high throughput scenarios, under the hood it runs [GraphBLAS](http://faculty.cse.tamu.edu/davis/GraphBLAS.html)  to perform graph operations using sparse linear algebra.

## Primary features

* Adopting the [Property Graph Model](https://github.com/opencypher/openCypher/blob/master/docs/property-graph-model.adoc)
* Supports [OpenCypher](http://www.opencypher.org/) query language with proprietary extensions
* Offers [Full-Text Search](/cypher/indexing#full-text-indexing), [Vector Similarly](/cypher/indexing#vector-indexing) & [Numeric indexing](/cypher/indexing).
* Interacts via either [RESP](https://redis.io/docs/reference/protocol-spec/) and [Bolt](https://en.wikipedia.org/wiki/Bolt_(network_protocol)) protocols
* Graphs represented as sparse adjacency matrices


## Give it a try

Launch an instance using docker, or use [FalkorDB Clouds](https://app.falkordb.cloud)

```sh
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:latest
```

Once loaded you can interact with FalkorDB using any of the supported [client libraries](/clients)

Here we'll use [FalkorDB Python client](https://pypi.org/project/FalkorDB/) to create a small graph representing a subset of motorcycle riders and teams taking part in the MotoGP league, once created we'll start querying our data.

```python
from falkordb import FalkorDB

# Connect to FalkorDB
db = FalkorDB(host='localhost', port=6379)

# Create the 'MotoGP' graph
g = db.select_graph('MotoGP')
# Clear out this graph in case you've run this script before.
g.delete()
g.query("""CREATE
           (:Rider {name:'Valentino Rossi'})-[:rides]->(:Team {name:'Yamaha'}),
           (:Rider {name:'Dani Pedrosa'})-[:rides]->(:Team {name:'Honda'}),
           (:Rider {name:'Andrea Dovizioso'})-[:rides]->(:Team {name:'Ducati'})""")

# Query which riders represents Yamaha?
res = g.query("""MATCH (r:Rider)-[:rides]->(t:Team)
                 WHERE t.name = 'Yamaha'
                 RETURN r.name""")

for row in res.result_set:
    print(row[0]) # Prints: "Valentino Rossi"

# Query how many riders represent team Ducati ?
res = g.query("""MATCH (r:Rider)-[:rides]->(t:Team {name:'Ducati'}) RETURN count(r)""")

print(res.result_set[0][0]) # Prints: 1
```

For additional demos please see visit [Demos](https://github.com/FalkorDB/demos).

## Client libraries

Language-specific clients have been written by the community and the FalkorDB team.
The full list and links can be found on the [Clients](/clients) page.

## Data import

When loading large graphs from CSV files, we recommend using [falkordb-bulk-loader](https://github.com/falkordb/falkordb-bulk-loader)

## Mailing List / Forum

Got questions? Please contact us at the [FalkorDB forum](https://github.com/FalkorDB/FalkorDB/discussions).

## License

FalkorDB is licensed under the [the Server Side Public License v1 (SSPLv1)](https://github.com/FalkorDB/FalkorDB/blob/master/LICENSE.txt).
