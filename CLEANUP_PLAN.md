# Cleanup Plan for Final Analysis

## ✅ KEEP - Essential Files

### Main Analysis
1. **siting_with_transmission.ipynb** - PRIMARY ANALYSIS (with transmission data)
2. **usa_bus_features_2016.csv** - Transmission substation data (82K substations)
3. **Untitled spreadsheet - PLNT23.csv** - eGRID plant data

### Documentation
4. **README.md** - Project overview
5. **GRANULARITY_SUMMARY.md** - Explains substation-level precision
6. **TRANSMISSION_DATA_SUMMARY.md** - PowerSimData capabilities
7. **MAP_VISUALIZATION_GUIDE.md** - How to use the maps
8. **LICENSE** - License file

### Latest Results (keep most recent only)
9. **meta_datacenter_top20_with_transmission_20251115_1651.csv** - Latest top 20 results
10. **all_substations_scored_20251115_1651.csv** - Latest full scoring

## ❌ DELETE - Unnecessary Files

### Duplicate/Old Results
- all_siting_scores_20251115_1603.csv (old)
- all_substations_scored_20251115_1626.csv (old)
- all_substations_scored_20251115_1629.csv (old)
- all_substations_scored_20251115_1633.csv (old)
- all_substations_scored_20251115_1635.csv (old)
- meta_datacenter_top20_with_transmission_20251115_1626.csv (old)
- meta_datacenter_top20_with_transmission_20251115_1629.csv (old)
- meta_datacenter_top20_with_transmission_20251115_1633.csv (old)
- meta_datacenter_top20_with_transmission_20251115_1635.csv (old)
- top_datacenter_locations_20251115_1603.csv (old)
- top_electrolyzer_locations_20251115_1603.csv (old)
- top_evh2_locations_20251115_1603.csv (old)

### Superseded Notebooks
- optimal_siting_analysis.ipynb (superseded by siting_with_transmission.ipynb)
- power_simulator_setup.ipynb (not needed - didn't use PowerSimData)
- modelTesting.ipynb (exploratory work, not final)

### Obsolete Documentation
- optimal_siting_analysis_notes.md (superseded)
- POWERSIMDATA_INSTALLATION_ISSUE.md (not relevant anymore)

### Unused Data
- cambium/ folder (Cambium data - not used in final analysis)
- simulations.py (empty/unused)

## Summary
- Keep: 10 essential files
- Delete: 22 unnecessary files
