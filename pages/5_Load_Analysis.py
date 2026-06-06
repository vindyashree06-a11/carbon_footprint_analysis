
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Load Analysis", layout="wide")
st.title("⚡ Load Analysis")

df = pd.read_csv("data/Steel_industry_data.csv")

load_summary = df.groupby("Load_Type").agg({
    "Usage_kWh":"sum",
    "CO2(tCO2)":"sum"
}).reset_index()

st.dataframe(load_summary, use_container_width=True)

fig1 = px.bar(
    load_summary,
    x="Load_Type",
    y="Usage_kWh",
    title="Energy Usage by Load Type"
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.pie(
    load_summary,
    names="Load_Type",
    values="CO2(tCO2)",
    title="Emission Contribution"
)
st.plotly_chart(fig2, use_container_width=True)

top = load_summary.sort_values("CO2(tCO2)", ascending=False).iloc[0]
st.info(f"{top['Load_Type']} contributes the highest emissions.")
