[![Discord](https://img.shields.io/discord/1146782921294884966?style=flat-square)](https://discord.gg/6M4QwDXn2w)
[![Try Free](https://img.shields.io/badge/Try%20Free-FalkorDB%20Cloud-FF8101?labelColor=FDE900&style=flat-square)](https://app.falkordb.cloud)

[![Trendshift](https://trendshift.io/api/badge/repositories/14787)](https://trendshift.io/repositories/14787)

# FalkorDB Documentation

Welcome to the FalkorDB documentation repository. This repository contains the source files for [https://docs.falkordb.com](https://docs.falkordb.com), published with [Mintlify](https://mintlify.com).

FalkorDB documentation spans three repositories, presented to readers as three products in a single site:

| Product | Repository |
| --- | --- |
| FalkorDB (this repo) | [FalkorDB/docs](https://github.com/FalkorDB/docs) |
| FalkorDB Cloud | [FalkorDB/falkordb-cloud-docs](https://github.com/FalkorDB/falkordb-cloud-docs) |
| FalkorDB Enterprise | [FalkorDB/FalkorDB-Enterprise](https://github.com/FalkorDB/FalkorDB-Enterprise) |

The product switcher is configured under `navigation.products` in `docs.json`.

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

To preview the documentation locally you need an LTS release of [Node.js](https://nodejs.org).

## Local Development

### Install the Mintlify CLI

```bash
npm i -g mint
```

### Run the Local Preview

```bash
mint dev
```

The documentation will be available at `http://localhost:3000`.

### Validate

```bash
mint broken-links                              # every internal link resolves
npm install --no-save @mdx-js/mdx remark-gfm   # one-time
node scripts/check_mdx.mjs                     # every page parses as MDX
```

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
4. Test locally with `mint dev`
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
- Use proper MDX syntax
- Keep line length reasonable (under 120 characters when possible)
- Do not write an H1 in the page body; Mintlify renders the front matter `title` as the H1

### Code Examples

When adding code examples:
- Provide examples in multiple languages when applicable (Python, JavaScript, Java, Rust)
- Ensure code is tested and working
- Include comments for complex operations
- Use realistic, meaningful variable names

### Components

Use [Mintlify components](https://mintlify.com/docs/components) instead of raw HTML.

#### `<CodeGroup>` — multi-language code tabs

````mdx
<CodeGroup>

```python Python
from falkordb import FalkorDB
```

```javascript JavaScript
import { FalkorDB } from 'falkordb';
```

</CodeGroup>
````

#### `<AccordionGroup>` — FAQs and collapsible sections

```mdx
<AccordionGroup>
  <Accordion title="What is FalkorDB?">
    FalkorDB is a high-performance graph database.
  </Accordion>
  <Accordion title="How do I get started?">
    See the [Getting Started](/getting-started) guide.
  </Accordion>
</AccordionGroup>
```

Callouts use `<Note>`, `<Tip>`, `<Warning>` and `<Info>`.

See `AGENTS.md` for the full authoring rules, including MDX escaping gotchas.

## Project Structure

```text
docs/
├── algorithms/          # Graph algorithms documentation
├── commands/            # Command reference
├── cypher/              # Cypher query language docs
├── genai-tools/         # AI/ML integrations
├── getting-started/     # Installation and setup
├── integration/         # Third-party integrations
├── operations/          # Deployment and operations
├── udfs/                # User-defined functions
├── scripts/             # Documentation tooling
├── docs.json            # Mintlify configuration and navigation
└── index.mdx            # Homepage
```

## License

The documentation is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

FalkorDB itself is licensed under the [Server Side Public License v1 (SSPLv1)](https://github.com/FalkorDB/FalkorDB/blob/master/LICENSE.txt).

## Support

- **Documentation**: [https://docs.falkordb.com](https://docs.falkordb.com)
- **GitHub Discussions**: [https://github.com/FalkorDB/FalkorDB/discussions](https://github.com/FalkorDB/FalkorDB/discussions)
- **Discord**: [https://discord.gg/6M4QwDXn2w](https://discord.gg/6M4QwDXn2w)
- **Website**: [https://www.falkordb.com](https://www.falkordb.com)
