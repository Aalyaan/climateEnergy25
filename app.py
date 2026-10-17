import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Nexsite - Data Center Siting Analysis",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the master data file"""
    try:
        df = pd.read_csv('power_plant_siting_master_data.csv', low_memory=False)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

@st.cache_data
def add_state_data(df):
    """Add electricity costs, SAIDI, and SAIFI by state"""
    # Electricity costs by state (cents per kWh)
    e_price_dict = {
        'AL': 14.56, 'AK': 22.49, 'AZ': 12.96, 'AR': 10.30, 'CA': 23.40, 'CO': 12.12, 'CT': 22.82,
        'DE': 15.55, 'DC': 21.03, 'FL': 11.23, 'GA': 11.93, 'HI': 37.80, 'ID': 9.30, 'IL': 13.57,
        'IN': 13.35, 'IA': 10.55, 'KS': 11.29, 'KY': 11.76, 'LA': 10.86, 'ME': 21.34, 'MD': 15.93,
        'MA': 20.33, 'MI': 14.86, 'MN': 12.44, 'MS': 12.55, 'MO': 10.39, 'MT': 12.05, 'NE': 8.95,
        'NV': 10.13, 'NH': 19.58, 'NJ': 16.20, 'NM': 11.22, 'NY': 20.29, 'NC': 10.26, 'ND': 7.53,
        'OH': 15.54, 'OK': 8.79, 'OR': 11.10, 'PA': 14.90, 'RI': 25.02, 'SC': 11.10, 'SD': 10.91,
        'TN': 12.77, 'TX': 8.81, 'UT': 9.18, 'VT': 19.29, 'VA': 9.28, 'WA': 11.09, 'WV': 11.80,
        'WI': 12.82, 'WY': 9.99
    }
    
    # SAIDI (minutes) and SAIFI (events/year) by state
    saidi_dict = {
        'AL': 294.2, 'AK': 374.8, 'AZ': 106.8, 'AR': 911.2, 'CA': 346.6, 'CO': 99.2, 'CT': 164.6,
        'DE': 108.2, 'DC': 71.9,  'FL': 160.1,  'GA': 349.2, 'HI': 491.8, 'ID': 137.5, 'IL': 208.2,
        'IN': 455.4, 'IA': 104.9, 'KS': 283.1, 'KY': 868.2, 'LA': 584.2, 'ME': 186.3, 'MD': 166.2,
        'MA': 259.4, 'MI': 1093.6,'MN': 126.4, 'MS': 802.1, 'MO': 371.8, 'MT': 118.7, 'NE': 72.6,
        'NV': 138.7, 'NH': 645.8, 'NJ': 108.3, 'NM': 168.9, 'NY': 120,   'NC': 252,   'ND': 208.6,
        'OH': 366.2, 'OK': 896.6, 'OR': 126.9, 'PA': 252.7, 'RI': 104.6, 'SC': 167.2, 'SD': 77,
        'TN': 857.9, 'TX': 496.2, 'UT': 127.1, 'VT': 744.4, 'VA': 221.1, 'WA': 151.7, 'WV': 751.5,
        'WI': 183,   'WY': 127.0
    }
    saifi_dict = {
        'AL': 0.979, 'AK': 2.366, 'AZ': 0.817, 'AR': 1.54,  'CA': 1.086, 'CO': 0.865, 'CT': 0.655,
        'DE': 0.692, 'DC': 0.318,  'FL': 0.823, 'GA': 1.357,  'HI': 1.398, 'ID': 0.985, 'IL': 0.605,
        'IN': 0.946, 'IA': 0.709,  'KS': 0.998, 'KY': 1.167,  'LA': 1.641, 'ME': 1.979, 'MD': 0.703,
        'MA': 0.78,  'MI': 0.921,  'MN': 0.785, 'MS': 2.142,  'MO': 0.876, 'MT': 1.055, 'NE': 0.48,
        'NV': 0.745, 'NH': 0.989,  'NJ': 0.831, 'NM': 0.997,  'NY': 0.586, 'NC': 1.274, 'ND': 0.907,
        'OH': 0.918, 'OK': 1.143,  'OR': 0.751, 'PA': 0.878,  'RI': 0.667, 'SC': 1.291, 'SD': 0.894,
        'TN': 1.898, 'TX': 1.175,  'UT': 0.879, 'VT': 1.58,   'VA': 1.283, 'WA': 0.908, 'WV': 1.871,
        'WI': 0.631, 'WY': 0.77
    }
    
    df = df.copy()
    if 'Plant state abbreviation' in df.columns:
        df['Plant state abbreviation'] = df['Plant state abbreviation'].str.upper()
        df['Electricity_Cost_State_cents_per_kWh'] = df['Plant state abbreviation'].map(e_price_dict)
        df['SAIDI_hours'] = df['Plant state abbreviation'].map(saidi_dict) / 60  # Convert to hours
        df['SAIFI_interruptions'] = df['Plant state abbreviation'].map(saifi_dict)
    
    return df

# Helper functions
def norm(col):
    """Normalize column (0 to 1)"""
    v = pd.to_numeric(col.astype(str).str.replace(',', ''), errors='coerce')
    if v.isnull().all() or v.max() == v.min():
        return pd.Series(0, index=col.index)
    return (v - v.min()) / (v.max() - v.min())

