---
title: "LOAD CSV"
nav_order: 17
description: >
    LOAD CSV allows a query to access data within a CSV file
parent: "Cypher Language"
---

# LOAD CSV

```cypher
LOAD CSV FROM 'file://actors.csv' AS row
MERGE (a:Actor {name: row[0]})
```

`LOAD CSV FROM` accepts a string path to a CSV file,
the file is parsed line by line, the current line is accessible through the 
variable specified by `AS`. Each parsed value is treated as a `string`, use
the right conversion functions e.g. `toInteger` to cast a value to its
appropriate type.

Additional clauses can follow and accesses the `row` variable

## IMPORTING DATA

### Importing local files

FalkorDB defines a data directory [see configuration](../configuration#import_folder)
Under which local CSV files should be stored, all `file://` URIs are resolved
relatively to that directory.

In the following example we'll load the `actors.csv` file into FalkorDB.

### actors.csv

| ||
| ---------------|-----------|
| Lee Pace       | 1979      | 
| Vin Diesel     | 1967      |
| Chris Pratt    | 1979      |
| Zoe Saldana    | 1978      |

```cypher
LOAD CSV FROM 'file://actors.csv'
AS row
MERGE (a:Actor {name: row[0], birth_year: toInteger(row[1])})
RETURN a.name, a.birth_year
```

Note that we've used indices e.g. `row[0]` to access the value at the corresponding
column.

In case the CSV contains a header row e.g.

### actors.csv

| name           | birthyear |
| :--------------| :---------|
| Lee Pace       | 1979      | 
| Vin Diesel     | 1967      |
| Chris Pratt    | 1979      |
| Zoe Saldana    | 1978      |

Then we should use the `WITH HEADERS` variation of the `LOAD CSV` clause

```cypher
LOAD CSV WITH HEADERS FROM 'file://actors.csv'
AS row
MERGE (a:Actor {name: row[name], birth_year: toInteger(row[birthyear])})
RETURN a.name, a.birth_year
```

Note when a header row exists and `WITH HEADER` is specified the `row` variable
is no longer an `array` but rather a `map`, accessing the individual elements
is done via their column name.


### Importing data from multiple CSVs

Building on our previous example we'll introduce a second csv file `acted_in.csv`
which ties actors to movies they've acted in


### acted_in.csv

| actor          | movie          |
| :--------------| :--------------|
| Lee Pace       | The Fall       | 
| Vin Diesel     | Fast & Furious |
| Chris Pratt    | Passengers     |
| Zoe Saldana    | Avatar         |


We'll create a new graph connecting actors to the movies they've acted in

Load actors:

```cypher
LOAD CSV WITH HEADER FROM 'file://actors.csv'
AS row
MERGE (a:Actor {name:row['name']})
```

Load movies and create `ACTED_IN` relations:

```cypher
LOAD CSV WITH HEADER FROM 'file://acted_in.csv'
AS row

MATCH (a:Actor {name: row['actor']})
MERGE (m:Movie {title: row['movie']})
MERGE (a)-[:ACTED_IN]->(m)
```

### Importing remote files

FalkorDB supports importing remote CSVs via HTTPS

Below we'll be loading the bigmac dataset from calmcode.io

```cypher
LOAD CSV WITH HEADERS FROM 'https://calmcode.io/static/data/bigmac.csv' AS row
RETURN row LIMIT 4

1) 1) "ROW"
2) 1) 1) "{date: 2002-04-01, currency_code: PHP, name: Philippines, local_price: 65.0, dollar_ex: 51.0, dollar_price: 1.27450980392157}"
   2) 1) "{date: 2002-04-01, currency_code: PEN, name: Peru, local_price: 8.5, dollar_ex: 3.43, dollar_price: 2.47813411078717}"
   3) 1) "{date: 2002-04-01, currency_code: NZD, name: New Zealand, local_price: 3.6, dollar_ex: 2.24, dollar_price: 1.60714285714286}"
   4) 1) "{date: 2002-04-01, currency_code: NOK, name: Norway, local_price: 35.0, dollar_ex: 8.56, dollar_price: 4.088785046728971}"
```

### Dealing with a large number of columns or missing entries

It's likely that not all cells in a CSV file are present, this makes
loading the data a bit more complicated. Luckly, there's an easy way around it
that's also useful for loading numerous of columns

Assuming this is the CSV file we're loading:


### missing_entries.csv

| name           | birthyear |
| :--------------| :---------|
| Lee Pace       | 1979      |
| Vin Diesel     |           |
| Chris Pratt    |           |
| Zoe Saldana    | 1978      |

Note: both Vin Diesel and Chris Pratt are missing their birthyear entry

Upon creating the Actor nodes We don't need to explicitly specify each column as we did so far,
the following query creates an empty Actor node and assigns the current CSV row to the node
this inturn sets the node's attribute-set to the current row

```cypher
LOAD CSV FROM 'file://missing_entries.csv' AS row
CREATE (a:Actor)
SET a = row
RETURN a

1) 1) "a"
2) 1) 1) 1) 1) "id"
            2) (integer) 0
         2) 1) "labels"
            2) 1) "Actor"
         3) 1) "properties"
            2) 1) 1) "name"
                  2) "Zoe Saldana"
               2) 1) "birthyear"
                  2) "1978"
   2) 1) 1) 1) "id"
            2) (integer) 1
         2) 1) "labels"
            2) 1) "Actor"
         3) 1) "properties"
            2) 1) 1) "name"
                  2) "Chris Pratt"
   3) 1) 1) 1) "id"
            2) (integer) 2
         2) 1) "labels"
            2) 1) "Actor"
         3) 1) "properties"
            2) 1) 1) "name"
                  2) "Vin Diesel"
   4) 1) 1) 1) "id"
            2) (integer) 3
         2) 1) "labels"
            2) 1) "Actor"
         3) 1) "properties"
            2) 1) 1) "name"
                  2) "Lee Pace"
               2) 1) "birthyear"
                  2) "1979"
```
