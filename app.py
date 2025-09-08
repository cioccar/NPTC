import streamlit as st
import pandas as pd
from urllib.parse import quote

# Define the HTML email template at the top of the file
EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<style>
    .header {
        background-color: #90EE90;
        color: white;
        padding: 10px;
        font-size: 24px;
        font-family: 'Calibri', sans-serif;
    }
    .content {
        font-family: 'Calibri', sans-serif;
        margin: 15px;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 10px 0;
    }
    th, td {
        border: 1px solid black;
        padding: 8px;
        text-align: center;
    }
    th {
        background-color: #f2f2f2;
    }
</style>
</head>
<body>
<div class="header">NPT Request</div>
<div class="content">
    <p>Hello team,</p>
    <p>This email is to inform you about NPT hours that can be taken by DE associates for Seller and Brand business units.</p>
    <p>This will help improve our occupancy rate, which has been below the YTD target for the last 4 weeks, as shown below:</p>
    
    {occupancy_table}
    
    <p>In the table below, you have the available hours divided by weeks and Staff Groups:</p>
    
    {hours_table}
    
    <p>To request NPT, you can use the River <a href="#">link</a> for NPT requests.</p>
    <p><strong>Note:</strong> Requests may be denied if we notice that the requested interval does not meet minimum coverage requirements.</p>
    <p>Thank you for your support!</p>
    <p>Best Regards,<br>EMEA WFM</p>
</div>
</body>
</html>
"""

# Helper functions for email generation
def create_occupancy_table(latest_week, actual_occupancy, ytd_goal):
    table = """
    <table>
        <tr>
            <th>Week {}</th>
            <th>Week {}</th>
            <th>Week {}</th>
            <th>Week {}</th>
        </tr>
        <tr>
            <td>{:.1f}%</td>
            <td>{:.1f}%</td>
            <td>{:.1f}%</td>
            <td>{:.1f}%</td>
        </tr>
        <tr>
            <td>{:.1f}%</td>
            <td>{:.1f}%</td>
            <td>{:.1f}%</td>
            <td>{:.1f}%</td>
        </tr>
    </table>
    """.format(
        latest_week-3, latest_week-2, latest_week-1, latest_week,
        *actual_occupancy,
        *ytd_goal
    )
    return table

def create_hours_table(data):
    table = "<table><tr><th>Staff Groups</th>"
    for col in data.columns[1:]:  # Skip Staff_Group column
        table += f"<th>{col}</th>"
    table += "</tr>"
    
    for _, row in data.iterrows():
        table += "<tr>"
        for val in row:
            table += f"<td>{val}</td>"
        table += "</tr>"
    table += "</table>"
    return table

st.title('NPT hours available')

# Sidebar headers with consistent styling
st.sidebar.markdown("""
<style>
    .sidebar-header {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 0px;
    }
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
    ">ShrShrinkage and Occupancy Dashboard</button>
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
    df = pd.read_csv(file)
    df_processed = pd.DataFrame({
        'Staff_Group': df['1. STAFF GROUP'],
        'Week': df['Period by'].str.extract(r'Week (\d+)')[0],
        'Occupancy': df['Occupancy %'] * 100,
        'Capacity_Delta': df['Capacity Delta Hrs']
    })
    return df_processed

if uploaded_files:
    all_data = pd.concat([process_file(file) for file in uploaded_files])
    
    st.sidebar.markdown("### Filters")
    
    available_weeks = sorted(all_data['Week'].unique(), reverse=True)
    available_weeks = [f'Week_{week}' for week in available_weeks]
    
    selected_weeks = st.sidebar.multiselect(
        'Select Weeks',
        available_weeks,
        default=[available_weeks[0]]
    )
    
    selected_groups = st.sidebar.multiselect(
        'Select Staff Groups',
        all_data['Staff_Group'].unique().tolist(),
        default=all_data['Staff_Group'].unique().tolist()
    )
    
    filtered_data = all_data[
        all_data['Staff_Group'].isin(selected_groups)
    ].copy()
    
    filtered_data['Week'] = 'Week_' + filtered_data['Week'].astype(str)
    
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
    
    display_df = occupancy_pivot.copy()
    
    selected_columns = ['Staff_Group'] + selected_weeks
    display_df = display_df[display_df.columns.intersection(selected_weeks)]
    capacity_pivot = capacity_pivot[capacity_pivot.columns.intersection(selected_weeks)]
    
    display_df['Avg_Occupancy'] = display_df.mean(axis=1)
    display_df['Avg_Capacity_Delta'] = capacity_pivot.mean(axis=1)
    display_df = display_df.reset_index()
    
    st.write("Occupancy Rates by Week (%) and Staff group & Delta hours available for Staff Group")
    
    formatted_df = display_df.copy()
    numeric_cols = [col for col in formatted_df.columns if col != 'Staff_Group']
    for col in numeric_cols:
        formatted_df[col] = pd.to_numeric(formatted_df[col], errors='coerce')

    def color_rows(row):
        avg_occupancy = row['Avg_Occupancy']
        colors = []
        for col in row.index:
            if col in ['Staff_Group', 'Avg_Occupancy', 'Avg_Capacity_Delta']:
                colors.append('background-color: #ffcccb' if avg_occupancy > 74 else 'background-color: #90EE90')
            else:
                colors.append('')
        return colors

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

    row_height = 35
    total_height = len(selected_groups) * row_height
    st.dataframe(styled_df, height=total_height)

    if selected_weeks:
        avg_occupancy = formatted_df[selected_weeks].mean().mean()
        unused_capacity = formatted_df[formatted_df['Avg_Occupancy'] <= 74]['Avg_Capacity_Delta'].sum()
        
        st.metric(
            f"Average Occupancy (Selected Weeks)", 
            f"{avg_occupancy:.1f}%"
        )
        st.metric(
            "Total Unused Capacity (Green Rows)", 
            f"{unused_capacity:.1f} hours"
        )

        # Email generation
        latest_week = max([int(week.replace('Week_', '')) for week in selected_weeks])
        
        email_table_df = formatted_df[['Staff_Group'] + selected_weeks].copy()
        for week in selected_weeks:
            email_table_df[week] = capacity_pivot[week].round(0)
        
        actual_occupancy = [67.5, 67.8, 66.2, 66.7]  # Replace with actual data
        ytd_goal = [78.5, 78.5, 78.5, 78.5]  # Replace with actual data
        
        # Create tables and insert into template
        occupancy_table = create_occupancy_table(latest_week, actual_occupancy, ytd_goal)
        hours_table = create_hours_table(email_table_df)
        
        email_html = EMAIL_TEMPLATE.format(
            occupancy_table=occupancy_table,
            hours_table=hours_table
        )
        
        # Create mailto link with HTML content
        encoded_html = quote(email_html)
        email_subject = f"NPT hours for XX Seller, Brand and Vendor | WK{latest_week}"
        
        # Add email button to sidebar
        st.sidebar.markdown('<p class="sidebar-header">Generate Email</p>', unsafe_allow_html=True)
        mailto_link = f'mailto:?subject={quote(email_subject)}&body={encoded_html}'
        
        st.sidebar.markdown(f'''
        <a href="{mailto_link}" target="_blank">
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
else:
    st.write("Please upload your data files")
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
