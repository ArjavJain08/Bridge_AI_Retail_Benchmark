import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os
import api_pipeline # This imports your data engine!

st.set_page_config(page_title="Bridge AI - Competitive Intelligence", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    div[data-testid="stMetric"] {background-color: #1a1f2c; border: 1px solid #2e364f; padding: 15px; border-radius: 10px;}
    div[data-testid="stMetric"] label {color: #94a3b8 !important; font-weight: 600 !important;}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {color: #38bdf8 !important;}
</style>
""", unsafe_allow_html=True)

# --- THE SMART DATA LOADER ---
@st.cache_data(ttl=600)
def load_data():
    # 1. If the database doesn't exist, tell the pipeline to build it right now!
    if not os.path.exists('retail_advanced.db'):
        api_pipeline.run_pipeline()
        
    # 2. Connect to the newly built database
    conn = sqlite3.connect('retail_advanced.db')
    data = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return data

# We can remove the try/except error block entirely because it fixes itself now!
df = load_data()

# ... (The rest of your dashboard code starting with st.title remains exactly the same below here) ...
st.title("⚡ Retail Price, Promotion & Brand Positioning")
