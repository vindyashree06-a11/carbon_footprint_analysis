# pages/6_Anomaly_Detection.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Anomaly Detection Center",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 Anomaly Detection Center")
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
# SIDEBAR SETTINGS
# ---------------------------------------------------------

st.sidebar.header("⚙ Detection Settings")

contamination = st.sidebar.slider(
    "Contamination Rate",
    min_value=0.01,
    max_value=0.10,
    value=0.02,
    step=0.01
)

rolling_factor = st.sidebar.slider(
    "Rolling Median Multiplier",
    min_value=1.0,
    max_value=3.0,
    value=1.5,
    step=0.1
)

# ---------------------------------------------------------
# FEATURES FOR DETECTION
# ---------------------------------------------------------

feature_cols = [
    "Usage_kWh",
    "CO2(tCO2)",
    "Lagging_Current_Reactive.Power_kVarh",
    "Leading_Current_Reactive_Power_kVarh",
    "Lagging_Current_Power_Factor",
    "Leading_Current_Power_Factor"
]

available_cols = [
    col
    for col in feature_cols
    if col in df.columns
]

X = df[available_cols].fillna(0)

# ---------------------------------------------------------
# SCALING
# ---------------------------------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ---------------------------------------------------------
# ISOLATION FOREST
# ---------------------------------------------------------

iso = IsolationForest(
    contamination=contamination,
    random_state=42
)

df["Anomaly"] = iso.fit_predict(
    X_scaled
)

df["Anomaly_Flag"] = np.where(
    df["Anomaly"] == -1,
    "Anomaly",
    "Normal"
)

# ---------------------------------------------------------
# ROLLING MEDIAN CHECKS
# ---------------------------------------------------------

window_size = 96

# Usage Spikes
usage_median = (
    df["Usage_kWh"]
    .rolling(window_size)
    .median()
)

df["Usage_Spike"] = (
    df["Usage_kWh"]
    >
    usage_median * rolling_factor
)

# CO2 Spikes
co2_median = (
    df["CO2(tCO2)"]
    .rolling(window_size)
    .median()
)

df["CO2_Spike"] = (
    df["CO2(tCO2)"]
    >
    co2_median * rolling_factor
)

# Reactive Power Spike

reactive_power = (
    df[
        "Lagging_Current_Reactive.Power_kVarh"
    ]
    +
    df[
        "Leading_Current_Reactive_Power_kVarh"
    ]
)

reactive_median = (
    reactive_power
    .rolling(window_size)
    .median()
)

df["Reactive_Spike"] = (
    reactive_power
    >
    reactive_median * rolling_factor
)

# Power Factor Issue

df["PF_Anomaly"] = (
    (
        df[
            "Lagging_Current_Power_Factor"
        ] < 80
    )
    |
    (
        df[
            "Leading_Current_Power_Factor"
        ] < 80
    )
)

# ---------------------------------------------------------
# ROOT CAUSE ANALYSIS
# ---------------------------------------------------------

def identify_root_cause(row):

    causes = []

    if row["Usage_Spike"]:
        causes.append(
            "Energy Usage Spike"
        )

    if row["CO2_Spike"]:
        causes.append(
            "Carbon Spike"
        )

    if row["Reactive_Spike"]:
        causes.append(
            "Reactive Power Issue"
        )

    if row["PF_Anomaly"]:
        causes.append(
            "Power Factor Deviation"
        )

    if len(causes) == 0:
        return "Normal"

    return ", ".join(causes)

df["Root_Cause"] = df.apply(
    identify_root_cause,
    axis=1
)

# ---------------------------------------------------------
# SEVERITY SCORE
# ---------------------------------------------------------

severity = (
    df["Usage_Spike"].astype(int)
    +
    df["CO2_Spike"].astype(int)
    +
    df["Reactive_Spike"].astype(int)
    +
    df["PF_Anomaly"].astype(int)
)

df["Severity_Score"] = (
    severity * 25
)

# ---------------------------------------------------------
# ALERT LEVEL
# ---------------------------------------------------------

def get_alert(score):

    if score >= 75:
        return "Critical"

    elif score >= 50:
        return "High"

    elif score >= 25:
        return "Medium"

    return "Low"

df["Alert_Level"] = (
    df["Severity_Score"]
    .apply(get_alert)
)

# Save to session state
st.session_state["data"] = df

# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

total_anomalies = len(
    df[
        df["Anomaly_Flag"] == "Anomaly"
    ]
)

critical_alerts = len(
    df[
        df["Alert_Level"]
        == "Critical"
    ]
)

high_alerts = len(
    df[
        df["Alert_Level"]
        == "High"
    ]
)

medium_alerts = len(
    df[
        df["Alert_Level"]
        == "Medium"
    ]
)

st.subheader("📊 Alert KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Anomalies",
        total_anomalies
    )

with c2:
    st.metric(
        "Critical Alerts",
        critical_alerts
    )

with c3:
    st.metric(
        "High Alerts",
        high_alerts
    )

with c4:
    st.metric(
        "Medium Alerts",
        medium_alerts
    )

st.markdown("---")

# ---------------------------------------------------------
# ANOMALY SCATTER
# ---------------------------------------------------------

st.subheader(
    "🔍 Anomaly Detection Scatter Plot"
)

fig = px.scatter(
    df,
    x="Usage_kWh",
    y="CO2(tCO2)",
    color="Anomaly_Flag",
    hover_data=[
        "Severity_Score",
        "Root_Cause"
    ]
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# ALERT LEVEL DISTRIBUTION
# ---------------------------------------------------------

st.subheader(
    "🚦 Alert Distribution"
)

alert_dist = (
    df["Alert_Level"]
    .value_counts()
    .reset_index()
)

alert_dist.columns = [
    "Alert_Level",
    "Count"
]

fig = px.pie(
    alert_dist,
    names="Alert_Level",
    values="Count",
    hole=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# SEVERITY DISTRIBUTION
# ---------------------------------------------------------

st.subheader(
    "📉 Severity Score Distribution"
)

fig = px.histogram(
    df,
    x="Severity_Score",
    nbins=20
)

fig.update_layout(
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# DAILY ALERT TREND
# ---------------------------------------------------------

if date_col:

    st.subheader(
        "📈 Alert Trend Over Time"
    )

    daily_alerts = (
        df.groupby(
            df[date_col].dt.date
        )["Severity_Score"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        daily_alerts,
        x=date_col,
        y="Severity_Score",
        markers=True
    )

    fig.update_layout(
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# ROOT CAUSE ANALYSIS
# ---------------------------------------------------------

st.subheader(
    "🧠 Root Cause Analysis"
)

root_summary = (
    df["Root_Cause"]
    .value_counts()
    .reset_index()
)

root_summary.columns = [
    "Cause",
    "Count"
]

fig = px.bar(
    root_summary.head(10),
    x="Cause",
    y="Count",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# HEATMAP
# ---------------------------------------------------------

st.subheader(
    "🔥 Alert Heatmap"
)

heatmap = pd.pivot_table(
    df,
    values="Severity_Score",
    index="Day_of_week",
    columns="Load_Type",
    aggfunc="mean"
)

fig = px.imshow(
    heatmap,
    text_auto=True,
    aspect="auto"
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# CRITICAL ALERT TABLE
# ---------------------------------------------------------

st.subheader(
    "🚨 Critical Alert Records"
)

critical_df = df[
    df["Alert_Level"]
    == "Critical"
]

st.dataframe(
    critical_df.sort_values(
        "Severity_Score",
        ascending=False
    ),
    use_container_width=True
)

# ---------------------------------------------------------
# AI INSIGHTS
# ---------------------------------------------------------

st.subheader(
    "🤖 AI Alert Insights"
)

if total_anomalies > 0:

    most_common = (
        root_summary.iloc[0]["Cause"]
    )

    st.success(
        f"Most common anomaly source: {most_common}"
    )

    st.warning(
        f"{critical_alerts} critical alerts require immediate investigation."
    )

    st.info(
        "Reactive power and poor power factor contribute significantly to anomaly generation."
    )

else:

    st.success(
        "No significant anomalies detected."
    )

# ---------------------------------------------------------
# DOWNLOAD ALERT REPORT
# ---------------------------------------------------------

st.subheader(
    "⬇ Export Alert Report"
)

csv = df.to_csv(
    index=False
)

st.download_button(
    label="Download Alert Report",
    data=csv,
    file_name="anomaly_alert_report.csv",
    mime="text/csv"
)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Steel Industry Carbon Footprint & ESG Analytics Platform | Anomaly Detection Center"
)
