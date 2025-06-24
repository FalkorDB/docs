---
title: "Rest API"
nav_order: 1
description: "Rest API detailed doc"
parent: "Integration"
---

## Table of Contents

### Authentication
- [Login - GET /api/auth/providers](#login---get-apiauthproviders)
- [Logout - POST /api/auth/signout](#logout---post-apiauthsignout)

### Settings
- [Set Configuration Value - POST /api/config](#set-configuration-value---post-apiconfig)
- [Get Configuration Value - GET /api/config](#get-configuration-value---get-apiconfig)
- [Create New User - POST /api/user](#create-new-user---post-apiuser)
- [Delete User - DELETE /api/user](#delete-user---delete-apiuser)
- [Get All Users - GET /api/user](#get-all-users---get-apiuser)
- [Modify a User - PATCH /api/user/{userName}](#modify-a-user---patch-apiuserusername)

### Graph
- [Create a Graph & Run A Query - GET /api/graph/{graphName}](#create-a-graph--run-a-query---get-apigraphgraphname)
- [Delete a Graph - DELETE /api/graph/{graphName}](#delete-a-graph---delete-apigraphgraphname)
- [Get All Graphs - GET /api/graph](#get-all-graphs---get-apigraph)
- [Duplicate a Graph - POST /api/graph/{destinationGraphName}](#duplicate-a-graph---post-apigraphdestinationgraphname)
- [Get Graph Count - GET /api/graph/{graphName}/count](#get-graph-count---get-apigraphgraphnamecount)
- [Add Node Attribute - POST /api/graph/{graphName}/{nodeId}/{attributeName}](#add-node-attribute---post-apigraphgraphnamenodeidattributename)
- [Delete Node Attribute - DELETE /api/graph/{graphName}/{nodeId}/{attributeName}](#delete-node-attribute---delete-apigraphgraphnamenodeidattributename)
- [Add Node Label - POST /api/graph/{graphName}/{nodeId}/label](#add-node-label---post-apigraphgraphnamenodeidlabel)
- [Delete Node Label - DELETE /api/graph/{graphName}/{nodeId}/label](#delete-node-label---delete-apigraphgraphnamenodeidlabel)
- [Delete Node - DELETE /api/graph/{graphName}/{nodeId}](#delete-node---delete-apigraphgraphnamenodeid)

### Schema
- [Create New Schema & Run A Query - GET /api/graph/{schemaName}](#create-new-schema--run-a-query---get-apigraphschemaname)
- [Delete a Schema - DELETE /api/graph/{schemaName}](#delete-a-schema---delete-apigraphschemaname)

---

## Authentication

### **Login** - `GET /api/auth/providers`

This endpoint retrieves information about authentication providers and their respective URLs for sign-in and callback.

#### Responses

- **200**: Successful authentication provider retrieval
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "credentials": {
        "id": "credentials",
        "name": "Credentials",
        "type": "credentials",
        "signinUrl": "http://localhost:3000/api/auth/signin/credentials",
        "callbackUrl": "http://localhost:3000/api/auth/callback/credentials"
      }
    }
    ```

### **Logout** - `POST /api/auth/signout`

This endpoint signs out a user, ending their authenticated session.

#### Request Body

- Content-Type: `application/x-www-form-urlencoded`
- Example request:

    ```json
    {
      "csrfToken": "insert csrfToken",
      "callbackUrl": "/login",
      "json": true
    }
    ```

#### Responses

- **200**: Successful logout
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "url": "http://localhost:3000/api/auth/signout?csrf=true"
    }
    ```

---

## Settings

### **Set Configuration Value** - `POST /api/config`

This endpoint sets a configuration value for `MAX_QUEUED_QUERIES`.

#### Parameters

- `cookie` (header, required): Cookie header with session and auth tokens.
- `config` (query, required): The configuration name.
- `value` (query, required): The integer value to set.

#### Responses

- **200**: Successful configuration update
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "config": "OK"
    }
    ```

### **Get Configuration Value** - `GET /api/config`

This endpoint retrieves the value for `MAX_QUEUED_QUERIES`.

#### Parameters

- `cookie` (header, required): Cookie header with session and auth tokens.
- `config` (query, required): The name of the configuration to retrieve.

#### Responses

- **200**: Successful configuration retrieval
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "config": [
        "MAX_QUEUED_QUERIES",
        25
      ]
    }
    ```

### **Create New User** - `POST /api/user`

This endpoint creates a new user with specified credentials.

#### Request Body

- Content-Type: `application/json`
- Example request:

    ```json
    {
      "username": "user",
      "password": "Pass123@",
      "role": "Read-Write"
    }
    ```

#### Responses

- **201**: User created successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "User created"
    }
    ```

### **Delete User** - `DELETE /api/user`

This endpoint deletes a user based on their username and role.

#### Request Body

- Content-Type: `application/json`
- Example request:

    ```json
    {
      "users": [
        {
          "username": "userName",
          "role": "Read-Write"
        }
      ]
    }
    ```

#### Responses

- **200**: User deleted successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "User deleted"
    }
    ```

### **Get All Users** - `GET /api/user`

This endpoint retrieves a list of all users.

#### Responses

- **200**: List of users retrieved successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": [
        {
          "username": "default",
          "role": "Admin",
          "checked": false
        }
      ]
    }
    ```

### **Modify A User** - `PATCH /api/user/{userName}`

This endpoint updates the role of a specific user.

#### Parameters

- `cookie` (header, required): Cookie header with session and auth tokens.
- `userName` (path, required): The username of the user to modify.
- `role` (query, required): The new role to assign to the user (`Admin`, `Read-Only`, `Read-Write`).

#### Responses

- **200**: User updated successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "User role updated"
    }
    ```

---

## Graph

### **Create A Graph & Run A Query** - `GET /api/graph/{graphName}`

This endpoint creates a graph and runs a query.

#### Parameters

- `cookie` (header, required): Cookie header with session and auth tokens.
- `graphName` (path, required): The name of the graph to be created.
- `query` (query, required): The query to run, such as `RETURN 1`.

#### Responses

- **200**: Graph created and query executed
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": {
        "metadata": [
          "Nodes created: 40",
          "Relationships created: 20",
          "Cached execution: 1",
          "Query internal execution time: 0.201420 milliseconds"
        ],
        "data": [
          {
            "queryData": "exampleData"
          }
        ]
      }
    }
    ```

### **Delete A Graph** - `DELETE /api/graph/{graphName}`

This endpoint deletes a specified graph.

#### Parameters

- `cookie` (header, required): Cookie header with session and auth tokens.
- `graphName` (path, required): The name of the graph to be deleted.

#### Responses

- **200**: Graph deleted successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "GraphName graph deleted"
    }
    ```

### **Get All Graphs** - `GET /api/graph`

This endpoint retrieves a list of all graphs.

#### Responses

- **200**: List of graphs retrieved successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": [
        "graphName"
      ]
    }
    ```

### **Duplicate A Graph** - `POST /api/graph/{destinationGraphName}`

This endpoint duplicates a graph from source to destination.

#### Parameters

- `destinationGraphName` (path, required): The name of the destination graph.
- `sourceName` (query, required): The name of the source graph to duplicate.

#### Responses

- **200**: Graph duplicated successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "success": "OK"
    }
    ```

### **Get Graph Count** - `GET /api/graph/{graphName}/count`

This endpoint retrieves the count of nodes and edges in a specified graph.

#### Parameters

- `cookie` (header, required): Cookie header with session and auth tokens.
- `graphName` (path, required): The name of the graph to count nodes and edges.

#### Responses

- **200**: Graph count retrieved successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": {
        "data": [
          {
            "nodes": 7417,
            "edges": 4341
          }
        ]
      }
    }
    ```

### **Add Node Attribute** - `POST /api/graph/{graphName}/{nodeId}/{attributeName}`

This endpoint adds an attribute to a node in a graph.

#### Parameters

- `cookie` (header, required): Cookie header with session and auth tokens.
- `graphName` (path, required): The name of the graph.
- `nodeId` (path, required): The ID of the node to which the attribute will be added.
- `attributeName` (path, required): The name of the attribute to add.

#### Request Body

- Content-Type: `application/json`
- Example request:

    ```json
    {
      "value": "your_attribute_value",
      "type": true
    }
    ```

#### Responses

- **200**: Node attribute added successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": {
        "metadata": [
          "Cached execution: 0",
          "Query internal execution time: 0.412958 milliseconds"
        ]
      }
    }
    ```

### **Delete Node Attribute** - `DELETE /api/graph/{graphName}/{nodeId}/{attributeName}`

This endpoint deletes an attribute from a node in a graph.

#### Parameters

- `cookie` (header, required): Cookie header with session and auth tokens.
- `graphName` (path, required): The name of the graph.
- `nodeId` (path, required): The ID of the node from which the attribute will be deleted.
- `attributeName` (path, required): The name of the attribute to delete.

#### Request Body

- Content-Type: `application/json`
- Example request:

    ```json
    {
      "type": true
    }
    ```

#### Responses

- **200**: Node attribute deleted successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": {
        "metadata": [
          "Cached execution: 0",
          "Query internal execution time: 0.407125 milliseconds"
        ]
      }
    }
    ```

### **Add Node Label** - `POST /api/graph/{graphName}/{nodeId}/label`

This endpoint adds a label to a node in a graph.

#### Parameters

- `cookie` (header, required): Cookie header with session and auth tokens.
- `graphName` (path, required): The name of the graph.
- `nodeId` (path, required): The ID of the node to which the label will be added.

#### Request Body

- Content-Type: `application/json`
- Example request:

    ```json
    {
      "label": "your_label_name"
    }
    ```

#### Responses

- **200**: Node label added successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "Label added successfully"
    }
    ```

### **Delete Node Label** - `DELETE /api/graph/{graphName}/{nodeId}/label`

This endpoint deletes a label from a node in a graph.

#### Parameters

- `cookie` (header, required): Cookie header with session and auth tokens.
- `graphName` (path, required): The name of the graph.
- `nodeId` (path, required): The ID of the node from which the label will be deleted.

#### Request Body

- Content-Type: `application/json`
- Example request:

    ```json
    {
      "label": "your_label_name"
    }
    ```

#### Responses

- **200**: Node label deleted successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "Label removed successfully"
    }
    ```

### **Delete Node** - `DELETE /api/graph/{graphName}/{nodeId}`

This endpoint deletes a node from a graph.

#### Parameters

- `cookie` (header, required): Cookie header with session and auth tokens.
- `graphName` (path, required): The name of the graph.
- `nodeId` (path, required): The ID of the node to delete.

#### Request Body

- Content-Type: `application/json`
- Example request:

    ```json
    {
      "type": true
    }
    ```

#### Responses

- **200**: Node deleted successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "Node deleted successfully"
    }
    ```

---

## Schema

### **Create New Schema & Run A Query** - `GET /api/graph/{schemaName}`

This endpoint creates a new schema and runs a query.

#### Parameters

- `schemaName` (path, required): The name of the schema to create.
- `query` (query, required): The query to execute.

#### Responses

- **200**: Schema created and query executed
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "result": {
        "metadata": [
          "Cached execution: 0",
          "Query internal execution time: 0.153307 milliseconds"
        ],
        "data": [
          {
            "1": 1
          }
        ]
      }
    }
    ```

### **Delete A Schema** - `DELETE /api/graph/{schemaName}`

This endpoint deletes a specified schema.

#### Parameters

- `schemaName` (path, required): The name of the schema to delete.

#### Responses

- **200**: Schema deleted successfully
  - Content-Type: `application/json`
  - Example response:

    ```json
    {
      "message": "SchemaName schema deleted"
    }
    ```
