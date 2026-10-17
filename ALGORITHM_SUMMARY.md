# Nexsite Algorithm Summary

## Overview
The Nexsite algorithm uses a two-stage scoring system to identify optimal data center locations across three categories: **Lowest Cost**, **Lowest Emissions**, and **Highest Reliability**.

---

## Stage 1: Parameter Calculation (P1-P6)

Six parameters are calculated for each location using **fixed default weights** (not user-adjustable):

### **P1: Proximity to Renewable Energy** (0-1 scale)
**Sub-components:**
- **Distance to RE** (40%): Inverse normalized distance to nearest renewable plant
- **Renewable Share** (35%): Percentage of renewable energy within 100km
- **Renewable Capacity** (25%): Normalized renewable capacity within 100km

**Formula:**
```
P1 = 0.40 × norm_inv(distance_to_RE) + 0.35 × renewable_share + 0.25 × norm(renewable_capacity)
```

### **P2: Emissions** (0-1 scale)
**Sub-components:**
- **Climate Impact** (75%):
  - CO2e (70%): Inverse normalized CO2 equivalent emissions
  - CO2 (30%): Inverse normalized CO2 emissions
- **Air Quality** (25%):
  - NOx (50%): Inverse normalized NOx emissions
  - SO2 (50%): Inverse normalized SO2 emissions

**Formula:**
```
S_climate = 0.70 × norm_inv(CO2e) + 0.30 × norm_inv(CO2)
S_air = 0.50 × norm_inv(NOx) + 0.50 × norm_inv(SO2)
P2 = 0.75 × S_climate + 0.25 × S_air
```

### **P3: Capital Investment** (0-1 scale)
**Sub-components:**
- **Land Cost** (40%): Inverse normalized property values (lower = better)
- **Transmission** (40%):
  - Transmission Distance (50%): Inverse normalized distance to renewable plant
  - Transmission Capacity (50%): Normalized existing line capacity
- **Electricity Cost** (20%): Inverse normalized state electricity rates

**Formula:**
```
t_score = 0.50 × norm_inv(trans_dist) + 0.50 × norm(trans_capacity)
P3 = 0.40 × norm_inv(land_value) + 0.40 × t_score + 0.20 × norm_inv(electricity_rate)
```

### **P4: Reliability** (0-1 scale)
**Sub-components:**
- **SAIDI** (35%): Inverse normalized System Average Interruption Duration Index (hours)
- **SAIFI** (35%): Inverse normalized System Average Interruption Frequency Index (interruptions/year)
- **Grid Degree** (15%): Normalized number of incident transmission lines
- **Capacity** (15%): Normalized transmission line capacity

**Formula:**
```
P4 = 0.35 × norm_inv(SAIDI) + 0.35 × norm_inv(SAIFI) + 0.15 × norm(num_lines) + 0.15 × norm(capacity)
```

### **P5: Water** (0-1 scale)
**Sub-components:**
- **Potable Capacity** (90%): Normalized potable water capacity (MGD)
- **Lower 48** (10%): Binary indicator (1 if in lower 48 states, 0 otherwise)

**Formula:**
```
P5 = 0.90 × norm(potable_capacity) + 0.10 × in_lower_48
```

### **P6: Transmission Capacity** (0-1 scale)
**Simple normalized value:**
- Normalized sum of transmission line capacity (MW)

**Formula:**
```
P6 = norm(sum_line_capacity_MW)
```

---

## Stage 2: Category Score Calculation (User-Adjustable)

Each category score (0-100) is calculated by weighting the six parameters. **Users can adjust these weights via sliders:**

### **Lowest Cost** (Default Weights)
```
Score = 100 × (
  0.10 × P1 +  # RE Proximity
  0.00 × P2 +  # Emissions (not considered for cost)
  0.60 × P3 +  # Capital Investment (most important)
  0.10 × P4 +  # Reliability
  0.20 × P5 +  # Water
  0.00 × P6    # Transmission Capacity
)
```