def norm_inv(col):
    """Inverse normalize column (1 to 0, lower is better)"""
    v = pd.to_numeric(col.astype(str).str.replace(',', ''), errors='coerce')
    if v.isnull().all() or v.max() == v.min():
        return pd.Series(0, index=col.index)
    return (v.max() - v) / (v.max() - v.min())

def safe_numeric(col, fill=0):
    """Safely convert to numeric with fill strategy"""
    v = pd.to_numeric(col.astype(str).str.replace(',', ''), errors='coerce')
    if v.isnull().all():
        return pd.Series(fill, index=col.index)
    if fill == 'min':
        return v.fillna(v.min())
    elif fill == 'max':
        return v.fillna(v.max())
    return v.fillna(fill)

def score_plants(df, param_weights, category_weights):
    """Calculate scores based on user-defined weights"""
    out = df.copy()
    
    # 1. Proximity to RE
    re_dist = norm_inv(safe_numeric(out['bus_dist_to_nearest_renewable_plant_km']))
    re_share = safe_numeric(out['bus_renewable_share_within_100km'], fill=0)
    re_cap = norm(safe_numeric(out['bus_renewable_capacity_within_100km_MW']))
    out['P1_Proximity_RE'] = (
        param_weights['P1_Proximity_RE']['dist'] * re_dist +
        param_weights['P1_Proximity_RE']['share'] * re_share +
        param_weights['P1_Proximity_RE']['cap'] * re_cap
    )
    
    # 2. Emissions
    co2e = safe_numeric(out['Plant annual CO2 equivalent total output emission rate (lb/MWh)'], fill=0)
    co2 = safe_numeric(out['Plant annual CO2 total output emission rate (lb/MWh)'], fill=0)
    nox = safe_numeric(out['Plant annual NOx total output emission rate (lb/MWh)'], fill=0)
    so2 = safe_numeric(out['Plant annual SO2 total output emission rate (lb/MWh)'], fill=0)
    S_CO2e = norm_inv(co2e)
    S_CO2 = norm_inv(co2)
    S_NOx = norm_inv(nox)
    S_SO2 = norm_inv(so2)
    S_climate = param_weights['P2_Emissions']['CO2e'] * S_CO2e + param_weights['P2_Emissions']['CO2'] * S_CO2
    S_air = param_weights['P2_Emissions']['NOx'] * S_NOx + param_weights['P2_Emissions']['SO2'] * S_SO2
    out['P2_Emissions'] = (
        param_weights['P2_Emissions']['climate'] * S_climate +
        param_weights['P2_Emissions']['air'] * S_air
    )
    
    # 3. Capital Investment
    land = safe_numeric(out['mean_property_value_3mi'], fill='max')
    tdist = norm_inv(safe_numeric(out['bus_dist_to_nearest_renewable_plant_km']))
    tcap = norm(safe_numeric(out['bus_sum_line_capacity_MW']))
    eprice = safe_numeric(out['Electricity_Cost_State_cents_per_kWh'], fill='min')
    l_score = norm_inv(land)
    t_score = (
        param_weights['P3_Capital_Investment']['trans_dist'] * tdist +
        param_weights['P3_Capital_Investment']['trans_cap'] * tcap
    )
    e_score = norm_inv(eprice)
    out['P3_Capital_Investment'] = (
        param_weights['P3_Capital_Investment']['land'] * l_score +
        param_weights['P3_Capital_Investment']['trans'] * t_score +
        param_weights['P3_Capital_Investment']['elec_cost'] * e_score
    )
    
    # 4. Reliability
    saidi = safe_numeric(out['SAIDI_hours'], fill='max')
    saifi = safe_numeric(out['SAIFI_interruptions'], fill='max')
    degree = norm(safe_numeric(out['bus_num_incident_lines']))
    cap = norm(safe_numeric(out['bus_sum_line_capacity_MW']))
    out['P4_Reliability'] = (
        param_weights['P4_Reliability']['SAIDI'] * norm_inv(saidi) +
        param_weights['P4_Reliability']['SAIFI'] * norm_inv(saifi) +
        param_weights['P4_Reliability']['degree'] * degree +
        param_weights['P4_Reliability']['cap'] * cap
    )
    
    # 5. Water
    potable = norm(safe_numeric(out['potable_capacity_mgd_weighted']))
    i48 = safe_numeric(out['in_lower_48'], fill=1)
    out['P5_Water'] = (
        param_weights['P5_Water']['potable'] * potable +
        param_weights['P5_Water']['lower48'] * i48
    )
    
    # Calculate P6: Transmission Capacity (normalized)
    out['P6_Transmission_Capacity'] = norm(safe_numeric(out['bus_sum_line_capacity_MW']))
    
    # Final category scores (0-100)
    cat_names = list(category_weights.keys())
    for cat in cat_names:
        w = category_weights[cat]
        out[cat + '_Score'] = 100 * (
            w[0] * out['P1_Proximity_RE'] +
            w[1] * out['P2_Emissions'] +
            w[2] * out['P3_Capital_Investment'] +
            w[3] * out['P4_Reliability'] +
            w[4] * out['P5_Water'] +
            w[5] * out['P6_Transmission_Capacity']
        )
    
    # Overall score as average of the 3 categories
    out['Overall_Score'] = out[[cat + '_Score' for cat in cat_names]].mean(axis=1)
    
    return out

