import os
import streamlit as st
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Prediction Center",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Carbon Emission Prediction Center")

# =====================================================
# LOAD DATA
# =====================================================

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

# =====================================================
# REQUIRED COLUMNS
# =====================================================

required_columns = [
    "Usage_kWh",
    "Lagging_Current_Reactive.Power_kVarh",
    "Leading_Current_Reactive_Power_kVarh",
    "Lagging_Current_Power_Factor",
    "Leading_Current_Power_Factor",
    "NSM",
    "CO2(tCO2)"
]

missing = [
    col for col in required_columns
    if col not in df.columns
]

if missing:

    st.error(
        f"Missing Columns: {missing}"
    )

    st.stop()

# =====================================================
# DATA PREPARATION
# =====================================================

features = [
    "Usage_kWh",
    "Lagging_Current_Reactive.Power_kVarh",
    "Leading_Current_Reactive_Power_kVarh",
    "Lagging_Current_Power_Factor",
    "Leading_Current_Power_Factor",
    "NSM"
]

target = "CO2(tCO2)"

df = df.dropna(
    subset=features + [target]
)

X = df[features]
y = df[target]

# =====================================================
# TRAIN MODEL
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    )
}

best_model = None
best_r2 = -999
best_name = ""

for name, model in models.items():

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", model)
    ])

    pipe.fit(
        X_train,
        y_train
    )

    preds = pipe.predict(
        X_test
    )

    score = r2_score(
        y_test,
        preds
    )

    if score > best_r2:

        best_r2 = score
        best_model = pipe
        best_name = name

# =====================================================
# SAVE MODEL
# =====================================================

os.makedirs(
    "models",
    exist_ok=True
)

joblib.dump(
    best_model,
    "models/best_carbon_model.pkl"
)

st.success(
    f"Best Model: {best_name} | R² = {best_r2:.4f}"
)

# =====================================================
# USER INPUT
# =====================================================

st.subheader(
    "Future CO₂ Emission Prediction"
)

col1, col2, col3 = st.columns(3)

with col1:
    usage = st.number_input(
        "Usage kWh",
        value=float(df["Usage_kWh"].median())
    )

with col2:
    lagging = st.number_input(
        "Lagging Reactive Power",
        value=float(
            df[
                "Lagging_Current_Reactive.Power_kVarh"
            ].median()
        )
    )

with col3:
    leading = st.number_input(
        "Leading Reactive Power",
        value=float(
            df[
                "Leading_Current_Reactive_Power_kVarh"
            ].median()
        )
    )

col4, col5, col6 = st.columns(3)

with col4:
    lag_pf = st.number_input(
        "Lagging Power Factor",
        value=float(
            df[
                "Lagging_Current_Power_Factor"
            ].median()
        )
    )

with col5:
    lead_pf = st.number_input(
        "Leading Power Factor",
        value=float(
            df[
                "Leading_Current_Power_Factor"
            ].median()
        )
    )

with col6:
    nsm = st.number_input(
        "NSM",
        value=float(
            df["NSM"].median()
        )
    )

# =====================================================
# PREDICT
# =====================================================

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
