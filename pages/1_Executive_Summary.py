import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Executive Summary",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Executive Summary")
st.markdown(
    "Enterprise ESG & Carbon Intelligence Dashboard"
)

# ==========================================
# DATA LOADER
# ==========================================

@st.cache_data
def load_data():

    try:
        return pd.read_csv(
            "data/Steel_industry_data.csv"
        )

    except Exception:
        return None


df = load_data()

if df is None:
    st.error(
        "Dataset not found.\n\n"
        "Place Steel_industry_data.csv inside data/ folder."
    )
    st.stop()

# ==========================================
# DATE PROCESSING
# ==========================================

if "Date" in df.columns:

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df = df.sort_values("Date")

# ==========================================
# BASIC CLEANING
# ==========================================

df = df.drop_duplicates()

df = df.fillna(
    df.select_dtypes(include=np.number).median()
)

# ==========================================
# FEATURE ENGINEERING
# ==========================================

df["Carbon_Intensity"] = (
    df["CO2(tCO2)"]
    /
    (df["Usage_kWh"] + 1)
)

df["Total_Reactive_Power"] = (
    df["Lagging_Current_Reactive.Power_kVarh"]
    +
    df["Leading_Current_Reactive_Power_kVarh"]
)

# ==========================================
# KPI CALCULATIONS
# ==========================================

total_emissions = df["CO2(tCO2)"].sum()

avg_daily_emission = (
    df.groupby(df["Date"].dt.date)
      ["CO2(tCO2)"]
      .sum()
      .mean()
)

total_energy = df["Usage_kWh"].sum()

avg_carbon_intensity = (
    df["Carbon_Intensity"].mean()
)

# ==========================================
# ESG SCORE
# ==========================================

emission_score = max(
    0,
    100 - (df["CO2(tCO2)"].mean() * 100)
)

efficiency_score = min(
    100,
    df["Lagging_Current_Power_Factor"].mean()
)

esg_score = round(
    (emission_score * 0.6)
    +
    (efficiency_score * 0.4),
    2
)

# ==========================================
# ALERTS
# ==========================================

alerts = 0

usage_threshold = (
    df["Usage_kWh"].median() * 1.5
)

alerts += (
    df["Usage_kWh"] > usage_threshold
).sum()

# ==========================================
# KPI ROW
# ==========================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Emissions",
        f"{total_emissions:,.2f} tCO₂"
    )

with col2:
    st.metric(
        "Avg Daily Emissions",
        f"{avg_daily_emission:,.2f}"
    )

with col3:
    st.metric(
        "Energy Usage",
        f"{total_energy:,.0f} kWh"
    )

with col4:
    st.metric(
        "Carbon Intensity",
        f"{avg_carbon_intensity:.4f}"
    )

with col5:
    st.metric(
        "ESG Score",
        f"{esg_score:.0f}/100"
    )

# ==========================================
# ESG GAUGE
# ==========================================

col1, col2 = st.columns([1, 2])

with col1:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=esg_score,
            title={"text": "ESG Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"thickness": 0.3},
                "steps": [
                    {"range": [0, 40]},
                    {"color": "red"},
                    {"range": [40, 70]},
                    {"color": "orange"},
                    {"range": [70, 100]},
                    {"color": "green"},
                ],
            },
        )
    )

    fig.update_layout(height=350)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# EMISSION TREND
# ==========================================

with col2:

    daily = (
        df.groupby(df["Date"].dt.date)
        ["CO2(tCO2)"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        daily,
        x="Date",
        y="CO2(tCO2)",
        title="Carbon Emission Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# LOAD TYPE ANALYSIS
# ==========================================

col1, col2 = st.columns(2)

with col1:

    load_summary = (
        df.groupby("Load_Type")
        ["CO2(tCO2)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        load_summary,
        values="CO2(tCO2)",
        names="Load_Type",
        title="Emission Contribution by Load Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    usage_summary = (
        df.groupby("Load_Type")
        ["Usage_kWh"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        usage_summary,
        x="Load_Type",
        y="Usage_kWh",
        title="Average Energy Usage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# MONTHLY ANALYSIS
# ==========================================

st.subheader("Monthly Carbon Analysis")

monthly = (
    df.groupby(
        df["Date"].dt.to_period("M")
    )["CO2(tCO2)"]
    .sum()
    .reset_index()
)

monthly["Date"] = (
    monthly["Date"]
    .astype(str)
)

fig = px.bar(
    monthly,
    x="Date",
    y="CO2(tCO2)",
    title="Monthly Emissions"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# ALERT CENTER
# ==========================================

st.subheader("Active Alerts")

alert_df = df[
    df["Usage_kWh"]
    >
    usage_threshold
]

if len(alert_df) > 0:

    st.warning(
        f"{len(alert_df)} high-energy records detected"
    )

    st.dataframe(
        alert_df[
            [
                "Date",
                "Usage_kWh",
                "CO2(tCO2)",
                "Load_Type"
            ]
        ].head(20),
        use_container_width=True
    )

else:

    st.success(
        "No active energy consumption alerts."
    )

# ==========================================
# EXECUTIVE INSIGHTS
# ==========================================

st.subheader("AI Executive Insights")

top_load = (
    load_summary
    .sort_values(
        "CO2(tCO2)",
        ascending=False
    )
    .iloc[0]
)

peak_day = (
    df.groupby("Day_of_week")
    ["Usage_kWh"]
    .mean()
    .idxmax()
)

st.info(
    f"""
• {top_load['Load_Type']} contributed the highest emissions.

• Total facility emissions reached {total_emissions:,.2f} tCO₂.

• Average carbon intensity is {avg_carbon_intensity:.4f}.

• Peak energy usage occurs on {peak_day}.

• ESG score currently stands at {esg_score}/100.

• {alerts} potential high-energy alerts detected.
"""
)

# ==========================================
# DATA SNAPSHOT
# ==========================================

with st.expander(
    "Dataset Snapshot"
):

    st.dataframe(
        df.head(),
        use_container_width=True
    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "Steel Industry Carbon Footprint & ESG Analytics Platform v2.0"
)
