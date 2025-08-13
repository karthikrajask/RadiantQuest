
# #############################################################################
# IMPORTS
# #############################################################################
import pandas as pd
import json

import streamlit as st
from streamlit_folium import st_folium

from app_banner import generate_banner
from app_dataloader import load_investment_data

import app_page_projects
import app_page_investment_navigator
import app_page_tender_navigator
import warnings
warnings.filterwarnings("ignore")






# #############################################################################
# STREAMLIT PAGE CONFIGRUATION
# #############################################################################

    # Streamlit page config
st.set_page_config(layout="wide")




# #############################################################################
# DATA LOADING
# #############################################################################    

@st.cache_data
def load_data():
    # Project Data
    project_data = pd.read_csv("../../data/processed_data/project_data.csv")
    
    # Investment Data
    investment_data, investment_data_india = load_investment_data()
        
    # Tender Data
    tender_data = pd.read_csv("../../data/processed_data/gov_tenders_processed.csv")
    
    # Geo Data
    with open("../../data/geography/Indian_States.json", "r", encoding="utf-8") as f:
        state_geo = json.load(f)
        
    # Return Data
    return project_data, investment_data, investment_data_india, tender_data, state_geo
project_data, investment_data, investment_data_india, tender_data, state_geo = load_data()




# #############################################################################
# USER INTERFACE LAYOUT
# #############################################################################    

# ########### BANNER
generate_banner()

# ########### TABS
tab_names = [
    "🗺️ Projects Overview",
    # "☀️ Solar Potential Explorer",
    "📈 Investment Navigator",
    "📄 Tender Explorer"
]
tabs = st.tabs(tab_names)

# ########### PROJECTS OVERVIEW
i = 0
with tabs[0]:
    col1, col2 = st.columns([2, 5])  # Adjust the ratio as needed

    # Filter Pane
    with col1:
        st.markdown("#### 🔍 Filter Projects")
        with st.container(height=600):  # Adjust height as needed
            filtered = app_page_projects.generate_filter_pane(i, project_data)

    # Map
    with col2:
        app_page_projects.generate_map(i, filtered, st_folium)

# ########### INVESTMENT NAVIGATOR
i = 1
with tabs[1]:
    col1, col2, col3 = st.columns([2, 5, 2])  # Adjust the ratio as needed

    # Filter Pane
    with col1:
        st.markdown("#### 🔍 Factor Explorer")
        with st.container(height=180):  # Adjust height as needed
            filtered = app_page_investment_navigator.generate_filter_pane(i, project_data, investment_data)
        st.markdown("#### 📊 Your Project Details")
        with st.container(height=400):  # Adjust height as needed
            app_page_investment_navigator.generate_company_details(i, project_data)
    # Map
    with col2:
        state_name = app_page_investment_navigator.generate_map(i, filtered, st_folium, state_geo)

    # Calculator
    with col3:
        st.markdown("#### 💰 Projected Business Statement")
        with st.container(height=600):  # Adjust height as needed
            app_page_investment_navigator.business_calculator_pane(i, state_name, project_data, investment_data)
        
# ########### TENDER NAVIGATOR
i = 2
with tabs[2]:
    col1, col2 = st.columns([2, 5])  # Adjust the ratio as needed

    with col1:
        # Filter Pane (top 50%)
        st.markdown("#### 🔍 Find Tenders")
        with st.container(height=250):  # Adjust height as needed
            filtered = app_page_tender_navigator.generate_filter_pane(i, tender_data)

        # Scrollable Results (bottom 50%)
        st.markdown("#### 📋 Tenders")
        with st.container(height=350):  # Adjust height as needed
            if filtered.empty:
                st.info("No tenders match the selected filters.")
            else:
                for idx, row in filtered.iterrows():
                    st.markdown(
                        f"""
                        <div style="padding:8px 0; border-bottom:1px solid #eee;">
                            ({row['tender_id']}) <b>{row['tender_title']}</b> <br>
                            <span style="color: #888;">{row['location']}, {row['tender_date']}, <a href="{row['tender_corrigendum']}">Details</a></span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    with col2:
        app_page_tender_navigator.generate_map(i, filtered, st_folium)