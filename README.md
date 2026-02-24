[![Workflow](https://github.com/FalkorDB/docs/actions/workflows/pages/pages-build-deployment/badge.svg?branch=main)](https://github.com/FalkorDB/docs/actions/workflows/pages/pages-build-deployment)
[![Discord](https://img.shields.io/discord/1146782921294884966?style=flat-square)](https://discord.gg/ErBEqN9E)
[![Try Free](https://img.shields.io/badge/Try%20Free-FalkorDB%20Cloud-FF8101?labelColor=FDE900&style=flat-square)](https://app.falkordb.cloud)

[![Trendshift](https://trendshift.io/api/badge/repositories/14787)](https://trendshift.io/repositories/14787)

# FalkorDB Documentation

Welcome to the FalkorDB documentation repository. This repository contains the source files for [https://docs.falkordb.com](https://docs.falkordb.com).

## About FalkorDB

FalkorDB is a low-latency, scalable graph database with OpenCypher support. It powers GraphRAG applications and serves as a high-performance property graph database for complex, interconnected data.

## Documentation Structure

- **Getting Started**: Installation, configuration, and client libraries
- **Cypher**: Query language reference and examples
- **Commands**: FalkorDB-specific commands
- **Algorithms**: Graph algorithms (BFS, PageRank, etc.)
- **GenAI Tools**: Integration with LlamaIndex, LangChain, and GraphRAG frameworks
- **Operations**: Deployment, clustering, and infrastructure
- **Integration**: Third-party tool integrations

## Prerequisites

To build and run the documentation locally, you need:

- Ruby (2.7 or later)
- Bundler gem

## Local Development

### Install Dependencies

```bash
bundle install
```

### Build the Documentation

```bash
bundle exec jekyll build
```

### Run Local Server

```bash
bundle exec jekyll serve
```

The documentation will be available at `http://localhost:4000`.

## Contributing

We welcome contributions to improve the documentation! Here's how you can help:

### Reporting Issues

If you find errors, typos, or unclear explanations:

1. Check if an issue already exists in the [issue tracker](https://github.com/FalkorDB/docs/issues)
2. If not, create a new issue with:
   - Clear description of the problem
   - Location in the documentation (file path and line number)
   - Suggested improvement (if applicable)

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b improve-documentation`)
3. Make your changes
4. Test locally with `bundle exec jekyll serve`
5. Commit your changes with clear, descriptive messages
6. Push to your fork
7. Open a Pull Request with:
   - Description of changes
   - Reason for the changes
   - Screenshots (if visual changes)

### Style Guidelines

- Use clear, concise language
- Include code examples where appropriate
- Follow existing formatting and structure
- Test all code examples
- Use proper Markdown syntax
- Keep line length reasonable (under 120 characters when possible)

### Code Examples

When adding code examples:
- Provide examples in multiple languages when applicable (Python, JavaScript, Java, Rust)
- Ensure code is tested and working
- Include comments for complex operations
- Use realistic, meaningful variable names

## Project Structure

```
docs/
├── algorithms/          # Graph algorithms documentation
├── commands/            # Command reference
├── cypher/             # Cypher query language docs
├── genai-tools/        # AI/ML integrations
├── getting-started/    # Installation and setup
├── integration/        # Third-party integrations
├── operations/         # Deployment and operations
├── udfs/              # User-defined functions
├── _config.yml        # Jekyll configuration
└── index.md           # Homepage
```

## License

The documentation is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

FalkorDB itself is licensed under the [Server Side Public License v1 (SSPLv1)](https://github.com/FalkorDB/FalkorDB/blob/master/LICENSE.txt).

## Support

- **Documentation**: [https://docs.falkordb.com](https://docs.falkordb.com)
- **GitHub Discussions**: [https://github.com/FalkorDB/FalkorDB/discussions](https://github.com/FalkorDB/FalkorDB/discussions)
- **Discord**: [https://discord.gg/ErBEqN9E](https://discord.gg/ErBEqN9E)
- **Website**: [https://www.falkordb.com](https://www.falkordb.com)
