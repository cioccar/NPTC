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
        'Week': df['Period by'].str.extract(r'Week 
