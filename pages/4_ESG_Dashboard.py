# pages/4_ESG_Dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="ESG Dashboard",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 ESG Compliance Dashboard")
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
# REQUIRED COLUMNS CHECK
# ---------------------------------------------------------

required_cols = [
    "CO2(tCO2)",
    "Usage_kWh"
]

missing = [
    col for col in required_cols
    if col not in df.columns
]

if missing:
    st.error(
        f"Missing required columns: {missing}"
    )
    st.stop()

# ---------------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------------

df["CO2(tCO2)"] = pd.to_numeric(
    df["CO2(tCO2)"],
    errors="coerce"
)

df["Usage_kWh"] = pd.to_numeric(
    df["Usage_kWh"],
    errors="coerce"
)

df = df.replace(
    [np.inf, -np.inf],
    np.nan
)

df = df.fillna(0)

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
# ESG TARGET SETTINGS
# ---------------------------------------------------------

st.sidebar.header("🎯 ESG Targets")

target_reduction = st.sidebar.slider(
    "Carbon Reduction Target (%)",
    5,
    50,
    10
)

target_esg_score = st.sidebar.slider(
    "Target ESG Score",
    50,
    100,
    85
)

# ---------------------------------------------------------
# ESG CALCULATIONS
# ---------------------------------------------------------

total_emissions = float(
    df["CO2(tCO2)"].sum()
)

total_energy = float(
    df["Usage_kWh"].sum()
)

avg_emissions = float(
    df["CO2(tCO2)"].mean()
)

target_emissions = (
    total_emissions *
    (1 - target_reduction / 100)
)

reduction_needed = (
    total_emissions -
    target_emissions
)

carbon_reduction_pct = (
    (
        reduction_needed /
        total_emissions
    ) * 100
    if total_emissions > 0
    else 0
)

carbon_intensity = (
    total_emissions /
    total_energy
    if total_energy > 0
    else 0
)

# ---------------------------------------------------------
# ESG SCORE MODEL
# ---------------------------------------------------------

intensity_score = max(
    0,
    100 - carbon_intensity * 1000
)

emission_score = max(
    0,
    100 - carbon_reduction_pct
)

energy_score = min(
    100,
    total_energy / 1000
)

esg_score = (
    intensity_score * 0.4 +
    emission_score * 0.4 +
    energy_score * 0.2
)

esg_score = round(
    min(100, max(0, esg_score)),
    2
)

# ---------------------------------------------------------
# ESG STATUS
# ---------------------------------------------------------

if esg_score >= 80:

    status = "Green"
    sustainability_rating = "Excellent"

elif esg_score >= 60:

    status = "Yellow"
    sustainability_rating = "Moderate"

else:

    status = "Red"
    sustainability_rating = "Poor"

# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.subheader("📊 ESG KPIs")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Current Emissions",
    f"{total_emissions:,.2f}"
)

c2.metric(
    "Target Emissions",
    f"{target_emissions:,.2f}"
)

c3.metric(
    "Reduction %",
    f"{carbon_reduction_pct:.2f}%"
)

c4.metric(
    "Carbon Intensity",
    f"{carbon_intensity:.5f}"
)

c5.metric(
    "ESG Score",
    esg_score
)

st.markdown("---")

# ---------------------------------------------------------
# ESG GAUGE
# ---------------------------------------------------------

left, right = st.columns([1, 2])

