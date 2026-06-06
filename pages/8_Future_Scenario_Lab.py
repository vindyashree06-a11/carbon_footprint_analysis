
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Future Scenario Lab", layout="wide")

st.title("🔮 Future Scenario Lab")

df = pd.read_csv("data/Steel_industry_data.csv")

base_usage = df["Usage_kWh"].mean()
base_co2 = df["CO2(tCO2)"].mean()

st.sidebar.header("Scenario Controls")

energy_change = st.sidebar.slider(
    "Energy Usage Change (%)",
    -50, 100, 0
)

power_factor_change = st.sidebar.slider(
    "Power Factor Change (%)",
    -20, 20, 0
)

reactive_change = st.sidebar.slider(
    "Reactive Power Change (%)",
    -50, 50, 0
)

production_growth = st.sidebar.slider(
    "Production Growth (%)",
    0, 100, 0
)

renewable = st.sidebar.slider(
    "Renewable Adoption (%)",
    0, 100, 0
)

future_usage = base_usage * (1 + energy_change/100)
future_usage *= (1 + production_growth/100)

future_co2 = base_co2 * (future_usage/base_usage)

future_co2 *= (1 - renewable/100 * 0.5)

projected_esg = max(
    0,
    min(100, 100 - future_co2 * 100)
)

c1,c2,c3 = st.columns(3)

c1.metric("Projected Usage", f"{future_usage:,.2f}")
c2.metric("Projected CO₂", f"{future_co2:.4f}")
c3.metric("Projected ESG", f"{projected_esg:.1f}")

st.subheader("Scenario Impact")

st.info(
    f"""
    Energy Change: {energy_change}%

    Production Growth: {production_growth}%

    Renewable Adoption: {renewable}%

    Estimated ESG Score: {projected_esg:.1f}
    """
)
