---
layout: default
title: Map Functions
description: "FLEX map functions for creating, merging, filtering, and transforming map values in Cypher queries."
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 50
---

# Map Functions

FLEX map utilities.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What are FLEX map functions?"
  a1="FLEX map functions provide utilities for creating, merging, filtering, and transforming map (object) values in Cypher queries."
  q2="How do I call a map function?"
  a2="Use the namespace `flex.map.<function>()`. For example: `flex.map.merge(map1, map2)` combines two maps."
  q3="Do map functions modify the original map?"
  a3="No. All FLEX map functions return new maps without mutating the input values."
%}
