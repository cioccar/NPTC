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
    'Occupancy_Rate': [
        67.23, 62.04, 63.40, 65.90, 64.07, 65.76,
        60.60, 70.97, 72.52, 53.65, 70.57, 66.85,
        69.12, 65.71
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
    
    # Sidebar
    st.sidebar.header('Filters')
    
    # Staff Group selection
    selected_groups = st.sidebar.multiselect(
        'Select Staff Groups',
        df['Staff_Group'].tolist(),
        default=df['Staff_Group'].tolist()
    )
    
    # Filter dataframe
    filtered_df = df[df['Staff_Group'].isin(selected_groups)]
    
    # Summary metrics
    st.header('Summary')
    col1, col2, col3 = st.columns(3)
    
    avg_occupancy = filtered_df['Occupancy_Rate'].mean()
    total_delta = filtered_df['Capacity_Delta_Hours'].sum()
    groups_below_target = len(filtered_df[filtered_df['Occupancy_Rate'] < 75])
    
    col1.metric("Average Occupancy", f"{avg_occupancy:.1f}%")
    col2.metric("Total Unused Capacity", f"{total_delta:.0f} hrs")
    col3.metric("Groups Below Target", groups_below_target)
    
    # Tables
    st.subheader('Occupancy Rates')
    occupancy_df = filtered_df[['Staff_Group', 'Occupancy_Rate']].sort_values('Occupancy_Rate', ascending=False)
    st.dataframe(
        occupancy_df.style.format({'Occupancy_Rate': '{:.1f}%'})
        .background_gradient(subset=['Occupancy_Rate'], cmap='RdYlGn'),
        use_container_width=True
    )
    
    st.subheader('Available Capacity')
    capacity_df = filtered_df[['Staff_Group', 'Capacity_Delta_Hours']].sort_values('Capacity_Delta_Hours', ascending=False)
    st.dataframe(
        capacity_df.style.format({'Capacity_Delta_Hours': '{:.1f}'})
        .background_gradient(subset=['Capacity_Delta_Hours'], cmap='RdYlGn_r'),
        use_container_width=True
    )
    
    # Chart
    st.subheader('Occupancy vs Target (75%)')
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=filtered_df['Staff_Group'],
        y=filtered_df['Occupancy_Rate'],
        name='Current Occupancy'
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
        yaxis_title="Occupancy Rate (%)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
