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
    c for c in df.columns
    if c not in exclude_cols
]

X = df[features].copy()

# Handle categorical columns

cat_cols = X.select_dtypes(
    include=["object", "string", "category"]
).columns

for col in cat_cols:

    X[col] = (
        X[col]
        .astype(str)
        .fillna("Unknown")
    )

X = pd.get_dummies(
    X,
    columns=cat_cols,
    drop_first=True
)

X = X.replace(
    [np.inf, -np.inf],
    np.nan
)

X = X.fillna(0)

y = df[TARGET]

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

            cv_score = np.mean(
                cross_val_score(
                    pipeline,
                    X,
                    y,
                    cv=5,
                    scoring="r2"
                )
            )

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

if "best_model" in st.session_state:

    model = st.session_state[
        "best_model"
    ]

else:

    if os.path.exists(
        "models/carbon_model.pkl"
    ):

        try:

            model = joblib.load(
                "models/carbon_model.pkl"
            )

        except Exception:

            st.error(
                """
                Saved model is incompatible
                with current Python/sklearn
                version.

                Delete:
                models/carbon_model.pkl

                Then retrain.
                """
            )

            st.stop()

    else:

        st.info(
            "Train a model first."
        )

        st.stop()

# ---------------------------------------------------
# FEATURE IMPORTANCE
# ---------------------------------------------------

st.markdown("---")
st.subheader(
    "📈 Feature Importance"
)

try:

    reg = model.named_steps[
        "model"
    ]

    if hasattr(
        reg,
        "feature_importances_"
    ):

        importance = pd.DataFrame({

            "Feature":
                X.columns,

            "Importance":
                reg.feature_importances_

        })

        importance = importance.sort_values(
            "Importance",
            ascending=False
        )

        fig = px.bar(
            importance.head(15),
            x="Importance",
            y="Feature",
            orientation="h",
            title="Top 15 Features"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

except Exception:

    st.info(
        "Feature importance unavailable."
    )

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
