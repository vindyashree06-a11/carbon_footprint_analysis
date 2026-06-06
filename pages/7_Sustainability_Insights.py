# pages/7_Sustainability_Insights.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Sustainability Insights",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Sustainability Insights Center")
st.markdown("---")

if "data" not in st.session_state:
    st.warning("Please upload dataset from Executive Summary page.")
    st.stop()

df = st.session_state["data"].copy()

date_col = None
for col in df.columns:
    if "date" in col.lower():
        date_col = col
        break

if date_col and date_col in df.columns:
    df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")

required_cols = ["Usage_kWh", "CO2(tCO2)"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing required column: {col}")
        st.stop()

total_energy = df["Usage_kWh"].sum()
total_emissions = df["CO2(tCO2)"].sum()

carbon_intensity = (
    total_emissions / total_energy
    if total_energy > 0 else 0
)

energy_efficiency = (
    total_energy / total_emissions
    if total_emissions > 0 else 0
)

sustainability_score = max(
    0,
    min(100, 100 - (carbon_intensity * 1000))
)

st.subheader("📊 Sustainability KPIs")

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("Total Energy", f"{total_energy:,.0f} kWh")

with c2:
    st.metric("Total CO₂", f"{total_emissions:,.2f}")

with c3:
    st.metric("Carbon Intensity", f"{carbon_intensity:.5f}")

with c4:
    st.metric("Energy Efficiency", f"{energy_efficiency:.2f}")

with c5:
    st.metric("Sustainability Score", f"{sustainability_score:.0f}")

st.markdown("---")

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=sustainability_score,
        title={"text": "Sustainability Index"},
        gauge={
            "axis": {"range": [0, 100]}
        }
    )
)
st.plotly_chart(fig, use_container_width=True)

monthly = None

if date_col and df[date_col].notna().sum() > 0:

    st.subheader("📈 Sustainability Progress Trend")

    monthly_df = df.dropna(subset=[date_col]).copy()

    monthly = (
        monthly_df
        .set_index(date_col)
        .resample("ME")
        .agg({
            "Usage_kWh": "sum",
            "CO2(tCO2)": "sum"
        })
        .reset_index()
    )

    monthly["Carbon_Intensity"] = np.where(
        monthly["Usage_kWh"] == 0,
        0,
        monthly["CO2(tCO2)"] / monthly["Usage_kWh"]
    )

    fig = px.line(
        monthly,
        x=date_col,
        y="Carbon_Intensity",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

if "Load_Type" in df.columns:

    st.subheader("🏭 Sustainability by Load Type")

    load_summary = (
        df.groupby("Load_Type")
        .agg(
            Energy=("Usage_kWh", "sum"),
            Emissions=("CO2(tCO2)", "sum")
        )
        .reset_index()
    )

    load_summary["Carbon_Intensity"] = np.where(
        load_summary["Energy"] == 0,
        0,
        load_summary["Emissions"] / load_summary["Energy"]
    )

    st.plotly_chart(
        px.bar(
            load_summary,
            x="Load_Type",
            y="Carbon_Intensity",
            color="Load_Type"
        ),
        use_container_width=True
    )

if "Day_of_week" in df.columns:

    st.subheader("📅 Weekday Sustainability Analysis")

    weekday = (
        df.groupby("Day_of_week")
        .agg(
            Energy=("Usage_kWh", "sum"),
            Emissions=("CO2(tCO2)", "sum")
        )
        .reset_index()
    )

    weekday["Carbon_Intensity"] = np.where(
        weekday["Energy"] == 0,
        0,
        weekday["Emissions"] / weekday["Energy"]
    )

    st.plotly_chart(
        px.bar(
            weekday,
            x="Day_of_week",
            y="Carbon_Intensity"
        ),
        use_container_width=True
    )

if "Load_Type" in df.columns:

    st.subheader("⚡ Energy vs Carbon Relationship")

    fig = px.scatter(
        df,
        x="Usage_kWh",
        y="CO2(tCO2)",
        color="Load_Type",
        size="Usage_kWh"
    )

    st.plotly_chart(fig, use_container_width=True)

st.subheader("🔥 Emission Hotspots")

top_emitters = (
    df.sort_values("CO2(tCO2)", ascending=False)
    .head(25)
)

st.dataframe(top_emitters, use_container_width=True)

st.subheader("🎯 Sustainability Targets")

target_reduction = st.slider(
    "Carbon Reduction Target (%)",
    5, 50, 15
)

target_emission = total_emissions * (1 - target_reduction / 100)
required_reduction = total_emissions - target_emission

progress = (
    target_emission / total_emissions * 100
    if total_emissions > 0 else 0
)

st.progress(int(min(100, progress)))

st.subheader("🤖 AI Sustainability Insights")

if "Load_Type" in df.columns:

    load_emission = (
        df.groupby("Load_Type")["CO2(tCO2)"]
        .sum()
    )

    top_load = load_emission.idxmax()

    top_load_pct = (
        load_emission.max() / load_emission.sum()
    ) * 100

    st.success(
        f"{top_load} contributed {top_load_pct:.1f}% of total emissions."
    )

if monthly is not None and len(monthly) > 1:

    monthly_growth = (
        monthly["CO2(tCO2)"]
        .pct_change()
        .mean()
    ) * 100

    st.info(
        f"Average monthly emission change: {monthly_growth:.2f}%."
    )

if "Day_of_week" in df.columns:

    peak_day = (
        df.groupby("Day_of_week")["Usage_kWh"]
        .sum()
        .idxmax()
    )

    st.warning(
        f"Peak consumption occurred on {peak_day}."
    )

if "Lagging_Current_Power_Factor" in df.columns:

    avg_pf = df["Lagging_Current_Power_Factor"].mean()

    if avg_pf < 90:
        st.warning(
            "Reactive power inefficiency is increasing carbon emissions."
        )

st.subheader("📋 Sustainability Report")

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

st.dataframe(report, use_container_width=True)

csv = report.to_csv(index=False)

st.download_button(
    "⬇ Download Sustainability Report",
    csv,
    "sustainability_report.csv",
    "text/csv"
)

st.markdown("---")

st.caption(
    "Steel Industry Carbon Footprint & ESG Analytics Platform | Sustainability Insights Center"
)
