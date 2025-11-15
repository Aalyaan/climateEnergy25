# Optimal Siting Framework for Energy-Intensive Infrastructure

## Problem Statement
Determine optimal locations for Meta's next data center (and other energy-intensive infrastructure like electrolyzers, EV/H2 hubs) based on comprehensive grid analysis.

## Main Analysis
**`siting_with_transmission.ipynb`** - Complete siting analysis with transmission data

### Features:
- ✅ **82,071 substations** analyzed (substation-level granularity)
- ✅ **12,612 power plants** from eGRID (including 93 nuclear plants)
- ✅ **14-factor SLACK-AWARE scoring model** ← CRITICAL UPDATE!
- ✅ **⚡ SLACK CAPACITY analysis** ← NEW! Filters for SPARE capacity, not just total
- ✅ **2GW data center feasibility filter** ← NEW per RWE!
- ✅ **Capacity factor matching** (nuclear, solar, wind) ← NEW per RWE!
- ✅ **Cost savings analysis** ($M annual & 10-year) ← NEW per RWE!
- ✅ **Zone demand filtering** ← NEW! Avoids congested urban areas
- ✅ **Transmission capacity** (≥2GW for data center)
- ✅ **Generation capacity** (≥3GW nearby)
- ✅ **Nuclear proximity** (high capacity factor)
- ✅ **Energy costs** with $ quantification
- ✅ **Co-location potential** (solar + wind + storage)
- ✅ **Interactive visualizations** (Plotly + Matplotlib)

### SLACK-AWARE RWE-Aligned Scoring Model (14 Factors!):
```
⚡ Grid SLACK Capacity (30%): ← CRITICAL! Now using SPARE capacity
  • Transmission SLACK (18%) ← Changed from total capacity
  • Generation SLACK (12%) ← Changed from total capacity

Capacity Factor Matching (20%): ← RWE Priority
  • Effective Capacity w/ CF (12%)
  • Nuclear Proximity (8%)

Economic Factors (20%):
  • Energy Costs (10%)
  • Congestion Risk (5%)
  • Transmission Cost (5%)

🏙️ Zone Demand (10%): ← NEW! Avoids congested areas
  • Lower Demand Score (10%)

Co-Location Potential (12%):
  • Solar Potential (7%)
  • Wind Potential (5%)

Plant-Level eGRID (8%):
  • Plant Proximity (4%)
  • eGRID Renewables (2%)
  • Low Emissions (2%)
```

**⚡ KEY CHANGE: SLACK vs TOTAL Capacity**
- Previous: Scored based on total capacity (favored West Coast cities)
- Updated: Scores based on SPARE capacity after existing demand
- Result: Avoids congested urban areas, finds locations with genuine spare capacity

**Aligned with RWE advisor priorities!**
**Filters for 2GW data center feasibility!**
**Includes cost savings analysis ($M)!**

## Data Sources
1. **usa_bus_features_2016.csv** - PowerSimData transmission substations (82K+ substations)
2. **Untitled spreadsheet - PLNT23.csv** - EPA eGRID plant data (12K+ plants)

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
- **SLACK_CAPACITY_UPDATE.md** - ⚡ CRITICAL! Explains slack capacity analysis ← READ THIS FIRST!
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
