import streamlit as st
import pandas as pd

# Create the data with weekly information
data = {
    'Staff_Group': [
        'DE_BRAND_CW_DE', 'DE_BRAND_PCW_DE', 'DE_FBA_CW_DE', 
        'DE_FBA_ILAC_CW_DE', 'DE_FBA_ILAC_PCW_DE', 'DE_FBA_ILAC_WI_DE',
        'DE_FBA_PCW_DE', 'DE_FBA_WI_DE', 'DE_KYC_PCW_DE', 
        'DE_M@_PCW_DE', 'DE_M@_WI_DE', 'DE_MAT_CW_DE',
        'DE_VAT_CW_DE', 'DE_VAT_PCW_DE'
    ],
    'Week_35_Occupancy': [  # Latest week
        67.23, 67.92, 62.22, 67.59, 60.90, 65.76,
        60.96, 70.97, 75.37, 49.57, 70.57, 68.21,
        69.12, 65.71
    ],
    'Week_35_Delta': [
        433.81, 159.23, 240.71, 339.25, 169.99, 60.80,
        202.12, 37.52, 98.84, 30.60, 11.82, 87.74,
        50.54, 51.14
    ],
    'Week_34_Occupancy': [
        61.02, 63.57, 63.40, 65.90, 64.07, 63.94,
        55.36, 68.19, 71.59, 53.65, 68.28, 66.85,
        67.91, 63.56
    ],
    'Week_34_Delta': [
        430.81, 155.23, 245.71, 335.25, 165.99, 65.80,
        205.12, 35.52, 95.84, 35.60, 13.82, 85.74,
        52.54, 53.14
    ],
    'Week_33_Occupancy': [
        62.15, 61.57, 64.40, 64.90, 63.07, 64.94,
        57.36, 69.19, 70.59, 52.65, 69.28, 65.85,
        66.91, 64.56
    ],
    'Week_33_Delta': [
        435.81, 158.23, 242.71, 338.25, 168.99, 62.80,
        203.12, 36.52, 97.84, 32.60, 12.82, 86.74,
        51.54, 52.14
    ],
    'Week_32_Occupancy': [
        63.02, 62.57, 62.40, 66.90, 65.07, 62.94,
        56.36, 67.19, 72.59, 51.65, 67.28, 67.85,
        68.91, 62.56
    ],
    'Week_32_Delta': [
        432.81, 157.23, 241.71, 337.25, 167.99, 61.80,
        204.12, 36.52, 96.84, 31.60, 12.82, 86.74,
        51.54, 52.14
    ],
    'Week_31_Occupancy': [
        64.02, 64.57, 61.40, 63.90, 66.07, 61.94,
        58.36, 66.19, 73.59, 54.65, 66.28, 68.85,
        69.91, 61.56
    ],
    'Week_31_Delta': [
        434.81, 156.23, 243.71, 336.25, 166.99, 63.80,
        201.12, 38.52, 97.84, 33.60, 11.82, 88.74,
        53.54, 51.14
    ],
    'Week_30_Occupancy': [
        65.02, 65.57, 60.40, 62.90, 67.07, 60.94,
        59.36, 65.19, 74.59, 55.65, 65.28, 69.85,
        70.91, 60.56
    ],
    'Week_30_Delta': [
        431.81, 154.23, 244.71, 334.25, 164.99, 64.80,
        200.12, 39.52, 96.84, 34.60, 10.82, 89.74,
        54.54, 50.14
    ]
}

df = pd.DataFrame(data)

st.title('NPT hours available')

# Sidebar with filters
st.sidebar.header('Filters')

# Week filter
available_weeks = ['Week_35', 'Week_34', 'Week_33', 'Week_32', 'Week_31', 'Week_30']
selected_weeks = st.sidebar.multiselect(
    'Select Weeks',
    available_weeks,
    default=['Week_35']  # Latest week selected by default
)

# Staff Group filter
selected_groups = st.sidebar.multiselect(
    'Select Staff Groups',
    df['Staff_Group'].tolist(),
    default=df['Staff_Group'].tolist()  # All groups selected by default
)

# Filter the dataframe based on selections
filtered_df = df[df['Staff_Group'].isin(selected_groups)].copy()

# Create display dataframe with occupancy rates
display_columns = ['Staff_Group']
occupancy_columns = []
for week in selected_weeks:
    display_columns.append(f'{week}_Occupancy')
    occupancy_columns.append(f'{week}_Occupancy')

display_df = filtered_df[display_columns].copy()

# Rename columns to remove '_Occupancy' suffix
display_df.columns = [col.replace('_Occupancy', '') for col in display_df.columns]

# Calculate average occupancy for selected weeks
display_df['Avg_Occupancy'] = filtered_df[occupancy_columns].mean(axis=1)

# Calculate average Capacity Delta Hours for selected weeks
delta_columns = [f'{week}_Delta' for week in selected_weeks]
display_df['Avg_Capacity_Delta'] = filtered_df[delta_columns].mean(axis=1)

# Display the filtered dataframe
st.write("Occupancy Rates by Week (%) and Average Capacity Delta Hours")
st.dataframe(
    display_df.style.format({
        'Week_35': '{:.1f}%',
        'Week_34': '{:.1f}%',
        'Week_33': '{:.1f}%',
        'Week_32': '{:.1f}%',
        'Week_31': '{:.1f}%',
        'Week_30': '{:.1f}%',
        'Avg_Occupancy': '{:.1f}%',
        'Avg_Capacity_Delta': '{:.1f}'
    })
)

# Calculate and display metrics for the most recent selected week
if selected_weeks:
    latest_week = selected_weeks[0]
    st.metric(f"Average Occupancy ({latest_week})", 
             f"{filtered_df[f'{latest_week}_Occupancy'].mean():.1f}%")
    st.metric("Average Unused Capacity", 
             f"{display_df['Avg_Capacity_Delta'].mean():.1f} hours")
