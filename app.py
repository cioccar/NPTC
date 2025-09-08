import streamlit as st
import pandas as pd
from urllib.parse import quote
import base64

st.title('NPT hours available')

# Sidebar headers with consistent styling
st.sidebar.markdown("""
<style>
    .sidebar-header {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 0px;  /* Reduced from 10px to 0px */
    }
    /* Add custom CSS to reduce space in file uploader */
    .css-1dhfmct {
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
</style>
""", unsafe_allow_html=True)

# Quicksight Link section
st.sidebar.markdown('<p class="sidebar-header">Quicksight Link</p>', unsafe_allow_html=True)
st.sidebar.markdown('''
<a href="https://us-east-1.quicksight.aws.amazon.com/sn/account/187419755406_SPS/dashboards/19ca18a9-c62b-4d22-94c3-b180f1cd9640/views/c7b9defa-5e1a-46b6-971a-dfecf4e7c45c" target="_blank">
    <button style="
        background-color: white; 
        border: 1px solid #cccccc;
        color: black;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 4px;
        transition: background-color 0.3s;
        width: 100%;
    ">Shrinkage and Occupancy Dashboard</button>
</a>
''', unsafe_allow_html=True)

# Data Upload section with reduced spacing
st.sidebar.markdown('<p class="sidebar-header">Data Upload</p>', unsafe_allow_html=True)
uploaded_files = st.sidebar.file_uploader(
    "From the above dashboard",
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

def generate_email_html(latest_week, email_table_df, actual_occupancy, ytd_goal):
    html_content = f"""
    <html>
    <head>
        <style>
            table {{border-collapse: collapse; width: 100%;}}
            th, td {{border: 1px solid black; padding: 8px; text-align: left;}}
            th {{background-color: #f2f2f2;}}
        </style>
    </head>
    <body>
        <h2 style="background-color: #90EE90; color: white; padding: 10px;">NPT Request</h2>
        <p>Hello team,</p>
        <p>This email is to inform you about NPT hours that can be taken by DE associates for Seller and Brand business units.</p>
        <p>This will help improve our occupancy rate, which has been below the YTD target for the last 4 weeks, as shown below:</p>
        
        <table>
            <tr>
                <th>Week {latest_week-3}</th>
                <th>Week {latest_week-2}</th>
                <th>Week {latest_week-1}</th>
                <th>Week {latest_week}</th>
            </tr>
            <tr>
                <td>Actual Occupancy %</td>
                {' '.join(f'<td>{occ:.1f}%</td>' for occ in actual_occupancy)}
            </tr>
            <tr>
                <td>YTD Goal %</td>
                {' '.join(f'<td>{goal:.1f}%</td>' for goal in ytd_goal)}
            </tr>
        </table>
        
        <p>In the table below, you have the available hours divided by weeks and Staff Groups:</p>
        
        <table>
            <tr>
                <th>Staff Groups</th>
                {' '.join(f'<th>{col}</th>' for col in email_table_df.columns if col != 'Staff_Group')}
            </tr>
            {email_table_df.to_html(index=False, header=False)}
        </table>
        
        <p>To request NPT, you can use the River <a href="#">link</a> for NPT requests.</p>
        <p><strong>Note:</strong> Requests may be denied if we notice that the requested interval does not meet minimum coverage requirements.</p>
        <p>Thank you for your support!</p>
        <p>Best Regards,<br>EMEA WFM</p>
    </body>
    </html>
    """
    return html_content

# Process all uploaded files
if uploaded_files:
    # Combine all uploaded files
    all_data = pd.concat([process_file(file) for file in uploaded_files])
    
    # Sidebar filters
    st.sidebar.markdown("### Filters")
    
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
    
    # Create display dataframe
    display_df = occupancy_pivot.copy()
    
    # Filter columns based on selected weeks
    selected_columns = ['Staff_Group'] + selected_weeks
    display_df = display_df[display_df.columns.intersection(selected_weeks)]
    capacity_pivot = capacity_pivot[capacity_pivot.columns.intersection(selected_weeks)]
    
    # Add average occupancy for selected weeks only
    display_df['Avg_Occupancy'] = display_df.mean(axis=1)
    
    # Add average capacity delta for selected weeks only
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

    # Modified color coding function to only color specific columns
    def color_rows(row):
        avg_occupancy = row['Avg_Occupancy']
        colors = []
        for col in row.index:
            if col in ['Staff_Group', 'Avg_Occupancy', 'Avg_Capacity_Delta']:
                colors.append('background-color: #ffcccb' if avg_occupancy > 74 else 'background-color: #90EE90')
            else:
                colors.append('')
        return colors

    # Apply formatting and styling
    styled_df = formatted_df.style\
        .format({
            'Avg_Occupancy': '{:.1f}%',
            'Avg_Capacity_Delta': '{:.1f}',
            **{col: '{:.1f}%' for col in formatted_df.columns if col not in ['Staff_Group', 'Avg_Capacity_Delta']}
        })\
        .apply(color_rows, axis=1)\
        .set_properties(**{
            'width': '100px',
            'text-align': 'center'
        })

    # Calculate dynamic height based on number of staff groups
    row_height = 35  # height per row in pixels
    total_height = len(selected_groups) * row_height  # removed header_height and extra row

    # Display the styled dataframe with dynamic height
    st.dataframe(styled_df, height=total_height)

    # Display metrics for selected weeks
    if selected_weeks:
        # Calculate average occupancy for selected weeks
        avg_occupancy = formatted_df[selected_weeks].mean().mean()
        
        # Calculate sum of capacity delta hours only for rows with occupancy < 74%
        unused_capacity = formatted_df[formatted_df['Avg_Occupancy'] <= 74]['Avg_Capacity_Delta'].sum()
        
        st.metric(
            f"Average Occupancy (Selected Weeks)", 
            f"{avg_occupancy:.1f}%"
        )
        st.metric(
            "Total Unused Capacity (Green Rows)", 
            f"{unused_capacity:.1f} hours"
        )

        # Generate email content
        latest_week = max([int(week.replace('Week_', '')) for week in selected_weeks])
        
        email_table_df = formatted_df[['Staff_Group'] + selected_weeks].copy()
        for week in selected_weeks:
            email_table_df[week] = capacity_pivot[week].round(0)
        
        # These are example data. You should replace them with real data from your DataFrame.
        actual_occupancy = [67.5, 67.8, 66.2, 66.7]
        ytd_goal = [78.5, 78.5, 78.5, 78.5]
        
        html_content = generate_email_html(latest_week, email_table_df, actual_occupancy, ytd_goal)
        
        # Encode the HTML content
        b64 = base64.b64encode(html_content.encode()).decode()
        
        # Add email button to sidebar
        st.sidebar.markdown('<p class="sidebar-header">Generate Email</p>', unsafe_allow_html=True)
        href = f'<a href="data:text/html;base64,{b64}" download="email_template.html">Download Email Template</a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
        st.sidebar.markdown("1. Click the link above to download the HTML template.")
        st.sidebar.markdown("2. Open a new email in Outlook.")
        st.sidebar.markdown("3. Go to 'Insert' > 'File' and select the downloaded HTML file.")
            
else:
    st.write("Please upload your data files")
    # Default email button when no data is loaded
    st.sidebar.markdown('<p class="sidebar-header">Generate Email</p>', unsafe_allow_html=True)
    st.sidebar.markdown('''
    <a href="mailto:?subject=NPT%20hours%20for%20XX%20Seller%2C%20Brand%20and%20Vendor&body=Please%20upload%20data%20first" target="_blank">
        <button style="
            background-color: white; 
            border: 1px solid #cccccc;
            color: black;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
            transition: background-color 0.3s;
            width: 100%;
        ">Generate Email</button>
    </a>
    ''', unsafe_allow_html=True)
