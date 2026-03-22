---
title: "OpenTelemetry Integration"
nav_order: 5
parent: Operations
description: "Comprehensive guide for setting up OpenTelemetry observability and tracing with FalkorDB Python applications"
redirect_from:
  - /opentelemetry.html
  - /opentelemetry
---

# OpenTelemetry Tracing with FalkorDB-py Guide

This guide explains how to set up and use OpenTelemetry (OTel) to monitor and trace your FalkorDB Python applications.

## Overview

OpenTelemetry is an observability framework that allows you to collect, process, and export telemetry data from your applications. When integrated with FalkorDB-py, it provides valuable insights into database operations and query performance through distributed tracing.

**Note:** This guide focuses on tracing capabilities. OpenTelemetry supports additional observability features like metrics and logs that can be configured separately.

## Prerequisites

- Python 3.9+
- FalkorDB server running (locally or remotely)
- Basic understanding of Python and FalkorDB

## Installation

Install the required packages using pip or poetry:

### Using pip

```bash
pip install falkordb
pip install opentelemetry-distro
pip install opentelemetry-instrumentation-redis
pip install opentelemetry-exporter-otlp
pip install opentelemetry-sdk
```

### Using poetry

```bash
poetry add falkordb
poetry add opentelemetry-distro
poetry add opentelemetry-instrumentation-redis
poetry add opentelemetry-exporter-otlp
poetry add opentelemetry-sdk
```

## Basic Setup

### 1. Import Required Modules

```python
import falkordb
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
```

### 2. Configure OpenTelemetry SDK

```python
# Create a resource that identifies your service
resource = Resource.create({"service.name": "falkordb-app"})

# Create a tracer provider with the resource
provider = TracerProvider(resource=resource)

# Add a span processor with console exporter for development
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

# Set the global tracer provider
trace.set_tracer_provider(provider)

# Get a tracer for your application
tracer = trace.get_tracer(__name__)
```

### 3. Connect to FalkorDB

```python
# Configure your FalkorDB connection
redis_user = 'your_username'  # Replace with your username
redis_password = 'your_password'  # Replace with your password

try:
    db = falkordb.FalkorDB(
        host='localhost', 
        port=6379, 
        username=redis_user, 
        password=redis_password
    )
    g = db.select_graph('my-graph')
except Exception as e:
    print(f"Could not connect to FalkorDB: {e}")
    exit()
```

## Tracing FalkorDB Operations

### Manual Span Creation

You can manually create spans around FalkorDB operations to track their performance and behavior:

```python
# Create a span around a FalkorDB query
with tracer.start_as_current_span("falkordb.query") as span:
    # Add attributes to provide context
    span.set_attribute("db.system", "falkordb")
    span.set_attribute("db.user", redis_user)
    
    # Define your query
    query = "CREATE (n:Person {name: 'Alice'}) RETURN n"
    span.set_attribute("db.statement", query)
    
    # Execute the query
    result = g.query(query).result_set
    
    # Add result metadata
    span.set_attribute("db.result.count", len(result))
    
    print(f"Query executed successfully. Results: {len(result)} rows")
```

### Advanced Span Attributes

You can add more detailed attributes to your spans for better observability:

```python
with tracer.start_as_current_span("falkordb.complex_query") as span:
    span.set_attribute("db.system", "falkordb")
    span.set_attribute("db.connection_string", f"{db.host}:{db.port}")
    span.set_attribute("db.user", redis_user)
    span.set_attribute("db.name", "my-graph")
    
    query = """
    MATCH (p:Person)
    WHERE p.age > 25
    RETURN p.name, p.age
    ORDER BY p.age DESC
    LIMIT 10
    """
    
    span.set_attribute("db.statement", query)
    span.set_attribute("db.operation", "SELECT")
    
    try:
        result = g.query(query).result_set
        span.set_attribute("db.result.count", len(result))
        span.set_status(Status(StatusCode.OK))
    except Exception as e:
        span.set_attribute("db.error", str(e))
        span.set_status(Status(StatusCode.ERROR))
        raise
```

