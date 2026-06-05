# pages/3_Prediction_Center.py

import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    GridSearchCV
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

# ---------------------------------------------------
# TARGET
# ---------------------------------------------------

TARGET = "CO2(tCO2)"

# ---------------------------------------------------
# FEATURE SELECTION
# ---------------------------------------------------

exclude_cols = [
    TARGET,
    "Date"
]

features = [
    c for c in df.columns
    if c not in exclude_cols
]

X = df[features].copy()

# encode categoricals

for col in X.select_dtypes(include="object").columns:
    X[col] = X[col].astype("category").cat.codes

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
# MODEL TRAINING BUTTON
# ---------------------------------------------------

if st.button("🚀 Train Models"):

    with st.spinner("Training Models..."):

        results = []

        models = {
            "Linear Regression": LinearRegression(),

            "Random Forest": RandomForestRegressor(
                random_state=42
            ),

            "Gradient Boosting": GradientBoostingRegressor(
                random_state=42
            )
        }

        best_model = None
        best_score = -999
        best_name = ""

        for name, model in models.items():

            pipeline = Pipeline([
                ("scaler", StandardScaler()),
                ("model", model)
            ])

            pipeline.fit(
                X_train,
                y_train
            )

            preds = pipeline.predict(X_test)

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

        joblib.dump(
            best_model,
            "models/carbon_model.pkl"
        )

        st.session_state["best_model"] = best_model
        st.session_state["best_model_name"] = best_name

        result_df = pd.DataFrame(
            results,
            columns=[
                "Model",
                "R2",
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

if "best_model" not in st.session_state:

    if os.path.exists(
        "models/carbon_model.pkl"
    ):

        model = joblib.load(
            "models/carbon_model.pkl"
        )

    else:

        st.info(
            "Train model first."
        )

        st.stop()

else:

    model = st.session_state["best_model"]

# ---------------------------------------------------
# FEATURE IMPORTANCE
# ---------------------------------------------------

st.markdown("---")
st.subheader("📈 Feature Importance")

try:

    reg = model.named_steps["model"]

    if hasattr(
        reg,
        "feature_importances_"
    ):

        importance = pd.DataFrame({

            "Feature": X.columns,

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
            orientation="h"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

except:
    st.info(
        "Feature importance unavailable."
    )

# ---------------------------------------------------
# SINGLE RECORD PREDICTION
# ---------------------------------------------------

st.markdown("---")
st.subheader("🎯 Predict Emissions")

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
st.subheader("📅 Next Day Forecast")

next_day = latest_record.copy()

next_day_prediction = model.predict(
    next_day
)[0]

st.metric(
    "Next Day CO₂",
    f"{next_day_prediction:.4f}"
)

# ---------------------------------------------------
# NEXT WEEK FORECAST
# ---------------------------------------------------

st.markdown("---")
st.subheader("📆 Next Week Forecast")

forecast_7 = []

base = latest_record.copy()

for i in range(7):

    pred = model.predict(base)[0]

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
# MONTHLY FORECAST
# ---------------------------------------------------

st.markdown("---")
st.subheader("📊 Monthly Emission Forecast")

forecast_30 = []

for i in range(30):

    pred = model.predict(base)[0]

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
# FORECAST SUMMARY
# ---------------------------------------------------

st.subheader("📋 Forecast Summary")

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
# FORECAST TABLE
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
    label="⬇ Download Forecast",
    data=csv,
    file_name="monthly_forecast.csv",
    mime="text/csv"
)

# ---------------------------------------------------
# MODEL INFO
# ---------------------------------------------------

st.markdown("---")

st.info(
    """
    Models Evaluated

    • Linear Regression

    • Random Forest Regressor

    • Gradient Boosting Regressor

    Best model is automatically selected
    based on highest R² Score.
    """
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "Steel Industry Carbon Footprint & ESG Analytics Platform | Prediction Center"
)
