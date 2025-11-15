# ⚡ YES! PowerSimData HAS Transmission Line Data

## What PowerSimData Includes:

### 🔌 **Branches** (Transmission Lines)
- **Thermal limits** (rateA, rateB, rateC in MW)
- **Impedance** (resistance and reactance)
- **Connectivity** (from_bus_id to to_bus_id)
- **Geographic routing**
- Thousands of transmission lines across US grid

### 📍 **Buses** (Substations/Nodes)
- **Coordinates** (lat, lon)
- **Voltage levels**
- **Base MVA**
- Connection points for plants and loads

### ⚡ **Plants** (Generation)
- Already in your eGRID data
- PowerSimData links them to buses

## How to Access:

```python
from powersimdata.input.grid import Grid

# Load grid
grid = Grid(['USA'])  # or 'Western', 'Eastern', 'Texas'

# Access transmission lines
transmission_lines = grid.branch
print(f"Total lines: {len(transmission_lines)}")
print(transmission_lines.columns)

# Access substations
substations = grid.bus
print(f"Total buses: {len(substations)}")
print(substations[['lat', 'lon', 'baseKV']].head())

# Access plants
plants = grid.plant
```

## What This Enables for Your Siting Analysis:

### ✅ **Congestion Analysis**
- Check thermal limits vs. current flow
- Identify bottlenecks
- Find low-congestion areas

### ✅ **Substation Proximity**
- Calculate distance to nearest substation
- Find available connection points
- Estimate interconnection costs

### ✅ **Power Flow Modeling**
- Run power flow simulations
- Test impact of new loads
- Model grid constraints

### ✅ **Network Topology**
- Understand grid connectivity
- Identify isolated vs. well-connected areas
- Map transmission corridors

## Integration with Your Current Analysis:

### Current Approach (optimal_siting_analysis.ipynb):
✅ Uses eGRID plant data
✅ Scores by renewable %, emissions, reliability
✅ Provides plant-level coordinates
❌ Missing transmission constraints

### Enhanced Approach (with PowerSimData):
✅ Everything above PLUS:
✅ Transmission line capacity
✅ Substation locations
✅ Congestion analysis
✅ Power flow constraints
✅ Network connectivity

## Quick Start:

1. **Install PowerSimData:**
   ```bash
   pip install powersimdata
   ```

2. **Run power_simulator_setup.ipynb:**
   - Cell 12 now shows how to access transmission data
   - Will load grid with branches and buses

3. **Enhance Your Siting Model:**
   ```python
   # Add transmission proximity score
   from scipy.spatial import cKDTree
   
   # Build tree of substation locations
   bus_coords = grid.bus[['lat', 'lon']].values
   tree = cKDTree(bus_coords)
   
   # For each candidate site, find nearest substation
   for site in candidate_sites:
       distance, idx = tree.query([site.lat, site.lon])
       site.transmission_score = 1 / (1 + distance)  # Closer = better
   ```

## Data Sources Comparison:

| Feature | eGRID (Current) | PowerSimData | HIFLD |
|---------|----------------|--------------|-------|
| Plant locations | ✅ | ✅ | ❌ |
| Generation data | ✅ | ✅ | ❌ |
| Transmission lines | ❌ | ✅ | ✅ |
| Substations | ❌ | ✅ | ✅ |
| Thermal limits | ❌ | ✅ | ⚠️ |
| Power flow | ❌ | ✅ | ❌ |
| Congestion | ❌ | ✅* | ❌ |

*Requires running simulations

## Recommendation:

**For your hackathon, you have TWO paths:**

### Path 1: Quick (Current)
- Use `optimal_siting_analysis.ipynb` as-is
- Plant-level coordinates already provided
- Good enough for initial screening
- **Time: Ready now**

### Path 2: Complete (With PowerSimData)
- Install PowerSimData
- Load grid with transmission data
- Add transmission proximity scoring
- Run power flow analysis
- **Time: 2-4 hours to integrate**

## Bottom Line:

**YES, PowerSimData has transmission line data!**

It includes:
- ~60,000+ transmission lines
- ~75,000+ buses/substations  
- Thermal limits for congestion analysis
- Geographic coordinates
- Network topology

This is exactly what you need for comprehensive siting analysis!

