---
layout: default
title: Date Functions
description: "FLEX date functions for formatting, parsing, truncating, and converting date/time values in Cypher queries."
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 30
---

# Date Functions

FLEX date utilities.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What are FLEX date functions?"
  a1="FLEX date functions provide formatting, parsing, truncating, and timezone conversion for date/time values in Cypher queries."
  q2="How do I call a date function?"
  a2="Use the namespace `flex.date.<function>()`. For example: `flex.date.format(datetime(), 'yyyy-MM-dd')` formats the current date."
  q3="What date/time types do these functions accept?"
  a3="FLEX date functions work with FalkorDB datetime values, timestamps, and date strings depending on the specific function."
%}
