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
    
    # Create a copy for formatting
    formatted_df = display_df.copy()
    
    # Ensure numeric columns are properly formatted
    numeric_cols = [col for col in formatted_df.columns if col != 'Staff_Group']
    for col in numeric_cols:
        formatted_df[col] = pd.to_numeric(formatted_df[col], errors='coerce')

    # Simplified color coding function
    def color_rows(row):
        avg_occupancy = row['Avg_Occupancy']
        return ['background-color: #ffcccb' if avg_occupancy > 74 else 'background-color: #90EE90' for _ in row]

    # Apply formatting and styling
    styled_df = formatted_df.style\
        .format({col: '{:.1f}' for col in formatted_df.columns if col != 'Staff_Group'})\
        .apply(color_rows, axis=1)

    # Display the styled dataframe
    st.dataframe(styled_df)

    # Display metrics
    if selected_weeks:
        # Debug information first
        st.write("Debug Information")
        st.write("DataFrame columns:", formatted_df.columns.tolist())
        st.write("Selected weeks:", selected_weeks)
        
        # Now try to calculate metrics
        try:
            latest_week = selected_weeks[0]
            # Try to find the correct column name
            week_cols = [col for col in formatted_df.columns if str(col).startswith('Week_')]
            
            if week_cols:
                latest_available_week = week_cols[0]
                st.metric(
                    f"Average Occupancy ({latest_available_week})", 
                    f"{formatted_df[latest_available_week].mean():.1f}%"
                )
            else:
                st.warning("No week columns found in the data")
            
            if 'Avg_Capacity_Delta' in formatted_df.columns:
                st.metric(
                    "Average Unused Capacity", 
                    f"{formatted_df['Avg_Capacity_Delta'].mean():.1f} hours"
                )
            else:
                st.warning("Avg_Capacity_Delta column not found")
                
        except Exception as e:
            st.error(f"Error calculating metrics: {str(e)}")
            st.write("Full column list:", formatted_df.columns.tolist())
            
else:
    st.write("Please upload your data files")
