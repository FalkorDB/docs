---
layout: default
title: Bitwise Functions
description: "FLEX bitwise functions for performing AND, OR, XOR, NOT, and bit shift operations on integers in Cypher queries."
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 10
---

# Bitwise Functions

FLEX bitwise utilities.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What are FLEX bitwise functions used for?"
  a1="Bitwise functions perform low-level binary operations on integers. Common use cases include managing permission flags, toggling feature bits, and performing binary arithmetic in Cypher queries."
  q2="What data type do bitwise functions operate on?"
  a2="All FLEX bitwise functions operate on integer values and return integer results. Non-integer inputs will produce unexpected results."
  q3="How do I call a bitwise function?"
  a3="Use the namespace `flex.bitwise.<function>()`. For example: `flex.bitwise.and(5, 3)` returns `1`."
%}
