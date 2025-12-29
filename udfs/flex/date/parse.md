# date.parse

## Description
Parses a date/time string into a Date object using an optional pattern. Supports explicit patterns and falls back to standard Date parsing for other formats.

## Syntax
```cypher
flex.date.parse(dateString, pattern, timezone)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dateString` | string | Yes | The date/time string to parse |
| `pattern` | string | No | Format pattern (supported: `'YYYY-MM-DD'`, `'YYYY-MM-DDTHH:mm:ss'` or `'YYYY-MM-DD HH:mm:ss'`, or auto-detect) |
| `timezone` | string | No | Timezone offset like `"+02:00"` to interpret input in specific timezone |

## Returns
**Type:** Date

A Date object representing the parsed date/time. Returns `null` if parsing fails.

## Examples

### Example 1: Parse Date Only
```cypher
RETURN flex.date.parse('2024-03-15', 'YYYY-MM-DD') AS date
```

**Output:**
```
date
-----------------------------
2024-03-15T00:00:00.000Z (Date object)
```

### Example 2: Parse DateTime
```cypher
RETURN flex.date.parse('2024-03-15T14:30:00', 'YYYY-MM-DDTHH:mm:ss') AS datetime
```

### Example 3: Auto-detect ISO Format
```cypher
RETURN flex.date.parse('2024-03-15T14:30:00Z') AS dt
```

### Example 4: Parse with Timezone Context
```cypher
WITH '2024-03-15 10:00:00' AS localTime
RETURN flex.date.parse(localTime, 'YYYY-MM-DDTHH:mm:ss', '+05:00') AS utcTime
```
(Interprets input as being in +05:00 timezone and converts to UTC)

### Example 5: Batch Import with Date Parsing
```cypher
UNWIND $events AS event
CREATE (e:Event {
    name: event.name,
    date: flex.date.parse(event.dateString, 'YYYY-MM-DD')
})
```

## Notes
- Returns `null` for invalid or unparseable date strings
- Supported explicit patterns: `'YYYY-MM-DD'`, `'YYYY-MM-DDTHH:mm:ss'` and `'YYYY-MM-DD HH:mm:ss'` (both `T` and space separators are accepted)
- Falls back to JavaScript Date constructor for other formats (ISO8601, etc.)
- Timezone parameter interprets the input time as local time in that offset
- All dates are normalized to UTC internally

## See Also
- [date.format](./format.md) - Format date to string
- [date.truncate](./truncate.md) - Truncate date to specific unit
- [date.toTimeZone](./toTimeZone.md) - Convert date to timezone
