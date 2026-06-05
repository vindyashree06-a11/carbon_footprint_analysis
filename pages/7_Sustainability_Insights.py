# pages/7_Sustainability_Insights.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Sustainability Insights",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Sustainability Insights Center")
st.markdown("---")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

if "data" not in st.session_state:
    st.warning(
        "Please upload dataset from Executive Summary page."
    )
    st.stop()

df = st.session_state["data"].copy()

# ---------------------------------------------------------
# DATE COLUMN
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# CORE SUSTAINABILITY METRICS
# ---------------------------------------------------------

total_energy = df["Usage_kWh"].sum()

total_emissions = df["CO2(tCO2)"].sum()

avg_energy = df["Usage_kWh"].mean()

avg_emissions = df["CO2(tCO2)"].mean()

carbon_intensity = (
    total_emissions /
    total_energy
)

energy_efficiency = (
    total_energy /
    total_emissions
)

# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.subheader("📊 Sustainability KPIs")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Total Energy",
        f"{total_energy:,.0f} kWh"
    )

with c2:
    st.metric(
        "Total CO₂",
        f"{total_emissions:,.2f}"
    )

with c3:
    st.metric(
        "Carbon Intensity",
        f"{carbon_intensity:.5f}"
    )

with c4:
    st.metric(
        "Energy Efficiency",
        f"{energy_efficiency:.2f}"
    )

with c5:
    sustainability_score = max(
        0,
        min(
            100,
            100 - (carbon_intensity * 1000)
        )
    )

    st.metric(
        "Sustainability Score",
        f"{sustainability_score:.0f}"
    )

st.markdown("---")

# ---------------------------------------------------------
# SUSTAINABILITY GAUGE
# ---------------------------------------------------------

st.subheader("🌱 Sustainability Score")

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=sustainability_score,
        title={
            "text":
            "Sustainability Index"
        },
        gauge={
            "axis": {
                "range": [0, 100]
            },
            "steps": [
                {
                    "range": [0, 50],
                    "color": "#ff4b4b"
                },
                {
                    "range": [50, 75],
                    "color": "#f7c948"
                },
                {
                    "range": [75, 100],
                    "color": "#00cc96"
                }
            ]
        }
    )
)

