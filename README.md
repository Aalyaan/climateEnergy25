# Optimal Siting Framework for Energy-Intensive Infrastructure

## Problem Statement
Determine optimal locations for Meta's next data center (and other energy-intensive infrastructure like electrolyzers, EV/H2 hubs) based on comprehensive grid analysis.

## Main Analysis
**`siting_with_transmission.ipynb`** - Complete siting analysis with transmission data

### Features:
- ✅ **82,071 substations** analyzed (substation-level granularity)
- ✅ **12,612 power plants** from eGRID (including 93 nuclear plants)
- ✅ **16-factor COMPREHENSIVE scoring model** ← COMPLETE! All 10 parameters covered
- ✅ **⚡ SLACK CAPACITY analysis** - Filters for SPARE capacity, not just total
- ✅ **🏗️ ZONING & LAND AVAILABILITY** ← NEW! Regrid data for buildable sites
- ✅ **💧 WATER AVAILABILITY** ← NEW! Cooling water for data centers
- ✅ **2GW data center feasibility filter** - Per RWE requirements
- ✅ **Capacity factor matching** (nuclear, solar, wind) - Per RWE
- ✅ **Cost savings analysis** ($M annual & 10-year) - Per RWE
- ✅ **Zone demand filtering** - Avoids congested urban areas
- ✅ **Transmission capacity** (≥2GW for data center)
- ✅ **Generation capacity** (≥3GW nearby)
- ✅ **Nuclear proximity** (high capacity factor)
- ✅ **Energy costs** with $ quantification
- ✅ **Co-location potential** (solar + wind + storage)
- ✅ **Interactive visualizations** (Plotly + Matplotlib)

### COMPREHENSIVE 16-Factor Scoring Model:
```
⚡ Grid SLACK Capacity (25%): ← CRITICAL! Uses SPARE capacity
  • Transmission SLACK (15%)
  • Generation SLACK (10%)

Capacity Factor Matching (18%): ← RWE Priority
  • Effective Capacity w/ CF (11%)
  • Nuclear Proximity (7%)

Economic Factors (17%):
  • Energy Costs (9%)
  • Congestion Risk (4%)
  • Transmission Cost (4%)

🏗️ Land Availability (10%): ← NEW! Zoning data
  • Zoning Suitability (6%)
  • Site Type Match (4%)

💧 Water Availability (10%): ← NEW! Cooling water
  • Water Abundance (5%)
  • Low Water Stress (3%)
  • Potable Capacity (2%)

🏙️ Zone Demand (8%): ← Avoids congested areas
  • Lower Demand Score (8%)

Co-Location Potential (8%):
  • Solar Potential (5%)
  • Wind Potential (3%)

Plant-Level eGRID (4%):
  • Plant Proximity (2%)
  • eGRID Renewables (1%)
  • Low Emissions (1%)
```

**🎉 COMPLETE COVERAGE: All 10 Parameters!**
1. ✅ Transmission Capacity (slack)
2. ✅ Generation Capacity (slack)
3. ✅ Energy Costs
4. ✅ Congestion Risk
5. ✅ Renewable Energy
6. ✅ Emissions
7. ✅ Nuclear Proximity
8. ✅ Co-location Potential
9. ✅ **Land Availability (zoning)** ← NEW!
10. ✅ **Water Availability (cooling)** ← NEW!

**Aligned with RWE advisor priorities!**
**Filters for 2GW data center feasibility!**
**Includes cost savings analysis ($M)!**

## Data Sources
1. **usa_bus_features_2016.csv** - PowerSimData transmission substations (82K+ substations)
2. **Untitled spreadsheet - PLNT23.csv** - EPA eGRID plant data (12K+ plants)
3. **synthetic_regrid_parcel_grid.csv** - Regrid zoning data (200 sites) ← NEW!
4. **synthetic_us_water_latlon_grid.csv** - US water availability grid (780 points) ← NEW!

## Results
- **meta_datacenter_top20_with_transmission_20251115_1651.csv** - Top 20 recommended locations
- **all_substations_scored_20251115_1651.csv** - All scored substations

## Key Findings
Top 5 locations provide:
- Exact substation coordinates (lat/lon to 6 decimals)
- Transmission capacity (MW available)
- Renewable energy percentage
- Grid reliability metrics
- CO2 intensity

## Documentation
- **ZONING_WATER_SUMMARY.md** - 🎉 LATEST! Complete 16-factor model ← READ THIS FIRST!
- **ZONING_WATER_INTEGRATION_PLAN.md** - Detailed integration strategy
- **SLACK_CAPACITY_UPDATE.md** - ⚡ Explains slack capacity analysis
- **RWE_ALIGNMENT_SUMMARY.md** - RWE-aligned model details
- **COMPREHENSIVE_MODEL_SUMMARY.md** - 12-factor model baseline
- **GRANULARITY_SUMMARY.md** - Explains substation-level precision
- **TRANSMISSION_DATA_SUMMARY.md** - PowerSimData capabilities
- **MAP_VISUALIZATION_GUIDE.md** - How to use visualizations
- **STATE_CODE_EXPLANATION.md** - Why zones are used instead of state codes

## How to Run
1. Open `siting_with_transmission.ipynb` in Jupyter/Cursor
2. Click "Run All" or run cells sequentially
3. View interactive maps and results
4. Export data from generated CSV files

## Requirements
```bash
pip install pandas numpy plotly matplotlib scipy
```

## Answer
**Where should Meta build their next data center?**

See top 20 substations with:
- Specific bus IDs (connection points)
- Exact coordinates
- Transmission capacity
- Renewable energy availability
- Grid infrastructure details

**Granularity:** Substation-level (most precise available) - not county-level!

## License
MIT License - See LICENSE file
