---
layout: default
title: Similarity Functions
description: "FLEX similarity functions for measuring resemblance between sets and strings."
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 60
---

# Similarity Functions

FLEX similarity utilities.

{% include faq_accordion.html title="Frequently Asked Questions" q1="What are FLEX similarity functions?" a1="FLEX similarity functions compute metrics that measure how alike two values are. Currently this includes the Jaccard coefficient for set similarity." q2="When should I use similarity functions vs text distance functions?" a2="Use `flex.sim.jaccard` for comparing **sets** (like tags or interests). Use `flex.text.levenshtein` or `flex.text.jaroWinkler` for comparing **strings** character by character." q3="How do I call a similarity function?" a3="Use the namespace `flex.sim.<function>()`. For example: `flex.sim.jaccard(['a','b'], ['b','c'])` returns `0.333`." %}
