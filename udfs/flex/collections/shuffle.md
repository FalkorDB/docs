---
layout: default
title: coll.shuffle
description: "Returns a randomly shuffled copy of a list using the Fisher-Yates algorithm."
parent: Collection Functions
grand_parent: FLEX Function Reference
nav_order: 3
---

# coll.shuffle

## Description
Randomly shuffles the elements of a list using the Fisher-Yates algorithm. Returns a new list with elements in random order without modifying the original.

## Syntax
```cypher
flex.coll.shuffle(list)
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `list` | list | Yes | The list to shuffle |

## Returns
**Type:** list

A new list containing the same elements in a randomized order. Returns an empty list if input is not an array.

## Examples

### Example 1: Basic Shuffle
```cypher
WITH [1, 2, 3, 4, 5] AS numbers
RETURN flex.coll.shuffle(numbers) AS shuffled
```

**Output:** (example, actual order will vary)
```text
shuffled
-----------
[3, 1, 5, 2, 4]
```

### Example 2: Random Sample Selection
```cypher
MATCH (q:Question)
WITH collect(q) AS allQuestions
WITH flex.coll.shuffle(allQuestions) AS randomized
RETURN randomized[0..10] AS quizQuestions
```

### Example 3: Randomizing Recommendations
```cypher
MATCH (u:User {id: $userId})-[:LIKES]->(p:Product)
MATCH (p)-[:SIMILAR_TO]->(rec:Product)
WITH collect(DISTINCT rec) AS recommendations
RETURN flex.coll.shuffle(recommendations)[0..5] AS randomRecs
```

### Example 4: Random Team Assignment
```cypher
MATCH (p:Player)
WITH collect(p.name) AS players
WITH flex.coll.shuffle(players) AS shuffled
RETURN shuffled[0..5] AS team1, shuffled[5..10] AS team2
```

## Notes
- Returns empty list if input is not an array or is `null`
- Uses the Fisher-Yates shuffle algorithm for uniform random distribution
- Creates a new list; does not modify the original
- Each element appears exactly once in the result
- Order is truly random on each execution

## See Also
- [coll.zip](./zip.md) - Combine two lists element-by-element
- [coll.union](./union.md) - Combine unique elements from lists

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="Is the shuffle result deterministic?"
  a1="No. `flex.coll.shuffle` produces a random permutation each time it is called, so results will vary between executions."
  q2="Does shuffle modify the original list?"
  a2="No. It returns a new shuffled list; the original remains unchanged."
%}
