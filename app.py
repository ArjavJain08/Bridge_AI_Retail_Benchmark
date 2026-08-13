import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Bridge AI - Competitive Intelligence", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    div[data-testid="stMetric"] {background-color: #1a1f2c; border: 1px solid #2e364f; padding: 15px; border-radius: 10px;}
    div[data-testid="stMetric"] label {color: #94a3b8 !important; font-weight: 600 !important;}
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {color: #38bdf8 !important;}
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def load_data():
    conn = sqlite3.connect('retail_advanced.db')
    data = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()
    return data

try:
    df = load_data()
except Exception:
    st.error("No database found. Please run python api_pipeline.py first.")
    st.stop()

st.title("⚡ Retail Price, Promotion & Brand Positioning")
st.markdown("#### Side-by-Side Competitive Benchmark Across Retail Platforms")
st.markdown("---")

st.sidebar.header("🔍 Global Benchmark Filters")
selected_platforms = st.sidebar.multiselect("Platform / Country", options=df['platform'].unique(), default=df['platform'].unique())
selected_brands = st.sidebar.multiselect("Chip Brand", options=df['brand'].unique(), default=df['brand'].unique())
selected_categories = st.sidebar.multiselect("Product Category", options=df['category'].unique(), default=df['category'].unique())

filtered_df = df[(df['platform'].isin(selected_platforms)) & (df['brand'].isin(selected_brands)) & (df['category'].isin(selected_categories))]

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Tracked SKUs", len(filtered_df))
kpi2.metric("Average Price", f"${filtered_df['price'].mean():,.2f}")
kpi3.metric("Active Promo Rate", f"{(filtered_df['is_on_promotion'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0:.1f}%")
kpi4.metric("Brand Compliance", f"{filtered_df['compliance_score'].mean():.1f}%")
kpi5.metric("Price Drop Alerts", (filtered_df['alert_flag'] == "🚨 SHARP DROP ALERT").sum())

tab1, tab2, tab3, tab4 = st.tabs(["📊 Visbility Share", "💰 Pricing & AI Alerts", "🛡️ Compliance Matrix", "🔎 SKU Explorer & Export"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Share of Shelf (%)")
        fig_sos = px.pie(filtered_df, names='brand', hole=0.45, color_discrete_sequence=px.colors.qualitative.Dark24)
        fig_sos.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
        st.plotly_chart(fig_sos, use_container_width=True)
    with c2:
        st.subheader("Homepage Banner Share")
        banners = filtered_df[filtered_df['has_homepage_banner'] == 1]['brand'].value_counts().reset_index()
        fig_banner = px.bar(banners, x='brand', y='count', color='brand')
        fig_banner.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
        st.plotly_chart(fig_banner, use_container_width=True)

with tab2:
    st.subheader("Price Positioning by Brand ($)")
    st.plotly_chart(px.box(filtered_df, x='brand', y='price', color='brand'), use_container_width=True)
    st.subheader("Automated AI Price Drop Alerts")
    anomalies = filtered_df[filtered_df['alert_flag'] == "🚨 SHARP DROP ALERT"]
    if not anomalies.empty:
        st.error("🚨 Anomalous price drops detected:")
        st.dataframe(anomalies[['sku', 'brand', 'price', 'list_price', 'discount_pct', 'platform']])
    else:
        st.success("✅ Prices stable.")

with tab3:
    st.subheader("Brand Compliance (85% Notebook / 15% Desktop Weighting)")
    rollup = []
    for b in filtered_df['brand'].unique():
        b_df = filtered_df[filtered_df['brand'] == b]
        nb = b_df[b_df['category'] == 'Notebook']['compliance_score'].mean()
        dt = b_df[b_df['category'] == 'Desktop']['compliance_score'].mean()
        nb = nb if not pd.isna(nb) else 0.0
        dt = dt if not pd.isna(dt) else 0.0
        rollup.append({'Brand': b, 'Notebook (85%)': f"{nb:.1f}%", 'Desktop (15%)': f"{dt:.1f}%", 'Weighted Total': f"{(0.85*nb + 0.15*dt):.1f}%"})
    st.table(pd.DataFrame(rollup))

with tab4:
    st.subheader("SKU Explorer: Full Attribute Drill-down")
    st.dataframe(filtered_df, use_container_width=True)
    c1, c2 = st.columns(2)
    c1.download_button("📥 Export as PSV", filtered_df.to_csv(sep='|', index=False), "benchmark.psv")
    c2.download_button("📥 Export as CSV", filtered_df.to_csv(index=False), "benchmark.csv")