def select_top_with_state_diversity(df, score_col, top_n=3, penalty_factor=0.1):
    """
    Select top N locations with penalty for same-state locations.
    
    Parameters:
    - df: DataFrame with scored locations
    - score_col: Column name for the score to rank by
    - top_n: Number of top locations to select
    - penalty_factor: Penalty multiplier (0.1 = 10% reduction per duplicate state)
    
    Returns:
    - DataFrame with top N locations considering state diversity
    """
    df_sorted = df.nlargest(top_n * 5, score_col).copy()  # Get more candidates to choose from
    selected = []
    selected_states = {}
    
    for idx, row in df_sorted.iterrows():
        state = row.get('Plant state abbreviation', 'Unknown')
        adjusted_score = row[score_col]
        
        # Apply penalty if state already represented
        if state in selected_states:
            # Penalty increases with number of duplicates
            penalty = penalty_factor * selected_states[state] * row[score_col]
            adjusted_score = row[score_col] - penalty
        
        # If we haven't filled all slots yet, add this location
        if len(selected) < top_n:
            row_dict = row.to_dict()
            row_dict[score_col + '_adjusted'] = adjusted_score
            selected.append(row_dict)
            
            # Update state count
            if state not in selected_states:
                selected_states[state] = 0
            selected_states[state] += 1
        else:
            # We have top_n locations, check if this one is better than the worst
            # Find the minimum adjusted score in selected
            min_adjusted = min([s.get(score_col + '_adjusted', s[score_col]) for s in selected])
            
            if adjusted_score > min_adjusted:
                # Find and remove the location with minimum adjusted score
                min_idx = min(range(len(selected)), 
                             key=lambda i: selected[i].get(score_col + '_adjusted', selected[i][score_col]))
                removed = selected.pop(min_idx)
                removed_state = removed.get('Plant state abbreviation', 'Unknown')
                
                # Update state count
                if removed_state in selected_states:
                    selected_states[removed_state] -= 1
                    if selected_states[removed_state] == 0:
                        del selected_states[removed_state]
                
                # Add current location
                row_dict = row.to_dict()
                row_dict[score_col + '_adjusted'] = adjusted_score
                selected.append(row_dict)
                
                # Update state count
                if state not in selected_states:
                    selected_states[state] = 0
                selected_states[state] += 1
    
    # Convert back to DataFrame and sort by original score
    result_df = pd.DataFrame(selected)
    if len(result_df) > 0:
        result_df = result_df.nlargest(top_n, score_col)
    
    return result_df

def create_map(df_scored, top3_per_category, top5_overall):
    """Create interactive map with top locations"""
    # Combine all locations to show
    all_locations_list = []
    
    # Add top 3 from each category
    for cat_name, top_df in top3_per_category.items():
        top_df_copy = top_df.copy()
        top_df_copy['Category'] = cat_name
        all_locations_list.append(top_df_copy)
    
    # Add top 5 overall
    top5_copy = top5_overall.copy()
    top5_copy['Category'] = 'Top 5 Overall'
    all_locations_list.append(top5_copy)
    
    # Combine and remove duplicates (keep first occurrence)
    all_locations = pd.concat(all_locations_list)
    all_locations = all_locations.drop_duplicates(
        subset=['Plant county name', 'Plant latitude', 'Plant longitude'],
        keep='first'
    )
    
    # Update category to show all categories a plant belongs to
    # First, collect all categories for each unique plant
    plant_categories = {}
    for cat_name, top_df in top3_per_category.items():
        for idx, row in top_df.iterrows():
            plant_key = (row.get('Plant county name', 'Unknown'), row['Plant latitude'], row['Plant longitude'])
            if plant_key not in plant_categories:
                plant_categories[plant_key] = set()
            plant_categories[plant_key].add(cat_name)
    
    # Add top 5 overall
    for idx, row in top5_overall.iterrows():
        plant_key = (row.get('Plant county name', 'Unknown'), row['Plant latitude'], row['Plant longitude'])
        if plant_key not in plant_categories:
            plant_categories[plant_key] = set()
        plant_categories[plant_key].add('Top 5 Overall')
    
    # Update the Category column
    all_locations['Category'] = all_locations.apply(
        lambda row: ', '.join(sorted(plant_categories.get(
            (row.get('Plant county name', 'Unknown'), row['Plant latitude'], row['Plant longitude']), 
            [row['Category']]
        ))),
        axis=1
    )
    
    # Create a color for each unique category combination
    unique_categories = sorted(all_locations['Category'].unique())
    colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181', '#FFD93D', '#6BCF7F', '#A8E6CF', '#FF8B94']
    color_map = {cat: colors[i % len(colors)] for i, cat in enumerate(unique_categories)}
    
    # Create map
    fig = px.scatter_geo(
        all_locations,
        lat='Plant latitude',
        lon='Plant longitude',
        size='Overall_Score',
        color='Category',
        hover_name='Plant county name',
        hover_data={
            'Plant county name': True,
            'Plant state abbreviation': True,
            'Plant name': True,
            'Lowest Cost_Score': ':.1f',
            'Lowest Emissions_Score': ':.1f',
            'Highest Reliability_Score': ':.1f',
            'Overall_Score': ':.1f',
            'Plant latitude': ':.4f',
            'Plant longitude': ':.4f',
            'Category': False
        },
        color_discrete_map=color_map,
        # title='🏢 Nexsite - Top Potential Data Center Locations<br><sub>Interactive Multi-Criteria Siting Analysis</sub>',
        title='Nexsite - Top Potential Data Center Locations<br><sub>Interactive Multi-Criteria Siting Analysis</sub>',
        scope='usa',
        height=800,
        size_max=30
    )
    
    # Add labels for top locations
    for idx, row in all_locations.iterrows():
        county_name = row.get('Plant county name', 'Unknown')
        if pd.notna(county_name):
            county_name = str(county_name)[:20] + '...' if len(str(county_name)) > 20 else str(county_name)
        else:
            county_name = 'Unknown'
        label_text = f"{county_name}<br>{row['Plant state abbreviation']}"
        
        fig.add_trace(go.Scattergeo(
            lon=[row['Plant longitude']],
            lat=[row['Plant latitude']],
            text=label_text,
            mode='text',
            textfont=dict(size=9, color='black', family='Arial'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            projection_scale=1.1
        ),
        font=dict(size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=9),
            itemsizing='constant',
            itemwidth=30
        ),
        margin=dict(l=0, r=0, t=80, b=100),
        height=800
    )
    
    return fig

