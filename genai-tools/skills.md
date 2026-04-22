---
title: "FalkorDB Skills"
parent: "GenAI Tools"
nav_order: 8
description: "Practical FalkorDB guidance packaged as an Agent Skill. Give your AI coding assistant deep knowledge of FalkorDB -- Cypher queries, user-defined functions, Docker operations, indexing, and more."
---

# FalkorDB Skills

[FalkorDB Skills](https://github.com/FalkorDB/skills) is an [Agent Skill](https://agentskills.io) that gives your AI coding assistant accurate, up-to-date knowledge of FalkorDB. It covers **27 runnable examples** across three categories:

- **Cypher** (16 skills) -- node/relationship CRUD, MERGE, parameterized queries, EXPLAIN/PROFILE, range/full-text/vector indexes, constraints, and known limitations
- **UDFs** (5 skills) -- load, call, list, and delete JavaScript user-defined function libraries
- **Docker Ops** (6 skills) -- run FalkorDB with browser UI, server-only mode, authentication, module config, and Docker Compose

## Usage

Clone the repository into your project and point your AI assistant at SKILL.md:

```bash
git clone https://github.com/FalkorDB/skills.git falkordb-skills
```

Or download `SKILL.md` directly and load it into any LLM context window.

For more details, see the [full README](https://github.com/FalkorDB/skills).
