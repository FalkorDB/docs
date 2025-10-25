---
layout: default
title: Home
nav_order: 1
description: "The fastest way to your knowledge"
permalink: /
---
[![Docker Hub](https://img.shields.io/docker/pulls/falkordb/falkordb?label=Docker&style=flat-square)](https://hub.docker.com/r/falkordb/falkordb/)
[![Discord](https://img.shields.io/discord/1146782921294884966?style=flat-square)](https://discord.gg/ErBEqN9E) 
[![Try Free](https://img.shields.io/badge/Try%20Free-FalkorDB%20Cloud-FF8101?labelColor=FDE900&style=flat-square)](https://app.falkordb.cloud)

<img src="https://github.com/user-attachments/assets/201b07e1-ac6d-4593-98cf-e58946d7766c" alt="FalkorDB Docs Readme Banner" fetchpriority="high" loading="eager">

# FalkorDB
### The Graph platform developers use to achieve accurate GraphRAG for enterprise GenAI

### About FalkorDB
FalkorDB delivers an **accurate, multi-tenant RAG solution powered by a low-latency, scalable graph database technology.** 

* Our solution is purpose-built for development teams working with complex, interconnected data—whether structured or unstructured—in real-time or interactive user environments. 

* The system supports the OpenCypher query language with proprietary enhancements that streamline interactions with graph data, and its efficient graph traversal and query capabilities render it well-suited for production environments.

### Choose Your Path
*   **Graph Path:** If you're interested in utilizing FalkorDB as a property graph database with OpenCypher support, continue with the sections below.
*   **GraphRAG Path:** If you're aiming to implement advanced graph reasoning and generative AI tasks, jump directly to the [GraphRAG SDK](https://github.com/FalkorDB/GraphRAG-SDK) section [1].


## Primary Features

* Adopts the [Property Graph Model](https://github.com/opencypher/openCypher/blob/master/docs/property-graph-model.adoc)
* Supports [OpenCypher](http://www.opencypher.org/) query language with proprietary extensions
* Offers [Full-Text Search](/cypher/indexing#full-text-indexing), [Vector Similarity](/cypher/indexing#vector-indexing) & [Numeric indexing](/cypher/indexing).
* Interacts via either [RESP](https://redis.io/docs/reference/protocol-spec/) and [Bolt](https://en.wikipedia.org/wiki/Bolt_(network_protocol)) protocols
* Graphs represented as sparse adjacency matrices
* Supports GraphRAG with the [GraphRAG SDK](https://github.com/FalkorDB/GraphRAG-SDK) for advanced graph reasoning and generative AI tasks.

## Get Started

Launch an instance using docker, or use [FalkorDB Clouds](https://app.falkordb.cloud)

```sh
docker run -p 6379:6379 -p 3000:3000 -it --rm falkordb/falkordb:latest
```

Once loaded you can interact with FalkorDB using any of the supported [client libraries](/clients)

Here we'll use [FalkorDB Python client](https://pypi.org/project/FalkorDB/) to create a small graph representing a subset of motorcycle riders and teams taking part in the MotoGP league, once created we'll start querying our data.

{% capture python_code %}
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
{% endcapture %}

{% capture javascript_code %}
import { FalkorDB } from 'falkordb';

const db = await FalkorDB.connect({
    // username: 'myUsername',
    // password: 'myPassword',
    socket: {
        host: 'localhost',
        port: 6379
    }
})

console.log('Connected to FalkorDB')

const graph = db.selectGraph('MotoGP')

await graph.query(`CREATE (:Rider {name:'Valentino Rossi'})-[:rides]->(:Team {name:'Yamaha'}),
        (:Rider {name:'Dani Pedrosa'})-[:rides]->(:Team {name:'Honda'}),
        (:Rider {name:'Andrea Dovizioso'})-[:rides]->(:Team {name:'Ducati'})`)

result = await graph.query(`MATCH (r:Rider)-[:rides]->(t:Team) 
                            WHERE t.name = $name RETURN r.name`, 
                            {params: {name: 'Yamaha'}})
                            
console.log(result) // Valentino Rossi

console.log(await db.list())
console.log(await db.info())

db.close()
{% endcapture %}


{% capture java_code %}
package com.falkordb;

import com.falkordb.*;
import java.util.*;

public class FalkorDBExample {
    public static void main(String[] args) {
        // Connect to FalkorDB
        Driver driver = FalkorDB.driver("localhost", 6379);

        // Select the graph
        Graph graph = driver.graph("MotoGP");

        // Create graph data
        graph.query("CREATE (:Rider {name:'Valentino Rossi'})-[:rides]->(:Team {name:'Yamaha'}), " +
                    "(:Rider {name:'Dani Pedrosa'})-[:rides]->(:Team {name:'Honda'}), " +
                    "(:Rider {name:'Andrea Dovizioso'})-[:rides]->(:Team {name:'Ducati'})");

        // Query with parameters
        Map<String, Object> params = new HashMap<>();
        params.put("name", "Yamaha");

        ResultSet resultSet = graph.query(
            "MATCH (r:Rider)-[:rides]->(t:Team) " +
            "WHERE t.name = $name RETURN r.name", params);

        // Process query results
        for (Record record : resultSet) {
            String riderName = record.getValue("r.name").toString();
            System.out.println(riderName); // Valentino Rossi
        }

        // Close the connection
        driver.close();
    }
}
{% endcapture %}

{% capture rust_code %}
use falkordb::{FalkorClientBuilder, FalkorConnectionInfo};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Connect to FalkorDB
    let connection_info: FalkorConnectionInfo = "falkor://127.0.0.1:6379"
        .try_into()
        .expect("Invalid connection info");

    let client = FalkorClientBuilder::new_async()
        .with_connection_info(connection_info)
        .build()
        .await?;

    // Select the 'MotoGP' graph
    let mut graph = client.select_graph("MotoGP");

    // Clear out this graph in case you've run this script before.
    graph.delete().await?;

    graph
        .query(
            r#"CREATE
           (:Rider {name:'Valentino Rossi'})-[:rides]->(:Team {name:'Yamaha'}),
           (:Rider {name:'Dani Pedrosa'})-[:rides]->(:Team {name:'Honda'}),
           (:Rider {name:'Andrea Dovizioso'})-[:rides]->(:Team {name:'Ducati'})"#,
        )
        .execute()
        .await?;

    // Query which riders represent Yamaha?
    let mut nodes = graph
        .query(
            r#"MATCH (r:Rider)-[:rides]->(t:Team)
                 WHERE t.name = 'Yamaha'
                 RETURN r.name"#,
        )
        .execute()
        .await?;

    for node in nodes.data.by_ref() {
        println!("{:?}", node);
    }

    // Query how many riders represent team Ducati?
    let mut nodes = graph
        .query(r#"MATCH (r:Rider)-[:rides]->(t:Team {name:'Ducati'}) RETURN count(r)"#)
        .execute()
        .await?;

    for node in nodes.data.by_ref() {
        println!("{:?}", node);
    }

    Ok(())
}
{% endcapture %}

{% capture shell_code %}
$ redis-cli -h localhost -p 6379

127.0.0.1:6379> GRAPH.QUERY MotoGP "CREATE (:Rider {name:'Valentino Rossi'})-[:rides]->(:Team {name:'Yamaha'}), (:Rider {name:'Dani Pedrosa'})-[:rides]->(:Team {name:'Honda'}), (:Rider {name:'Andrea Dovizioso'})-[:rides]->(:Team {name:'Ducati'})"
1) 1) "Labels added: 2"
   2) "Nodes created: 6"
   3) "Properties set: 6"
   4) "Relationships created: 3"
   5) "Cached execution: 0"
   6) "Query internal execution time: 9.155705 milliseconds"

127.0.0.1:6379> GRAPH.QUERY MotoGP "MATCH (r:Rider)-[:rides]->(t:Team) WHERE t.name = 'Yamaha' RETURN r.name"
1) 1) "r.name"
2) 1) 1) "Valentino Rossi"
3) 1) "Cached execution: 0"
   2) "Query internal execution time: 5.389149 milliseconds"

127.0.0.1:6379> GRAPH.QUERY MotoGP "MATCH (r:Rider)-[:rides]->(t:Team {name:'Ducati'}) RETURN count(r)"
1) 1) "count(r)"
2) 1) 1) (integer) 1
3) 1) "Cached execution: 0"
   2) "Query internal execution time: 1.153678 milliseconds"
{% endcapture %}

{% include code_tabs.html id="code_tabs_0" python=python_code javascript=javascript_code java=java_code rust=rust_code shell=shell_code %}

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