## Exporter Configuration

### Console Exporter (Development)

The console exporter is useful for development and debugging:

```python
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor

processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
```

### OTLP Exporter (Production)

For production environments, you can export to observability platforms:

```python
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",  # Your OTLP endpoint
    headers={"api-key": "your-api-key"}  # If required
)

processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)
```

### Jaeger Exporter

To export traces to Jaeger:

```python
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
```

## Complete Example

Here's a complete working example:

```python
import falkordb
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor

def setup_telemetry():
    """Setup OpenTelemetry configuration"""
    resource = Resource.create({"service.name": "falkordb-telemetry-demo"})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    return trace.get_tracer(__name__)

def main():
    # Setup telemetry
    tracer = setup_telemetry()
    
    # Connect to FalkorDB
    redis_user = 'alice'
    try:
        db = falkordb.FalkorDB(
            host='localhost', 
            port=6379, 
            username=redis_user, 
            password='password'
        )
        g = db.select_graph('telemetry-demo')
    except Exception as e:
        print(f"Could not connect to FalkorDB: {e}")
        return

    # Example operations with tracing
    with tracer.start_as_current_span("create_person") as span:
        span.set_attribute("db.system", "falkordb")
        span.set_attribute("db.user", redis_user)
        
        query = "CREATE (n:Person {name: 'Alice', age: 30}) RETURN n"
        span.set_attribute("db.statement", query)
        
        result = g.query(query).result_set
        span.set_attribute("db.result.count", len(result))
        print("Person created successfully")

    with tracer.start_as_current_span("find_persons") as span:
        span.set_attribute("db.system", "falkordb")
        span.set_attribute("db.user", redis_user)
        
        query = "MATCH (n:Person) RETURN n.name, n.age"
        span.set_attribute("db.statement", query)
        
        result = g.query(query).result_set
        span.set_attribute("db.result.count", len(result))
        print(f"Found {len(result)} persons")

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Service Naming

Use descriptive service names that identify your application:
```python
resource = Resource.create({
    "service.name": "my-falkordb-app",
    "service.version": "1.0.0",
    "environment": "production"
})
```

### 2. Meaningful Span Names

Use descriptive span names that indicate the operation:
```python
with tracer.start_as_current_span("user.create") as span:
    # Create user logic
    pass

with tracer.start_as_current_span("user.find_by_email") as span:
    # Find user logic
    pass
```

### 3. Error Handling

Always handle errors properly in your spans:
```python
with tracer.start_as_current_span("falkordb.query") as span:
    try:
        result = g.query(query).result_set
        span.set_status(Status(StatusCode.OK))
    except Exception as e:
        span.set_attribute("error.message", str(e))
        span.set_status(Status(StatusCode.ERROR))
        raise
```

### 4. Sensitive Data

Avoid logging sensitive information in span attributes:
```python
# Good - log query structure, not sensitive data
span.set_attribute("db.statement", "MATCH (u:User {email: ?}) RETURN u")

# Bad - don't log actual sensitive values
# span.set_attribute("user.email", "user@example.com")
```

## Troubleshooting

### Common Issues

1. **No traces appearing**: Ensure the tracer provider is set before creating spans
2. **Connection errors**: Verify FalkorDB server is running and accessible
3. **Missing dependencies**: Install all required OpenTelemetry packages

### Debug Mode

Enable debug logging to troubleshoot issues:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Additional Resources

- [OpenTelemetry Python Documentation](https://opentelemetry.io/docs/languages/python/)
- [FalkorDB Python Client Documentation](https://github.com/FalkorDB/falkordb-py)
- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)

## Conclusion

By integrating OpenTelemetry with FalkorDB-py, you gain powerful observability capabilities that help you monitor, debug, and optimize your graph database applications. Start with the basic setup and gradually add more sophisticated tracing as your application grows in complexity.