def estimate_total_cost(row, dc_size_mw=2000):
    """
    Estimate total cost of ownership for a data center location.
    
    Parameters:
    - row: DataFrame row with location data
    - dc_size_mw: Assumed data center size in MW (default 2000MW = 2GW data center)
    
    Returns:
    - Dictionary with cost breakdown and total estimates
    """
    # Assumptions for cost estimation
    # Scale land needed with data center size (roughly 50 acres per 100MW)
    land_acres_needed = (dc_size_mw / 100) * 50  # Scale proportionally
    electricity_utilization = 0.85  # 85% utilization factor
    hours_per_year = 8760
    # Transmission line costs: $1-3M per mile for high-voltage lines
    # For 2GW, typically need 500kV+ lines, cost ~$2M per mile = ~$1.24M per km
    # Base cost scales with capacity and distance
    transmission_base_cost_per_km = 1240000  # $1.24M per km base cost
    transmission_cost_per_mw_per_km = 200000  # Additional $200k per MW per km for capacity
    land_cost_per_acre_multiplier = 0.1  # Assume 10% of property value per acre (rough estimate)
    
    costs = {}
    
    # 1. Land/Property Costs
    property_value = row.get('mean_property_value_3mi', 0)
    if pd.notna(property_value) and property_value > 0:
        # Estimate land cost (property value is average in 3mi radius, use as proxy)
        estimated_land_cost = property_value * land_cost_per_acre_multiplier * land_acres_needed
        costs['Land Acquisition'] = estimated_land_cost
    else:
        costs['Land Acquisition'] = 5000000  # Default $5M if no data
    
    # 2. Annual Electricity Costs
    electricity_rate = row.get('Electricity_Cost_State_cents_per_kWh', 10.0) / 100  # Convert cents to dollars
    annual_energy_mwh = dc_size_mw * electricity_utilization * hours_per_year / 1000
    annual_electricity_cost = annual_energy_mwh * electricity_rate * 1000  # Convert back to kWh
    costs['Annual Electricity'] = annual_electricity_cost
    
    # 3. Transmission Line Construction Costs (one-time)
    # This is a major cost component - building new transmission lines for 2GW can cost $500M-$2B+
    transmission_distance = row.get('bus_dist_to_nearest_renewable_plant_km', 10)
    transmission_capacity = row.get('bus_sum_line_capacity_MW', 0)
    
    # Base transmission line cost (right-of-way, towers, conductors, substations)
    base_line_cost = transmission_distance * transmission_base_cost_per_km
    
    # Capacity-dependent costs (larger capacity requires more expensive equipment)
    capacity_cost = transmission_distance * transmission_cost_per_mw_per_km * dc_size_mw
    
    if transmission_capacity > 0:
        # If existing transmission capacity is sufficient, we may only need upgrades/connections
        if transmission_capacity >= dc_size_mw:
            # Existing capacity sufficient - only need connection/upgrade costs (30% of new build)
            connection_cost = (base_line_cost + capacity_cost) * 0.3
            costs['Transmission Line Construction'] = connection_cost
            costs['Transmission Cost Type'] = 'Upgrade/Connection'
        elif transmission_capacity >= dc_size_mw * 0.5:
            # Partial capacity exists - need significant upgrades (60% of new build)
            connection_cost = (base_line_cost + capacity_cost) * 0.6
            costs['Transmission Line Construction'] = connection_cost
            costs['Transmission Cost Type'] = 'Major Upgrade'
        else:
            # Insufficient capacity - need new transmission lines (full cost)
            connection_cost = base_line_cost + capacity_cost
            costs['Transmission Line Construction'] = connection_cost
            costs['Transmission Cost Type'] = 'New Construction'
    else:
        # No existing capacity - full new transmission line construction
        connection_cost = base_line_cost + capacity_cost
        costs['Transmission Line Construction'] = connection_cost
        costs['Transmission Cost Type'] = 'New Construction'
    
    # Additional transmission infrastructure costs (substations, switchyards, etc.)
    # For 2GW, typically need multiple substations: ~$50-100M each
    substation_cost = 75000000  # $75M per major substation
    num_substations = max(1, int(dc_size_mw / 1000))  # One per GW, minimum 1
    costs['Substation/Switchyard'] = substation_cost * num_substations
    
    total_transmission_cost = costs['Transmission Line Construction'] + costs['Substation/Switchyard']
    costs['Transmission Connection (One-time)'] = total_transmission_cost
    
    # 4. Water Costs (annual, if available)
    potable_capacity = row.get('potable_capacity_mgd_weighted', 0)
    if potable_capacity > 0:
        # Typical data center uses ~1-3 MGD, estimate $5 per 1000 gallons
        water_usage_mgd = min(3.0, potable_capacity * 0.5)  # Use 50% of available capacity
        annual_water_cost = water_usage_mgd * 365 * 1000 * 5  # $5 per 1000 gallons
        costs['Annual Water'] = annual_water_cost
    else:
        costs['Annual Water'] = 500000  # Default $500k/year
    
    # 5. Calculate totals
    one_time_costs = costs.get('Land Acquisition', 0) + costs.get('Transmission Connection (One-time)', 0)
    annual_operating_costs = costs.get('Annual Electricity', 0) + costs.get('Annual Water', 0)
    
    # 10-year TCO (simplified, no discounting)
    ten_year_tco = one_time_costs + (annual_operating_costs * 10)
    
    costs['Total One-Time Costs'] = one_time_costs
    costs['Total Annual Operating Costs'] = annual_operating_costs
    costs['10-Year TCO'] = ten_year_tco
    
    return costs

