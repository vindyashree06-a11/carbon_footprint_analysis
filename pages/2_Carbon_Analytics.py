# pages/2_Carbon_Analytics.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.emissions import emission_summary

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Carbon Analytics",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 Carbon Footprint Analytics")
st.markdown("---")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if "data" not in st.session_state:
    st.warning("Please upload dataset from Executive Summary page.")
    st.stop()

df = st.session_state["data"].copy()

# --------------------------------------------------
# DATE HANDLING
# --------------------------------------------------

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

# --------------------------------------------------
# EMISSION SUMMARY
# --------------------------------------------------

summary = emission_summary(df)

total_emissions = summary["total_emission"]
avg_emissions = summary["average_emission"]
annualized = summary["annualized_emission"]

daily_emissions = (
    df.groupby(df[date_col].dt.date)["CO2(tCO2)"]
    .sum()
    .reset_index()
)

monthly_emissions = (
    df
    .set_index(date_col)
    .resample("ME")
    ["CO2(tCO2)"]
    .sum()
    .reset_index()
)

weekly_emissions = (
    df.groupby(
        pd.Grouper(
            key=date_col,
            freq="W"
        )
    )["CO2(tCO2)"]
    .sum()
    .reset_index()
)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.subheader("📊 Carbon KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total CO₂",
        f"{total_emissions:,.2f}"
    )

with c2:
    st.metric(
        "Average CO₂",
        f"{avg_emissions:.4f}"
    )

with c3:
    st.metric(
        "Annualized CO₂",
        f"{annualized:,.2f}"
    )

with c4:

    carbon_intensity = (
        df["CO2(tCO2)"].sum()
        /
        df["Usage_kWh"].sum()
    )

    st.metric(
        "Carbon Intensity",
        f"{carbon_intensity:.4f}"
    )

st.markdown("---")

# --------------------------------------------------
# DAILY EMISSIONS
# --------------------------------------------------

st.subheader("📈 Daily Carbon Emissions")

fig = px.line(
    daily_emissions,
    x=date_col,
    y="CO2(tCO2)",
    markers=True
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# WEEKLY EMISSIONS
# --------------------------------------------------

st.subheader("📅 Weekly Emission Analysis")

fig = px.area(
    weekly_emissions,
    x=date_col,
    y="CO2(tCO2)"
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# MONTHLY EMISSIONS
# --------------------------------------------------

st.subheader("🗓 Monthly Carbon Trend")

fig = px.bar(
    monthly_emissions,
    x=date_col,
    y="CO2(tCO2)",
    text_auto=True
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# EMISSION DISTRIBUTION
# --------------------------------------------------

st.subheader("📉 Emission Distribution")

fig = px.histogram(
    df,
    x="CO2(tCO2)",
    nbins=50
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# LOAD TYPE CONTRIBUTION
# --------------------------------------------------

st.subheader("🏭 Emission Contribution By Load Type")

load_emissions = (
    df.groupby("Load_Type")
    ["CO2(tCO2)"]
    .sum()
    .reset_index()
)

fig = px.pie(
    load_emissions,
    names="Load_Type",
    values="CO2(tCO2)",
    hole=0.5
)

fig.update_layout(height=550)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# LOAD TYPE COMPARISON
# --------------------------------------------------

st.subheader("⚙ Load Type Carbon Comparison")

fig = px.bar(
    load_emissions,
    x="Load_Type",
    y="CO2(tCO2)",
    color="Load_Type",
    text_auto=True
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# CARBON INTENSITY TREND
# --------------------------------------------------

st.subheader("🌍 Carbon Intensity Trend")

daily_intensity = (
    df.groupby(df[date_col].dt.date)
    .agg({
        "CO2(tCO2)": "sum",
        "Usage_kWh": "sum"
    })
    .reset_index()
)

daily_intensity["Carbon_Intensity"] = (
    daily_intensity["CO2(tCO2)"]
    /
    daily_intensity["Usage_kWh"]
)

fig = px.line(
    daily_intensity,
    x=date_col,
    y="Carbon_Intensity",
    markers=True
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# HEATMAP
# --------------------------------------------------

st.subheader("🔥 Weekly Energy Usage Heatmap")

heatmap_data = pd.pivot_table(
    df,
    values="Usage_kWh",
    index="Day_of_week",
    columns="Load_Type",
    aggfunc="mean"
)

fig = px.imshow(
    heatmap_data,
    text_auto=True,
    aspect="auto"
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# TOP EMISSION PERIODS
# --------------------------------------------------

st.subheader("🚨 Top 20 Carbon Emission Records")

top_emissions = (
    df.sort_values(
        "CO2(tCO2)",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_emissions,
    use_container_width=True
)

# --------------------------------------------------
# EMISSION STATISTICS
# --------------------------------------------------

st.subheader("📋 Emission Statistics")

stats = pd.DataFrame({
    "Metric": [
        "Minimum",
        "Maximum",
        "Mean",
        "Median",
        "Std Dev",
        "Variance"
    ],
    "Value": [
        df["CO2(tCO2)"].min(),
        df["CO2(tCO2)"].max(),
        df["CO2(tCO2)"].mean(),
        df["CO2(tCO2)"].median(),
        df["CO2(tCO2)"].std(),
        df["CO2(tCO2)"].var()
    ]
})

st.dataframe(
    stats,
    use_container_width=True
)

# --------------------------------------------------
# SUSTAINABILITY SCORECARD
# --------------------------------------------------

st.subheader("🌱 Sustainability Scorecard")

emission_target = total_emissions * 0.90

reduction_needed = (
    total_emissions - emission_target
)

progress = (
    (emission_target / total_emissions)
    * 100
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Current CO₂",
        f"{total_emissions:,.2f}"
    )

with col2:
    st.metric(
        "Target CO₂",
        f"{emission_target:,.2f}"
    )

with col3:
    st.metric(
        "Reduction Required",
        f"{reduction_needed:,.2f}"
    )

st.progress(progress / 100)

# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

st.subheader("⬇ Export Carbon Analytics")

csv = monthly_emissions.to_csv(
    index=False
)

st.download_button(
    label="Download Monthly Carbon Report",
    data=csv,
    file_name="monthly_carbon_report.csv",
    mime="text/csv"
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "Carbon Analytics Module | Steel Industry Carbon Footprint & ESG Analytics Platform"
)
