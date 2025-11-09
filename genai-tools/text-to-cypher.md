---
title: "Text-to-Cypher"
nav_order: 7
description: "Convert natural language to Cypher queries using AI-powered text-to-cypher service."
parent: "GenAI Tools"
---

# Text-to-Cypher

A high-performance Rust-based API service that translates natural language text to Cypher queries for graph databases, featuring integration with genai and FalkorDB. Complete all-in-one Docker solution with integrated FalkorDB database, web browser interface, text-to-cypher API, and Model Context Protocol (MCP) server support!

## Features

- **Text to Cypher Translation**: Convert natural language queries to Cypher database queries using AI
- **Graph Schema Discovery**: Automatically discover and analyze graph database schemas
- **RESTful API**: Clean HTTP API with comprehensive OpenAPI/Swagger documentation
- **MCP Server**: Model Context Protocol server for AI assistant integrations
- **Streaming Responses**: Real-time Server-Sent Events (SSE) streaming of query processing results
- **Integrated FalkorDB**: Built-in FalkorDB graph database with web browser interface
- **All-in-One Docker Solution**: Complete stack in a single container - database, web UI, API, and MCP server
- **AI Model Integration**: Powered by genai for natural language processing with support for multiple providers
- **Environment Configuration**: Flexible configuration via `.env` file with fallback to request parameters
- **Production Ready**: Comprehensive error handling, logging, and robust architecture
- **Multi-Platform Support**: Docker images available for both AMD64 and ARM64 architectures

## Quick Start

### Using Docker (Recommended)

The easiest way to get started is using our all-in-one Docker image that includes FalkorDB database, web browser interface, text-to-cypher API, and MCP server:

```bash
# Run the complete stack with all services
docker run -p 6379:6379 -p 3000:3000 -p 8080:8080 -p 3001:3001 \
  -e DEFAULT_MODEL=gpt-4o-mini -e DEFAULT_KEY=your-api-key \
  falkordb/text-to-cypher:latest

# Or using environment file
docker run -p 6379:6379 -p 3000:3000 -p 8080:8080 -p 3001:3001 \
  --env-file .env \
  falkordb/text-to-cypher:latest

# Or mounting .env file for full MCP server functionality
docker run -p 6379:6379 -p 3000:3000 -p 8080:8080 -p 3001:3001 \
  -v $(pwd)/.env:/app/.env:ro \
  falkordb/text-to-cypher:latest
```

### Available Services

Once running, access the services at:

- **FalkorDB Database**: `localhost:6379` (Redis protocol)
- **FalkorDB Web Interface**: `http://localhost:3000` (Interactive graph database browser)
- **Text-to-Cypher API**: `http://localhost:8080` (REST API)
- **Swagger UI**: `http://localhost:8080/swagger-ui/` (API documentation)
- **MCP Server**: `localhost:3001` (Model Context Protocol server)
- **OpenAPI Spec**: `http://localhost:8080/api-doc/openapi.json`

### Local Development

If you prefer to run locally without Docker:

```bash
# Prerequisites: You'll need FalkorDB running separately
docker run -d -p 6379:6379 falkordb/falkordb:latest

# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Clone and run the text-to-cypher service
git clone https://github.com/FalkorDB/text-to-cypher.git
cd text-to-cypher
cp .env.example .env  # Edit with your configuration
cargo run
```

The local development setup requires:

- **FalkorDB instance**: Running on port 6379 (can be Docker or native)
- **Rust environment**: For building and running the text-to-cypher service

## Configuration

The application supports flexible configuration via environment variables or `.env` file:

- `DEFAULT_MODEL`: Default AI model to use (e.g., "openai:gpt-4")
- `DEFAULT_KEY`: Default API key for the AI service

Create a `.env` file from the provided example:

```bash
cp .env.example .env
# Edit .env with your preferred default model and API key
```

### MCP Server Configuration

**Important**: The MCP server will only start if:

1. Both `DEFAULT_MODEL` and `DEFAULT_KEY` are configured
2. The `.env` file physically exists (not just environment variables)

For Docker deployments:

- Use `--env-file .env` or `-e` flags for HTTP server only (MCP server also starts if both MODEL and KEY are provided)
- Use `-v $(pwd)/.env:/app/.env:ro` to ensure MCP server starts with mounted `.env` file

## Architecture

The integrated Docker solution runs four concurrent services:

### FalkorDB Database (Port 6379)

- Graph database server with Redis protocol compatibility
- Stores and manages graph data structures
- Accessible via Redis clients and graph query languages

