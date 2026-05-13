---
layout: default
title: JSON Functions
description: "FLEX JSON functions for serializing values to JSON strings and parsing JSON strings into maps or lists."
parent: FLEX Function Reference
grand_parent: UDFs
has_children: true
nav_order: 40
---

# JSON Functions

FLEX json utilities.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What are FLEX JSON functions?"
  a1="FLEX JSON functions provide serialization (value to JSON string) and parsing (JSON string to map or list) utilities for use in Cypher queries."
  q2="How do FLEX JSON functions handle invalid input?"
  a2="They handle errors gracefully — `fromJsonMap` returns an empty map `{}` and `fromJsonList` returns an empty list `[]` on parse failures, without throwing exceptions."
  q3="How do I call a JSON function?"
  a3="Use the namespace `flex.json.<function>()`. For example: `flex.json.toJson({name: 'Alice'})` returns a JSON string."
%}