fig.update_layout(
    height=400
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# MONTHLY SUSTAINABILITY TREND
# ---------------------------------------------------------

if date_col:

    st.subheader(
        "📈 Sustainability Progress Trend"
    )

    monthly = (
        df.groupby(
            pd.Grouper(
                key=date_col,
                freq="M"
            )
        )
        .agg({
            "Usage_kWh": "sum",
            "CO2(tCO2)": "sum"
        })
        .reset_index()
    )

    monthly["Carbon_Intensity"] = (
        monthly["CO2(tCO2)"]
        /
        monthly["Usage_kWh"]
    )

    fig = px.line(
        monthly,
        x=date_col,
        y="Carbon_Intensity",
        markers=True,
        title="Monthly Carbon Intensity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# LOAD TYPE SUSTAINABILITY
# ---------------------------------------------------------

st.subheader(
    "🏭 Sustainability by Load Type"
)

load_summary = (
    df.groupby("Load_Type")
    .agg(
        Energy=("Usage_kWh", "sum"),
        Emissions=("CO2(tCO2)", "sum")
    )
    .reset_index()
)

load_summary["Carbon_Intensity"] = (
    load_summary["Emissions"]
    /
    load_summary["Energy"]
)

fig = px.bar(
    load_summary,
    x="Load_Type",
    y="Carbon_Intensity",
    color="Load_Type",
    text_auto=True
)

fig.update_layout(
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# WEEKDAY ANALYSIS
# ---------------------------------------------------------

st.subheader(
    "📅 Weekday Sustainability Analysis"
)

weekday = (
    df.groupby("Day_of_week")
    .agg(
        Energy=("Usage_kWh", "sum"),
        Emissions=("CO2(tCO2)", "sum")
    )
    .reset_index()
)

weekday["Carbon_Intensity"] = (
    weekday["Emissions"]
    /
    weekday["Energy"]
)

fig = px.bar(
    weekday,
    x="Day_of_week",
    y="Carbon_Intensity",
    color="Carbon_Intensity"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# ENERGY VS EMISSIONS
# ---------------------------------------------------------

st.subheader(
    "⚡ Energy vs Carbon Relationship"
)

fig = px.scatter(
    df,
    x="Usage_kWh",
    y="CO2(tCO2)",
    color="Load_Type",
    size="Usage_kWh",
    opacity=0.7
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# EMISSION HOTSPOTS
# ---------------------------------------------------------

st.subheader(
    "🔥 Emission Hotspots"
)

top_emitters = (
    df.sort_values(
        "CO2(tCO2)",
        ascending=False
    )
    .head(25)
)

st.dataframe(
    top_emitters,
    use_container_width=True
)

# ---------------------------------------------------------
# SUSTAINABILITY TARGETS
# ---------------------------------------------------------

st.subheader(
    "🎯 Sustainability Targets"
)

target_reduction = st.slider(
    "Carbon Reduction Target (%)",
    5,
    50,
    15
)

target_emission = (
    total_emissions *
    (1 - target_reduction / 100)
)

required_reduction = (
    total_emissions -
    target_emission
)

progress = (
    target_emission /
    total_emissions
) * 100

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Current Emissions",
        f"{total_emissions:,.2f}"
    )

with c2:
    st.metric(
        "Target Emissions",
        f"{target_emission:,.2f}"
    )

with c3:
    st.metric(
        "Reduction Needed",
        f"{required_reduction:,.2f}"
    )

st.progress(
    int(progress)
)

# ---------------------------------------------------------
# AI INSIGHTS ENGINE
# ---------------------------------------------------------

st.subheader(
    "🤖 AI Sustainability Insights"
)

# Heavy Load Contribution

load_emission = (
    df.groupby("Load_Type")
    ["CO2(tCO2)"]
    .sum()
)

top_load = load_emission.idxmax()

top_load_pct = (
    load_emission.max()
    /
    load_emission.sum()
) * 100

st.success(
    f"{top_load} contributed {top_load_pct:.1f}% of total emissions."
)

# Monthly Growth

if date_col:

    monthly_growth = (
        monthly["CO2(tCO2)"]
        .pct_change()
        .mean()
    ) * 100

    st.info(
        f"Average monthly emission change: {monthly_growth:.2f}%."
    )

# Peak Consumption

peak_day = (
    df.groupby("Day_of_week")
    ["Usage_kWh"]
    .sum()
    .idxmax()
)

st.warning(
    f"Peak consumption occurred on {peak_day}."
)

# Power Factor Insight

if (
    "Lagging_Current_Power_Factor"
    in df.columns
):

    avg_pf = df[
        "Lagging_Current_Power_Factor"
    ].mean()

    if avg_pf < 90:

        st.warning(
            "Reactive power inefficiency is increasing carbon emissions."
        )

# Sustainability Status

if sustainability_score >= 80:

    st.success(
        "Facility sustainability performance is excellent."
    )

elif sustainability_score >= 60:

    st.warning(
        "Sustainability performance is moderate. Improvement opportunities exist."
    )

else:

    st.error(
        "Sustainability performance requires immediate attention."
    )

# ---------------------------------------------------------
# RECOMMENDATION ENGINE
# ---------------------------------------------------------

st.subheader(
    "💡 Sustainability Recommendations"
)

recommendations = []

recommendations.append(
    "Optimize high-emission load operations."
)

recommendations.append(
    "Reduce peak-hour energy consumption."
)

recommendations.append(
    "Improve power factor correction systems."
)

recommendations.append(
    "Deploy energy-efficient equipment."
)

recommendations.append(
    "Increase renewable energy utilization."
)

recommendations.append(
    "Monitor anomaly alerts regularly."
)

recommendations.append(
    "Implement predictive maintenance strategies."
)

for rec in recommendations:
    st.success(rec)

# ---------------------------------------------------------
# SUSTAINABILITY REPORT
# ---------------------------------------------------------

st.subheader(
    "📋 Sustainability Report"
)

report = pd.DataFrame({

    "Metric": [
        "Total Energy",
        "Total Emissions",
        "Carbon Intensity",
        "Energy Efficiency",
        "Sustainability Score"
    ],

    "Value": [
        total_energy,
        total_emissions,
        carbon_intensity,
        energy_efficiency,
        sustainability_score
    ]
})

st.dataframe(
    report,
    use_container_width=True
)

# ---------------------------------------------------------
# DOWNLOAD REPORT
# ---------------------------------------------------------

csv = report.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download Sustainability Report",
    data=csv,
    file_name="sustainability_report.csv",
    mime="text/csv"
)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Steel Industry Carbon Footprint & ESG Analytics Platform | Sustainability Insights Center"
)