with left:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=esg_score,
            title={"text": "ESG Score"},
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "steps": [
                    {
                        "range": [0, 60],
                        "color": "#ff4b4b"
                    },
                    {
                        "range": [60, 80],
                        "color": "#f7c948"
                    },
                    {
                        "range": [80, 100],
                        "color": "#00cc96"
                    }
                ]
            }
        )
    )

    fig.update_layout(
        height=350
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader(
        "🌍 ESG Compliance Status"
    )

    if status == "Green":
        st.success("On Target")

    elif status == "Yellow":
        st.warning("Warning Zone")

    else:
        st.error("Target Exceeded")

    st.metric(
        "Sustainability Rating",
        sustainability_rating
    )

    st.metric(
        "Target ESG Score",
        target_esg_score
    )

# ---------------------------------------------------------
# PROGRESS
# ---------------------------------------------------------

st.subheader(
    "📈 Sustainability Progress"
)

progress = (
    (
        target_emissions /
        total_emissions
    ) * 100
    if total_emissions > 0
    else 0
)

st.progress(
    int(min(progress, 100))
)

st.write(
    f"Progress Toward Target: {progress:.2f}%"
)

# ---------------------------------------------------------
# MONTHLY TREND (FIXED)
# ---------------------------------------------------------

if (
    date_col is not None
    and df[date_col].notna().sum() > 0
):

    st.subheader(
        "📅 Monthly ESG Trend"
    )

    monthly_df = df.dropna(
        subset=[date_col]
    ).copy()

    monthly = (
        monthly_df
        .set_index(date_col)
        .resample("ME")
        .agg({
            "CO2(tCO2)": "sum",
            "Usage_kWh": "sum"
        })
        .reset_index()
    )

    monthly["Carbon_Intensity"] = (
        monthly["CO2(tCO2)"] /
        monthly["Usage_kWh"].replace(
            0,
            np.nan
        )
    )

    monthly = monthly.fillna(0)

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
# LOAD TYPE ANALYSIS
# ---------------------------------------------------------

if "Load_Type" in df.columns:

    st.subheader(
        "🏭 Load Type ESG Analysis"
    )

    load_summary = (
        df.groupby("Load_Type")
        .agg({
            "CO2(tCO2)": "sum",
            "Usage_kWh": "sum"
        })
        .reset_index()
    )

    load_summary["Carbon_Intensity"] = (
        load_summary["CO2(tCO2)"] /
        load_summary["Usage_kWh"]
    )

    load_summary = load_summary.fillna(0)

    fig = px.bar(
        load_summary,
        x="Load_Type",
        y="Carbon_Intensity",
        color="Load_Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# SCORE COMPONENTS
# ---------------------------------------------------------

st.subheader(
    "🧩 ESG Score Components"
)

component_df = pd.DataFrame({

    "Component": [
        "Carbon Intensity",
        "Emission Reduction",
        "Energy Efficiency"
    ],

    "Score": [
        intensity_score,
        emission_score,
        energy_score
    ]
})

fig = px.bar(
    component_df,
    x="Component",
    y="Score",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------

st.subheader(
    "💡 Sustainability Recommendations"
)

recommendations = []

if carbon_intensity > 0.0005:
    recommendations.append(
        "Improve energy efficiency to reduce carbon intensity."
    )

if reduction_needed > 0:
    recommendations.append(
        "Implement carbon reduction initiatives."
    )

if esg_score < 80:
    recommendations.append(
        "Increase renewable energy utilization."
    )

if (
    "Lagging_Current_Power_Factor"
    in df.columns
):

    if (
        df[
            "Lagging_Current_Power_Factor"
        ].mean()
        < 80
    ):
        recommendations.append(
            "Improve power factor correction systems."
        )

if not recommendations:
    recommendations.append(
        "Current ESG performance is excellent."
    )

for rec in recommendations:
    st.success(rec)

# ---------------------------------------------------------
# REPORT
# ---------------------------------------------------------

st.subheader(
    "📋 ESG Compliance Report"
)

report = pd.DataFrame({

    "Metric": [
        "Current Emissions",
        "Target Emissions",
        "Reduction %",
        "Carbon Intensity",
        "ESG Score",
        "Rating",
        "Status"
    ],

    "Value": [
        round(total_emissions, 2),
        round(target_emissions, 2),
        round(carbon_reduction_pct, 2),
        round(carbon_intensity, 5),
        esg_score,
        sustainability_rating,
        status
    ]
})

st.dataframe(
    report,
    use_container_width=True
)

# ---------------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------------

csv = report.to_csv(
    index=False
)

st.download_button(
    "⬇ Download ESG Report",
    csv,
    "esg_report.csv",
    "text/csv"
)

# ---------------------------------------------------------
# INSIGHTS
# ---------------------------------------------------------

st.subheader(
    "🤖 ESG Insights"
)

st.info(
    f"""
Current ESG Score: {esg_score}

Sustainability Rating: {sustainability_rating}

Carbon Reduction Target: {target_reduction}%

Reduction Required: {reduction_needed:,.2f} tCO₂

Carbon Intensity: {carbon_intensity:.5f}
"""
)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Steel Industry Carbon Footprint & ESG Analytics Platform | ESG Dashboard"
)