def get_plant_details(row):
    """Get detailed information about a plant"""
    details = {
        'County': row.get('Plant county name', 'N/A'),
        'Plant Name': row.get('Plant name', 'N/A'),
        'State': row.get('Plant state abbreviation', 'N/A'),
        'Coordinates': f"{row.get('Plant latitude', 0):.4f}°N, {row.get('Plant longitude', 0):.4f}°W",
        'Fuel Type': row.get('Plant primary fuel category', 'N/A'),
        'Capacity': f"{row.get('Plant nameplate capacity (MW)', 0):,.0f} MW",
        'Scores': {
            'Lowest Cost': f"{row.get('Lowest Cost_Score', 0):.1f}/100",
            'Lowest Emissions': f"{row.get('Lowest Emissions_Score', 0):.1f}/100",
            'Highest Reliability': f"{row.get('Highest Reliability_Score', 0):.1f}/100",
            'Overall': f"{row.get('Overall_Score', 0):.1f}/100"
        },
        'Parameters': {
            'Proximity to RE': f"{row.get('P1_Proximity_RE', 0):.3f}",
            'Emissions': f"{row.get('P2_Emissions', 0):.3f}",
            'Capital Investment': f"{row.get('P3_Capital_Investment', 0):.3f}",
            'Reliability': f"{row.get('P4_Reliability', 0):.3f}",
            'Water': f"{row.get('P5_Water', 0):.3f}",
            'Transmission Capacity': f"{row.get('P6_Transmission_Capacity', 0):.3f}"
        },
        'Transmission': {
            'Line Capacity': f"{row.get('bus_sum_line_capacity_MW', 0):,.0f} MW",
            'Number of Lines': f"{row.get('bus_num_incident_lines', 0):.0f}",
            'Distance to RE Plant': f"{row.get('bus_dist_to_nearest_renewable_plant_km', 0):.1f} km"
        },
        'Economics': {
            'Electricity Cost': f"{row.get('Electricity_Cost_State_cents_per_kWh', 0):.2f} ¢/kWh",
            'Property Value (3mi)': f"${row.get('mean_property_value_3mi', 0):,.0f}" if pd.notna(row.get('mean_property_value_3mi')) else 'N/A'
        },
        'Cost Estimates': estimate_total_cost(row, dc_size_mw=2000)
    }
    return details

