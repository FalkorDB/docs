---
title: "Commands"
description: Commands overview
nav_order: 3
has_children: true
---

# Commands

## FalkorDB Features

FalkorDB is a graph database that exposes its functionality using the [openCypher](https://opencypher.org/) query language. Its basic commands accept openCypher queries, while additional commands are exposed for configuration or metadata retrieval.

## FalkorDB API

Command details can be retrieved by filtering for the [module](/commands/?group=graph) or for a specific command, e.g., `GRAPH.QUERY`.
The details include the syntax for the commands, where:

*   Optional arguments are enclosed in square brackets, for example `[timeout]`.
*   Additional optional arguments are indicated by an ellipsis: `...`

Most commands require a graph key name as their first argument.

{% include faq_accordion.html title="Frequently Asked Questions" q1="What query language does FalkorDB use?" a1="FalkorDB uses the **openCypher** query language, an open standard for graph query languages. Most of the Cypher specification is supported." q2="How are FalkorDB commands structured?" a2="FalkorDB commands are Redis module commands prefixed with `GRAPH.` (e.g., `GRAPH.QUERY`, `GRAPH.DELETE`). Most commands require a graph key name as their first argument." q3="What does the square bracket notation mean in command syntax?" a3="Square brackets like `[timeout]` indicate optional arguments. An ellipsis (`...`) after optional arguments means additional optional parameters may follow." q4="Do I need to create a graph before querying it?" a4="No. FalkorDB automatically creates a graph when you first run a `GRAPH.QUERY` command against a new graph key name. There is no separate 'CREATE GRAPH' command." q5="Can I use FalkorDB with any Redis client?" a5="Yes. Since FalkorDB is a Redis module, you can use any Redis client to send commands. However, dedicated FalkorDB client libraries (Python, JavaScript, Java, Rust) provide higher-level abstractions for easier use." %}
