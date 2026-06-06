
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="ESG Dashboard", layout="wide")
st.title("🌱 ESG Dashboard")

df = pd.read_csv("data/Steel_industry_data.csv")
total_emissions = df["CO2(tCO2)"].sum()
energy = df["Usage_kWh"].sum()

esg_score = max(0, min(100, 100 - (df["CO2(tCO2)"].mean() * 100)))

status = "Green" if esg_score >= 85 else "Yellow" if esg_score >= 65 else "Red"

c1,c2,c3 = st.columns(3)
c1.metric("ESG Score", f"{esg_score:.1f}")
c2.metric("Total Emissions", f"{total_emissions:.2f}")
c3.metric("Status", status)

fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=esg_score,
    title={"text":"ESG Score"},
    gauge={"axis":{"range":[0,100]}}
))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Recommendations")
st.info("Improve power factor, reduce peak load usage, and increase renewable adoption.")
