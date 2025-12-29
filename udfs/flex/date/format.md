# date.format

## Description
Formats a date/time value using a simple token-based pattern. Supports common date/time tokens and optional timezone offset adjustment.

## Syntax
```cypher
flex.date.format(datetime, pattern, timezone)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `datetime` | Date/number/string | Yes | The date/time value to format |
| `pattern` | string | No | Format pattern using tokens (default: `'YYYY-MM-DDTHH:mm:ss[Z]'`) |
| `timezone` | string | No | Timezone offset like `"+02:00"` or `"-05:00"` |

### Supported Pattern Tokens
| Token | Description | Example |
|-------|-------------|---------|
| `YYYY` | 4-digit year | `2024` |
| `MM` | 2-digit month (01-12) | `03` |
| `DD` | 2-digit day (01-31) | `15` |
| `HH` | 2-digit hour (00-23) | `14` |
| `mm` | 2-digit minute (00-59) | `30` |
| `ss` | 2-digit second (00-59) | `45` |
| `SSS` | 3-digit milliseconds | `123` |
| `[Z]` | Literal 'Z' character | `Z` |

## Returns
**Type:** string

A formatted date/time string according to the pattern. Returns `null` if the input date is invalid.

## Examples

### Example 1: Basic Date Formatting
```cypher
WITH datetime('2024-03-15T14:30:00Z') AS dt
RETURN flex.date.format(dt, 'YYYY-MM-DD') AS date
```

**Output:**
```
date
----------
2024-03-15
```

### Example 2: Full DateTime with Time
```cypher
WITH datetime('2024-03-15T14:30:45Z') AS dt
RETURN flex.date.format(dt, 'YYYY-MM-DD HH:mm:ss') AS formatted
```

**Output:**
```
formatted
-------------------
2024-03-15 14:30:45
```

### Example 3: Custom Format with Timezone
```cypher
WITH datetime('2024-03-15T14:30:00Z') AS dt
RETURN flex.date.format(dt, 'DD/MM/YYYY HH:mm', '+02:00') AS localTime
```

**Output:**
```
localTime
-----------------
15/03/2024 16:30
```
(Adjusted for +02:00 timezone)

### Example 4: Formatting Node Timestamps
```cypher
MATCH (e:Event)
RETURN e.name, flex.date.format(e.timestamp, 'YYYY-MM-DD') AS eventDate
ORDER BY e.timestamp DESC
```

## Notes
- Returns `null` for invalid date inputs
- Default pattern is ISO8601-like: `'YYYY-MM-DDTHH:mm:ss[Z]'`
- Timezone parameter adjusts the displayed time for the given offset
- All calculations are UTC-based internally
- Milliseconds are optional in the pattern

## See Also
- [date.parse](./parse.md) - Parse string to date
- [date.truncate](./truncate.md) - Truncate date to specific unit
- [date.toTimeZone](./toTimeZone.md) - Convert date to timezone
