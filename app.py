import streamlit as st
import pandas as pd

st.title('NPT hours available')

# File uploader in sidebar
st.sidebar.header('Data Upload')
uploaded_files = st.sidebar.file_uploader(
    "Upload your data files", 
    accept_multiple_files=True,
    type=['csv']
)

def process_file(file):
    # Read the file
    df = pd.read_csv(file)
    
    # Extract relevant columns
    df_processed = pd.DataFrame({
        'Staff_Group': df['1. STAFF GROUP'],
        'Week': df['Period by'].str.extract(r'Week (\d+)')[0],
        'Occupancy': df['Occupancy %'] * 100,  # Convert to percentage
        'Capacity_Delta': df['Capacity Delta Hrs']
    })
    
    return df_processed

# Process all uploaded files
if uploaded_files:
    # Combine all uploaded files
    all_data = pd.concat([process_file(file) for file in uploaded_files])
    
    # Sidebar filters
    st.sidebar.header('Filters')
    
    # Get available weeks
    available_weeks = sorted(all_data['Week'].unique(), reverse=True)
    available_weeks = [f'Week_{week}' for week in available_weeks]
    
    # Week filter
    selected_weeks = st.sidebar.multiselect(
        'Select Weeks',
        available_weeks,
        default=[available_weeks[0]]  # Latest week selected by default
    )
    
    # Staff Group filter
    selected_groups = st.sidebar.multiselect(
        'Select Staff Groups',
        all_data['Staff_Group'].unique().tolist(),
        default=all_data['Staff_Group'].unique().tolist()
    )
    
    # Filter and pivot the data
    filtered_data = all_data[
        all_data['Staff_Group'].isin(selected_groups)
    ].copy()
    
    # Create pivot tables for Occupancy and Capacity Delta
    occupancy_pivot = filtered_data.pivot(
        index='Staff_Group',
        columns='Week',
        values='Occupancy'
    )
    
    capacity_pivot = filtered_data.pivot(
        index='Staff_Group',
        columns='Week',
        values='Capacity_Delta'
    )
    
    # Create display dataframe
    display_df = occupancy_pivot.copy()
    
    # Add average occupancy
    display_df['Avg_Occupancy'] = display_df.mean(axis=1)
    
    # Add average capacity delta
    display_df['Avg_Capacity_Delta'] = capacity_pivot.mean(axis=1)
    
    # Reset index to make Staff_Group a column
    display_df = display_df.reset_index()
    
    # Display the dataframe
    st.write("Occupancy Rates by Week (%) and Staff group & Delta hours available for Staff Group")
    
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
    
    # Display metrics
    if selected_weeks:
        latest_week = selected_weeks[0]
        st.metric(
            f"Average Occupancy ({latest_week})", 
            f"{display_df[latest_week].mean():.1f}%"
        )
        st.metric(
            "Average Unused Capacity", 
            f"{display_df['Avg_Capacity_Delta'].mean():.1f} hours"
        )
else:
    st.write("Please upload your data files")