### **Lowest Emissions** (Default Weights)
```
Score = 100 × (
  0.20 × P1 +  # RE Proximity
  0.60 × P2 +  # Emissions (most important)
  0.00 × P3 +  # Capital Investment (not considered)
  0.10 × P4 +  # Reliability
  0.10 × P5 +  # Water
  0.00 × P6    # Transmission Capacity
)
```

### **Highest Reliability** (Default Weights)
```
Score = 100 × (
  0.20 × P1 +  # RE Proximity
  0.00 × P2 +  # Emissions (not considered)
  0.10 × P3 +  # Capital Investment
  0.60 × P4 +  # Reliability (most important)
  0.10 × P5 +  # Water
  0.00 × P6    # Transmission Capacity
)
```

### **Overall Score**
```
Overall = (Lowest_Cost_Score + Lowest_Emissions_Score + Highest_Reliability_Score) / 3
```

---

## Stage 3: Location Selection (With State Diversity Penalty)

### **State Diversity Penalty**
- **Fixed penalty factor: 0.5 (50%)**
- When selecting top locations, if multiple locations are in the same state:
  - **1st location in state**: No penalty
  - **2nd location in same state**: 50% score reduction
  - **3rd location in same state**: 100% score reduction (effectively excluded)

### **Selection Process**
1. **Top 3 per Category**: 
   - Selects top 3 locations for each category (Lowest Cost, Lowest Emissions, Highest Reliability)
   - Applies state diversity penalty during selection
   - Ensures geographic diversity in results

2. **Top 5 Overall**:
   - Selects top 5 locations based on Overall Score
   - Applies state diversity penalty during selection

3. **Final Display**:
   - Shows top 3 locations in each category
   - Shows top 5 overall locations
   - All locations displayed on interactive map

---

## Normalization Functions

### **norm(X)**: Standard Normalization (Higher is Better)
```
norm(X) = (X - min(X)) / (max(X) - min(X))
```
- Maps values to 0-1 range
- Higher values → higher score

### **norm_inv(X)**: Inverse Normalization (Lower is Better)
```
norm_inv(X) = (max(X) - X) / (max(X) - min(X))
```
- Maps values to 0-1 range
- Lower values → higher score
- Used for costs, emissions, distances (where lower is better)

---

## Data Sources

- **Power Plant Data**: eGRID plant-level data (12,291 plants)
- **Transmission Data**: PowerSimData substation data (82,071 substations)
- **State-Level Data**: 
  - Electricity costs by state
  - SAIDI/SAIFI reliability metrics by state
- **Geographic Data**: Property values, water capacity, coordinates

---

## Key Features

1. **Multi-Criteria Analysis**: Considers 6 parameters across 3 categories
2. **User Customization**: Adjust category weights via sliders
3. **Geographic Diversity**: State diversity penalty ensures results aren't concentrated in one state
4. **Cost Estimation**: Converts scores to dollar amounts (2GW facility, 10-year TCO)
5. **Median Comparison**: Shows how each location compares to median cost across all locations

---

## Example Calculation

For a location with:
- **P1** = 0.75 (good RE proximity)
- **P2** = 0.60 (moderate emissions)
- **P3** = 0.85 (low capital costs)
- **P4** = 0.70 (good reliability)
- **P5** = 0.80 (good water access)
- **P6** = 0.65 (moderate transmission capacity)

**Lowest Cost Score** (with default weights):
```
= 100 × (0.10×0.75 + 0.00×0.60 + 0.60×0.85 + 0.10×0.70 + 0.20×0.80 + 0.00×0.65)
= 100 × (0.075 + 0 + 0.51 + 0.07 + 0.16 + 0)
= 100 × 0.815
= 81.5/100
```

This location would rank highly for "Lowest Cost" due to its strong P3 (Capital Investment) score.

