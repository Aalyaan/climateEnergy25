# 🏗️ Zoning & Water Data Integration Plan

## New Datasets Overview

### 1. 📋 Regrid Zoning Data (`synthetic_regrid_parcel_grid.csv`)
- **Size:** 200 sites
- **Purpose:** Land availability based on zoning laws
- **Key Columns:**
  - `SiteID`, `Latitude`, `Longitude`
  - `CountyFIPS` - County identifier
  - `SiteType` - PowerPlant, BusStation, TransmissionNode
  - `GridNodeID` - Links to grid infrastructure
  - `PlantID` - Links to power plants (if applicable)
  - `ZoningCode` - **CRITICAL for data center siting**

### 2. 💧 US Water Data (`synthetic_us_water_latlon_grid.csv`)
- **Size:** 780 grid points (lat/lon grid covering US)
- **Purpose:** Water availability for data center cooling
- **Key Columns:**
  - `Latitude`, `Longitude`
  - `SurfaceWater_Availability` - Surface water resources
  - `Groundwater_Availability` - Groundwater resources
  - `Water_Stress_Index` - 0 (low stress) to 1 (high stress)
  - `Potable_Population_Served` - Population served
  - `Potable_Capacity_MGD` - Million Gallons per Day capacity

---

## Zoning Code Analysis

### Zoning Categories (from sample):
1. **DATA_CENTER_OK** - Explicitly zoned for data centers ✅
2. **COMMERCIAL** - Commercial zoning (likely suitable) ✅
3. **INDUSTRIAL** - Industrial zoning (likely suitable) ✅
4. **NO_DATA_CENTER** - Explicitly prohibited ❌
5. **AGRICULTURAL** - Agricultural zoning (unlikely suitable) ⚠️
6. **RESIDENTIAL** - Residential zoning (prohibited) ❌

### Suitability for Different Infrastructure:
- **Data Centers:** DATA_CENTER_OK, COMMERCIAL, INDUSTRIAL
- **Electrolyzers:** INDUSTRIAL, COMMERCIAL
- **EV Hubs:** COMMERCIAL, INDUSTRIAL
- **Hydrogen Hubs:** INDUSTRIAL

---

## Water Availability Analysis

### Key Metrics:
1. **Total Water Availability** = SurfaceWater + Groundwater
2. **Water Stress Index:**
   - Low stress (<0.2): Abundant water ✅
   - Medium stress (0.2-0.8): Moderate availability ⚠️
   - High stress (>0.8): Scarce water ❌

3. **Potable Capacity (MGD):**
   - Data centers need significant cooling water
   - 2GW data center: ~5-10 MGD for cooling
   - Higher capacity = better suitability

### Water Requirements by Infrastructure Type:
- **Data Centers:** High (cooling towers, evaporative cooling)
  - 2GW data center: ~5-10 MGD
- **Electrolyzers:** Very High (water is feedstock)
  - 1 kg H2 requires ~9 liters of water
- **EV Charging Hubs:** Low (minimal water needs)
- **Hydrogen Hubs:** High (if producing hydrogen on-site)

---

## Integration Strategy

### Step 1: Spatial Matching
Match substations to nearest zoning site and water grid point using:
- `scipy.spatial.cKDTree` for nearest neighbor search
- Distance-weighted interpolation for water data

### Step 2: Add New Scoring Factors

#### 🏗️ Land Availability Score (10% weight)
- **Zoning Suitability** (6%):
  - DATA_CENTER_OK: 1.0
  - COMMERCIAL: 0.8
  - INDUSTRIAL: 0.9
  - NO_DATA_CENTER: 0.0
  - AGRICULTURAL: 0.3
  - RESIDENTIAL: 0.0

- **Site Type Match** (4%):
  - BusStation near substation: Bonus
  - PowerPlant near generation: Bonus

#### 💧 Water Availability Score (10% weight)
- **Water Abundance** (5%):
  - Total water = SurfaceWater + Groundwater
  - Higher is better
  
- **Low Water Stress** (3%):
  - Inverse of Water_Stress_Index
  - Lower stress is better
  
- **Potable Capacity** (2%):
  - MGD capacity
  - Higher is better (need 5-10 MGD for 2GW DC)

### Step 3: Updated Scoring Model (16 Factors!)

**Previous: 14 factors, 100% weight**

**New: 16 factors, 100% weight**

Rebalance to accommodate new factors:

