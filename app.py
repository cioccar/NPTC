import streamlit as st
import pandas as pd

[... keep all your code until the display part ...]

    # Color coding function
    def color_rows(row):
        # Get week columns (excluding Staff_Group, Avg_Occupancy, and Avg_Capacity_Delta)
        week_cols = [col for col in row.index if col.startswith('Week_')]
        
        # Calculate average occupancy from week columns only
        week_values = [row[col] for col in week_cols if pd.notnull(row[col])]
        avg_occupancy = sum(week_values) / len(week_values) if week_values else 0
        
        # Apply colors based on average occupancy
        return ['color: red' if (avg_occupancy > 74 and col in ['Staff_Group', 'Avg_Capacity_Delta']) 
                else 'color: green' if (avg_occupancy <= 74 and col in ['Staff_Group', 'Avg_Capacity_Delta'])
                else '' for col in row.index]

    # Format the display dataframe
    formatted_df = display_df.copy()
    
    # Ensure all numeric columns are properly formatted
    for col in formatted_df.columns:
        if col != 'Staff_Group':
            formatted_df[col] = pd.to_numeric(formatted_df[col], errors='coerce')

    # Display formatted dataframe
    st.dataframe(
        formatted_df.style
        .format({
            col: '{:.1f}%' if col not in ['Staff_Group', 'Avg_Capacity_Delta'] else '{:.1f}'
            for col in formatted_df.columns
        })
        .apply(color_rows, axis=1)
    )

[... keep rest of your code ...]
