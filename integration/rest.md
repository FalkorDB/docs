---
title: "Rest API"
nav_order: 1
description: "Rest API detailed doc"
parent: "Integration"
---

# Rest API

## Table of Contents

- [Login - GET /api/auth/providers](#login---get-apiauthproviders)
- [Logout - POST /api/auth/signout](#logout---post-apiauthsignout)
- [Set Configuration Value - POST /api/config](#set-configuration-value---post-apiconfig)
- [Get Configuration Value - GET /api/config](#get-configuration-value---get-apiconfig)
- [Create New User - POST /api/user](#create-new-user---post-apiuser)
- [Delete User - POST /api/user](#delete-user---post-apiuser)
- [Get All Users - GET /api/user](#get-all-users---get-apiuser)
- [Modify a User - PATCH /api/user/{userName}](#modify-a-user---patch-apiuserusername)
- [Create a Graph & Run A Query - GET /api/graph/{graphName}](#create-a-graph--run-a-query---get-apigraphgraphname)
- [Delete a Graph - DELETE /api/graph/{graphName}](#delete-a-graph---delete-apigraphgraphname)
- [Get All Graphs - GET /api/graph](#get-all-graphs---get-apigraph)
- [Duplicate a Graph - POST /api/graph/{destinationGraphName}](#duplicate-a-graph---post-apigraphdestinationgraphname)
- [Create New Schema & Run A Query - GET /api/graph/{schemaName}](#create-new-schema--run-a-query---get-apigraphschemaname)
- [Delete a Schema - DELETE /api/graph/{schemaName}](#delete-a-schema---delete-apigraphschemaname)

---

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

### **Delete User** - `POST /api/user`

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
