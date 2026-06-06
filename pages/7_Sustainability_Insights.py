
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sustainability Insights", layout="wide")

st.title("🌿 Sustainability Insights")

df = pd.read_csv("data/Steel_industry_data.csv")

total_co2 = df["CO2(tCO2)"].sum()
avg_co2 = df["CO2(tCO2)"].mean()

load_emissions = (
    df.groupby("Load_Type")["CO2(tCO2)"]
    .sum()
    .sort_values(ascending=False)
)

top_load = load_emissions.index[0]

st.metric("Total CO₂", f"{total_co2:,.2f}")
st.metric("Average CO₂", f"{avg_co2:.4f}")

fig = px.bar(
    load_emissions.reset_index(),
    x="Load_Type",
    y="CO2(tCO2)",
    title="Emission Contribution by Load Type"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("AI Sustainability Insights")

st.success(
    f"""
    • {top_load} contributes the highest emissions.

    • Carbon reduction efforts should focus on peak load periods.

    • Improving power factor may reduce carbon intensity.

    • Renewable integration can improve ESG performance.
    """
)
