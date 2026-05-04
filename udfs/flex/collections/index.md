---
layout: default
title: Collection Functions
description: "FLEX collection functions for set operations, frequency analysis, and list manipulation in Cypher queries."
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 20
---

# Collection Functions

FLEX collections utilities.

{% include faq_accordion.html title="Frequently Asked Questions" q1="What are FLEX collection functions?" a1="FLEX collection functions provide set operations and list transformations including union, intersection, shuffling, frequency counting, and zipping lists together." q2="How do I call a collection function?" a2="Use the namespace `flex.coll.<function>()`. For example: `flex.coll.union([1,2,3], [3,4,5])` returns `[1,2,3,4,5]`." q3="Do collection functions modify the original list?" a3="No. All FLEX collection functions return new lists and do not mutate the input values." %}
