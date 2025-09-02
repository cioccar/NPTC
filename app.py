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
    min_occupancy = st.sidebar.slider('Minimum Occupancy Rate', 0, 100, 0)
    max_delta = st.sidebar.slider('Maximum Capacity Delta Hours', 0, 500, 500)
    
    # Filter data
    filtered_df = df[
        (df['Occupancy_Rate'] >= min_occupancy) & 
        (df['Capacity_Delta_Hours'] <= max_delta)
    ]
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Occupancy Rates vs Target (75%)')
        fig_occupancy = go.Figure()
        fig_occupancy.add_trace(go.Bar(
            x=filtered_df['Staff_Group'],
            y=filtered_df['Occupancy_Rate'],
            name='Current Occupancy'
        ))
        fig_occupancy.add_hline(
            y=75, 
            line_dash="dash", 
            line_color="red",
            annotation_text="Target 75%"
        )
        fig_occupancy.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        st.plotly_chart(fig_occupancy, use_container_width=True)

    with col2:
        st.subheader('Unused Capacity (Hours)')
        fig_capacity = px.bar(
            filtered_df,
            x='Staff_Group',
            y='Capacity_Delta_Hours',
            color='Capacity_Delta_Hours',
            color_continuous_scale='Reds'
        )
        fig_capacity.update_layout(
            xaxis_tickangle=-45,
            height=500
        )
        st.plotly_chart(fig_capacity, use_container_width=True)
    
    # Data table
    st.subheader('Detailed Data')
    st.dataframe(
        filtered_df.style.background_gradient(
            subset=['Occupancy_Rate', 'Capacity_Delta_Hours'],
            cmap='RdYlGn_r'
        )
    )
    
    # Key Insights
    st.subheader('Key Insights')
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.metric(
            "Average Occupancy Rate", 
            f"{filtered_df['Occupancy_Rate'].mean():.1f}%",
            f"{filtered_df['Occupancy_Rate'].mean() - 75:.1f}%"
        )
    
    with col4:
        st.metric(
            "Total Unused Capacity", 
            f"{filtered_df['Capacity_Delta_Hours'].sum():.0f} hours"
        )
    
    with col5:
        st.metric(
            "Groups Below Target", 
            f"{len(filtered_df[filtered_df['Occupancy_Rate'] < 75])}"
        )

if __name__ == "__main__":
    main()