# Main app
def main():
    # Header
    st.markdown('<div class="main-header">🏢 Nexsite</div>', unsafe_allow_html=True)
    # st.markdown('<div class="main-header">Nexsite</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Data Center Placement Multi-Criteria Siting Analysis<br><em style="font-size: 1.0rem; color: #888;">Find what\'s next.</em></div>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner("Loading data... This may take a moment."):
        df = load_data()
        df = add_state_data(df)
    
    st.success(f"✓ Loaded {len(df):,} power plants")
    
    # Sidebar for category weights only
    st.sidebar.header("📊 Category Weights")
    st.sidebar.markdown("Weight of each parameter in each category:")
    
    st.sidebar.subheader("Lowest Cost")
    lc_p1 = st.sidebar.slider("P1 (RE Proximity)", 0.0, 1.0, 0.10, 0.05)
    lc_p2 = st.sidebar.slider("P2 (Emissions)", 0.0, 1.0, 0.00, 0.05)
    lc_p3 = st.sidebar.slider("P3 (Capital)", 0.0, 1.0, 0.60, 0.05)
    lc_p4 = st.sidebar.slider("P4 (Reliability)", 0.0, 1.0, 0.10, 0.05)
    lc_p5 = st.sidebar.slider("P5 (Water)", 0.0, 1.0, 0.20, 0.05)
    lc_p6 = st.sidebar.slider("P6 (Transmission Capacity)", 0.0, 1.0, 0.00, 0.05)
    lc_total = lc_p1 + lc_p2 + lc_p3 + lc_p4 + lc_p5 + lc_p6
    if lc_total > 0:
        lc_p1, lc_p2, lc_p3, lc_p4, lc_p5, lc_p6 = lc_p1/lc_total, lc_p2/lc_total, lc_p3/lc_total, lc_p4/lc_total, lc_p5/lc_total, lc_p6/lc_total
    
    st.sidebar.subheader("Lowest Emissions")
    le_p1 = st.sidebar.slider("P1 (RE Proximity)", 0.0, 1.0, 0.20, 0.05, key='le_p1')
    le_p2 = st.sidebar.slider("P2 (Emissions)", 0.0, 1.0, 0.60, 0.05, key='le_p2')
    le_p3 = st.sidebar.slider("P3 (Capital)", 0.0, 1.0, 0.00, 0.05, key='le_p3')
    le_p4 = st.sidebar.slider("P4 (Reliability)", 0.0, 1.0, 0.10, 0.05, key='le_p4')
    le_p5 = st.sidebar.slider("P5 (Water)", 0.0, 1.0, 0.10, 0.05, key='le_p5')
    le_p6 = st.sidebar.slider("P6 (Transmission Capacity)", 0.0, 1.0, 0.00, 0.05, key='le_p6')
    le_total = le_p1 + le_p2 + le_p3 + le_p4 + le_p5 + le_p6
    if le_total > 0:
        le_p1, le_p2, le_p3, le_p4, le_p5, le_p6 = le_p1/le_total, le_p2/le_total, le_p3/le_total, le_p4/le_total, le_p5/le_total, le_p6/le_total
    
    st.sidebar.subheader("Highest Reliability")
    hr_p1 = st.sidebar.slider("P1 (RE Proximity)", 0.0, 1.0, 0.20, 0.05, key='hr_p1')
    hr_p2 = st.sidebar.slider("P2 (Emissions)", 0.0, 1.0, 0.00, 0.05, key='hr_p2')
    hr_p3 = st.sidebar.slider("P3 (Capital)", 0.0, 1.0, 0.10, 0.05, key='hr_p3')
    hr_p4 = st.sidebar.slider("P4 (Reliability)", 0.0, 1.0, 0.60, 0.05, key='hr_p4')
    hr_p5 = st.sidebar.slider("P5 (Water)", 0.0, 1.0, 0.10, 0.05, key='hr_p5')
    hr_p6 = st.sidebar.slider("P6 (Transmission Capacity)", 0.0, 1.0, 0.00, 0.05, key='hr_p6')
    hr_total = hr_p1 + hr_p2 + hr_p3 + hr_p4 + hr_p5 + hr_p6
    if hr_total > 0:
        hr_p1, hr_p2, hr_p3, hr_p4, hr_p5, hr_p6 = hr_p1/hr_total, hr_p2/hr_total, hr_p3/hr_total, hr_p4/hr_total, hr_p5/hr_total, hr_p6/hr_total
    
    # Build weight dictionaries with default values for P1-P5
    # Default P1 weights
    p1_dist, p1_share, p1_cap = 0.40, 0.35, 0.25
    
    # Default P2 weights
    p2_co2e, p2_co2 = 0.70, 0.30
    p2_nox, p2_so2 = 0.50, 0.50
    p2_climate, p2_air = 0.75, 0.25
    
    # Default P3 weights
    p3_land, p3_trans, p3_elec = 0.40, 0.40, 0.20
    p3_trans_dist, p3_trans_cap = 0.50, 0.50
    
    # Default P4 weights
    p4_saidi, p4_saifi, p4_degree, p4_cap = 0.35, 0.35, 0.15, 0.15
    
    # Default P5 weights
    p5_potable, p5_lower48 = 0.90, 0.10
    
    param_weights = {
        'P1_Proximity_RE': {'dist': p1_dist, 'share': p1_share, 'cap': p1_cap},
        'P2_Emissions': {
            'CO2e': p2_co2e, 'CO2': p2_co2, 'NOx': p2_nox, 'SO2': p2_so2,
            'climate': p2_climate, 'air': p2_air
        },
        'P3_Capital_Investment': {
            'land': p3_land, 'trans': p3_trans, 'elec_cost': p3_elec,
            'trans_dist': p3_trans_dist, 'trans_cap': p3_trans_cap
        },
        'P4_Reliability': {'SAIDI': p4_saidi, 'SAIFI': p4_saifi, 'degree': p4_degree, 'cap': p4_cap},
        'P5_Water': {'potable': p5_potable, 'lower48': p5_lower48}
    }
    
    category_weights = {
        'Lowest Cost': [lc_p1, lc_p2, lc_p3, lc_p4, lc_p5, lc_p6],
        'Lowest Emissions': [le_p1, le_p2, le_p3, le_p4, le_p5, le_p6],
        'Highest Reliability': [hr_p1, hr_p2, hr_p3, hr_p4, hr_p5, hr_p6]
    }
    
    # State diversity penalty is fixed at 0.5
    penalty_factor = 0.5
    
    # Calculate scores
    with st.spinner("Calculating scores..."):
        df_scored = score_plants(df, param_weights, category_weights)
    
    # Calculate median costs for comparison
    with st.spinner("Calculating cost estimates..."):
        all_costs = []
        for idx, row in df_scored.iterrows():
            costs = estimate_total_cost(row, dc_size_mw=2000)
            all_costs.append(costs.get('10-Year TCO', 0))
        
        median_tco = 0
        if all_costs and len(all_costs) > 0:
            median_tco = float(np.median(all_costs))
            st.session_state['median_tco'] = median_tco  # Store in session state for access
        else:
            st.session_state['median_tco'] = 0
    
    # Retrieve median from session state if available
    median_tco = st.session_state.get('median_tco', 0)
    
    # Get top locations with state diversity penalty
    top3_cost = select_top_with_state_diversity(df_scored, 'Lowest Cost_Score', top_n=3, penalty_factor=penalty_factor)
    top3_emissions = select_top_with_state_diversity(df_scored, 'Lowest Emissions_Score', top_n=3, penalty_factor=penalty_factor)
    top3_reliability = select_top_with_state_diversity(df_scored, 'Highest Reliability_Score', top_n=3, penalty_factor=penalty_factor)
    top5_overall = select_top_with_state_diversity(df_scored, 'Overall_Score', top_n=5, penalty_factor=penalty_factor)
    
    top3_per_category = {
        'Lowest Cost': top3_cost,
        'Lowest Emissions': top3_emissions,
        'Highest Reliability': top3_reliability
    }
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # st.header("🗺️ Interactive Map")
        st.header("Interactive Map")

        fig = create_map(df_scored, top3_per_category, top5_overall)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # st.header("📊 Top Locations")
        st.header("Top Locations")
        
        # Top 3 per category
        for cat_name, top_df in top3_per_category.items():
            with st.expander(f"🏆 Top 3: {cat_name}", expanded=False):
                for idx, (i, row) in enumerate(top_df.iterrows(), 1):
                    county_name = row.get('Plant county name', 'Unknown')
                    st.write(f"**#{idx}** {county_name}")
                    st.write(f"Score: {row[cat_name + '_Score']:.1f}/100")
                    st.write(f"State: {row['Plant state abbreviation']}")
                    # Show cost estimate for Lowest Cost category
                    if cat_name == 'Lowest Cost':
                        cost_est = estimate_total_cost(row, dc_size_mw=2000)
                        location_tco = cost_est.get('10-Year TCO', 0)
                        st.write(f"**Est. 10-Year TCO:** ${location_tco:,.0f}")
                        if median_tco > 0:
                            savings = median_tco - location_tco
                            savings_pct = (savings / median_tco * 100) if median_tco > 0 else 0
                            savings_color = "green" if savings > 0 else "red"
                            st.markdown(f"**vs. Median:** <span style='color: {savings_color}'>{'$' + f'{savings:+,.0f}'} ({savings_pct:+.1f}%)</span>", unsafe_allow_html=True)
                            st.caption(f"Median TCO: ${median_tco:,.0f}")
                    if st.button(f"View Details", key=f"details_{cat_name}_{i}"):
                        st.session_state['selected_plant'] = i
                    st.write("---")
        
        # Top 5 Overall
        with st.expander("🌟 Top 5 Overall", expanded=True):
            for idx, (i, row) in enumerate(top5_overall.iterrows(), 1):
                county_name = row.get('Plant county name', 'Unknown')
                st.write(f"**#{idx}** {county_name}")
                st.write(f"Overall Score: {row['Overall_Score']:.1f}/100")
                st.write(f"State: {row['Plant state abbreviation']}")
                # Show cost estimate
                cost_est = estimate_total_cost(row, dc_size_mw=2000)
                location_tco = cost_est.get('10-Year TCO', 0)
                st.write(f"**Est. 10-Year TCO:** ${location_tco:,.0f}")
                if median_tco > 0:
                    savings = median_tco - location_tco
                    savings_pct = (savings / median_tco * 100) if median_tco > 0 else 0
                    savings_color = "green" if savings > 0 else "red"
                    st.markdown(f"**vs. Median:** <span style='color: {savings_color}'>{'$' + f'{savings:+,.0f}'} ({savings_pct:+.1f}%)</span>", unsafe_allow_html=True)
                    st.caption(f"Median TCO: ${median_tco:,.0f}")
                if st.button(f"View Details", key=f"details_overall_{i}"):
                    st.session_state['selected_plant'] = i
                st.write("---")
    
    # Plant details section
    if 'selected_plant' in st.session_state and st.session_state['selected_plant'] is not None:
        plant_idx = st.session_state['selected_plant']
        if plant_idx in df_scored.index:
            st.header("📋 Plant Details")
            plant_row = df_scored.loc[plant_idx]
            details = get_plant_details(plant_row)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Basic Info")
                st.write(f"**County:** {details['County']}")
                st.write(f"**State:** {details['State']}")
                st.write(f"**Plant Name:** {details['Plant Name']}")
                st.write(f"**Coordinates:** {details['Coordinates']}")
                st.write(f"**Fuel Type:** {details['Fuel Type']}")
                st.write(f"**Capacity:** {details['Capacity']}")
            
            with col2:
                st.subheader("Scores")
                for k, v in details['Scores'].items():
                    st.write(f"**{k}:** {v}")
            
            with col3:
                st.subheader("Parameters")
                for k, v in details['Parameters'].items():
                    st.write(f"**{k}:** {v}")
            
            st.subheader("Additional Information")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Transmission:**")
                for k, v in details['Transmission'].items():
                    st.write(f"- {k}: {v}")
            with col2:
                st.write("**Economics:**")
                for k, v in details['Economics'].items():
                    st.write(f"- {k}: {v}")
            
            st.subheader("💰 Cost Estimates (2GW Data Center)")
            cost_col1, cost_col2, cost_col3 = st.columns(3)
            with cost_col1:
                st.write("**One-Time Costs:**")
                st.write(f"- Land: ${details['Cost Estimates'].get('Land Acquisition', 0):,.0f}")
                trans_line = details['Cost Estimates'].get('Transmission Line Construction', 0)
                substation = details['Cost Estimates'].get('Substation/Switchyard', 0)
                trans_type = details['Cost Estimates'].get('Transmission Cost Type', 'N/A')
                st.write(f"- Transmission Lines: ${trans_line:,.0f}")
                st.caption(f"  ({trans_type})")
                st.write(f"- Substations: ${substation:,.0f}")
                st.write(f"- **Total Transmission:** ${details['Cost Estimates'].get('Transmission Connection (One-time)', 0):,.0f}")
                st.write(f"- **Total One-Time:** ${details['Cost Estimates'].get('Total One-Time Costs', 0):,.0f}")
            with cost_col2:
                st.write("**Annual Operating Costs:**")
                st.write(f"- Electricity: ${details['Cost Estimates'].get('Annual Electricity', 0):,.0f}")
                st.write(f"- Water: ${details['Cost Estimates'].get('Annual Water', 0):,.0f}")
                st.write(f"- **Total:** ${details['Cost Estimates'].get('Total Annual Operating Costs', 0):,.0f}")
            with cost_col3:
                st.write("**Total Cost of Ownership:**")
                location_tco = details['Cost Estimates'].get('10-Year TCO', 0)
                st.write(f"- **10-Year TCO:** ${location_tco:,.0f}")
                if median_tco > 0:
                    savings = median_tco - location_tco
                    savings_pct = (savings / median_tco * 100) if median_tco > 0 else 0
                    st.write(f"- **Median TCO:** ${median_tco:,.0f}")
                    st.write(f"- **vs. Median:** ${savings:+,.0f} ({savings_pct:+.1f}%)")
            st.caption("*Estimates assume 2GW (2000MW) facility, 85% utilization")
            
            if st.button("Close Details"):
                st.session_state['selected_plant'] = None
                st.rerun()
    
    # Statistics
    st.header("📈 Analysis Statistics")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Plants", f"{len(df_scored):,}")
    with col2:
        st.metric("Avg Overall Score", f"{df_scored['Overall_Score'].mean():.1f}")
    with col3:
        st.metric("Max Overall Score", f"{df_scored['Overall_Score'].max():.1f}")
    with col4:
        st.metric("Min Overall Score", f"{df_scored['Overall_Score'].min():.1f}")
    with col5:
        if median_tco > 0:
            st.metric("Median 10-Year TCO (2GW)", f"${median_tco:,.0f}")
        else:
            st.metric("Median 10-Year TCO (2GW)", "Calculating...")
    
    # Export
    st.header("💾 Export Results")
    export_df = pd.concat([
        top3_cost[['Plant county name', 'Plant name', 'Plant state abbreviation', 'Plant latitude', 'Plant longitude', 'Lowest Cost_Score']],
        top3_emissions[['Plant county name', 'Plant name', 'Plant state abbreviation', 'Plant latitude', 'Plant longitude', 'Lowest Emissions_Score']],
        top3_reliability[['Plant county name', 'Plant name', 'Plant state abbreviation', 'Plant latitude', 'Plant longitude', 'Highest Reliability_Score']],
        top5_overall[['Plant county name', 'Plant name', 'Plant state abbreviation', 'Plant latitude', 'Plant longitude', 'Overall_Score']]
    ]).drop_duplicates()
    
    csv = export_df.to_csv(index=False)
    st.download_button(
        label="Download Top Locations CSV",
        data=csv,
        file_name=f"Nexsite_top_locations_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
