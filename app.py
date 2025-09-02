import streamlit as st
import pandas as pd

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

st.title('Workforce Capacity Analysis Dashboard')

# Display the dataframe
st.write(df)

# Simple metrics
st.metric("Average Occupancy", f"{df['Occupancy_Rate'].mean():.1f}%")
