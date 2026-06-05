# pages/1_Executive_Summary.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.preprocessing import preprocess_data
from utils.feature_engineering import engineer_features
from utils.emissions import emission_summary
from utils.esg import calculate_esg
from utils.insights import generate_insights

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Executive Summary",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Steel Industry Carbon Footprint & ESG Analytics")
st.markdown("---")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

if "data" not in st.session_state:

    uploaded_file = st.file_uploader(
        "Upload Steel Industry Dataset",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        df = preprocess_data(df)

        df = engineer_features(df)

        st.session_state["data"] = df

    else:
        st.info("Upload dataset to continue.")
        st.stop()

else:
    df = st.session_state["data"]

# ---------------------------------------------------
# DATE PARSING
# ---------------------------------------------------

date_col = None

for col in df.columns:

    if "date" in col.lower():
        date_col = col
        break

if date_col:

    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce"
    )

# ---------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------

total_emissions = df["CO2(tCO2)"].sum()

avg_daily_emissions = (
    df.groupby(df[date_col].dt.date)["CO2(tCO2)"]
    .sum()
    .mean()
    if date_col
    else df["CO2(tCO2)"].mean()
)

total_energy = df["Usage_kWh"].sum()

carbon_intensity = (
    total_emissions /
    total_energy
    if total_energy > 0
    else 0
)

esg_results = calculate_esg(df)

esg_score = esg_results.get(
    "score",
    0
)

active_alerts = 0

if "Alert_Level" in df.columns:

    active_alerts = len(
        df[df["Alert_Level"] == "High"]
    )

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.subheader("📈 Executive KPIs")

c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.metric(
        "Total Emissions",
        f"{total_emissions:,.2f}"
    )

with c2:
    st.metric(
        "Avg Daily CO₂",
        f"{avg_daily_emissions:,.2f}"
    )

with c3:
    st.metric(
        "Carbon Intensity",
        f"{carbon_intensity:.4f}"
    )

with c4:
    st.metric(
        "ESG Score",
        f"{esg_score:.0f}"
    )

with c5:
    st.metric(
        "Active Alerts",
        active_alerts
    )

with c6:
    st.metric(
        "Energy Usage",
        f"{total_energy:,.0f}"
    )

st.markdown("---")

# ---------------------------------------------------
# ESG GAUGE
# ---------------------------------------------------

left, right = st.columns([1, 2])

with left:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=esg_score,
            title={"text": "ESG Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 60], "color": "red"},
                    {"range": [60, 80], "color": "yellow"},
                    {"range": [80, 100], "color": "green"}
                ]
            }
        )
    )

    fig.update_layout(height=350)

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# ---------------------------------------------------
# MONTHLY EMISSIONS
# ---------------------------------------------------

with right:

    st.subheader("📉 Monthly Carbon Emissions")

    if date_col:

        monthly = (
            df
            .set_index(date_col)
            .resample("ME")
            ["CO2(tCO2)"]
            .sum()
            .reset_index()
        )

        fig = px.line(
            monthly,
            x=date_col,
            y="CO2(tCO2)",
            markers=True,
            title="Monthly Carbon Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
# ---------------------------------------------------
# LOAD TYPE ANALYSIS
# ---------------------------------------------------

st.subheader("⚙️ Emission Contribution by Load Type")

load_emission = (
    df.groupby("Load_Type")
    ["CO2(tCO2)"]
    .sum()
    .reset_index()
)

fig = px.pie(
    load_emission,
    names="Load_Type",
    values="CO2(tCO2)",
    hole=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# WEEKLY ENERGY CONSUMPTION
# ---------------------------------------------------

st.subheader("⚡ Weekly Energy Consumption")

if date_col:

    weekly = (
        df
        .set_index(date_col)
        .resample("W")
        ["Usage_kWh"]
        .sum()
        .reset_index()
    )

    fig = px.area(
        weekly,
        x=date_col,
        y="Usage_kWh",
        title="Weekly Energy Usage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# ---------------------------------------------------
# ENERGY VS EMISSIONS
# ---------------------------------------------------

st.subheader("🔍 Energy Usage vs Carbon Emissions")

fig = px.scatter(
    df,
    x="Usage_kWh",
    y="CO2(tCO2)",
    color="Load_Type",
    size="Usage_kWh",
    opacity=0.7
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# LOAD TYPE SUMMARY
# ---------------------------------------------------

st.subheader("🏭 Load Type Summary")

load_summary = (
    df.groupby("Load_Type")
    .agg(
        Energy=("Usage_kWh", "sum"),
        Emissions=("CO2(tCO2)", "sum"),
        Avg_Emission=("CO2(tCO2)", "mean")
    )
    .reset_index()
)

st.dataframe(
    load_summary,
    use_container_width=True
)

# ---------------------------------------------------
# TOP EMISSION DAYS
# ---------------------------------------------------

if date_col:

    st.subheader("🚨 Highest Emission Days")

    top_days = (
        df.groupby(df[date_col].dt.date)
        ["CO2(tCO2)"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(
        top_days,
        use_container_width=True
    )

# ---------------------------------------------------
# AI INSIGHTS
# ---------------------------------------------------

st.subheader("🤖 Sustainability Insights")

insights = generate_insights(df)

for insight in insights:

    st.success(insight)

# ---------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------

with st.expander("View Dataset Preview"):

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Steel Industry Carbon Footprint & ESG Analytics Platform | Executive Dashboard"
)
