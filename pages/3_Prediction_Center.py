import os
import joblib
import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
r2_score,
mean_absolute_error,
mean_squared_error
)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
RandomForestRegressor,
GradientBoostingRegressor
)

st.set_page_config(
page_title="Prediction Center",
page_icon="🤖",
layout="wide"
)

st.title("🤖 Carbon Emission Prediction Center")

=====================================================
LOAD DATA
=====================================================

try:

if (
    "dataset" in st.session_state
    and st.session_state.dataset is not None
):
    df = st.session_state.dataset.copy()

else:
    df = pd.read_csv(
        "data/Steel_industry_data.csv"
    )

except Exception as e:

st.error(f"Dataset Error: {e}")
st.stop()
=====================================================
REQUIRED COLUMNS
=====================================================

required_columns = [
"Usage_kWh",
"Lagging_Current_Reactive.Power_kVarh",
"Leading_Current_Reactive_Power_kVarh",
"CO2(tCO2)",
"Lagging_Current_Power_Factor",
"Leading_Current_Power_Factor",
"NSM"
]

missing = [
c for c in required_columns
if c not in df.columns
]

if missing:

st.error(
    f"Missing columns: {missing}"
)

st.stop()
=====================================================
PREPROCESSING
=====================================================

if "Date" in df.columns:

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

target = "CO2(tCO2)"

features = [
"Usage_kWh",
"Lagging_Current_Reactive.Power_kVarh",
"Leading_Current_Reactive_Power_kVarh",
"Lagging_Current_Power_Factor",
"Leading_Current_Power_Factor",
"NSM"
]

df = df.dropna(
subset=features + [target]
)

X = df[features]
y = df[target]

=====================================================
DATA DEBUG
=====================================================

st.subheader("Dataset Information")

c1, c2, c3 = st.columns(3)

with c1:
st.metric(
"Rows",
len(df)
)

with c2:
st.metric(
"Unique CO₂ Values",
int(y.nunique())
)

with c3:
st.metric(
"Average CO₂",
round(float(y.mean()), 4)
)

=====================================================
TRAIN MODEL
=====================================================

X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.2,
random_state=42
)

models = {
"Linear Regression":
LinearRegression(),

"Random Forest":
    RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ),

"Gradient Boosting":
    GradientBoostingRegressor(
        random_state=42
    )

}

best_model = None
best_name = ""
best_r2 = -999

results = []

for name, model in models.items():

pipe = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "model",
        model
    )
])

pipe.fit(
    X_train,
    y_train
)

preds = pipe.predict(
    X_test
)

r2 = r2_score(
    y_test,
    preds
)

mae = mean_absolute_error(
    y_test,
    preds
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        preds
    )
)

results.append(
    [
        name,
        round(r2, 4),
        round(mae, 4),
        round(rmse, 4)
    ]
)

if r2 > best_r2:

    best_r2 = r2
    best_model = pipe
    best_name = name
=====================================================
SAVE MODEL
=====================================================

os.makedirs(
"models",
exist_ok=True
)

joblib.dump(
best_model,
"models/best_carbon_model.pkl"
)

=====================================================
MODEL RESULTS
=====================================================

st.subheader("Model Comparison")

results_df = pd.DataFrame(
results,
columns=[
"Model",
"R²",
"MAE",
"RMSE"
]
)

st.dataframe(
results_df,
use_container_width=True
)

st.success(
f"Best Model: {best_name} | R² = {best_r2:.4f}"
)

=====================================================
USER INPUT
=====================================================

st.subheader(
"Future CO₂ Emission Prediction"
)

col1, col2, col3 = st.columns(3)

usage = col1.number_input(
"Usage kWh",
value=float(df["Usage_kWh"].median())
)

lagging = col2.number_input(
"Lagging Reactive Power",
value=float(
df[
"Lagging_Current_Reactive.Power_kVarh"
].median()
)
)

leading = col3.number_input(
"Leading Reactive Power",
value=float(
df[
"Leading_Current_Reactive_Power_kVarh"
].median()
)
)

col4, col5, col6 = st.columns(3)

lag_pf = col4.number_input(
"Lagging Power Factor",
value=float(
df[
"Lagging_Current_Power_Factor"
].median()
)
)

lead_pf = col5.number_input(
"Leading Power Factor",
value=float(
df[
"Leading_Current_Power_Factor"
].median()
)
)

nsm = col6.number_input(
"NSM",
value=float(df["NSM"].median())
)

=====================================================
PREDICTION
=====================================================

if st.button(
"Predict CO₂ Emission"
):

sample = pd.DataFrame(
    [[
        usage,
        lagging,
        leading,
        lag_pf,
        lead_pf,
        nsm
    ]],
    columns=features
)

prediction = float(
    best_model.predict(sample)[0]
)

st.metric(
    "Predicted CO₂ Emission",
    f"{prediction:.6f} tCO₂"
)

st.info(
    f"""

Next Day Forecast:
{prediction:.6f} tCO₂

Next Week Forecast:
{prediction * 7:.6f} tCO₂

Next Month Forecast:
{prediction * 30:.6f} tCO₂
"""
)
