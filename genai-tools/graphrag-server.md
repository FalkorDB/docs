---
title: "GraphRAG Server"
nav_order: 2
description: "Turn your documents into an accurate, explainable AI assistant, with no code and no knowledge-graph expertise required. Hosted GraphRAG by FalkorDB."
parent: "GenAI Tools"
---

# GraphRAG Server

## Turn your documents into an accurate, explainable AI assistant

GraphRAG Server is the fastest way to turn your own documents into a smart, searchable assistant. It's fully hosted with no code required: upload your files and it automatically builds a [knowledge graph](https://www.falkordb.com/blog/what-is-graphrag/) behind the scenes, so you can ask questions in plain language and get accurate, cited answers. You get the power of a knowledge graph in seconds.

**Resources:**
- 🚀 [Try GraphRAG Server](https://graphrag.falkordb.com/)
- 🔗 [FalkorDB](https://www.falkordb.com)
- 💻 [GraphRAG-SDK GitHub Repository](https://github.com/FalkorDB/GraphRAG-SDK)

---

## Why GraphRAG?

Vanilla RAG (Retrieval-Augmented Generation) finds text snippets that look similar to your question and hands them to an LLM. That works for simple lookups, but it struggles when the answer depends on how facts connect across different documents.

GraphRAG first organizes your documents into a **knowledge graph**: the people, places, products, and concepts in your content, and the relationships between them. Asking questions against that graph gives you:

- **More accurate answers**: it connects related facts *across* your documents instead of matching keywords in isolation.
- **Cited answers**: every response points back to the source documents it came from, so you can trust and verify it.
- **Explainability**: see the small graph of entities and relationships behind each answer, so you understand *why* you got it.
- **A view of your knowledge**: explore everything the system learned from your documents as an interactive graph.

---

## How it works

1. **Sign in** at [graphrag.falkordb.com](https://graphrag.falkordb.com/) with your Google account.
2. **Upload your documents**: PDF, plain text, or Markdown. GraphRAG Server reads them and builds your knowledge graph automatically, showing live progress as it goes.
3. **Ask questions** in plain language. You get an answer with citations to your sources, plus a small "explainability" graph showing the facts behind it.
4. **Explore visually**: browse the entities and relationships extracted from your documents in an interactive graph view.

That's it. Nothing to install, no Cypher to write, and no graph knowledge needed to get started. Settings are there if you want them, but the defaults work out of the box.

---

## Key features

- **Document upload**: bring your own PDF, TXT, or Markdown files.
- **Natural-language Q&A**: ask in plain English and get grounded answers.
- **Citations**: every answer links back to the source documents it used.
- **Explainability subgraphs**: see the entities and relationships behind each answer.
- **Interactive graph visualization**: explore your knowledge as a graph you can click through.
- **AI-suggested questions**: get starter questions tailored to your own content.
- **Private to your account**: your documents and graph belong to you and aren't shared with other users.

---

## Embed it on your site

Once you've built a knowledge graph, you can publish it as a **chat widget** and embed it on your own website or documentation so your visitors can ask questions about your content too, without leaving your site.

---

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Do I need to know anything about graphs or knowledge graphs?"
  a1="No. GraphRAG Server builds the knowledge graph for you automatically when you upload your documents. You only ever interact with it by uploading files and asking questions in plain language."
  q2="What kinds of files can I upload?"
  a2="PDF, plain text (TXT), and Markdown (.md) files."
  q3="Is my data private?"
  a3="Yes. Each account's documents and knowledge graph are isolated to that account and are not shared with other users."
  q4="I'm a developer and want to build GraphRAG in my own code. Where do I start?"
  a4="Use the [GraphRAG-SDK](https://docs.falkordb.com/genai-tools/graphrag-sdk.html), a Python library for building GraphRAG applications directly against FalkorDB."
%}
