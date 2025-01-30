---
title: "Kafka Connect sink"
nav_order: 2
description: "Kafka Connect sink detailed doc"
parent: "integration"
---

## Table of Contents

- [Obtaining the connector](#obtaining-the-connector)
- [Configuring the connector](#configuring-the-connector)
- [Kafka message format](#kafka-message-format)
---

### **Obtaining the connector**

The connector can be built from [source](https://github.com/FalkorDB/falkordb-kafka-connect) or extract the
connector [jar](https://github.com/FalkorDB/falkordb-kafka-connect/releases/download/v1.0.0/falkordb-kafka-connect-uber.jar)
from the [releases](https://github.com/FalkorDB/falkordb-kafka-connect/releases). There is a README in
the [GitHub](https://github.com/FalkorDB/falkordb-kafka-connect?tab=readme-ov-file#how-to-run-the-example) repository
that explains how to run the connector locally.

### **Configuring the connector**

Kafka Connector Properties Explanation

This document provides a detailed explanation of the properties used to configure the FalkorDB Sink Connector for Apache
Kafka. The configuration is specified in a properties file format.

#### Properties Overview

- **name**: This property specifies the unique name of the connector instance. In this case, it is named
  `falkordb-connector`. This name is used to identify the connector in the Kafka Connect framework.

- **connector.class**: This property defines the Java class that implements the connector logic. Here,
  `com.falkordb.FalkorDBSinkConnector` indicates that this connector is designed to write data from Kafka topics to
  FalkorDB.

- **tasks.max**: This property sets the maximum number of tasks that can be created for this connector. A value of `1`
  means that only one task will be used to process data from the specified topic. Increasing this number can improve
  throughput but may require additional resources.

- **topics**: This property specifies which Kafka topic(s) the connector should consume messages from. In this case, it
  is set to `falkordb-topic`, meaning that the connector will read messages from this specific topic.

- **key.converter**: This property defines the converter class used to convert message keys from Kafka into a format
  that can be processed by the sink. Here, `StringConverter` indicates that keys will be treated as simple strings.

- **value.converter**: Similar to `key.converter`, this property specifies how message values should be converted. The
  use of `StringConverter` means that values will also be treated as strings.

- **value.converter.schemas.enable**: This property indicates whether schemas should be included with message values.
  Setting it to `false` means that no schema information will be sent along with the data, which may simplify processing
  if schemas are not needed.

- **falkor.url**: This property specifies the connection URL for FalkorDB. In this case, it points to a Redis instance
  running on `localhost` at port `6379`. This URL is crucial for establishing a connection between the Kafka connector
  and FalkorDB.

The above properties configure a Kafka Sink Connector that reads messages from a specified topic and writes them into
FalkorDB using string conversion for both keys and values. Adjusting these properties allows you to tailor the
connector's behavior according to your application's requirements.

Example:

  ```properties
name=falkordb-connector
connector.class=com.falkordb.FalkorDBSinkConnector
tasks.max=1
topics=falkordb-topic
key.converter=org.apache.kafka.connect.storage.StringConverter
value.converter=org.apache.kafka.connect.storage.StringConverter
value.converter.schemas.enable=false
falkor.url=redis://localhost:6379
  ```

### *Kafka message format*

#### JSON Structure Overview

The message is an array containing multiple objects, each representing a command to be executed on the graph database.
Below is a breakdown of the key components of each message object.

Example:

```json
[
  {
    "graphName": "falkordb",
    "command": "GRAPH_QUERY",
    "cypherCommand": "CREATE (p:Person {name: $name_param, age: $age_param, location: $location_param}) RETURN p",
    "parameters": {
      "location_param": "Location 0",
      "age_param": 20,
      "name_param": "Person 0"
    }
  },
  {
    "graphName": "falkordb",
    "command": "GRAPH_QUERY",
    "cypherCommand": "CREATE (p:Person {name: $name_param, age: $age_param, location: $location_param}) RETURN p",
    "parameters": {
      "location_param": "Location 1",
      "age_param": 21,
      "name_param": "Person 1"
    }
  }
]

```

#### Key Components

##### 1. `graphName`

- **Description**: This property specifies the name of the graph database where the command will be executed.
- **Example**: In this case, it is set to `"falkordb"`, it is possible to have one kafka messages update multiple graphs.

##### 2. `command`

- **Description**: This property indicates the type of operation being performed. Here, it is set to `"GRAPH_QUERY"`,
  signifying that a query will be executed against the graph database.

##### 3. `cypherCommand`

- **Description**: This property contains the actual Cypher query that will be executed. Cypher is a query language for
  graph databases.
- **Example**:

 ```cypher
   CREATE (p:Person {name: $name_param, age: $age_param, location: $location_param}) RETURN p
 ```

This command creates a new node labeled `Person` with properties for `name`, `age`, and `location`.

##### 4. `parameters`

- **Description**: This object holds the parameters that will replace placeholders in the `cypherCommand`. Each key
  corresponds to a placeholder in the Cypher query.
- **Example**:

```json
{
  "location_param": "Location 0",
  "age_param": 20,
  "name_param": "Person 0"
}
```

In this example, the parameters specify that a person named `"Person 0"` who is `20` years old and located at
`"Location 0"` will be created.

