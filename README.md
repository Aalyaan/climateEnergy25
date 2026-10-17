# Nexsite: Data Center Siting on the US Grid

Built at the MIT Energy and Climate Hackathon 2025 (November 14 to 16) by Aalyaan and Snigdha.

**Prompt:** where do we place a data center on the grid?

Nexsite scores 12,612 US power plant sites on renewable access, emissions, capital
cost, grid reliability, water, and transmission capacity, then ranks the best
locations for three goals: lowest cost, lowest emissions, and highest reliability.
An interactive Streamlit app lets you change the weights and see the map update.

## How it works

1. **Build the dataset** (`notebooks/01_build_master_dataset.ipynb`). Each eGRID power
   plant is matched to its nearest grid substation from PowerSimData (haversine
   distance). Property values (mean within 3 miles) and water capacity are attached.
   Output: `data/processed/power_plant_siting_master_data.csv`.
2. **Score** (`notebooks/02_scoring_model.ipynb`, `app.py`). Six parameters, each 0 to 1:
   P1 renewable proximity, P2 emissions, P3 capital investment, P4 reliability,
   P5 water, P6 transmission capacity. Three category scores weight these parameters,
   and a state diversity penalty keeps the top picks from clustering in one state.
   Full formulas: [docs/algorithm.md](docs/algorithm.md).
3. **Explore** (`app.py`). Adjust weights, view the top 3 per category and top 5
   overall on a map, and see a rough 10-year cost estimate for a 2 GW facility.

An earlier substation-level version of the model (12, then 16 factors, including
slack capacity and zoning) lives in `notebooks/substation_siting_model.ipynb`, with
its write-ups in `docs/archive/`.

## Data

| File | Source |
| --- | --- |
| `data/raw/egrid2023_plants.csv` | EPA eGRID plant file (PLNT23) |
| `data/raw/usa_bus_features_2016.csv` | Substation features exported from Breakthrough Energy's PowerSimData USA grid |
| `data/raw/synthetic_us_water_latlon_grid.csv` | **Synthetic.** Generated placeholder for water availability |
| `data/raw/synthetic_regrid_parcel_grid.csv` | **Synthetic.** Generated placeholder for land parcels and zoning |
| `data/raw/places_fmv_all.tif` | Property value raster, not included (125 MB) |
| State tables in `app.py` | Electricity price (cents/kWh), SAIDI and SAIFI by state |

**Limitations.** The water (P5) and zoning inputs are synthetic placeholders made
during the hackathon, so any score that uses them is illustrative, not real.
Electricity price and reliability are state averages, not site-level values.
Cost estimates are back-of-envelope.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

To re-run the notebooks: `pip install -r requirements-notebooks.txt`. The raster is needed
for notebook 01, and PowerSimData only for the scenario export cells at the end of
the substation notebook.

## License

MIT
