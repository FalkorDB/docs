---
title: "References"
description: "Explore FalkorDB resources including blog posts, videos, research papers, tutorials, and technical articles about graph databases, GraphBLAS, and performance benchmarks."
has_children: true
nav_order: 999
redirect_from:
  - /References.html
---

# References

## FalkorDB Resources

* [FalkorDB Blog](https://www.falkordb.com/blog)
* [FalkorDB GitHub](https://github.com/FalkorDB/FalkorDB)
* [FalkorDB Demos](https://github.com/FalkorDB/demos)
* [FalkorDB Discord Community](https://discord.gg/ErBEqN9E)

## Videos

* [Introduction to FalkorDB](https://www.youtube.com/watch?v=z0XO4pb2t5Y)
* [FalkorDB GraphRAG Overview](https://www.youtube.com/watch?v=xjpLPoQgo2s)

## Research & Technical Background

* Article - [RedisGraph GraphBLAS Enabled Graph Database](https://arxiv.org/abs/1905.01294).
Cailliau, Pieter & Davis, Tim & Gadepally, Vijay & Kepner, Jeremy & Lipman, Roi & Lovitz, Jeffrey & Ouaknine, Keren (IEEE IPDPS 2019 GrAPL workshop).
([pdf](http://www.mit.edu/~kepner/NEDB2019/NEDB2019-RedisGraph-NEDB.pdf))

## Legacy RedisGraph Resources

> **Note:** FalkorDB originated from the RedisGraph project. The following resources reference RedisGraph but remain relevant to understanding FalkorDB's architecture and design.

* Video
  - [Building a Multi-dimensional Analytics Engine with RedisGraph](https://www.youtube.com/watch?v=6FYYn-9fPXE)
  - [A Practical Introduction to RedisGraph](https://www.youtube.com/watch?v=aGHALjV6JGc)
  - [Redis Graph with Roi Lipman](https://www.youtube.com/watch?v=HpEa2cftbnc)
  - [RedisGraph 2.2: The Fastest Way to Query Your Highly Connected Data in Redis](https://www.youtube.com/watch?v=JNpHba2kRGM)

* Slides
  - [RedisGraph A Low Latency Graph DB](https://www.slideshare.net/RedisLabs/redisgraph-a-low-latency-graph-db-pieter-cailliau)

* Blog
  - [RedisGraph 2.0 Boosts Performance Up to 6x](https://redis.com/blog/redisgraph-2-0-boosts-performance-up-to-6x/)
  - [Getting Started with Knowledge Graphs in RedisGraph](https://redis.com/blog/getting-started-with-knowledge-graphs-in-redisgraph/)
  - [Introducing RedisGraph 2.0](https://redis.com/blog/introducing-redisgraph-2-0/)

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Where can I find the FalkorDB source code?"
  a1="The FalkorDB source code is available on GitHub at [https://github.com/FalkorDB/FalkorDB](https://github.com/FalkorDB/FalkorDB). You can also find demo projects at [https://github.com/FalkorDB/demos](https://github.com/FalkorDB/demos)."
  q2="Is there a community forum or chat for FalkorDB?"
  a2="Yes! FalkorDB has an active **Discord community** where you can ask questions, share projects, and connect with other users and the development team. Join at [https://discord.gg/ErBEqN9E](https://discord.gg/ErBEqN9E)."
  q3="What is the relationship between FalkorDB and RedisGraph?"
  a3="FalkorDB **originated from the RedisGraph project**. Many older resources reference RedisGraph but remain relevant to understanding FalkorDB's architecture, query language, and design principles."
  q4="Are there academic papers about FalkorDB's architecture?"
  a4="Yes. The paper *RedisGraph GraphBLAS Enabled Graph Database* (IEEE IPDPS 2019 GrAPL workshop) by Cailliau, Davis, Gadepally, Kepner, Lipman, Lovitz, and Ouaknine describes the GraphBLAS-based architecture that FalkorDB builds upon."
%}
