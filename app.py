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
    'Week_35': [  # Latest week
        67.23, 67.92, 62.22, 67.59, 60.90, 65.76,
        60.96, 70.97, 75.37, 49.57, 70.57, 68.21,
        69.12, 65.71
    ],
    'Week_34': [
        61.02, 63.57, 63.40, 65.90, 64.07, 63.94,
        55.36, 68.19, 71.59, 53.65, 68.28, 66.85,
        67.91, 63.56
    ],
    'Week_33': [
        62.15, 61.57, 64.40, 64.90, 63.07, 64.94,
        57.36, 69.19, 70.59, 52.65, 69.28, 65.85,
        66.91, 64.56
    ],
    'Week_32': [
        63.02, 62.57, 62.40, 66.90, 65.07, 62.94,
        56.36, 67.19, 72.59, 51.65, 67.28, 67.85,
        68.91, 62.56
    ],
    'Week_31': [
        64.02, 64.57, 61.40, 63.90, 66.07, 61.94,
        58.36, 66.19, 73.59, 54.65, 66.28, 68.85,
        69.91, 61.56
    ],
    'Week_30': [
        65.02, 65.57, 60.40, 62.90, 67.07, 60.94,
        59.36, 65.19, 74.59, 55.65, 65.28, 69.85,
        70.91, 60.56
    ],
    'Capacity_Delta_Hours': [
        433.81, 159.23, 240.71, 339.25, 169.99, 60.80,
        202.12, 37.52, 98.84, 30.60, 11.82, 87.74,
        50.54, 51.14
    ]
}

df = pd.DataFrame(data)

st.title('Workforce Capacity Analysis Dashboard')

# Sidebar with filters
st.sidebar.header('Filters')

# Week filter
selected_weeks = st.sidebar.multiselect(
    'Select Weeks',
    ['Week_35', 'Week_34', 'Week_33', 'Week_32', 'Week_31', 'Week_30'],
    default=['Week_35']  # Latest week selected by default
)

# Staff Group filter
selected_groups = st.sidebar.multiselect(
    'Select Staff Groups',
    df['Staff_Group'].tolist(),
    default=df['Staff_Group'].tolist()  # All groups selected by default
)

# Filter the dataframe based on selections
filtered_df = df[df['Staff_Group'].isin(selected_groups)]

# Create a view for selected weeks
selected_columns = ['Staff_Group'] + selected_weeks + ['Capacity_Delta_Hours']
display_df = filtered_df[selected_columns]

# Display the filtered dataframe
st.write("Occupancy Rates by Week (%)")
st.write(display_df)

# Calculate and display metrics for the most recent selected week
if selected_weeks:
    latest_week = selected_weeks[0]
    st.metric(f"Average Occupancy ({latest_week})", 
             f"{filtered_df[latest_week].mean():.1f}%")
    st.metric("Total Unused Capacity", 
             f"{filtered_df['Capacity_Delta_Hours'].sum():.1f} hours")
