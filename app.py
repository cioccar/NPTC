    # Process all uploaded files
    if uploaded_files:
        # Combine all uploaded files
        all_data = pd.concat([process_file(file) for file in uploaded_files])
        
        # Sidebar filters
        st.sidebar.header('Filters')
        
        # Get available weeks and add "Week_" prefix
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
        
        # Add "Week_" prefix to the Week column before pivoting
        filtered_data['Week'] = 'Week_' + filtered_data['Week'].astype(str)
        
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
        
        # Rest of your code remains the same...
        
        # Display metrics
        if selected_weeks:
            latest_week = selected_weeks[0]
            
            if latest_week in formatted_df.columns:
                st.metric(
                    f"Average Occupancy ({latest_week})", 
                    f"{formatted_df[latest_week].mean():.1f}%"
                )
                st.metric(
                    "Average Unused Capacity", 
                    f"{formatted_df['Avg_Capacity_Delta'].mean():.1f} hours"
                )
            else:
                st.error(f"Column {latest_week} not found. Available columns: {formatted_df.columns.tolist()}")
