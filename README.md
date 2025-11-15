# Optimal Siting Framework for Energy-Intensive Infrastructure

## Problem Statement
Determine optimal locations for Meta's next data center (and other energy-intensive infrastructure like electrolyzers, EV/H2 hubs) based on comprehensive grid analysis.

## Main Analysis
**`siting_with_transmission.ipynb`** - Complete siting analysis with transmission data

### Features:
- ✅ **82,071 substations** analyzed (substation-level granularity)
- ✅ **12,612 power plants** from eGRID integrated
- ✅ **12-factor scoring model** covering grid, economics, and co-location
- ✅ **Transmission line capacity** and infrastructure
- ✅ **Distance to actual power plants**
- ✅ **Plant-level emissions** (actual CO2 rates)
- ✅ **Plant-level renewable energy** (actual generation mix)
- ✅ **Energy costs** (retail electricity prices) ← NEW!
- ✅ **Congestion risk** analysis ← NEW!
- ✅ **Solar/wind co-location potential** ← NEW!
- ✅ **Interactive visualizations** (Plotly + Matplotlib)

### Comprehensive Scoring Model (12 Factors!):
```
Grid Infrastructure (30%):
  • Transmission Capacity (12%)
  • Generation Capacity (10%)
  • Grid Infrastructure (8%)

Plant-Level eGRID Data (25%):
  • Plant Proximity (10%)
  • eGRID Renewables (8%)
  • eGRID Emissions (7%)

Economic Factors (20%): ← NEW!
  • Energy Costs (10%)
  • Congestion Risk (5%)
  • Transmission Cost (5%)

Co-Location Potential (15%): ← NEW!
  • Solar Potential (8%)
  • Wind Potential (7%)

Sustainability (10%):
  • Plant Density (10%)
```

**Covers 8 out of 10 required parameters (80%)!**

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
- **COMPREHENSIVE_MODEL_SUMMARY.md** - LATEST! 12-factor model details ← READ THIS FIRST!
- **EGRID_INTEGRATION_SUMMARY.md** - eGRID data integration details
- **METRICS_COVERAGE.md** - What metrics are covered vs missing (80% coverage!)
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
