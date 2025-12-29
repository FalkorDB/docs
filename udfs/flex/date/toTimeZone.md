# date.toTimeZone

## Description
Converts a date/time instant to represent the wall clock time in a given timezone offset. The returned Date represents the same instant but shifted so UTC fields reflect local time.

## Syntax
```cypher
flex.date.toTimeZone(datetime, timezone)
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `datetime` | Date/number/string | Yes | The date/time value to convert |
| `timezone` | string | Yes | Timezone offset like `"+02:00"`, `"-05:00"`, or `"+0530"` |

## Returns
**Type:** Date

A Date object adjusted to show local time in the given timezone. Returns `null` if input is invalid. Returns original date if timezone format is invalid.

## Examples

### Example 1: Convert UTC to Eastern Time
```cypher
WITH datetime('2024-03-15T14:00:00Z') AS utc
RETURN flex.date.toTimeZone(utc, '-05:00') AS eastern
```

**Output:**
```
eastern
--------------------------
2024-03-15T09:00:00.000Z
```
(UTC fields now show 09:00 which is the local time in -05:00)

### Example 2: Convert to Multiple Timezones
```cypher
WITH datetime('2024-03-15T12:00:00Z') AS utc
RETURN 
    flex.date.format(utc, 'HH:mm') AS utcTime,
    flex.date.format(flex.date.toTimeZone(utc, '+00:00'), 'HH:mm') AS london,
    flex.date.format(flex.date.toTimeZone(utc, '+01:00'), 'HH:mm') AS paris,
    flex.date.format(flex.date.toTimeZone(utc, '+05:30'), 'HH:mm') AS india,
    flex.date.format(flex.date.toTimeZone(utc, '-05:00'), 'HH:mm') AS newYork
```

### Example 3: Display User Events in Local Time
```cypher
MATCH (u:User {id: $userId})
MATCH (e:Event)-[:ASSIGNED_TO]->(u)
WITH e, flex.date.toTimeZone(e.timestamp, u.timezone) AS localTime
RETURN e.name, flex.date.format(localTime, 'YYYY-MM-DD HH:mm') AS localDisplay
ORDER BY e.timestamp
```

### Example 4: Adjust for Daylight Saving Time Context
```cypher
WITH datetime('2024-07-15T12:00:00Z') AS summer
RETURN flex.date.format(
    flex.date.toTimeZone(summer, '-04:00'), 
    'YYYY-MM-DD HH:mm'
) AS edtTime
```

## Notes
- Returns `null` for invalid date inputs
- Invalid timezone format returns the original date unchanged
- Timezone format accepts `+HH:MM`, `-HH:MM`, `+HHMM`, or `-HHMM`
- Does not handle DST transitions automatically
- The returned Date's UTC methods will show the local time
- Useful for displaying times in user's local timezone

## See Also
- [date.format](./format.md) - Format date with timezone support
- [date.parse](./parse.md) - Parse date with timezone context
- [date.truncate](./truncate.md) - Truncate date to specific unit
