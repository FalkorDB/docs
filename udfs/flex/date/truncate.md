# date.truncate

## Description
Truncates a date/time value to the specified unit (e.g., day, month, year), setting all smaller units to their minimum values. All operations are UTC-based.

## Syntax
```cypher
flex.date.truncate(datetime, unit)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `datetime` | Date/number/string | Yes | The date/time value to truncate |
| `unit` | string | Yes | The unit to truncate to |

### Supported Units
| Unit | Description | Truncates To |
|------|-------------|--------------|
| `'minute'` | Truncate to start of minute | Sets seconds and milliseconds to 0 |
| `'hour'` | Truncate to start of hour | Sets minutes, seconds, and milliseconds to 0 |
| `'day'` | Truncate to start of day | Sets time to 00:00:00.000 |
| `'week'` | Truncate to start of week | Sets to Monday 00:00:00.000 |
| `'month'` | Truncate to start of month | Sets to 1st day at 00:00:00.000 |
| `'quarter'` | Truncate to start of quarter | Sets to 1st day of quarter month at 00:00:00.000 |
| `'year'` | Truncate to start of year | Sets to January 1st at 00:00:00.000 |

## Returns
**Type:** Date

A new Date object truncated to the specified unit. Returns `null` if input is invalid. Returns the original date if unit is unrecognized.

## Examples

### Example 1: Truncate to Day
```cypher
WITH datetime('2024-03-15T14:30:45Z') AS dt
RETURN flex.date.truncate(dt, 'day') AS truncated
```

**Output:**
```
truncated
--------------------------
2024-03-15T00:00:00.000Z
```

### Example 2: Truncate to Month
```cypher
WITH datetime('2024-03-15T14:30:45Z') AS dt
RETURN flex.date.truncate(dt, 'month') AS truncated
```

**Output:**
```
truncated
--------------------------
2024-03-01T00:00:00.000Z
```

### Example 3: Group Events by Week
```cypher
MATCH (e:Event)
WITH flex.date.truncate(e.timestamp, 'week') AS week, count(*) AS eventCount
RETURN week, eventCount
ORDER BY week
```

### Example 4: Monthly Aggregation
```cypher
MATCH (s:Sale)
WITH flex.date.truncate(s.date, 'month') AS month, sum(s.amount) AS totalSales
RETURN month, totalSales
ORDER BY month
```

### Example 5: Quarter Analysis
```cypher
MATCH (o:Order)
WITH flex.date.truncate(o.orderDate, 'quarter') AS quarter, count(*) AS orders
RETURN quarter, orders
ORDER BY quarter DESC
```

## Notes
- Returns `null` for invalid date inputs
- All operations use UTC timezone
- Week starts on Monday (ISO week convention)
- Quarters: Q1 (Jan-Mar), Q2 (Apr-Jun), Q3 (Jul-Sep), Q4 (Oct-Dec)
- Unknown units return the original normalized date
- Useful for time-series aggregation and bucketing

## See Also
- [date.format](./format.md) - Format date to string
- [date.parse](./parse.md) - Parse string to date
- [date.toTimeZone](./toTimeZone.md) - Convert date to timezone
