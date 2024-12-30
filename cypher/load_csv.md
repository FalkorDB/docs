---
title: "LOAD CSV"
nav_order: 17
description: >
    LOAD CSV alows a query to access data within a CSV file
parent: "Cypher Language"
---

# LOAD CSV

```sh
LOAD CSV FROM 'file://actors.csv' AS row
MERGE (a:Actor {name: row[0]})
```

`LOAD CSV FROM` accepts a string containing the path to a CSV file,
the file is parsed line by line, the current line is accessible through the 
variable specified by `AS`. Each parsed value is treated as a `string`, use
the right convertion functions e.g. `toInteger` to cast a value to its
appropriate type.

Additional clauses can follow and accesses the `row` variable

## IMPORTING DATA

### Importing local files

FalkorDB defines a data directory ![see configuration](../configuration)
Under which local CSV files should be stored, all `file://` URIs are resolved
relatively to that directory.

In the following example we'll load the `actors.csv` file into FalkorDB.

### actors.csv

| Lee Pace       | 1979      | 
| ---------------|-----------|
| Vin Diesel     | 1967      |
| Chris Pratt    | 1979      |
| Zoe Saldana    | 1978      |

```sh
LOAD CSV FROM 'file://actors.csv'
AS row
MERGE (a:Actor {name: row[0], birth_year: toInteger(row[1])})
RETURN a.name, a.birth_year
```

Note that we've used indicies e.g. `row[0]` to access the value at the coresponding
column.

In case the CSV contains a header row e.g.

### actors.csv

| name           | birthyear |
| ---------------|-----------|
| Lee Pace       | 1979      | 
| Vin Diesel     | 1967      |
| Chris Pratt    | 1979      |
| Zoe Saldana    | 1978      |

Then we should use the `WITH HEADERS` variation of the `LOAD CSV` clause

```
LOAD CSV WITH HEADERS FROM 'file://actors.csv'
AS row
MERGE (a:Actor {name: row[name], birth_year: toInteger(row[birthyear])})
RETURN a.name, a.birth_year
```

Note when a header row exists and `WITH HEADER` is specified the `row` variable
is no longer an `array` but rather a `map`, accessing the individual elements
is done via their column name.


### Importing data from multiple csvs

Building on our previous example we'll introduce a second csv file `acted_in.csv`
which ties actors to movies they've acted in


### acted_in.csv

| actor          | movie          |
| ---------------|----------------|
| Lee Pace       | The Fall       | 
| Vin Diesel     | Fast & Furious |
| Chris Pratt    | Passengers     |
| Zoe Saldana    | Avatar         |


We'll create a new graph connecting actors to the movies they've acted in

Load actors:

```sh
LOAD CSV WITH HEADER FROM 'file://actors.csv'
AS row
MERGE (a:Actor {name:row['name']})
```

Load movies and create `ACTED_IN` relations:

```sh
LOAD CSV WITH HEADER FROM 'file://acted_in.csv'
AS row

MATCH (a:Actor {name: row['actor']})
MERGE (m:Movie {title: row['movie']})
MERGE (a)-[:ACTED_IN]->(m)
```

