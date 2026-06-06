# pages/3_Prediction_Center.py

import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from sklearn.model_selection import (
    train_test_split,
    cross_val_score
)

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error
)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Prediction Center",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Carbon Emission Prediction Center")
st.markdown("---")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

if "data" not in st.session_state:
    st.warning(
        "Please upload dataset from Executive Summary page."
    )
    st.stop()

df = st.session_state["data"].copy()

TARGET = "CO2(tCO2)"

# ---------------------------------------------------
# DATA CLEANING
# ---------------------------------------------------

df = df.replace(
    [np.inf, -np.inf],
    np.nan
)

df = df.dropna(
    subset=[TARGET]
)

df = df.fillna(0)

# ---------------------------------------------------
# FEATURE SELECTION
# ---------------------------------------------------

exclude_cols = [TARGET]

if "Date" in df.columns:
    exclude_cols.append("Date")

features = [
    col
    for col in df.columns
    if col not in exclude_cols
]

X = df[features].copy()

# Convert booleans

for col in X.select_dtypes(include=["bool"]).columns:
    X[col] = X[col].astype(int)

# Convert categoricals safely

categorical_cols = X.select_dtypes(
    include=["object", "string", "category"]
).columns.tolist()

if len(categorical_cols) > 0:

    X = pd.get_dummies(
        X,
        columns=categorical_cols,
        drop_first=True,
        dtype=int
    )

# Convert everything to numeric

X = X.apply(
    pd.to_numeric,
    errors="coerce"
)

X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

X = X.fillna(0)

y = pd.to_numeric(
    df[TARGET],
    errors="coerce"
).fillna(0)

# ---------------------------------------------------
# TRAIN TEST SPLIT
# ---------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# ---------------------------------------------------
# TRAIN MODELS
# ---------------------------------------------------

if st.button("🚀 Train Models"):

    with st.spinner("Training Models..."):

        results = []

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
        best_score = -999999

        for name, model in models.items():

            pipeline = Pipeline([
                (
                    "scaler",
                    StandardScaler()
                ),
                (
                    "model",
                    model
                )
            ])

            pipeline.fit(
                X_train,
                y_train
            )

            preds = pipeline.predict(
                X_test
            )

            r2 = r2_score(
                y_test,
                preds
            )

            rmse = np.sqrt(
                mean_squared_error(
                    y_test,
                    preds
                )
            )

            mae = mean_absolute_error(
                y_test,
                preds
            )

            try:

                cv_score = np.mean(
                    cross_val_score(
                        pipeline,
                        X,
                        y,
                        cv=min(5, len(X)),
                        scoring="r2"
                    )
                )
            
            except Exception:

                cv_score = 0

            results.append([
                name,
                r2,
                rmse,
                mae,
                cv_score
            ])

            if r2 > best_score:

                best_score = r2
                best_model = pipeline
                best_name = name

        # -----------------------------------
        # SAVE MODEL
        # -----------------------------------

        os.makedirs(
            "models",
            exist_ok=True
        )

        try:

            joblib.dump(
                best_model,
                "models/carbon_model.pkl"
            )

        except Exception as e:

            st.warning(
                f"Model save failed: {e}"
            )

        st.session_state[
            "best_model"
        ] = best_model

        st.session_state[
            "best_model_name"
        ] = best_name

        result_df = pd.DataFrame(
            results,
            columns=[
                "Model",
                "R²",
                "RMSE",
                "MAE",
                "CV Score"
            ]
        )

        st.success(
            f"Best Model: {best_name}"
        )

        st.subheader(
            "📊 Model Performance"
        )

        st.dataframe(
            result_df,
            use_container_width=True
        )

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

model = None

if "best_model" in st.session_state:

    model = st.session_state["best_model"]

else:

    model_file = "models/carbon_model.pkl"

    if os.path.exists(model_file):

        try:

            model = joblib.load(
                model_file
            )

        except Exception:

            st.warning(
                """
                Saved model is incompatible with
                current Python/sklearn version.

                Delete:

                models/carbon_model.pkl

                Then click Train Models again.
                """
            )

            st.stop()

    else:

        st.info(
            "No trained model found. Click Train Models."
        )

        st.stop()

# ---------------------------------------------------
# PREDICTION
# ---------------------------------------------------

st.markdown("---")
st.subheader(
    "🎯 Predict Emissions"
)

latest_record = X.iloc[-1:]

prediction = model.predict(
    latest_record
)[0]

st.metric(
    "Predicted CO₂ Emission",
    f"{prediction:.4f}"
)

# ---------------------------------------------------
# NEXT DAY FORECAST
# ---------------------------------------------------

st.markdown("---")
st.subheader(
    "📅 Next Day Forecast"
)

next_day_prediction = model.predict(
    latest_record
)[0]

st.metric(
    "Next Day CO₂",
    f"{next_day_prediction:.4f}"
)

# ---------------------------------------------------
# WEEK FORECAST
# ---------------------------------------------------

st.markdown("---")
st.subheader(
    "📆 Next Week Forecast"
)

forecast_7 = []

for _ in range(7):

    pred = model.predict(
        latest_record
    )[0]

    forecast_7.append(pred)

forecast_week = pd.DataFrame({

    "Day":
        np.arange(1, 8),

    "Forecast_CO2":
        forecast_7

})

fig = px.line(
    forecast_week,
    x="Day",
    y="Forecast_CO2",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# MONTH FORECAST
# ---------------------------------------------------

st.markdown("---")
st.subheader(
    "📊 Monthly Forecast"
)

forecast_30 = []

for _ in range(30):

    pred = model.predict(
        latest_record
    )[0]

    forecast_30.append(pred)

monthly_forecast = pd.DataFrame({

    "Day":
        np.arange(1, 31),

    "Forecast_CO2":
        forecast_30

})

fig = px.area(
    monthly_forecast,
    x="Day",
    y="Forecast_CO2"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# SUMMARY
# ---------------------------------------------------

st.subheader(
    "📋 Forecast Summary"
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Next Day",
        round(
            forecast_30[0],
            4
        )
    )

with c2:
    st.metric(
        "7-Day Total",
        round(
            sum(forecast_7),
            4
        )
    )

with c3:
    st.metric(
        "30-Day Total",
        round(
            sum(forecast_30),
            4
        )
    )

# ---------------------------------------------------
# TABLE
# ---------------------------------------------------

st.subheader(
    "Forecast Dataset"
)

st.dataframe(
    monthly_forecast,
    use_container_width=True
)

# ---------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------

csv = monthly_forecast.to_csv(
    index=False
)

st.download_button(
    "⬇ Download Forecast",
    csv,
    "monthly_forecast.csv",
    "text/csv"
)

# ---------------------------------------------------
# INFO
# ---------------------------------------------------

st.markdown("---")

st.info(
    """
    Models Evaluated

    • Linear Regression
    • Random Forest Regressor
    • Gradient Boosting Regressor

    Best model is selected automatically
    using highest R² score.
    """
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Steel Industry Carbon Footprint & ESG Analytics Platform | Prediction Center"
)
