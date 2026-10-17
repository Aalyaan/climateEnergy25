# 🏢 DataPlace - Data Center Siting Analysis

DataPlace is an interactive web application for analyzing optimal data center locations based on transmission infrastructure, generation capacity, renewable energy availability, and economic factors.

## Features

- **Interactive Parameter Sliders**: Adjust weights for 12 different scoring factors
- **Real-time Scoring**: Calculate data center suitability scores based on your preferences
- **Interactive Maps**: Visualize top locations on an interactive US map with detailed hover information
- **Comprehensive Analysis**: Includes:
  - Grid Infrastructure (transmission capacity, generation capacity, grid infrastructure)
  - Plant-Level Data (proximity, renewable energy, emissions)
  - Economic Factors (energy costs, congestion risk, transmission costs)
  - Co-Location Potential (solar and wind potential)
  - Sustainability Metrics (plant density)

## Installation

1. **Activate your virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Navigate to the climateEnergy25 directory**:
   ```bash
   cd climateEnergy25
   ```

2. **Run Streamlit**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser**: The app will automatically open at `http://localhost:8501`

## Usage

1. **Adjust Parameters**: Use the sliders in the sidebar to adjust the weights for different scoring factors
2. **View Results**: The map will update automatically to show the top locations based on your parameters
3. **Explore Locations**: Click on locations in the map or expand the top locations panel to see detailed information
4. **Export Data**: Download the top locations as a CSV file for further analysis

## Data Sources

- **Transmission Data**: PowerSimData - 82,071 substations with transmission line capacity
- **Plant Data**: eGRID Plant Data - 12,291 power plants with generation capacity, fuel type, and emissions data

## Scoring Model

The scoring model uses 12 factors organized into 5 categories:

1. **Grid Infrastructure (30%)**
   - Transmission Capacity (12%)
   - Generation Capacity (10%)
   - Grid Infrastructure (8%)

2. **Plant-Level Data (25%)**
   - Plant Proximity (10%)
   - eGRID Renewable Energy (8%)
   - Low Emissions (7%)

3. **Economic Factors (20%)**
   - Energy Costs (10%)
   - Congestion Risk (5%)
   - Transmission Cost (5%)

4. **Co-Location Potential (15%)**
   - Solar Potential (8%)
   - Wind Potential (7%)

5. **Sustainability (10%)**
   - Plant Density (10%)

## Technical Details

- **Framework**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy, SciPy
- **Analysis Level**: Substation-level (most granular grid data available)

## Notes

- The analysis is performed at the **substation level**, providing precise coordinates for each location
- Each location represents a specific electrical substation with a unique bus ID
- Scores are calculated dynamically based on your parameter settings
- The map shows up to 50 top locations, with the top 10 labeled with rank, bus ID, and zone name

## Troubleshooting

If you encounter issues:

1. **Data files not found**: Ensure `usa_bus_features_2016.csv` and `Untitled spreadsheet - PLNT23.csv` are in the same directory as `app.py`

2. **Import errors**: Make sure all packages in `requirements.txt` are installed

3. **Performance**: The initial data loading may take a moment. Subsequent interactions should be fast due to caching.

## License

See LICENSE file for details.

