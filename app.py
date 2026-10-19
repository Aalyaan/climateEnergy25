import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'data', 'processed', 'power_plant_siting_master_data.csv')

# Page configuration
st.set_page_config(
    page_title="Nexsite: Data Center Siting",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

TEXT = '#E6EAED'
MUTED = '#8B96A0'
SURFACE = '#1A2129'
RULE = '#2A333C'
GOAL_COLORS = {
    'Lowest Cost': '#E0A93B',
    'Lowest Emissions': '#4FB37A',
    'Highest Reliability': '#5B8DEF',
}
GOAL_SHORT = {'Lowest Cost': 'Cost', 'Lowest Emissions': 'Emissions', 'Highest Reliability': 'Reliability'}
FACTORS = [
    ('P1_Proximity_RE', 'Renewables nearby'),
    ('P2_Emissions', 'Low emissions'),
    ('P3_Capital_Investment', 'Low capital cost'),
    ('P4_Reliability', 'Grid reliability'),
    ('P5_Water', 'Water (synthetic data)'),
    ('P6_Transmission_Capacity', 'Transmission capacity'),
]
DC_SIZE_MW = 2000

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&display=swap');

    .stApp {{ font-family: 'Public Sans', sans-serif; }}
    h1, h2, h3, h4 {{ font-family: 'Public Sans', sans-serif !important; }}
    .block-container {{ padding-top: 2.5rem; max-width: 1320px; }}

    [data-testid="stAppDeployButton"], [data-testid="stMainMenu"], footer {{ display: none !important; }}
    header[data-testid="stHeader"] {{ background: transparent; }}

    .topbar {{ display: flex; justify-content: space-between; align-items: center; gap: 1rem;
               padding-bottom: 1rem; margin-bottom: 1.75rem; border-bottom: 1px solid {RULE}; }}
    .brand {{ display: flex; align-items: center; gap: 0.6rem; }}
    .brand .word {{ font-weight: 700; font-size: 1.15rem; color: {TEXT}; }}
    .brand .tag {{ color: {MUTED}; font-size: 0.9rem; }}
    .pill {{ border: 1px solid {RULE}; border-radius: 999px; padding: 0.25rem 0.75rem;
             color: {MUTED}; font-size: 0.82rem; font-variant-numeric: tabular-nums; white-space: nowrap; }}
    .pill b {{ color: {TEXT}; font-weight: 600; }}
    .page-title {{ font-weight: 700; font-size: 1.9rem; line-height: 1.2; color: {TEXT}; margin: 0; }}
    .page-sub {{ color: {MUTED}; font-size: 1rem; margin: 0.4rem 0 1.5rem 0; max-width: 64ch; }}

    .panel {{ background: {SURFACE}; border: 1px solid {RULE}; border-radius: 12px;
              padding: 1.25rem 1.4rem; margin-bottom: 1rem; }}
    .hero {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(7.5rem, 1fr)); gap: 1.25rem 1.5rem;
             align-items: end; }}
    .hero .lead {{ grid-column: span 2; min-width: 0; }}
    .eyebrow {{ color: {MUTED}; font-size: 0.82rem; margin-bottom: 0.3rem; }}
    .hero .place {{ font-weight: 700; font-size: 1.6rem; color: {TEXT}; line-height: 1.15; }}
    .hero .near {{ color: {MUTED}; font-size: 0.9rem; margin-top: 0.2rem; white-space: nowrap;
                   overflow: hidden; text-overflow: ellipsis; }}
    .stat .v {{ font-weight: 700; font-size: 1.45rem; color: {TEXT}; font-variant-numeric: tabular-nums; }}

    div[data-testid="stVerticalBlock"]:has(> div[data-testid="stElementContainer"] .panel-anchor) {{
        background: {SURFACE}; border-color: {RULE} !important; border-radius: 12px; }}

    .section-title {{ font-weight: 600; font-size: 1rem; color: {TEXT}; margin: 0 0 0.9rem 0; }}

    .rank-table {{ display: grid; grid-template-columns: 1.5rem minmax(0, 1fr) repeat(3, 5.5rem) 4rem;
                   column-gap: 0.75rem; align-items: baseline; font-variant-numeric: tabular-nums; }}
    .rank-table > div {{ padding: 0.6rem 0; border-bottom: 1px solid {RULE}; }}
    .rank-table .h {{ color: {MUTED}; font-size: 0.8rem; padding-top: 0; }}
    .rank-table .num {{ text-align: right; }}
    .rank-table .n {{ color: {MUTED}; }}
    .rank-table .site {{ color: {TEXT}; font-weight: 600; white-space: nowrap; overflow: hidden;
                         text-overflow: ellipsis; }}
    .rank-table .site span {{ color: {MUTED}; font-weight: 400; margin-left: 0.5rem; }}
    .rank-table .overall {{ color: {TEXT}; font-weight: 700; }}
    .panel {{ container-type: inline-size; }}
    @container (max-width: 34rem) {{
        .rank-table {{ grid-template-columns: 1.5rem minmax(0, 1fr) 4rem; }}
        .rank-table .g {{ display: none; }}
    }}

    .leader {{ display: grid; grid-template-columns: 1.5rem minmax(0, 1fr) auto; gap: 0.75rem;
               padding: 0.5rem 0; border-bottom: 1px solid {RULE}; color: {TEXT}; }}
    .leader .n {{ color: {MUTED}; }}
    .leader .score {{ font-weight: 600; font-variant-numeric: tabular-nums; }}

    .panels {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(19rem, 1fr));
               gap: 1.5rem 3rem; }}
    .leader .site {{ white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .kv {{ display: grid; grid-template-columns: 9rem minmax(0, 1fr); gap: 0.45rem 1rem; font-size: 0.9rem; }}
    .kv dt {{ color: {MUTED}; }}
    .kv dd {{ margin: 0; color: {TEXT}; font-variant-numeric: tabular-nums; }}
    .meter {{ display: grid; grid-template-columns: 10rem minmax(2rem, 1fr) 2rem; gap: 0.5rem 0.75rem;
              align-items: center; font-size: 0.85rem; color: {MUTED}; margin-bottom: 1.2rem; }}
    .meter .track {{ height: 6px; background: {RULE}; border-radius: 3px; overflow: hidden; }}
    .meter .track span {{ display: block; height: 100%; border-radius: 3px; }}
    .meter .v {{ color: {TEXT}; text-align: right; font-variant-numeric: tabular-nums; }}
    .cost-total {{ font-weight: 700; font-size: 2rem; color: {TEXT}; font-variant-numeric: tabular-nums; }}
    .note {{ color: {MUTED}; font-size: 0.85rem; max-width: 72ch; }}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the master data file"""
    try:
        df = pd.read_csv(DATA_PATH, low_memory=False)
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
            row_dict["_source_index"] = idx
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
                row_dict["_source_index"] = idx
                row_dict[score_col + '_adjusted'] = adjusted_score
                selected.append(row_dict)
                
                # Update state count
                if state not in selected_states:
                    selected_states[state] = 0
                selected_states[state] += 1
    
    # Convert back to DataFrame and sort by original score
    result_df = pd.DataFrame(selected)
    if len(result_df) > 0:
        result_df = result_df.set_index("_source_index")
        result_df.index.name = None
    if len(result_df) > 0:
        result_df = result_df.nlargest(top_n, score_col)
    
    return result_df

def site_label(row):
    county = row.get('Plant county name')
    county = str(county) if pd.notna(county) else 'Unknown county'
    return f"{county}, {row.get('Plant state abbreviation', '')}"

def create_map(df_scored, top3_per_category, top5_overall):
    """Map every scored site faintly, then the shortlisted sites on top."""
    fig = go.Figure()

    # Every plant site as a faint dot, so the grid's footprint is visible.
    fig.add_trace(go.Scattergeo(
        lat=df_scored['Plant latitude'], lon=df_scored['Plant longitude'],
        mode='markers', marker=dict(size=2.5, color='#6B7680', opacity=0.35),
        hoverinfo='skip', showlegend=False,
    ))

    def hover(df):
        return [
            f"<b>{site_label(r)}</b><br>"
            f"<span style='color:{MUTED}'>{r.get('Plant name', '')}</span><br><br>"
            f"Overall: <b>{r['Overall_Score']:.1f}</b><br>"
            + '<br>'.join(f"{GOAL_SHORT[c]}: {r[c + '_Score']:.0f}" for c in GOAL_COLORS)
            for _, r in df.iterrows()
        ]

    # Overall top 5 as rings, drawn under the goal dots so a site in both shows a ringed dot.
    fig.add_trace(go.Scattergeo(
        lat=top5_overall['Plant latitude'], lon=top5_overall['Plant longitude'],
        mode='markers', name='Top 5 overall',
        marker=dict(size=22, color='rgba(0,0,0,0)', line=dict(color=TEXT, width=2)),
        hovertext=hover(top5_overall), hoverinfo='text',
    ))

    for cat_name, top_df in top3_per_category.items():
        fig.add_trace(go.Scattergeo(
            lat=top_df['Plant latitude'], lon=top_df['Plant longitude'],
            mode='markers', name=f"Top 3 {GOAL_SHORT[cat_name].lower()}",
            marker=dict(size=11, color=GOAL_COLORS[cat_name], line=dict(color='#0E1117', width=1)),
            hovertext=hover(top_df), hoverinfo='text',
        ))

    fig.update_geos(
        scope='usa', projection_type='albers usa',
        showland=True, landcolor=SURFACE, showlakes=False,
        subunitcolor=RULE, subunitwidth=0.8, countrycolor=RULE,
        bgcolor='rgba(0,0,0,0)',
    )
    fig.update_layout(
        height=460, margin=dict(l=0, r=0, t=0, b=0), dragmode=False,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Public Sans, sans-serif', color=MUTED, size=12),
        legend=dict(orientation='h', yanchor='top', y=1.0, xanchor='left', x=0.0,
                    bgcolor='rgba(0,0,0,0)', font=dict(color=MUTED)),
        hoverlabel=dict(bgcolor=SURFACE, bordercolor=RULE,
                        font=dict(family='Public Sans, sans-serif', color=TEXT)),
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
    hectares_per_acre = 0.404686

    costs = {}

    # 1. Land/Property Costs
    # mean_property_value_3mi comes from the PLACES fair market value raster
    # (Nolte 2020), which stores ln(USD per hectare) in Jan 2017 dollars.
    log_value_per_ha = row.get('mean_property_value_3mi', np.nan)
    if pd.notna(log_value_per_ha):
        value_per_acre = np.exp(log_value_per_ha) * hectares_per_acre
        costs['Land Acquisition'] = value_per_acre * land_acres_needed
    else:
        costs['Land Acquisition'] = 5000000  # Default $5M if no data

    # 2. Annual Electricity Costs
    electricity_rate = row.get('Electricity_Cost_State_cents_per_kWh', 10.0) / 100  # $/kWh
    annual_energy_kwh = dc_size_mw * 1000 * electricity_utilization * hours_per_year
    costs['Annual Electricity'] = annual_energy_kwh * electricity_rate
    
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

@st.cache_data
def compute_tco(df):
    """10-year TCO per site. Independent of the weights, so it is computed once."""
    return pd.Series([estimate_total_cost(r, dc_size_mw=DC_SIZE_MW)['10-Year TCO'] for _, r in df.iterrows()],
                     index=df.index)

def money(x):
    if abs(x) >= 1e9:
        return f"${x / 1e9:,.2f}B"
    if abs(x) >= 1e6:
        return f"${x / 1e6:,.1f}M"
    return f"${x:,.0f}"

def meters(items):
    """items: (label, value 0-100, color). Rendered as labeled horizontal bars."""
    html = '<div class="meter">'
    for label, v, color in items:
        html += (f'<div>{label}</div><div class="track"><span style="width:{max(v, 0):.0f}%;'
                 f'background:{color}"></span></div><div class="v">{v:.0f}</div>')
    return html + '</div>'

def rank_list(top_df):
    html = '<div class="rank-table"><div class="h"></div><div class="h">Site</div>'
    html += ''.join(f'<div class="h num g">{GOAL_SHORT[c]}</div>' for c in GOAL_COLORS)
    html += '<div class="h num">Overall</div>'
    for rank, (_, row) in enumerate(top_df.iterrows(), 1):
        html += (f'<div class="n">{rank}</div>'
                 f'<div class="site">{site_label(row)}<span>{row.get("Plant name", "")}</span></div>')
        html += ''.join(f'<div class="num g" style="color:{GOAL_COLORS[c]}">{row[c + "_Score"]:.0f}</div>'
                        for c in GOAL_COLORS)
        html += f'<div class="num overall">{row["Overall_Score"]:.1f}</div>'
    return html + '</div>'

def leader_list(top_df, cat):
    html = ''
    for rank, (_, row) in enumerate(top_df.iterrows(), 1):
        html += (f'<div class="leader"><div class="n">{rank}</div><div class="site">{site_label(row)}</div>'
                 f'<div class="score" style="color:{GOAL_COLORS[cat]}">{row[cat + "_Score"]:.1f}</div></div>')
    return html

DEFAULT_WEIGHTS = {
    'lc': [0.10, 0.00, 0.60, 0.10, 0.20, 0.00],
    'le': [0.20, 0.60, 0.00, 0.10, 0.10, 0.00],
    'hr': [0.20, 0.00, 0.10, 0.60, 0.10, 0.00],
}

LOGO = ('<svg width="28" height="28" viewBox="0 0 28 28" aria-hidden="true">'
        '<rect width="28" height="28" rx="7" fill="#5B8DEF"/>'
        '<path d="M15.5 5 8 16h5l-1.5 7L19 12h-5z" fill="#0E1117"/></svg>')

def reset_weights():
    for prefix, values in DEFAULT_WEIGHTS.items():
        for (code, _), v in zip(FACTORS, values):
            st.session_state[f'{prefix}_{code}'] = v

def factor_sliders(prefix):
    weights = [st.slider(label, 0.0, 1.0, default, 0.05, key=f'{prefix}_{code}')
               for (code, label), default in zip(FACTORS, DEFAULT_WEIGHTS[prefix])]
    total = sum(weights)
    return [w / total for w in weights] if total > 0 else weights

def panel(title, body):
    return f'<div class="panel"><div class="section-title">{title}</div>{body}</div>'

# Main app
def main():
    with st.spinner("Loading plant data"):
        df = add_state_data(load_data())

    # Sidebar: one tab of factor weights per goal
    with st.sidebar:
        st.markdown('<div class="section-title">Goal weights</div>', unsafe_allow_html=True)
        st.caption("Each goal blends six site factors. Weights are rescaled to add up to 1.")
        tab_cost, tab_emis, tab_rel = st.tabs(['Cost', 'Emissions', 'Reliability'])
        with tab_cost:
            lc = factor_sliders('lc')
        with tab_emis:
            le = factor_sliders('le')
        with tab_rel:
            hr = factor_sliders('hr')
        st.button("Reset to defaults", on_click=reset_weights, use_container_width=True)

    # Sub-weights inside each factor stay fixed (see docs/algorithm.md)
    param_weights = {
        'P1_Proximity_RE': {'dist': 0.40, 'share': 0.35, 'cap': 0.25},
        'P2_Emissions': {'CO2e': 0.70, 'CO2': 0.30, 'NOx': 0.50, 'SO2': 0.50, 'climate': 0.75, 'air': 0.25},
        'P3_Capital_Investment': {'land': 0.40, 'trans': 0.40, 'elec_cost': 0.20,
                                  'trans_dist': 0.50, 'trans_cap': 0.50},
        'P4_Reliability': {'SAIDI': 0.35, 'SAIFI': 0.35, 'degree': 0.15, 'cap': 0.15},
        'P5_Water': {'potable': 0.90, 'lower48': 0.10},
    }
    category_weights = {'Lowest Cost': lc, 'Lowest Emissions': le, 'Highest Reliability': hr}

    df_scored = score_plants(df, param_weights, category_weights)
    df_scored['TCO'] = compute_tco(df)
    median_tco = float(df_scored['TCO'].median())

    penalty_factor = 0.5  # State diversity penalty
    top3_per_category = {
        cat: select_top_with_state_diversity(df_scored, cat + '_Score', top_n=3, penalty_factor=penalty_factor)
        for cat in GOAL_COLORS
    }
    top5_overall = select_top_with_state_diversity(df_scored, 'Overall_Score', top_n=5, penalty_factor=penalty_factor)

    # Top bar and page heading
    st.markdown(
        f'<div class="topbar"><div class="brand">{LOGO}<span class="word">Nexsite</span>'
        f'<span class="tag">Data center siting</span></div>'
        f'<div class="pill"><b>{len(df):,}</b> sites scored</div></div>'
        '<div class="page-title">Where do we place a data center on the grid?</div>'
        '<p class="page-sub">Every US power plant site, scored on cost, emissions, and reliability. '
        'Change the goal weights in the sidebar to see the ranking update.</p>',
        unsafe_allow_html=True)

    # Recommended site
    best = top5_overall.iloc[0]
    best_cost = estimate_total_cost(best, dc_size_mw=DC_SIZE_MW)['10-Year TCO']
    fuel = str(best.get('Plant primary fuel category', '')).lower()
    stats = [('Overall', f"{best['Overall_Score']:.1f}", TEXT)]
    stats += [(GOAL_SHORT[c], f"{best[c + '_Score']:.0f}", GOAL_COLORS[c]) for c in GOAL_COLORS]
    stats += [('10-year cost', money(best_cost), TEXT)]
    st.markdown(
        '<div class="panel hero"><div class="lead"><div class="eyebrow">Recommended site</div>'
        f'<div class="place">{site_label(best)}</div>'
        f'<div class="near">Near {best.get("Plant name", "")}, {fuel} plant</div></div>'
        + ''.join(f'<div class="stat"><div class="eyebrow">{k}</div><div class="v" style="color:{c}">{v}</div></div>'
                  for k, v, c in stats)
        + '</div>', unsafe_allow_html=True)

    # Map
    with st.container(border=True):
        st.markdown('<span class="panel-anchor"></span><div class="section-title">Shortlisted sites</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(create_map(df_scored, top3_per_category, top5_overall),
                        use_container_width=True, config={'displayModeBar': False, 'scrollZoom': False})

    # Rankings
    st.markdown(panel('Top 5 overall', rank_list(top5_overall)), unsafe_allow_html=True)
    st.markdown(panel('Leaders by goal', '<div class="panels">' + ''.join(
        f'<div><div style="font-weight:600;color:{GOAL_COLORS[cat]};margin-bottom:0.25rem">{cat}</div>'
        f'{leader_list(top_df, cat)}</div>'
        for cat, top_df in top3_per_category.items()) + '</div>'), unsafe_allow_html=True)

    # Site inspector
    shortlist = {}
    for rank, (i, row) in enumerate(top5_overall.iterrows(), 1):
        shortlist.setdefault(i, f"{site_label(row)} (overall #{rank})")
    for cat, top_df in top3_per_category.items():
        for rank, (i, row) in enumerate(top_df.iterrows(), 1):
            shortlist.setdefault(i, f"{site_label(row)} ({GOAL_SHORT[cat].lower()} #{rank})")

    with st.container(border=True):
        st.markdown('<span class="panel-anchor"></span><div class="section-title">Inspect a site</div>',
                    unsafe_allow_html=True)
        choice = st.selectbox("Shortlisted site", list(shortlist), format_func=shortlist.get,
                              label_visibility='collapsed')
        row = df_scored.loc[choice]
        costs = estimate_total_cost(row, dc_size_mw=DC_SIZE_MW)

        log_land = row.get('mean_property_value_3mi')
        capacity = row.get('Plant nameplate capacity (MW)')
        facts = {
            'Plant': row.get('Plant name', ''),
            'Fuel': str(row.get('Plant primary fuel category', '')).capitalize(),
            'Capacity': f"{capacity:,.0f} MW" if pd.notna(capacity) else 'No data',
            'Coordinates': f"{row['Plant latitude']:.3f}, {row['Plant longitude']:.3f}",
            'Bus line capacity': f"{row.get('bus_sum_line_capacity_MW', 0):,.0f} MW",
            'Lines at bus': f"{row.get('bus_num_incident_lines', 0):.0f}",
            'Nearest renewable': f"{row.get('bus_dist_to_nearest_renewable_plant_km', 0):.1f} km",
            'Electricity price': f"{row.get('Electricity_Cost_State_cents_per_kWh', 0):.2f}¢/kWh",
            'Land value': (money(np.exp(log_land) * 0.404686) + '/acre') if pd.notna(log_land) else 'No data',
        }
        breakdown = {
            'Land': costs['Land Acquisition'],
            'Transmission': costs['Transmission Line Construction'],
            'Substations': costs['Substation/Switchyard'],
            'Electricity/yr': costs['Annual Electricity'],
            'Water/yr': costs['Annual Water'],
        }
        delta = costs['10-Year TCO'] - median_tco
        kv = lambda d: '<dl class="kv">' + ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in d.items()) + '</dl>'
        st.markdown(
            '<div class="panels" style="margin-top:1rem">'
            f'<div><div class="eyebrow">Site</div>{kv(facts)}</div>'
            '<div><div class="eyebrow">Goal scores</div>'
            + meters([(GOAL_SHORT[c], row[c + '_Score'], GOAL_COLORS[c]) for c in GOAL_COLORS])
            + '<div class="eyebrow">Factors</div>'
            + meters([(label, float(row.get(code, 0)) * 100, MUTED) for code, label in FACTORS])
            + '</div>'
            f'<div><div class="eyebrow">10-year cost</div>'
            f'<div class="cost-total">{money(costs["10-Year TCO"])}</div>'
            f'<div class="note" style="margin-bottom:1rem">{money(abs(delta))} '
            f'{"below" if delta < 0 else "above"} the median site</div>'
            f'{kv({k: money(v) for k, v in breakdown.items()})}</div>'
            '</div>', unsafe_allow_html=True)

    st.markdown(
        '<p class="note" style="margin-top:1.5rem">Water scores use a synthetic placeholder dataset, so treat '
        'them as illustrative. Electricity prices and outage figures are state averages. Costs are rough '
        'estimates for a 2 GW facility at 85% utilization, with no discounting.</p>',
        unsafe_allow_html=True)

    export_cols = ['Plant county name', 'Plant name', 'Plant state abbreviation', 'Plant latitude',
                   'Plant longitude', 'Lowest Cost_Score', 'Lowest Emissions_Score',
                   'Highest Reliability_Score', 'Overall_Score', 'TCO']
    export_df = df_scored.loc[list(shortlist), export_cols].rename(columns={'TCO': '10-Year TCO (USD)'})
    st.download_button(
        label="Download shortlist (CSV)",
        data=export_df.to_csv(index=False),
        file_name=f"nexsite_shortlist_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    main()
