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
    min_value=5,
    max_value=50,
    value=10
)

target_esg_score = st.sidebar.slider(
    "Target ESG Score",
    min_value=50,
    max_value=100,
    value=85
)

# ---------------------------------------------------------
# ESG CALCULATIONS
# ---------------------------------------------------------

total_emissions = df["CO2(tCO2)"].sum()

total_energy = df["Usage_kWh"].sum()

avg_emissions = df["CO2(tCO2)"].mean()

target_emissions = (
    total_emissions *
    (1 - target_reduction / 100)
)

reduction_needed = (
    total_emissions -
    target_emissions
)

carbon_reduction_pct = (
    reduction_needed /
    total_emissions
) * 100

carbon_intensity = (
    total_emissions /
    total_energy
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
    color = "green"

elif esg_score >= 60:
    status = "Yellow"
    sustainability_rating = "Moderate"
    color = "orange"

else:
    status = "Red"
    sustainability_rating = "Poor"
    color = "red"

# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.subheader("📊 ESG KPIs")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Current Emissions",
        f"{total_emissions:,.2f}"
    )

with c2:
    st.metric(
        "Target Emissions",
        f"{target_emissions:,.2f}"
    )

with c3:
    st.metric(
        "Reduction %",
        f"{carbon_reduction_pct:.2f}%"
    )

with c4:
    st.metric(
        "Carbon Intensity",
        f"{carbon_intensity:.4f}"
    )

with c5:
    st.metric(
        "ESG Score",
        esg_score
    )

st.markdown("---")

# ---------------------------------------------------------
# ESG SCORE GAUGE
# ---------------------------------------------------------

left, right = st.columns([1, 2])

with left:

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=esg_score,
            title={
                "text": "ESG Score"
            },
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
        st.success(
            "On Target"
        )

    elif status == "Yellow":
        st.warning(
            "Warning Zone"
        )

    else:
        st.error(
            "Target Exceeded"
        )

    st.metric(
        "Sustainability Rating",
        sustainability_rating
    )

    st.metric(
        "Target ESG Score",
        target_esg_score
    )

# ---------------------------------------------------------
# EMISSION PROGRESS
# ---------------------------------------------------------

st.subheader("📈 Sustainability Progress")

progress = (
    target_emissions /
    total_emissions
) * 100

st.progress(
    min(100, int(progress))
)

st.write(
    f"Progress Toward Target: {progress:.2f}%"
)

# ---------------------------------------------------------
# MONTHLY ESG TREND
# ---------------------------------------------------------

if date_col:

    st.subheader(
        "📅 Monthly ESG Trend"
    )

    monthly = (
        df.groupby(
            pd.Grouper(
                key=date_col,
                freq="M"
            )
        )
        .agg({
            "CO2(tCO2)": "sum",
            "Usage_kWh": "sum"
        })
        .reset_index()
    )

    monthly["Carbon_Intensity"] = (
        monthly["CO2(tCO2)"] /
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
# LOAD TYPE ESG ANALYSIS
# ---------------------------------------------------------

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

fig = px.bar(
    load_summary,
    x="Load_Type",
    y="Carbon_Intensity",
    color="Load_Type",
    text_auto=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# ESG SCORE COMPONENTS
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
# SUSTAINABILITY RECOMMENDATIONS
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

if df[
    "Lagging_Current_Power_Factor"
].mean() < 80:
    recommendations.append(
        "Improve power factor correction systems."
    )

if len(recommendations) == 0:
    recommendations.append(
        "Current ESG performance is excellent."
    )

for rec in recommendations:
    st.success(rec)

# ---------------------------------------------------------
# ESG REPORT TABLE
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
# DOWNLOAD ESG REPORT
# ---------------------------------------------------------

csv = report.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download ESG Report",
    data=csv,
    file_name="esg_report.csv",
    mime="text/csv"
)

# ---------------------------------------------------------
# AI GENERATED ESG INSIGHTS
# ---------------------------------------------------------

st.subheader(
    "🤖 ESG Insights"
)

st.info(
    f"""
    Current ESG score is {esg_score}.

    Sustainability rating is {sustainability_rating}.

    Carbon reduction target is {target_reduction}%.

    Estimated reduction required:
    {reduction_needed:,.2f} tCO₂.

    Carbon intensity currently stands at
    {carbon_intensity:.5f}.
    """
)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Steel Industry Carbon Footprint & ESG Analytics Platform | ESG Dashboard"
)
