---
title: "GRAPH.PROFILE"
nav_order: 6
description: >
    Executes a query and returns an execution plan augmented with metrics for each operation's execution
parent: "Commands"
---

# GRAPH.PROFILE

Executes a query and produces an execution plan augmented with metrics for each operation's execution.

Arguments: `Graph name, Query`

Returns: `String representation of a query execution plan, with details on results produced by and time spent in each operation.`

`GRAPH.PROFILE` is a parallel entrypoint to `GRAPH.QUERY`. It accepts and executes the same queries, but it will not emit results,
instead returning the operation tree structure alongside the number of records produced and total runtime of each operation.

It is important to note that this blends elements of [GRAPH.QUERY](/commands/graph.query) and [GRAPH.EXPLAIN](/commands/graph.explain).
It is not a dry run and will perform all graph modifications expected of the query, but will not output results produced by a `RETURN` clause or query statistics.

{% capture shell_0 %}
GRAPH.PROFILE imdb \
"MATCH (actor_a:Actor)-[:ACT]->(:Movie)<-[:ACT]-(actor_b:Actor)
WHERE actor_a <> actor_b
CREATE (actor_a)-[:COSTARRED_WITH]->(actor_b)"

1) "Create | Records produced: 11208, Execution time: 168.208661 ms"
2) "    Filter | Records produced: 11208, Execution time: 1.250565 ms"
3) "        Conditional Traverse | Records produced: 12506, Execution time: 7.705860 ms"
4) "            Node By Label Scan | (actor_a:Actor) | Records produced: 1317, Execution time: 0.104346 ms"
{% endcapture %}

{% capture python_0 %}
from falkordb import FalkorDB
client = FalkorDB()
graph = client.select_graph('imdb')
query = '''\
MATCH (actor_a:Actor)-[:ACT]->(:Movie)<-[:ACT]-(actor_b:Actor)
WHERE actor_a <> actor_b
CREATE (actor_a)-[:COSTARRED_WITH]->(actor_b)
'''
result = graph.profile(query)
for line in result:
    print(line)
{% endcapture %}

{% capture javascript_0 %}
import { FalkorDB } from 'falkordb';
const client = await FalkorDB.connect();
const graph = client.selectGraph('imdb');
const query = `\
MATCH (actor_a:Actor)-[:ACT]->(:Movie)<-[:ACT]-(actor_b:Actor)
WHERE actor_a <> actor_b
CREATE (actor_a)-[:COSTARRED_WITH]->(actor_b)
`;
const result = await graph.profile(query);
result.forEach(line => console.log(line));
{% endcapture %}

{% capture java_0 %}
FalkorDB client = new FalkorDB();
Graph graph = client.selectGraph("imdb");
String query = """
MATCH (actor_a:Actor)-[:ACT]->(:Movie)<-[:ACT]-(actor_b:Actor)
WHERE actor_a <> actor_b
CREATE (actor_a)-[:COSTARRED_WITH]->(actor_b)
""";
ResultSet result = graph.profile(query);
for (String line : result) {
    System.out.println(line);
}
{% endcapture %}

{% capture rust_0 %}
let client = FalkorDB::connect_default();
let graph = client.select_graph("imdb");
let query = r#"
MATCH (actor_a:Actor)-[:ACT]->(:Movie)<-[:ACT]-(actor_b:Actor)
WHERE actor_a <> actor_b
CREATE (actor_a)-[:COSTARRED_WITH]->(actor_b)
"#;
let result = graph.profile(query)?;
for line in result {
    println!("{}", line);
}
{% endcapture %}

{% include code_tabs.html id="profile_tabs" shell=shell_0 python=python_0 javascript=javascript_0 java=java_0 rust=rust_0 %}
