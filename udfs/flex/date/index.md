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

FLEX date utilities provide functions for working with dates, times, and timestamps. These functions enable date formatting, parsing, timezone conversion, and date manipulation operations.

## Available Functions

| Function | Description |
|----------|-------------|
| [date.format](./format.md) | Format a date/timestamp into a string representation |
| [date.parse](./parse.md) | Parse a date string into a timestamp |
| [date.toTimeZone](./toTimeZone.md) | Convert a timestamp to a different timezone |
| [date.truncate](./truncate.md) | Truncate a timestamp to a specific unit (day, hour, etc.) |

## Common Use Cases

- **Date Formatting**: Display dates in human-readable formats
- **Date Parsing**: Convert date strings from various formats into timestamps
- **Timezone Handling**: Work with dates across different timezones
- **Time Bucketing**: Group events by time periods (hourly, daily, etc.)