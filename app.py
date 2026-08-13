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

# --- THE BULLETPROOF DATA LOADER ---
@st.cache_data(ttl=600)
def load_data():
    try:
        # 1. First, try to read the data normally
        conn = sqlite3.connect('retail_advanced.db')
        data = pd.read_sql_query("SELECT * FROM products", conn)
        conn.close()
        return data
    except Exception:
        # 2. If it crashes (because the file is empty or missing), build it!
        import api_pipeline
        api_pipeline.run_pipeline()
        
        # 3. Now connect to the freshly built data
        conn = sqlite3.connect('retail_advanced.db')
        data = pd.read_sql_query("SELECT * FROM products", conn)
        conn.close()
        return data

df = load_data()
