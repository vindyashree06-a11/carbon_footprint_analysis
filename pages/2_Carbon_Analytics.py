import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Carbon Analytics", page_icon="🌍", layout="wide")

st.title("🌍 Carbon Analytics")
st.caption("Steel Industry Carbon Footprint Analytics")

@st.cache_data
def load_data():
    return pd.read_csv("data/Steel_industry_data.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Dataset load error: {e}")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"]).drop_duplicates()

numeric_cols = df.select_dtypes(include=np.number).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

df["Carbon_Intensity"] = df["CO2(tCO2)"] / (df["Usage_kWh"] + 1)

st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df["Date"].min().date())
end_date = st.sidebar.date_input("End Date", df["Date"].max().date())

filtered = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
].copy()

total_emissions = filtered["CO2(tCO2)"].sum()
avg_daily = filtered.groupby(filtered["Date"].dt.date)["CO2(tCO2)"].sum().mean()
annualized = avg_daily * 365 if pd.notna(avg_daily) else 0
carbon_intensity = filtered["Carbon_Intensity"].mean()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Emissions", f"{total_emissions:,.2f} tCO₂")
c2.metric("Avg Daily", f"{avg_daily:,.2f}")
c3.metric("Annualized", f"{annualized:,.2f}")
c4.metric("Carbon Intensity", f"{carbon_intensity:.4f}")

st.subheader("Emission Trend")

daily = filtered.groupby(filtered["Date"].dt.date)["CO2(tCO2)"].sum().reset_index()
daily["7DMA"] = daily["CO2(tCO2)"].rolling(7, min_periods=1).mean()

fig = go.Figure()
fig.add_trace(go.Scatter(x=daily["Date"], y=daily["CO2(tCO2)"], name="Daily"))
fig.add_trace(go.Scatter(x=daily["Date"], y=daily["7DMA"], name="7DMA"))
st.plotly_chart(fig, use_container_width=True)

col1,col2 = st.columns(2)

with col1:
    st.subheader("Load Type Contribution")
    load = filtered.groupby("Load_Type")["CO2(tCO2)"].sum().reset_index()
    fig = px.pie(load, names="Load_Type", values="CO2(tCO2)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Carbon Intensity")
    fig = px.box(filtered, y="Carbon_Intensity", x="Load_Type")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Monthly Emissions")
monthly = filtered.groupby(filtered["Date"].dt.to_period("M"))["CO2(tCO2)"].sum().reset_index()
monthly["Date"] = monthly["Date"].astype(str)
fig = px.bar(monthly, x="Date", y="CO2(tCO2)")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Emission Distribution")
fig = px.histogram(filtered, x="CO2(tCO2)", nbins=40)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Reactive Power Impact")
fig = px.scatter(
    filtered,
    x="Lagging_Current_Reactive.Power_kVarh",
    y="CO2(tCO2)",
    color="Load_Type"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("AI Insights")

top_load = load.sort_values("CO2(tCO2)", ascending=False).iloc[0]

st.info(
    f"""
    • {top_load['Load_Type']} contributes the highest emissions.

    • Total emissions are {total_emissions:,.2f} tCO₂.

    • Average carbon intensity is {carbon_intensity:.4f}.

    • Annualized emissions are estimated at {annualized:,.2f} tCO₂.
    """
)
