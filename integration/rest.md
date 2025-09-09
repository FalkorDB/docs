---
title: "Rest API"
nav_order: 1
description: "Rest API detailed doc"
parent: "Integration"
---

# FalkorDB Browser REST API

REST API for FalkorDB Browser - Graph Database Management Interface

**Version:** 1.4.6

**Base URL:** Your FalkorDB Browser instance URL

**Authentication:** Bearer Token (JWT)

## Table of Contents

### Authentication
- [User login - POST /api/auth/login](#user-login---post-apiauthlogin)

### Status
- [Check FalkorDB connection status - GET /api/status](#check-falkordb-connection-status---get-apistatus)

### Graph Management
- [List all graphs - GET /api/graph](#list-all-graphs---get-apigraph)
- [Execute graph query - GET /api/graph/{graph}](#execute-graph-query---get-apigraphgraph)
- [Create or verify a graph - POST /api/graph/{graph}](#create-or-verify-a-graph---post-apigraphgraph)
- [Rename graph - PATCH /api/graph/{graph}](#rename-graph---patch-apigraphgraph)
- [Delete a graph - DELETE /api/graph/{graph}](#delete-a-graph---delete-apigraphgraph)
- [Get query execution plan - GET /api/graph/{graph}/explain](#get-query-execution-plan---get-apigraphgraphexplain)
- [Profile query execution - GET /api/graph/{graph}/profile](#profile-query-execution---get-apigraphgraphprofile)
- [Get graph information - GET /api/graph/{graph}/info](#get-graph-information---get-apigraphgraphinfo)
- [Get graph element counts - GET /api/graph/{graph}/count](#get-graph-element-counts---get-apigraphgraphcount)
- [Export graph data - GET /api/graph/{graph}/export](#export-graph-data---get-apigraphgraphexport)
- [Duplicate a graph - PATCH /api/graph/{graph}/duplicate](#duplicate-a-graph---patch-apigraphgraphduplicate)
- [Get node information - GET /api/graph/{graph}/{node}](#get-node-information---get-apigraphgraphnode)
- [Delete node or relationship - DELETE /api/graph/{graph}/{node}](#delete-node-or-relationship---delete-apigraphgraphnode)
- [Add node label - POST /api/graph/{graph}/{node}/label](#add-node-label---post-apigraphgraphnodelabel)
- [Remove node label - DELETE /api/graph/{graph}/{node}/label](#remove-node-label---delete-apigraphgraphnodelabel)
- [Set node/relationship property - POST /api/graph/{graph}/{node}/{key}](#set-noderelationship-property---post-apigraphgraphnodekey)
- [Remove node/relationship property - DELETE /api/graph/{graph}/{node}/{key}](#remove-noderelationship-property---delete-apigraphgraphnodekey)

### Configuration Management
- [Get all configuration values - GET /api/graph/config](#get-all-configuration-values---get-apigraphconfig)
- [Get specific configuration value - GET /api/graph/config/{config}](#get-specific-configuration-value---get-apigraphconfigconfig)
- [Set configuration value - POST /api/graph/config/{config}](#set-configuration-value---post-apigraphconfigconfig)

### Schema Management
- [List all schemas - GET /api/schema](#list-all-schemas---get-apischema)
- [Get schema information - GET /api/schema/{schema}](#get-schema-information---get-apischemaschema)
- [Create new schema - POST /api/schema/{schema}](#create-new-schema---post-apischemaschema)
- [Rename schema - PATCH /api/schema/{schema}](#rename-schema---patch-apischemaschema)
- [Delete schema - DELETE /api/schema/{schema}](#delete-schema---delete-apischemaschema)
- [Get schema element counts - GET /api/schema/{schema}/count](#get-schema-element-counts---get-apischemaschemacount)
- [Duplicate schema - PATCH /api/schema/{schema}/duplicate](#duplicate-schema---patch-apischemaschemaduplicat)
- [Create node or relationship in schema - POST /api/schema/{schema}/new](#create-node-or-relationship-in-schema---post-apischemaschemanew)
- [Create node in schema - POST /api/schema/{schema}/nodes](#create-node-in-schema---post-apischemaschemanode)
- [Create relationship in schema - POST /api/schema/{schema}/relationships](#create-relationship-in-schema---post-apischemaschemarelationships)
- [Delete node from schema - DELETE /api/schema/{schema}/{nodeId}](#delete-node-from-schema---delete-apischemaschemanodeid)
- [Delete relationship from schema - DELETE /api/schema/{schema}/{relationshipId}](#delete-relationship-from-schema---delete-apischemaschemarelationshipid)
- [Add label to node - POST /api/schema/{schema}/{node}/label](#add-label-to-node---post-apischemaschemanode/label)
- [Remove label from node - DELETE /api/schema/{schema}/{node}/label](#remove-label-from-node---delete-apischemaschemanode/label)
- [Add/Update attribute to node - PATCH /api/schema/{schema}/{nodeId}/{key}](#addupdate-attribute-to-node---patch-apischemaschemanodeidkey)
- [Remove attribute from node - DELETE /api/schema/{schema}/{nodeId}/{key}](#remove-attribute-from-node---delete-apischemaschemanodeidkey)
- [Add/Update attribute to relationship - PATCH /api/schema/{schema}/{relationshipId}/{key}](#addupdate-attribute-to-relationship---patch-apischemaschemarelationshipidkey)
- [Remove attribute from relationship - DELETE /api/schema/{schema}/{relationshipId}/{key}](#remove-attribute-from-relationship---delete-apischemaschemarelationshipidkey)

### User Management
- [List all users - GET /api/user](#list-all-users---get-apiuser)
- [Create new user - POST /api/user](#create-new-user---post-apiuser)
- [Delete multiple users - DELETE /api/user](#delete-multiple-users---delete-apiuser)
- [Update user role - PATCH /api/user/{user}](#update-user-role---patch-apiuseruser)

---

## Authentication

All endpoints except `/api/auth/login` require authentication using a JWT bearer token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### **User login** - `POST /api/auth/login`

Authenticate user with username and password.

#### Request Body

- Content-Type: `application/json`
- Required fields: `username`, `password`

Example request:
```json
{
  "username": "default",
  "password": "password"
}
```

#### Responses

- **200**: Login successful
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": {
        "username": "default",
        "role": "Admin"
      }
    }
    ```

- **400**: Bad request - missing username or password
- **401**: Invalid credentials
- **500**: Internal server error

---

## Status

### **Check FalkorDB connection status** - `GET /api/status`

Returns the current connection status to the FalkorDB database.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Responses

- **200**: Database is online and accessible
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "status": "online"
    }
    ```

- **404**: Database is offline or not accessible
- **500**: Internal server error

---

## Graph Management

### **List all graphs** - `GET /api/graph`

Get a list of all graphs in the FalkorDB instance.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Responses

- **200**: List of graphs retrieved successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "opts": [
        "social_network",
        "product_catalog",
        "user_interactions"
      ]
    }
    ```

- **400**: Bad request
- **500**: Internal server error

### **Execute graph query** - `GET /api/graph/{graph}`

Execute a Cypher query on the specified graph (Server-Sent Events).

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name to query
  - Example: `social_network`
- `query` (query, required): Cypher query to execute
  - Example: `MATCH (n) RETURN n LIMIT 10`
- `timeout` (query, required): Query timeout in milliseconds
  - Example: `30000`

#### Responses

- **200**: Query executed successfully (Server-Sent Events stream)

### **Create or verify a graph** - `POST /api/graph/{graph}`

Create a new graph or verify that a graph exists.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name to create or verify

#### Responses

- **200**: Graph created or verified successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "Graph created successfully"
    }
    ```

- **400**: Bad request
- **500**: Internal server error

### **Rename graph** - `PATCH /api/graph/{graph}`

Rename an existing graph to a new name.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): New graph name
- `sourceName` (query, required): Current graph name to rename

#### Responses

- **200**: Graph renamed successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "data": {
        "result": "Graph renamed successfully"
      }
    }
    ```

- **400**: Bad request - graph already exists or missing sourceName
- **500**: Internal server error

### **Delete a graph** - `DELETE /api/graph/{graph}`

Delete a graph from the FalkorDB instance.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name to delete

#### Responses

- **200**: Graph deleted successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "graph_name graph deleted"
    }
    ```

- **400**: Bad request
- **500**: Internal server error

### **Get query execution plan** - `GET /api/graph/{graph}/explain`

Get the execution plan for a Cypher query without executing it.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name
- `query` (query, required): Cypher query to explain

#### Responses

- **200**: Query execution plan returned successfully

### **Profile query execution** - `GET /api/graph/{graph}/profile`

Get detailed profiling information for a Cypher query.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name
- `query` (query, required): Cypher query to profile

#### Responses

- **200**: Query profiling information returned successfully

### **Get graph information** - `GET /api/graph/{graph}/info`

Get specific information about a graph (functions, property keys, labels, or relationship types).

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name
- `type` (query, required): Type of information to retrieve
  - Options: `(function)`, `(property key)`, `(label)`, `(relationship type)`
  - Example: `(label)`

#### Responses

- **200**: Graph information retrieved successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": {
        "data": [
          {"(label)": "Person"},
          {"(label)": "Company"}
        ]
      }
    }
    ```

- **400**: Bad request - missing or invalid type parameter

### **Get graph element counts** - `GET /api/graph/{graph}/count`

Get the count of nodes and relationships in a graph.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name

#### Responses

- **200**: Element counts retrieved successfully

### **Export graph data** - `GET /api/graph/{graph}/export`

Export graph data in various formats.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name

#### Responses

- **200**: Graph data exported successfully

### **Duplicate a graph** - `PATCH /api/graph/{graph}/duplicate`

Create a copy of an existing graph with a new name.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): New graph name for the duplicate
- `sourceName` (query, required): Source graph name to duplicate from

#### Responses

- **200**: Graph duplicated successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": {
        "status": "Graph duplicated successfully"
      }
    }
    ```

- **400**: Bad request - missing sourceName parameter
- **500**: Internal server error

### **Get node information** - `GET /api/graph/{graph}/{node}`

Get detailed information about a specific node.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name
- `node` (path, required): Node ID

#### Responses

- **200**: Node information retrieved successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": {
        "data": [
          {
            "node": {
              "id": 1,
              "labels": ["Person"],
              "properties": {
                "name": "John Doe",
                "age": 30
              }
            },
            "relationships": []
          }
        ]
      }
    }
    ```

- **400**: Bad request
- **500**: Internal server error

### **Delete node or relationship** - `DELETE /api/graph/{graph}/{node}`

Delete a node or relationship from the graph.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name
- `node` (path, required): Node or relationship ID

#### Request Body

- Content-Type: `application/json`
- Required field: `type`

Example request:
```json
{
  "type": true
}
```

- `type`: `true` to delete a node, `false` to delete a relationship

#### Responses

- **200**: Node or relationship deleted successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "Node deleted successfully"
    }
    ```

- **400**: Bad request - missing type parameter
- **500**: Internal server error

### **Add node label** - `POST /api/graph/{graph}/{node}/label`

Add a label to a specific node.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name
- `node` (path, required): Node ID

#### Request Body

- Content-Type: `application/json`

Example request:
```json
{
  "label": "your_label"
}
```

#### Responses

- **200**: Label added successfully

### **Remove node label** - `DELETE /api/graph/{graph}/{node}/label`

Remove a label from a specific node.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name
- `node` (path, required): Node ID

#### Request Body

- Content-Type: `application/json`

Example request:
```json
{
  "label": "your_label"
}
```

#### Responses

- **200**: Label removed successfully

### **Set node/relationship property** - `POST /api/graph/{graph}/{node}/{key}`

Set a property value on a node or relationship.

**IMPORTANT:** Use `type=true` for nodes, `type=false` for relationships.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name
- `node` (path, required): Node or relationship ID
- `key` (path, required): Property key name

#### Request Body

- Content-Type: `application/json`
- Required fields: `value`, `type`

Example request:
```json
{
  "value": "your_property_value",
  "type": true
}
```

- `value`: Property value to set
- `type`: `true` for nodes, `false` for relationships

#### Responses

- **200**: Property set successfully

### **Remove node/relationship property** - `DELETE /api/graph/{graph}/{node}/{key}`

Remove a property from a node or relationship.

**IMPORTANT:** Use `type=true` for nodes, `type=false` for relationships.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `graph` (path, required): Graph name
- `node` (path, required): Node or relationship ID
- `key` (path, required): Property key name

#### Request Body

- Content-Type: `application/json`
- Required field: `type`

Example request:
```json
{
  "type": true
}
```

- `type`: `true` for nodes, `false` for relationships

#### Responses

- **200**: Property removed successfully

---

## Configuration Management

### **Get all configuration values** - `GET /api/graph/config`

Get all FalkorDB configuration parameters and their values.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Responses

- **200**: Configuration values retrieved successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "configs": {
        "MAX_INFO_QUERIES": 700,
        "CMD_INFO": "server",
        "TIMEOUT": 1000
      }
    }
    ```

- **400**: Bad request
- **500**: Internal server error

### **Get specific configuration value** - `GET /api/graph/config/{config}`

Get the value of a specific configuration parameter.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `config` (path, required): Configuration parameter name
  - Example: `MAX_INFO_QUERIES`

#### Responses

- **200**: Configuration value retrieved successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "config": 700
    }
    ```

- **400**: Bad request
- **500**: Internal server error

### **Set configuration value** - `POST /api/graph/config/{config}`

Set the value of a specific configuration parameter.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `config` (path, required): Configuration parameter name
  - Example: `MAX_INFO_QUERIES`
- `value` (query, required): Configuration value to set (numeric values will be parsed as integers except for CMD_INFO)
  - Example: `700`

#### Responses

- **200**: Configuration value set successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "config": "OK"
    }
    ```

- **400**: Bad request - missing value or invalid value
- **500**: Internal server error

---

## Schema Management

### **List all schemas** - `GET /api/schema`

Get a list of all schemas in the FalkorDB instance.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Responses

- **200**: List of schemas retrieved successfully

### **Get schema information** - `GET /api/schema/{schema}`

Get detailed information about a specific schema.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name

#### Responses

- **200**: Schema information retrieved successfully

### **Create new schema** - `POST /api/schema/{schema}`

Create a new schema with the specified name.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name to create

#### Responses

- **201**: Schema created successfully

### **Rename schema** - `PATCH /api/schema/{schema}`

Rename an existing schema to a new name.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): New schema name
- `sourceName` (query, required): Current schema name to rename

#### Responses

- **200**: Schema renamed successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "data": {
        "result": "Schema renamed successfully"
      }
    }
    ```

- **400**: Bad request - schema already exists or missing sourceName
- **500**: Internal server error

### **Delete schema** - `DELETE /api/schema/{schema}`

Delete a schema and all its data permanently.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name to delete

#### Responses

- **200**: Schema deleted successfully

### **Get schema element counts** - `GET /api/schema/{schema}/count`

Get the count of nodes and relationships in a schema.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name

#### Responses

- **200**: Schema element counts retrieved successfully

### **Duplicate schema** - `PATCH /api/schema/{schema}/duplicate`

Create a copy of an existing schema with a new name, preserving all data and structure.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): New schema name for the duplicate
- `sourceName` (query, required): Source schema name to duplicate from

#### Responses

- **200**: Schema duplicated successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": {
        "status": "Schema duplicated successfully"
      }
    }
    ```

- **400**: Bad request - missing sourceName parameter
- **500**: Internal server error

### **Create node or relationship in schema** - `POST /api/schema/{schema}/new`

The actual backend endpoint for creating nodes and relationships. Use `type=true` for nodes, `type=false` for relationships.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name

#### Request Body

- Content-Type: `application/json`
- Required fields: `type`, `label`, `attributes`

Example request for node creation:
```json
{
  "type": true,
  "label": ["Person", "User"],
  "attributes": [
    ["name", ["STRING", "", "false", "true"]],
    ["age", ["INTEGER", "0", "false", "false"]]
  ]
}
```

Example request for relationship creation:
```json
{
  "type": false,
  "label": ["KNOWS"],
  "attributes": [
    ["since", ["STRING", "2024", "false", "false"]]
  ],
  "selectedNodes": [{"id": 1}, {"id": 2}]
}
```

- `type`: `true` for node creation, `false` for relationship creation
- `label`: For nodes: Multiple labels supported (e.g., `["Person", "User"]`). For relationships: Relationship type (only first label used, e.g., `["KNOWS"]`)
- `attributes`: Attribute definitions: `[[key, [type, default, unique, required]], ...]`
- `selectedNodes`: Required for relationship creation only. Source and target nodes (exactly 2 nodes)

#### Responses

- **200**: Node or relationship created successfully

### **Create node in schema** - `POST /api/schema/{schema}/nodes`

Create a new node in the specified schema. Multiple labels are supported and will be joined with colons (e.g., `:Person:User`). This endpoint maps to `/api/schema/{schema}/new` with `type=true`.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name

#### Request Body

- Content-Type: `application/json`
- Required fields: `type`, `label`, `attributes`

Example request:
```json
{
  "type": true,
  "label": ["Person", "User"],
  "attributes": [
    ["name", ["STRING", "", "false", "true"]],
    ["age", ["INTEGER", "0", "false", "false"]]
  ]
}
```

- `type`: Must be `true` for node creation
- `label`: Labels for the node (multiple labels supported)
- `attributes`: Attribute definitions: `[[key, [type, default, unique, required]], ...]`

#### Responses

- **200**: Node created successfully

### **Create relationship in schema** - `POST /api/schema/{schema}/relationships`

Create a new relationship between two nodes in the specified schema. Only the first label in the array is used as the relationship type. This endpoint maps to `/api/schema/{schema}/new` with `type=false`.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name

#### Request Body

- Content-Type: `application/json`
- Required fields: `type`, `label`, `attributes`, `selectedNodes`

Example request:
```json
{
  "type": false,
  "label": ["KNOWS"],
  "attributes": [
    ["since", ["STRING", "2024", "false", "false"]]
  ],
  "selectedNodes": [{"id": 1}, {"id": 2}]
}
```

- `type`: Must be `false` for relationship creation
- `label`: Relationship type (only first label used)
- `attributes`: Attribute definitions: `[[key, [type, default, unique, required]], ...]`
- `selectedNodes`: Source and target nodes for the relationship (exactly 2 nodes)

#### Responses

- **200**: Relationship created successfully

### **Delete node from schema** - `DELETE /api/schema/{schema}/{nodeId}`

Delete a specific node from the schema by ID. Set `type=true` for node deletion.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name
- `nodeId` (path, required): Node ID to delete

#### Request Body

- Content-Type: `application/json`
- Required field: `type`

Example request:
```json
{
  "type": true
}
```

- `type`: Must be `true` for node deletion

#### Responses

- **200**: Node deleted successfully

### **Delete relationship from schema** - `DELETE /api/schema/{schema}/{relationshipId}`

Delete a specific relationship from the schema by ID. Set `type=false` for relationship deletion.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name
- `relationshipId` (path, required): Relationship ID to delete

#### Request Body

- Content-Type: `application/json`
- Required field: `type`

Example request:
```json
{
  "type": false
}
```

- `type`: Must be `false` for relationship deletion

#### Responses

- **200**: Relationship deleted successfully

### **Add label to node** - `POST /api/schema/{schema}/{node}/label`

Add a new label to an existing node in the schema.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name
- `node` (path, required): Node ID

#### Request Body

- Content-Type: `application/json`
- Required field: `label`

Example request:
```json
{
  "label": "your_label"
}
```

#### Responses

- **200**: Label added successfully

### **Remove label from node** - `DELETE /api/schema/{schema}/{node}/label`

Remove a specific label from an existing node in the schema.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name
- `node` (path, required): Node ID

#### Request Body

- Content-Type: `application/json`
- Required field: `label`

Example request:
```json
{
  "label": "your_label"
}
```

#### Responses

- **200**: Label removed successfully

### **Add/Update attribute to node** - `PATCH /api/schema/{schema}/{nodeId}/{key}`

Add a new attribute or update an existing attribute on a node in the schema.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name (example: `test`)
- `nodeId` (path, required): Node ID (example: `2`)
- `key` (path, required): Attribute key to add/update (example: `attribute_key`)

#### Request Body

- Content-Type: `application/json`
- Required fields: `type`, `attribute`

Example request:
```json
{
  "type": true,
  "attribute": ["STRING", "your_description", "false", "true"]
}
```

- `type`: Must be `true` for node attributes
- `attribute`: Attribute configuration `[type, default, unique, required]`

#### Responses

- **200**: Attribute added/updated successfully

### **Remove attribute from node** - `DELETE /api/schema/{schema}/{nodeId}/{key}`

Remove a specific attribute from a node in the schema.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name (example: `test`)
- `nodeId` (path, required): Node ID (example: `2`)
- `key` (path, required): Attribute key to remove (example: `attribute_key`)

#### Request Body

- Content-Type: `application/json`
- Required field: `type`

Example request:
```json
{
  "type": true
}
```

- `type`: Must be `true` for node attributes

#### Responses

- **200**: Attribute removed successfully

### **Add/Update attribute to relationship** - `PATCH /api/schema/{schema}/{relationshipId}/{key}`

Add a new attribute or update an existing attribute on a relationship in the schema.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name (example: `test`)
- `relationshipId` (path, required): Relationship ID (example: `1`)
- `key` (path, required): Attribute key to add/update (example: `since`)

#### Request Body

- Content-Type: `application/json`
- Required fields: `type`, `attribute`

Example request:
```json
{
  "type": false,
  "attribute": ["STRING", "2024", "false", "false"]
}
```

- `type`: Must be `false` for relationship attributes
- `attribute`: Attribute configuration `[type, default, unique, required]`

#### Responses

- **200**: Attribute added/updated successfully

### **Remove attribute from relationship** - `DELETE /api/schema/{schema}/{relationshipId}/{key}`

Remove a specific attribute from a relationship in the schema.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `schema` (path, required): Schema name (example: `test`)
- `relationshipId` (path, required): Relationship ID (example: `1`)
- `key` (path, required): Attribute key to remove (example: `since`)

#### Request Body

- Content-Type: `application/json`
- Required field: `type`

Example request:
```json
{
  "type": false
}
```

- `type`: Must be `false` for relationship attributes

#### Responses

- **200**: Attribute removed successfully

---

## User Management

### **List all users** - `GET /api/user`

Get a list of all FalkorDB users.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Responses

- **200**: List of users retrieved successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": [
        {
          "username": "john_doe",
          "role": "Read-Write",
          "selected": false
        },
        {
          "username": "admin_user",
          "role": "Admin",
          "selected": false
        }
      ]
    }
    ```

- **400**: Bad request
- **500**: Internal server error

### **Create new user** - `POST /api/user`

Create a new FalkorDB user with specified username, password, and role.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Request Body

- Content-Type: `application/json`
- Required fields: `username`, `password`, `role`

Example request:
```json
{
  "username": "new_user",
  "password": "secure_password",
  "role": "Read-Write"
}
```

- `username`: Username for the new user
- `password`: Password for the new user
- `role`: Role to assign to the user (`Admin`, `Read-Write`, `Read-Only`)

#### Responses

- **201**: User created successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "Success"
    }
    ```

  - Headers:
    - `location`: Location of the created user resource (example: `/api/db/user/new_user`)

- **400**: Bad request - missing parameters
- **409**: User already exists
- **500**: Internal server error

### **Delete multiple users** - `DELETE /api/user`

Delete multiple FalkorDB users by providing an array of usernames.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Request Body

- Content-Type: `application/json`
- Required field: `users`

Example request:
```json
{
  "users": [
    { "username": "user_1741261105156" },
    { "username": "another_user" }
  ]
}
```

- `users`: Array of user objects to delete

#### Responses

- **200**: Users deleted successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "Users deleted"
    }
    ```

- **400**: Bad request
- **500**: Internal server error

### **Update user role** - `PATCH /api/user/{user}`

Update the role of a FalkorDB user.

#### Headers
- `Authorization: Bearer <token>` (required)

#### Parameters
- `user` (path, required): Username to update
- `role` (query, required): New role for the user (`Admin`, `Read-Write`, `Read-Only`)

#### Responses

- **200**: User role updated successfully

---

## Error Responses

All endpoints may return the following common error responses:

- **401**: Unauthorized - Invalid or missing authentication token
- **403**: Forbidden - Insufficient permissions for the requested operation
- **404**: Not Found - Requested resource does not exist
- **500**: Internal Server Error - Unexpected server error

## Data Types

### Attribute Types
The following data types are supported for node and relationship attributes:

- `STRING`: Text values
- `INTEGER`: Numeric integer values  
- `FLOAT`: Numeric decimal values
- `BOOLEAN`: True/false values

### Attribute Configuration
When defining attributes, use the following format:
```json
[type, default_value, unique, required]
```

- `type`: One of the supported data types (`STRING`, `INTEGER`, `FLOAT`, `BOOLEAN`)
- `default_value`: Default value for the attribute
- `unique`: `"true"` if the attribute must be unique, `"false"` otherwise
- `required`: `"true"` if the attribute is required, `"false"` otherwise

Example:
```json
["STRING", "default_name", "false", "true"]
```
