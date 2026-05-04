---
title: "Apache Jena"
nav_order: 3
description: "How to use FalkorDB with Apache Jena via the jena-falkordb-adapter."
parent: "Integration"
---

# Apache Jena Integration

This page describes how to integrate FalkorDB with [Apache Jena](https://jena.apache.org/) using the [jena-falkordb-adapter](https://github.com/FalkorDB/jena-falkordb-adapter).

## Overview

The jena-falkordb-adapter allows applications built on Jena to use FalkorDB as a backend for RDF data storage and querying. This enables seamless graph data management and SPARQL query execution on FalkorDB.

## Getting Started

Follow the [GETTING_STARTED.md](https://github.com/FalkorDB/jena-falkordb-adapter/blob/main/GETTING_STARTED.md) guide for step-by-step instructions on setting up the adapter and connecting Jena to FalkorDB.

### Install from Maven

Add the FalkorDB Jena adapter dependency to your project's `pom.xml`. Replace the version with the latest release from the adapter repository.

```xml
<dependency>
  <groupId>com.falkordb</groupId>
  <artifactId>jena-falkordb-adapter</artifactId>
  <version>0.2.0</version>
</dependency>
```

If the adapter is published to a non-standard Maven repository, add the repository block shown in the adapter's README. Otherwise the dependency should resolve from Maven Central (if published there).

### Quick Getting Started (Java)

The snippet below shows a minimal Jena program that registers the FalkorDB adapter and runs a simple SPARQL query. This is intentionally small — see the adapter's `GETTING_STARTED.md` and `Main.java` for a complete example with configuration and connection options.

```java
import org.apache.jena.query.*;
import org.apache.jena.rdf.model.Model;

public class JenaFalkorExample {
    public static void main(String[] args) {
        // Create or obtain a Jena Model backed by FalkorDB.
        // The exact factory method depends on the adapter; check the adapter README/Main.java for the
        // connection options (hostname, port, credentials, etc.).
        Model model = FalkorDBJenaFactory.createModel("http://localhost:7474");

        // Example: add a triple
        model.createResource("http://example.org/alice")
             .addProperty(model.createProperty("http://example.org/knows"),
                          model.createResource("http://example.org/bob"));

        // Run a simple SPARQL SELECT
        String sparql = "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10";
        try (QueryExecution qexec = QueryExecutionFactory.create(sparql, model)) {
            ResultSet rs = qexec.execSelect();
            ResultSetFormatter.out(System.out, rs);
        }

        // Remember to close the model when finished
        model.close();
    }
}
```

Notes:
- Replace `FalkorDBJenaFactory.createModel(...)` with the actual adapter factory call used in the adapter (see `Main.java`).
- Use the adapter's configuration options (connection URL, authentication) when creating the model.


## Usage Example

See the [Main.java](https://github.com/FalkorDB/jena-falkordb-adapter/blob/main/src/main/java/com/falkordb/jena/Main.java) for a sample Java application demonstrating how to use the adapter.

## Reference

- [Adapter README](https://github.com/FalkorDB/jena-falkordb-adapter/blob/main/README.md)
- [Getting Started](https://github.com/FalkorDB/jena-falkordb-adapter/blob/main/GETTING_STARTED.md)
- [Sample Main.java](https://github.com/FalkorDB/jena-falkordb-adapter/blob/main/src/main/java/com/falkordb/jena/Main.java)

{% include faq_accordion.html title="Frequently Asked Questions" q1="What is the jena-falkordb-adapter used for?" a1="The adapter allows applications built on **Apache Jena** to use FalkorDB as a backend for RDF data storage and SPARQL query execution, enabling seamless graph data management with Jena's API." q2="How do I install the Jena FalkorDB adapter?" a2="Add the Maven dependency with groupId `com.falkordb` and artifactId `jena-falkordb-adapter` to your `pom.xml`. Check the [adapter repository](https://github.com/FalkorDB/jena-falkordb-adapter) for the latest version." q3="Can I run SPARQL queries against FalkorDB using Jena?" a3="Yes, once the adapter is configured, you can run standard **SPARQL SELECT, CONSTRUCT, and ASK** queries using Jena's `QueryExecutionFactory` against data stored in FalkorDB." q4="What Java version is required?" a4="Check the adapter's README for the exact Java version requirement. The adapter is built as a standard Maven project and typically requires **Java 11 or later**." %}
