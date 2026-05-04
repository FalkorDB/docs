---
layout: default
title: Text Functions
description: "FLEX text functions for case conversion, string formatting, padding, searching, and similarity metrics in Cypher queries."
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 70
---

# Text Functions

FLEX text utilities.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What are FLEX text functions?"
  a1="FLEX text functions provide string manipulation utilities including case conversion, formatting, padding, searching, regex matching, and string similarity metrics."
  q2="How do I call a text function?"
  a2="Use the namespace `flex.text.<function>()`. For example: `flex.text.camelCase('hello world')` returns `'helloWorld'`."
  q3="Do text functions handle null input?"
  a3="Yes. All FLEX text functions return `null` when given `null` input, making them safe to use with optional properties."
%}
