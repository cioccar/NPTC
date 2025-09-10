import streamlit as st
import pandas as pd
from urllib.parse import quote

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
    .stSelectbox [data-baseweb="select"] {
        max-width: 100%;
    }
    .stMultiSelect [data-baseweb="select"] {
        max-width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Quicksight Link section
st.sidebar.markdown('<p class="sidebar-header">Quicksight Links</p>', unsafe_allow_html=True)
st.sidebar.markdown(
    '<a href="https://us-east-1.quicksight.aws.amazon.com/sn/account/187419755406_SPS/dashboards/19ca18a9-c62b-4d22-94c3-b180f1cd9640/views/07e65948-7d03-4795-88e5-76143c5c09ce">'
    '<button style="'
    'background-color: white;'
    'border: 1px solid #cccccc;'
    'color: black;'
    'padding: 10px 24px;'
    'text-align: center;'
    'text-decoration: none;'
    'display: inline-block;'
    'font-size: 16px;'
    'margin: 4px 2px;'
    'cursor: pointer;'
    'border-radius: 4px;'
    'transition: background-color 0.3s;'
    'width: 100%;">'
    'Deep Dive Dashboard</button>'
    '</a>',
    unsafe_allow_html=True
)

# Add Occupancy WBR Dashboard button
st.sidebar.markdown(
    '<a href="https://us-east-1.quicksight.aws.amazon.com/sn/account/187419755406_SPS/dashboards/19ca18a9-c62b-4d22-94c3-b180f1cd9640/views/e7c15434-94c8-40a8-aafe-15b6be3c68da" target="_blank">'
    '<button style="'
    'background-color: white;'
    'border: 1px solid #cccccc;'
    'color: black;'
    'padding: 10px 24px;'
    'text-align: center;'
    'text-decoration: none;'
    'display: inline-block;'
    'font-size: 16px;'
    'margin: 4px 2px;'
    'cursor: pointer;'
    'border-radius: 4px;'
    'transition: background-color 0.3s;'
    'width: 100%;">'
    'Occupancy WBR Dashboard</button>'
    '</a>',
    unsafe_allow_html=True
)

# Data Upload section with reduced spacing
st.sidebar.markdown('<p class="sidebar-header">Data Upload</p>', unsafe_allow_html=True)
uploaded_files = st.sidebar.file_uploader(
r(
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

# Simple email template that matches the screenshot
email_template = """Hello team,

This email is to inform you about NPT hours that can be taken by DE associates for Seller, Brand and Vendor business units.

This will help improve our occupancy rate, which has been below the YTD target for the last 4 weeks, as shown below:

                Week 32   Week 33   Week 34   Week 35
Actual Occupancy %   67.5%     67.8%     66.2%     66.7%
YTD Goal %          78.5%     78.5%     78.5%     78.5%

In the table below, you have the available hours divided by weeks and Staff Groups:

{table_placeholder}

To request NPT, you can use the River link for NPT requests.

Note: Requests may be denied if we notice that the requested interval does not meet minimum coverage requirements.

Thank you for your support!

Best Regards,
EMEA WFM"""

def format_table_for_email(df):
    # Create a formatted string representation of the table
    table_rows = []
    
    # Add headers
    headers = [str(col) for col in df.columns]
    table_rows.append("    ".join(headers))
    
    # Add separator
    table_rows.append("-" * (len("    ".join(headers))))
    
    # Add data rows
    for _, row in df.iterrows():
        # Format numeric values with appropriate precision
        formatted_row = []
        for val in row:
            if isinstance(val, float):
                if val > 100:  # For capacity delta
                    formatted_row.append(f"{val:.1f}")
                else:  # For percentages
                    formatted_row.append(f"{val:.1f}%")
            else:
                   formatted_row.append(str(val))
        table_rows.append("    ".join(formatted_row))
    
    return "\n".join(table_rows)

# Process all uploaded files
if uploaded_files:
    all_data = pd.concat([process_file(file) for file in uploaded_files])
    
    available_weeks = sorted(all_data['Week'].unique(), reverse=True)
    available_weeks = [f'Week_{week}' for week in available_weeks]
    
    selected_weeks = st.sidebar.multiselect(
        'Select Weeks',
        available_weeks,
        defdefault=[available_weeks[0]]
    )
    
    selected_groups = st.sidebar.multiselect(
        'Select Staff Groups',
        all_data['Staff_GroGroup'].unique().tolist(),
        default=all_data['Staff_Group'].unique().tolist()
    )
    
    # New filter for Available/Unavailable staff groups
    availability_filter = st.sidebar.multiselect(
        'Available',
        ['Available', 'Unavailable'],
        default=['Available', 'Unavailable']
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
    display_df = display_df[display_df.columns.intersection(selected_weeks)]
    capacity_pivot = capacity_pivot[capacity_pivot.columns.intersection(selected_weeks)]
    
    display_df['Avg_Occupancy'] = display_df.mean(axis=1)
    display_df['Avg_Capacity_Delta'] = capacity_pivot.mean(axis=1)
    display_df = display_df.reset_index()
    
    formatted_df = display_df.copy()
    
    numeric_cols = [col for col in formatted_df.columns if col != 'Staff_Group']
    for col in numeric_cols:
        formatted_df[col] = pd.to_numeric(formatted_df[col], errors='coerce')

    def color_rows(row):
        avg_occupancy = row['Avg_Occupancy']
        colors = []
 )
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

    # Filter based on availability
    if 'Available' in availability_filter and 'Unavailable' not in availability_filter:
        styled_df = styled_df.data[styled_df.data['Avg_Occupancy'] <= 74]
    elif 'Unavailable' in availability_filter and 'Available' not in availability_filter:
        styled_df = styled_df.data[styled_df.data['Avg_Occupancy'] > 74]
    else:
        styled_df = styled_df.data
    
    row_height = 35
    total_height = len(styled_df) * row_height

    st.write("Occupancy Rates by Week (%) and Staff group & Delta hours available for Staff Group")
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

    email_table = format_table_for_email(formatted_df)
    
    st.sidebar.markdown('<p class="sidebar-header">Outlook</p>', unsafe_allow_html=True)
    subject = "NPT hours for DE Seller, Brand and Vendor | WKXX"
    email_body = email_template.format(table_placeholder=email_table)
    encoded_body = quote(email_body)
    st.sidebar.markdown(f'''
    <a href="mailto:?subject={quote(subject)}&body={encoded_body}" target="_blank">
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
    
    st.sidebar.markdown('<p class="sidebar-header">Outlook</p>', unsafe_allow_html=True)
    subject = "NPT hours for DE Seller, Brand and Vendor | WKXX"
    email_body = email_template.format(table_placeholder="[No data available]")
    encoded_body = quote(email_body)
    st.sidebar.markdown(f'''
    <a href="mailto:?subject={quote(subject)}&body={encoded_body}" target="_blank">
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
