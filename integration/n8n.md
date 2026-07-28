---
title: "n8n GraphRAG Nodes"
description: "Use FalkorDB GraphRAG from n8n workflows with a pipeline node, an AI Agent tool, and a shared credential."
parent: "Integration"
nav_order: 9
---

# n8n GraphRAG Nodes

The [FalkorDB GraphRAG n8n community node](https://github.com/FalkorDB/GraphRAG-n8n) connects n8n workflows to a [FalkorDB GraphRAG-Server](https://github.com/FalkorDB/GraphRAG-Server). It does not talk to FalkorDB directly. Instead, it uses the GraphRAG-Server REST API to ingest content into a knowledge graph and answer questions against that graph.

The package ships two nodes and one shared credential:

- `FalkorDB GraphRAG`: a regular pipeline node for ingest and question-answering steps.
- `FalkorDB GraphRAG Tool`: an AI Agent tool node that can be called autonomously.
- `FalkorDB GraphRAG Server API`: the credential that stores the server URL, API token, and request timeout.

## Typical workflow

```mermaid
flowchart LR
  A[n8n workflow] --> B[FalkorDB GraphRAG node]
  B --> C[GraphRAG-Server]
  C --> D[FalkorDB]
```

## Installation

Install `@falkordb/n8n-nodes-graphrag` from the n8n Community Nodes UI, or use npm in a self-hosted n8n instance:

```bash
npm install @falkordb/n8n-nodes-graphrag
```

After installation, the two nodes appear under the FalkorDB category in the node picker.

## Setup

Create one credential under **Credentials -> New -> FalkorDB GraphRAG Server API** and reuse it across both nodes.

| Field | Required | Description |
| --- | --- | --- |
| **Server URL** | yes | Base URL of your GraphRAG-Server instance, for example `http://localhost:8000`. |
| **API Token** | no | Sent as `Authorization: Bearer ...` when the server requires authentication. |
| **Request Timeout (Seconds)** | yes | Per-request timeout for GraphRAG-Server calls. |

## How to get an API token

Use these steps in GraphRAG-Server before configuring the n8n credential.

### 1. Open Settings and API Access

Open your graph in GraphRAG-Server, then go to **Settings** and keep the **API Access** tab selected.

![GraphRAG-Server Settings page with API Access selected](../images/n8n/n8n-graphrag-settings-overview.png)

### 2. Add your LLM key

In **Your LLM Keys**, add a provider key if one is not already present. API tokens run on your own LLM key, so this step is required first.

![LLM key section in GraphRAG-Server Settings](../images/n8n/n8n-graphrag-llm-key.png)

### 3. Generate the client API token

In **API Tokens**, enter a token name (for example, `n8n production`), choose expiration, and click **Generate**. Copy the raw token value when shown and paste it into the n8n credential **API Token** field.

![API Tokens panel showing token generation controls](../images/n8n/n8n-graphrag-api-token.png)

## Screenshots

### Node picker

![Node picker showing FalkorDB GraphRAG and FalkorDB GraphRAG Tool](../images/n8n/n8n-node-picker.png)

### Pipeline node

![Pipeline node configuration for the main action flow](../images/n8n/n8n-action-config.png)

### AI Agent tool

![AI Agent tool configuration](../images/n8n/n8n-tool-config.png)

### Credential

![FalkorDB GraphRAG Server API credential screen](../images/n8n/n8n-credential-settings.png)

### Retrieve only workflow

![Retrieve-only workflow canvas with Manual Trigger, Set Question, and FalkorDB GraphRAG](../images/n8n/n8n-retrieve-only-workflow.png)

## When to use it

Use the pipeline node when you want to ingest documents, list documents, or answer questions as part of a workflow. Use the AI Agent tool when you want the agent to decide when to query the knowledge graph and fill the node parameters automatically.