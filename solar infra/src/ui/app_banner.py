import warnings
warnings.filterwarnings("ignore")

import logging
logging.getLogger('streamlit').setLevel(logging.ERROR)

import streamlit as st
st.set_option('client.showErrorDetails', False)
def generate_banner():
    st.image("banner.png", use_column_width=True)

