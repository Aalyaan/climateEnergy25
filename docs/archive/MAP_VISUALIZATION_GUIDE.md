# 🗺️ How to See the Map Visualizations

## Why You Can't See the Map Yet:

The map code is in the notebook, but **you need to RUN the cells** to generate the visualizations!

## Steps to See the Maps:

### 1. **Open the Notebook**
   - File: `siting_with_transmission.ipynb`
   - Should already be open in Cursor

### 2. **Run All Cells**
   - Option A: Click "Run All" button at the top
   - Option B: Press `Shift + Enter` on each cell sequentially
   - Option C: Use menu: `Cell` → `Run All`

### 3. **Wait for Execution**
   - Cells will run in order
   - You'll see output appear below each cell
   - Maps will appear when cells 17 and 21 execute

## Two Maps Available:

### Map 1: Interactive Plotly Map (Cell 17)
- **Type**: Interactive web-based map
- **Features**: 
  - Hover to see details
  - Zoom and pan
  - Color-coded by score
  - Sized by transmission capacity
- **Location**: After "Interactive Map: Top 20 Locations" header

### Map 2: Static Matplotlib Map (Cell 21)
- **Type**: Static scatter plot
- **Features**:
  - Simple and reliable
  - Top 5 labeled
  - Color gradient
  - Size legend
- **Location**: After "Alternative: Simple Scatter Map" header

## Troubleshooting:

### If Plotly Map Doesn't Show:
1. Check if plotly is installed: `pip list | grep plotly`
2. Restart kernel and run again
3. Use the matplotlib backup map (Cell 21)

### If No Maps Show:
1. Make sure you're running the cells (not just viewing code)
2. Check for errors in earlier cells
3. Restart kernel: `Kernel` → `Restart`
4. Run all cells again

### If Kernel Issues:
```bash
# In terminal:
pip install plotly pandas numpy matplotlib scipy
```

Then restart notebook kernel and run all cells.

## What You Should See:

### Interactive Map (Plotly):
- USA map outline
- 20 colored dots (substations)
- Top 10 labeled with #1, #2, etc.
- Hover shows: Bus ID, coordinates, capacity, score

### Static Map (Matplotlib):
- Scatter plot with lat/lon axes
- 20 dots sized by transmission capacity
- Color gradient (red → yellow → green)
- Top 5 labeled with zone names

## Quick Test:

Run this in a notebook cell to test if plotting works:

```python
import plotly.express as px
import pandas as pd

# Simple test
df = pd.DataFrame({'lat': [40, 35, 45], 'lon': [-100, -120, -80]})
fig = px.scatter_geo(df, lat='lat', lon='lon', scope='usa')
fig.show()
```

If you see a map → Plotly works!
If not → Use the matplotlib backup.

## Expected Output:

After running all cells, you should see:
1. ✅ Top 5 detailed text output
2. ✅ Top 20 table with coordinates
3. ✅ Interactive Plotly map (or error message)
4. ✅ Static matplotlib map (backup)
5. ✅ Geographic distribution statistics

## Still Not Working?

The data and analysis are complete - you have:
- Top 20 substations with exact coordinates
- All scores and metrics
- Export CSV files

You can:
1. Use the exported CSV to create maps in other tools (Tableau, Excel, etc.)
2. Copy coordinates to Google Maps
3. Use the text output (has all the data)

The visualizations are nice-to-have, but the analysis is complete!
