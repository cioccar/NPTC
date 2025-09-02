import streamlit as st
import pandas as pd

[... keep all your existing code until the color_rows function ...]

    # Color coding function
    def color_rows(row):
        try:
            # Get numeric columns excluding 'Staff_Group'
            numeric_cols = [col for col in row.index if col not in ['Staff_Group']]
            
            # Calculate average occupancy (excluding Avg_Capacity_Delta)
            occupancy_cols = [col for col in numeric_cols if col != 'Avg_Capacity_Delta']
            avg_occupancy = row[occupancy_cols].mean()
            
            # Create color list
            colors = []
            for col in row.index:
                if col in ['Staff_Group', 'Avg_Capacity_Delta']:
                    colors.append(f'color: {"red" if avg_occupancy > 74 else "green"}')
                else:
                    colors.append('')
            return colors
        except Exception as e:
            st.error(f"Error in color_rows: {str(e)}")
            return [''] * len(row.index)

    # Ensure numeric columns are properly formatted
    numeric_cols = [col for col in display_df.columns if col not in ['Staff_Group']]
    for col in numeric_cols:
        display_df[col] = pd.to_numeric(display_df[col], errors='coerce')

    # Display formatted dataframe
    st.dataframe(
        display_df.style
        .format({
            col: '{:.1f}%' if col not in ['Staff_Group', 'Avg_Capacity_Delta'] else '{:.1f}'
            for col in display_df.columns
        })
        .apply(color_rows, axis=1)
    )

[... keep all your remaining code ...]
