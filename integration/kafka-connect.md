
![FalkorDB x Kafka Connect Banner](https://github.com/user-attachments/assets/941bb532-8613-4135-b4c9-232a700da314)


| **Title**           | **Kafka Connect Sink**            |
|----------------------|-------------------------------------|
| **Nav Order**        | 2                                   |
| **Description**      | Kafka Connect sink detailed doc    |
| **Parent**           | Integration                         |



## Get Started

- [Obtaining the connector](#obtaining-the-connector)
- [Configuring the connector](#configuring-the-connector)
- [Kafka message format](#kafka-message-format)

---

### **1️⃣ Obtaining the Connector**

You can build the connector from [source](https://github.com/FalkorDB/falkordb-kafka-connect) or download the pre-built  [JAR](https://github.com/FalkorDB/falkordb-kafka-connect/releases/download/v1.0.0/falkordb-kafka-connect-uber.jar) file from the releases. The GitHub repository includes a README with instructions for running the connector locally. The [GitHub](https://github.com/FalkorDB/falkordb-kafka-connect?tab=readme-ov-file#how-to-run-the-example) repository includes a README with instructions for running the connector locally.

### **2️⃣ Configuring the Connector**

Kafka Connector Properties Overview: 
This document explains the properties required to configure the FalkorDB Sink Connector for Apache Kafka. 
>Configurations should be specified in a properties file format.

#### Properties Overview

| **Property**                  | **Description**                                                                                                                                  |
|--------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `name`                        | Specifies the unique name of the connector instance, e.g., `falkordb-connector`. This name identifies the connector in the Kafka Connect framework. |
| `connector.class`             | Defines the Java class that implements the connector logic. Use `com.falkordb.FalkorDBSinkConnector` to write data from Kafka topics to FalkorDB. |
| `tasks.max`                   | Sets the maximum number of tasks for the connector. A value of `1` uses a single task. Increasing this can boost throughput but requires resources. |
| `topics`                      | Specifies the Kafka topic(s) to consume messages from. Set to `falkordb-topic` to read messages from this topic.                                  |
| `key.converter`               | Defines the converter class for message keys. `StringConverter` treats keys as simple strings.                                                   |
| `value.converter`             | Specifies the converter for message values. `StringConverter` treats values as strings.                                                           |
| `value.converter.schemas.enable` | Indicates whether schemas should be included with message values. Setting to `false` excludes schema information.                                |
| `falkor.url`                  | Specifies the connection URL for FalkorDB. Example: `redis://localhost:6379`. Essential for connecting Kafka to FalkorDB.                         |



>The above properties configure a Kafka Sink Connector that reads messages from a specified topic and writes them into
FalkorDB using string conversion for both keys and values. Adjusting these properties allows you to tailor the
connector's behavior according to your application's requirements.


## Configuration Example

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

## Kafka Message Format

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

The table below explains essential properties for executing commands in FalkorDB through Kafka messages.

| **Property**      | **Description**                                                                                                           | **Example**                                                                                             | **Explainer**                                                                                         |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| `graphName`       | Specifies the name of the graph database where the command will be executed.                                              | `"falkordb"`. Kafka messages can update multiple graphs.                                                |                                                    |
| `command`         | Indicates the type of operation being performed. `"GRAPH_QUERY"` means a query will be executed against the graph database. | `"GRAPH_QUERY"`                                                                                          |                                                   |
| `cypherCommand`   | Contains the actual Cypher query to be executed. Cypher is a query language for graph databases.                           | ```cypher CREATE (p:Person {name: $name_param, age: $age_param, location: $location_param}) RETURN p ``` | Creates a `Person` node with `name`, `age`, and `location` properties.                                |
| `parameters`      | Holds key-value pairs for placeholders in the `cypherCommand`.                                                             | ```json {"name_param": "Person 0", "age_param": 20, "location_param": "Location 0"} ```                  | Used to define properties for the new node.                                                           |

