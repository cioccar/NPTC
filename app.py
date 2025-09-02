import streamlit as st
import pandas as pd

[Previous data dictionary remains the same...]

st.title('NPT hours available')

# Sidebar with filters
st.sidebar.header('Filters')

[Previous filter code remains the same...]

# Display the filtered dataframe
st.write("Occupancy Rates by Week (%) and Staff group & Delta hours available for Staff Group")

# Create a function to color rows based on Week 35 occupancy
def color_rows(row):
    color = 'red' if row.get('Week_35', 0) > 74 else 'green'
    return [f'color: {color}' if col in ['Staff_Group', 'Avg_Capacity_Delta'] else '' 
            for col in row.index]

st.dataframe(
    display_df.style
    .format({
        'Week_35': '{:.1f}%',
        'Week_34': '{:.1f}%',
        'Week_33': '{:.1f}%',
        'Week_32': '{:.1f}%',
        'Week_31': '{:.1f}%',
        'Week_30': '{:.1f}%',
        'Avg_Occupancy': '{:.1f}%',
        'Avg_Capacity_Delta': '{:.1f}'
    })
    .apply(color_rows, axis=1)
)

# Calculate and display metrics for the most recent selected week
if selected_weeks:
    latest_week = selected_weeks[0]
    st.metric(f"Average Occupancy ({latest_week})", 
             f"{filtered_df[f'{latest_week}_Occupancy'].mean():.1f}%")
    st.metric("Average Unused Capacity", 
             f"{display_df['Avg_Capacity_Delta'].mean():.1f} hours")
