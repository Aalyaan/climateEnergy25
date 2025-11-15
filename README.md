# Optimal Siting Framework for Energy-Intensive Infrastructure

## Problem Statement
Determine optimal locations for Meta's next data center (and other energy-intensive infrastructure like electrolyzers, EV/H2 hubs) based on comprehensive grid analysis.

## Main Analysis
**`siting_with_transmission.ipynb`** - Complete siting analysis with transmission data

### Features:
- ✅ **82,071 substations** analyzed (substation-level granularity)
- ✅ **Transmission line capacity** and infrastructure
- ✅ **Generation capacity** within 100km
- ✅ **Renewable energy** availability
- ✅ **Emissions** analysis (CO2 intensity)
- ✅ **Multi-criteria scoring** model
- ✅ **Interactive visualizations** (Plotly + Matplotlib)

### Scoring Model:
```
Data Center Score = 
  Transmission Capacity (25%) +
  Generation Capacity (20%) +
  Renewable Energy (20%) +
  Low Emissions (20%) +
  Grid Infrastructure (15%)
```

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
- **GRANULARITY_SUMMARY.md** - Explains substation-level precision
- **TRANSMISSION_DATA_SUMMARY.md** - PowerSimData capabilities
- **MAP_VISUALIZATION_GUIDE.md** - How to use visualizations

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
