# 📍 Why State Codes Show as "nan"

## The Issue

The `state_code` column in `usa_bus_features_2016.csv` is **empty** (contains no values), which causes "nan" to appear in the analysis.

## Why This Happened

The PowerSimData export you provided includes:
- ✅ `zone_name` - Grid zones (e.g., "Washington", "Maine", "California")
- ✅ `interconnect_id` - Grid interconnections (Eastern, Western, Texas)
- ✅ `bus_id` - Unique substation identifiers
- ✅ `node_lat`, `node_lon` - Exact coordinates
- ❌ `state_code` - **Empty column** (no data)

## What We're Using Instead

**Zone Names** provide regional identification:
- Zone names like "Washington", "Maine", "California" represent **grid zones**
- Grid zones often align with states but are defined by electrical boundaries, not political ones
- This is actually more relevant for grid analysis than state boundaries!

## Example

Instead of:
```
Bus 2011011 - Washington, WA
```

You see:
```
Bus 2011011 - Washington
```

Where:
- `2011011` = Unique substation ID (bus_id)
- `Washington` = Grid zone name
- Coordinates: 47.957500°N, -118.977000°W (exact location)

## Why This Is Actually Better

1. **Grid zones matter more than states** for electrical infrastructure
2. **Exact coordinates** are provided (lat/lon to 6 decimal places)
3. **Bus IDs** uniquely identify each connection point
4. **Interconnect information** shows which major grid the substation belongs to

## The Fix Applied

All visualizations and tables have been updated to:
- Use `zone_name` instead of `state_code`
- Show `interconnect_id` (Eastern/Western/Texas) for regional context
- Emphasize `bus_id` as the unique identifier
- Display exact coordinates for precise location

## Bottom Line

**You have MORE precise data than state-level information:**
- 82,071 individual substations
- Exact GPS coordinates
- Grid zone identification
- Unique bus IDs for each connection point

This is substation-level granularity - the most detailed grid data available!