```
⚡ Grid SLACK Capacity (25%): ← Reduced from 30%
  • Transmission SLACK (15%) ← Reduced from 18%
  • Generation SLACK (10%) ← Reduced from 12%

Capacity Factor Matching (18%): ← Reduced from 20%
  • Effective Capacity w/ CF (11%)
  • Nuclear Proximity (7%)

Economic Factors (17%): ← Reduced from 20%
  • Energy Costs (9%)
  • Congestion Risk (4%)
  • Transmission Cost (4%)

🏗️ Land Availability (10%): ← NEW!
  • Zoning Suitability (6%)
  • Site Type Match (4%)

💧 Water Availability (10%): ← NEW!
  • Water Abundance (5%)
  • Low Water Stress (3%)
  • Potable Capacity (2%)

🏙️ Zone Demand (8%): ← Reduced from 10%
  • Lower Demand Score (8%)

Co-Location Potential (8%): ← Reduced from 12%
  • Solar Potential (5%)
  • Wind Potential (3%)

Plant-Level eGRID (4%): ← Reduced from 8%
  • Plant Proximity (2%)
  • eGRID Renewables (1%)
  • Low Emissions (1%)
```

**Total: 16 factors, 100% weight**

---

## Implementation Steps

### 1. Load New Datasets
```python
regrid = pd.read_csv('synthetic_regrid_parcel_grid.csv')
water = pd.read_csv('synthetic_us_water_latlon_grid.csv')
```

### 2. Spatial Matching
```python
from scipy.spatial import cKDTree

# Match substations to nearest zoning site
regrid_coords = regrid[['Latitude', 'Longitude']].values
regrid_tree = cKDTree(regrid_coords)
distances_zoning, indices_zoning = regrid_tree.query(subs_coords, k=1)

# Match substations to nearest water grid point
water_coords = water[['Latitude', 'Longitude']].values
water_tree = cKDTree(water_coords)
distances_water, indices_water = water_tree.query(subs_coords, k=1)
```

### 3. Add Zoning Scores
```python
# Map zoning codes to suitability scores
zoning_scores = {
    'DATA_CENTER_OK': 1.0,
    'COMMERCIAL': 0.8,
    'INDUSTRIAL': 0.9,
    'NO_DATA_CENTER': 0.0,
    'AGRICULTURAL': 0.3,
    'RESIDENTIAL': 0.0
}

substations['nearest_zoning_code'] = regrid.iloc[indices_zoning]['ZoningCode'].values
substations['zoning_suitability'] = substations['nearest_zoning_code'].map(zoning_scores)
substations['dist_to_zoning_site_km'] = distances_zoning * 111
```

### 4. Add Water Scores
```python
substations['surface_water'] = water.iloc[indices_water]['SurfaceWater_Availability'].values
substations['groundwater'] = water.iloc[indices_water]['Groundwater_Availability'].values
substations['total_water'] = substations['surface_water'] + substations['groundwater']
substations['water_stress_index'] = water.iloc[indices_water]['Water_Stress_Index'].values
substations['potable_capacity_mgd'] = water.iloc[indices_water]['Potable_Capacity_MGD'].values
substations['dist_to_water_grid_km'] = distances_water * 111
```

### 5. Calculate New Scores
```python
# Land availability
substations['zoning_score'] = normalize(substations['zoning_suitability']) * 0.06
substations['site_type_score'] = ... * 0.04

# Water availability
substations['water_abundance_score'] = normalize(substations['total_water']) * 0.05
substations['low_water_stress_score'] = inverse_normalize(substations['water_stress_index']) * 0.03
substations['potable_capacity_score'] = normalize(substations['potable_capacity_mgd']) * 0.02
```

### 6. Update Filtering
Add water availability filter:
```python
subs_filtered = subs_filtered[
    (subs_filtered['water_stress_index'] < 0.8) &  # Not high water stress
    (subs_filtered['potable_capacity_mgd'] >= 5.0) &  # At least 5 MGD for 2GW DC
    (subs_filtered['zoning_suitability'] >= 0.8)  # Commercial or Industrial or DC_OK
].copy()
```

---

## Expected Impact

### Locations that will RISE:
- ✅ Areas with DATA_CENTER_OK zoning
- ✅ Industrial zones near substations
- ✅ Regions with abundant water (Great Lakes, Pacific Northwest, Southeast)
- ✅ Low water stress areas

### Locations that will FALL:
- ❌ Residential or agricultural zones
- ❌ NO_DATA_CENTER zoning
- ❌ High water stress areas (Southwest deserts)
- ❌ Low potable capacity regions

---

## Data Center Cooling Requirements

### Typical 2GW Data Center:
- **Water consumption:** 5-10 MGD (million gallons per day)
- **Cooling methods:**
  - Evaporative cooling (water-intensive)
  - Air cooling (less efficient, higher energy cost)
  - Hybrid systems

### Water Stress Considerations:
- **Low stress (<0.2):** No restrictions, evaporative cooling OK
- **Medium stress (0.2-0.8):** May need water recycling
- **High stress (>0.8):** Air cooling required or water import needed

---

## Next Steps

1. ✅ Create new cells in notebook for zoning/water integration
2. Load and spatially match both datasets
3. Add new scoring factors (land + water = 20% total)
4. Rebalance existing factors to 80%
5. Update filtering criteria
6. Re-run analysis and compare results
7. Document water requirements for different infrastructure types
8. Update README and documentation

---

*This integration addresses 2 critical missing parameters: Land Availability (zoning) and Water Availability (cooling).*