### FalkorDB Web Interface (Port 3000)

- Interactive web-based graph database browser
- Visual query builder and result visualization
- Database administration and monitoring tools
- Graph data exploration interface

### Text-to-Cypher HTTP API (Port 8080)

- Main REST API for text-to-cypher conversion
- Swagger UI documentation at `http://localhost:8080/swagger-ui/`
- OpenAPI specification at `http://localhost:8080/api-doc/openapi.json`
- Supports both synchronous and streaming responses

### MCP Server (Port 3001)

- Model Context Protocol server for AI assistant integration
- Enables seamless integration with AI tools and applications
- Requires proper `.env` configuration to start

## API Usage Examples

### Basic Text-to-Cypher Request

```bash
curl -X POST "http://localhost:8080/text_to_cypher" \
  -H "Content-Type: application/json" \
  -d '{
    "graph_name": "movies",
    "chat_request": {
      "messages": [
        {
          "role": "User",
          "content": "Find all actors who appeared in movies released after 2020"
        }
      ]
    },
    "model": "gpt-4o-mini",
    "key": "your-api-key"
  }'
```

### Using the FalkorDB Web Interface

1. **Access the web interface**: Open `http://localhost:3000` in your browser
2. **Connect to database**: The interface automatically connects to the local FalkorDB instance
3. **Create sample data**: Use the visual interface to create nodes and relationships
4. **Run queries**: Test Cypher queries directly in the web interface
5. **Export/Import**: Save your graph data or load sample datasets

### Using Server-Sent Events (SSE)

The API supports streaming responses for real-time progress updates:

```javascript
const eventSource = new EventSource('/text_to_cypher', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    graph_name: "social_network",
    chat_request: {
      messages: [{ role: "User", content: "Who are John's friends?" }]
    }
  })
});

eventSource.onmessage = (event) => {
  const progress = JSON.parse(event.data);
  console.log('Progress:', progress);
};
```

### Complete Workflow Example

```bash
# 1. Start the complete stack
docker run -p 6379:6379 -p 3000:3000 -p 8080:8080 -p 3001:3001 \
  -e DEFAULT_MODEL=gpt-4o-mini -e DEFAULT_KEY=your-api-key \
  falkordb/text-to-cypher:latest

# 2. Create a graph using FalkorDB web interface (http://localhost:3000)
# Add some sample data: people, relationships, etc.

# 3. Query using natural language via the API
curl -X POST "http://localhost:8080/text_to_cypher" \
  -H "Content-Type: application/json" \
  -d '{
    "graph_name": "social_network",
    "chat_request": {
      "messages": [
        {
          "role": "User", 
          "content": "Find all people who have more than 3 friends"
        }
      ]
    },
    "model": "gpt-4o-mini",
    "key": "your-api-key"
  }'

# 4. Use MCP server for AI assistant integrations (port 3001)
# Connect your AI assistant to http://localhost:3001
```

## Troubleshooting

### Common Issues

**Services not starting**:

- Ensure all required ports (6379, 3000, 8080, 3001) are available
- Check that `DEFAULT_MODEL` and `DEFAULT_KEY` are properly configured
- View logs: `docker logs -f <container-name>`

**MCP Server not starting**:

- Verify both `DEFAULT_MODEL` and `DEFAULT_KEY` environment variables are set
- For local builds, ensure `.env` file exists in the working directory

**FalkorDB connection issues**:

- The integrated FalkorDB automatically starts with the container
- No external FalkorDB instance needed when using the Docker image
- Database is accessible at `localhost:6379` (Redis protocol)

**Web interface not accessible**:

- Ensure port 3000 is properly mapped: `-p 3000:3000`
- Try accessing `http://localhost:3000` directly
- Check firewall settings if running on a remote server

### Getting Help

- **API Documentation**: `http://localhost:8080/swagger-ui/`
- **Web Interface**: `http://localhost:3000` for graph exploration
- **Logs**: Use `docker logs -f <container-name>` to view all service logs
- **Issues**: Report problems at [GitHub Issues](https://github.com/FalkorDB/text-to-cypher/issues)

## Resources

- 🔗 [GitHub Repository](https://github.com/FalkorDB/text-to-cypher)
- 📚 [API Documentation (Swagger)](http://localhost:8080/swagger-ui/)
- 🐳 [Docker Hub](https://hub.docker.com/r/falkordb/text-to-cypher)

## License

This project is licensed under the MIT License.
