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

# =====================================================
# LOAD DATA
# =====================================================

if (
    "dataset" in st.session_state
    and st.session_state.dataset is not None
):
    df = st.session_state.dataset.copy()

else:
    try:
        df = pd.read_csv(
            "data/Steel_industry_data.csv"
        )

    except Exception as e:

        st.error(
            f"Dataset Error: {e}"
        )

        st.stop()

# =====================================================
# VALIDATE DATASET
# =====================================================

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
    col
    for col in required_columns
    if col not in df.columns
]

if missing:

    st.error(
        f"Missing Columns: {missing}"
    )

    st.stop()

# =====================================================
# PREPROCESSING
# =====================================================

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

# =====================================================
# MODEL
# =====================================================

MODEL_PATH = "models/best_carbon_model.pkl"

best_model = None

if os.path.exists(MODEL_PATH):

    try:

        best_model = joblib.load(
            MODEL_PATH
        )

        st.success(
            "Loaded Existing Trained Model"
        )

    except:

        best_model = None

# =====================================================
# TRAIN MODEL
# =====================================================

if best_model is None:

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

    best_r2 = -999
    best_name = ""

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
                r2,
                mae,
                rmse
            ]
        )

        if r2 > best_r2:

            best_r2 = r2
            best_model = pipe
            best_name = name

    os.makedirs(
        "models",
        exist_ok=True
    )

    joblib.dump(
        best_model,
        MODEL_PATH
    )

    st.success(
        f"Best Model Saved: {best_name}"
    )

# =====================================================
# INPUTS
# =====================================================

st.subheader(
    "Future CO₂ Emission Prediction"
)

col1, col2, col3 = st.columns(3)

usage = col1.number_input(
    "Usage kWh",
    value=float(
        df["Usage_kWh"].median()
    )
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
    value=float(
        df["NSM"].median()
    )
)

# =====================================================
# PREDICTION
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

    prediction = max(
        prediction,
        0
    )

    st.write(
        "Raw Prediction:",
        prediction
    )

    st.metric(
        "Predicted CO₂ Emission",
        f"{prediction:.8f} tCO₂"
    )

    st.info(
        f"""
Next Day Forecast:
{prediction:.8f} tCO₂

Next Week Forecast:
{prediction*7:.8f} tCO₂

Next Month Forecast:
{prediction*30:.8f} tCO₂
"""
    )
