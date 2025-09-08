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

# Email Button section (placed after Data Upload)
st.sidebar.markdown('<p class="sidebar-header">Generate Email</p>', unsafe_allow_html=True)
st.sidebar.markdown('''
<a href="mailto:?subject=NPT%20Hours%20Available&body=Please%20find%20the%20NPT%20hours%20available%20report%20in%20the%20following%20dashboard:%0D%0A%0D%0Ahttps://us-east-1.quicksight.aws.amazon.com/sn/account/187419755406_SPS/dashboards/19ca18a9-c62b-4d22-94c3-b180f1cd9640/views/c7b9defa-5e1a-46b6-971a-dfecf4e7c45c" target="_blank">
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

# [Rest of your existing code goes here]
