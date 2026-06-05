# pages/5_Load_Analysis.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Load Analysis",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Load Analysis Center")
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
# DATE HANDLING
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
# LOAD KPIs
# ---------------------------------------------------------

total_energy = df["Usage_kWh"].sum()

avg_load = df["Usage_kWh"].mean()

peak_load = df["Usage_kWh"].max()

min_load = df["Usage_kWh"].min()

load_factor = (
    avg_load / peak_load
    if peak_load > 0
    else 0
)

st.subheader("📊 Load KPIs")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Total Energy (kWh)",
        f"{total_energy:,.0f}"
    )

with c2:
    st.metric(
        "Average Load",
        f"{avg_load:.2f}"
    )

with c3:
    st.metric(
        "Peak Load",
        f"{peak_load:.2f}"
    )

with c4:
    st.metric(
        "Minimum Load",
        f"{min_load:.2f}"
    )

with c5:
    st.metric(
        "Load Factor",
        f"{load_factor:.2f}"
    )

st.markdown("---")

# ---------------------------------------------------------
# LOAD TYPE SUMMARY
# ---------------------------------------------------------

st.subheader("🏭 Load Type Summary")

load_summary = (
    df.groupby("Load_Type")
    .agg(
        Total_Energy=("Usage_kWh", "sum"),
        Avg_Load=("Usage_kWh", "mean"),
        Peak_Load=("Usage_kWh", "max"),
        Total_CO2=("CO2(tCO2)", "sum")
    )
    .reset_index()
)

st.dataframe(
    load_summary,
    use_container_width=True
)

# ---------------------------------------------------------
# LOAD TYPE COMPARISON
# ---------------------------------------------------------

st.subheader("⚙ Load Type Energy Consumption")

fig = px.bar(
    load_summary,
    x="Load_Type",
    y="Total_Energy",
    color="Load_Type",
    text_auto=True
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# LOAD TYPE CO2 COMPARISON
# ---------------------------------------------------------

st.subheader("🌍 Load Type Carbon Emissions")

fig = px.bar(
    load_summary,
    x="Load_Type",
    y="Total_CO2",
    color="Load_Type",
    text_auto=True
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# ENERGY USAGE TREND
# ---------------------------------------------------------

if date_col:

    st.subheader("📈 Energy Usage Trend")

    daily_usage = (
        df.groupby(df[date_col].dt.date)
        ["Usage_kWh"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        daily_usage,
        x=date_col,
        y="Usage_kWh",
        markers=True
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# LOAD DISTRIBUTION
# ---------------------------------------------------------

st.subheader("📊 Load Distribution")

fig = px.histogram(
    df,
    x="Usage_kWh",
    nbins=50
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# POWER FACTOR ANALYSIS
# ---------------------------------------------------------

st.subheader("🔌 Power Factor Analysis")

pf_cols = []

if "Lagging_Current_Power_Factor" in df.columns:
    pf_cols.append(
        "Lagging_Current_Power_Factor"
    )

if "Leading_Current_Power_Factor" in df.columns:
    pf_cols.append(
        "Leading_Current_Power_Factor"
    )

if len(pf_cols) > 0:

    pf_data = df[pf_cols].mean()

    pf_df = pd.DataFrame({

        "Power Factor":
            pf_data.index,

        "Average":
            pf_data.values

    })

    fig = px.bar(
        pf_df,
        x="Power Factor",
        y="Average",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# REACTIVE POWER ANALYSIS
# ---------------------------------------------------------

st.subheader("⚡ Reactive Power Analysis")

reactive_cols = [
    "Lagging_Current_Reactive.Power_kVarh",
    "Leading_Current_Reactive_Power_kVarh"
]

reactive_df = pd.DataFrame({

    "Type": [
        "Lagging Reactive",
        "Leading Reactive"
    ],

    "Power": [
        df[
            "Lagging_Current_Reactive.Power_kVarh"
        ].sum(),

        df[
            "Leading_Current_Reactive_Power_kVarh"
        ].sum()
    ]

})

fig = px.pie(
    reactive_df,
    names="Type",
    values="Power",
    hole=0.4
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# WEEKDAY ANALYSIS
# ---------------------------------------------------------

st.subheader("📅 Day of Week Analysis")

weekday_usage = (
    df.groupby("Day_of_week")
    ["Usage_kWh"]
    .sum()
    .reset_index()
)

fig = px.bar(
    weekday_usage,
    x="Day_of_week",
    y="Usage_kWh",
    color="Usage_kWh"
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# WEEK STATUS ANALYSIS
# ---------------------------------------------------------

st.subheader("🗓 Weekday vs Weekend")

week_status = (
    df.groupby("WeekStatus")
    .agg(
        Energy=("Usage_kWh", "sum"),
        Emissions=("CO2(tCO2)", "sum")
    )
    .reset_index()
)

fig = px.bar(
    week_status,
    x="WeekStatus",
    y="Energy",
    color="WeekStatus",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# HEATMAP
# ---------------------------------------------------------

st.subheader("🔥 Energy Usage Heatmap")

heatmap = pd.pivot_table(
    df,
    values="Usage_kWh",
    index="Day_of_week",
    columns="Load_Type",
    aggfunc="mean"
)

fig = px.imshow(
    heatmap,
    text_auto=True,
    aspect="auto"
)

fig.update_layout(height=600)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# PEAK LOAD ANALYSIS
# ---------------------------------------------------------

st.subheader("🚨 Peak Load Records")

threshold = df["Usage_kWh"].quantile(
    0.95
)

peak_df = df[
    df["Usage_kWh"] >= threshold
]

st.metric(
    "Peak Load Events",
    len(peak_df)
)

st.dataframe(
    peak_df.sort_values(
        "Usage_kWh",
        ascending=False
    ).head(50),
    use_container_width=True
)

# ---------------------------------------------------------
# LOAD EFFICIENCY SCORE
# ---------------------------------------------------------

st.subheader("📉 Energy Efficiency Score")

efficiency_score = max(
    0,
    min(
        100,
        (
            100
            -
            (
                peak_load /
                avg_load
            )
        )
    )
)

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=efficiency_score,
        title={
            "text":
            "Energy Efficiency Score"
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

fig.update_layout(height=400)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# AI LOAD INSIGHTS
# ---------------------------------------------------------

st.subheader("🤖 Load Insights")

top_load_type = (
    load_summary
    .sort_values(
        "Total_Energy",
        ascending=False
    )
    .iloc[0]["Load_Type"]
)

top_day = (
    weekday_usage
    .sort_values(
        "Usage_kWh",
        ascending=False
    )
    .iloc[0]["Day_of_week"]
)

st.success(
    f"{top_load_type} is the largest energy consumer."
)

st.success(
    f"Highest energy usage occurs on {top_day}."
)

if load_factor < 0.6:
    st.warning(
        "Load factor indicates inefficient utilization of capacity."
    )

if df[
    "Lagging_Current_Power_Factor"
].mean() < 90:
    st.warning(
        "Power factor optimization may reduce energy losses."
    )

# ---------------------------------------------------------
# DOWNLOAD REPORT
# ---------------------------------------------------------

st.subheader("⬇ Export Load Analysis")

csv = load_summary.to_csv(
    index=False
)

st.download_button(
    label="Download Load Report",
    data=csv,
    file_name="load_analysis_report.csv",
    mime="text/csv"
)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Steel Industry Carbon Footprint & ESG Analytics Platform | Load Analysis Center"
)
