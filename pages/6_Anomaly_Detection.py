
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Anomaly Detection", layout="wide")
st.title("🚨 Anomaly Detection")

df = pd.read_csv("data/Steel_industry_data.csv")

features = [
    "Usage_kWh",
    "CO2(tCO2)",
    "Lagging_Current_Reactive.Power_kVarh"
]

X = df[features]

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

df["anomaly"] = model.fit_predict(X)

anomalies = df[df["anomaly"] == -1]

c1,c2 = st.columns(2)
c1.metric("Records", len(df))
c2.metric("Anomalies", len(anomalies))

fig = px.scatter(
    df,
    x="Usage_kWh",
    y="CO2(tCO2)",
    color=df["anomaly"].astype(str),
    title="Anomaly Detection"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(anomalies.head(100), use_container_width=True)
