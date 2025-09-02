import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Create the data
data = {
    'Staff_Group': [
        'DE_BRAND_CW_DE', 'DE_BRAND_PCW_DE', 'DE_FBA_CW_DE', 
        'DE_FBA_ILAC_CW_DE', 'DE_FBA_ILAC_PCW_DE', 'DE_FBA_ILAC_WI_DE',
        'DE_FBA_PCW_DE', 'DE_FBA_WI_DE', 'DE_KYC_PCW_DE', 
        'DE_M@_PCW_DE', 'DE_M@_WI_DE', 'DE_MAT_CW_DE',
        'DE_VAT_CW_DE', 'DE_VAT_PCW_DE'
    ],
    'Week_35': [
        67.23, 67.92, 62.22, 67.59, 60.90, 65.76,
        60.96, 70.97, 75.37, 49.57, 70.57, 68.21,
        69.12, 65.71
    ],
    'Week_34': [
        61.02, 63.57, 63.40, 65.90, 64.07, 63.94,
        55.36, 68.19, 71.59, 53.65, 68.28, 66.85,
        67.91, 63.56
    ],
    'Capacity_Delta_Hours': [
        433.81, 159.23, 240.71, 339.25, 169.99, 60.80,
        202.12, 37.52, 98.84, 30.60, 11.82, 87.74,
        50.54, 51.14
    ]
}

df = pd.DataFrame(data)

def main():
    st.title('Workforce Capacity Analysis Dashboard')
    
    # Sidebar Filters
    st.sidebar.header('Filters')
    
    # Week selection
    selected_week = st.sidebar.selectbox(
        'Select Week',
        ['Week_35', 'Week_34'],
        index=0
    )
    
    # Staff Group selection
    selected_groups = st.sidebar.multiselect(
        'Select Staff Groups',
        df['Staff_Group'].tolist(),
        default=df['Staff_Group'].tolist()
    )
    
    # Filter dataframe based on selection
    filtered_df = df[df['Staff_Group'].isin(selected_groups)].copy()
    
    # Calculate trend
    filtered_df['Current_Week_Occupancy'] = filtered_df[selected_week]
    filtered_df['Previous_Week_Occupancy'] = filtered_df['Week_34'] if selected_week == 'Week_35' else None
    filtered_df['Trend'] = filtered_df['Current_Week_Occupancy'] - filtered_df['Previous_Week_Occupancy']
    
    # Summary Section
    st.header(f'Occupancy Summary - {selected_week}')
    
    cols = st.columns(3)
    
    # Calculate metrics for filtered data
    avg_occupancy = filtered_df['Current_Week_Occupancy'].mean()
    total_delta = filtered_df['Capacity_Delta_Hours'].sum()
    groups_below_target = len(filtered_df[filtered_df['Current_Week_Occupancy'] < 75])
    
    cols[0].metric("Average Occupancy", f"{avg_occupancy:.1f}%")
    cols[1].metric("Total Unused Capacity", f"{total_delta:.0f} hrs")
    cols[2].metric("Groups Below Target", groups_below_target)
    
    # Occupancy Trends Table
    st.subheader('Weekly Occupancy Trends')
    
    trend_df = filtered_df[['Staff_Group', 'Current_Week_Occupancy', 'Previous_Week_Occupancy', 'Trend']]
    trend_df = trend_df.sort_values('Current_Week_Occupancy', ascending=False)
    
    def color_trend(val):
        if pd.isna(val):
            return ''
        color = 'green' if val > 0 else 'red'
        return f'color: {color}'
    
    styled_trend = trend_df.style\
        .format({
            'Current_Week_Occupancy': '{:.1f}%',
            'Previous_Week_Occupancy': '{:.1f}%',
            'Trend': '{:+.1f}%'
        })\
        .applymap(color_trend, subset=['Trend'])\
        .background_gradient(subset=['Current_Week_Occupancy'], cmap='RdYlGn')
    
    st.dataframe(styled_trend, use_container_width=True)
    
    # Capacity Delta Hours Table
    st.subheader('Available Capacity by Staff Group')
    
    capacity_df = filtered_df[['Staff_Group', 'Capacity_Delta_Hours']]\
        .sort_values('Capacity_Delta_Hours', ascending=False)
    
    styled_capacity = capacity_df.style\
        .format({
            'Capacity_Delta_Hours': '{:.1f}'
        })\
        .background_gradient(subset=['Capacity_Delta_Hours'], cmap='RdYlGn_r')
    
    st.dataframe(styled_capacity, use_container_width=True)
    
    # Visualization
    st.subheader('Occupancy vs Target (75%)')
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=filtered_df['Staff_Group'],
        y=filtered_df['Current_Week_Occupancy'],
        name='Current Week'
    ))
    
    fig.add_hline(
        y=75,
        line_dash="dash",
        line_color="red",
        annotation_text="Target 75%"
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        yaxis_title="Occupancy Rate (%)",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
