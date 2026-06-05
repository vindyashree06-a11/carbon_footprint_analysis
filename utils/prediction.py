# utils/prediction.py

import os
import joblib
import logging
import warnings

import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    GridSearchCV
)

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

warnings.filterwarnings("ignore")

# -------------------------------------------------------
# LOGGER
# -------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -------------------------------------------------------
# CONSTANTS
# -------------------------------------------------------

TARGET = "CO2(tCO2)"

MODEL_PATH = "models/carbon_model.pkl"

# -------------------------------------------------------
# PREPARE DATA
# -------------------------------------------------------

def prepare_data(df):

    data = df.copy()

    drop_cols = []

    if TARGET in data.columns:
        pass
    else:
        raise ValueError(
            f"{TARGET} column missing."
        )

    if "Date" in data.columns:
        drop_cols.append("Date")

    X = data.drop(
        columns=[TARGET] + drop_cols,
        errors="ignore"
    )

    y = data[TARGET]

    # Encode categoricals

    for col in X.select_dtypes(
        include=["object", "category"]
    ).columns:

        X[col] = (
            X[col]
            .astype("category")
            .cat.codes
        )

    X = X.fillna(0)

    return X, y

# -------------------------------------------------------
# TRAIN TEST SPLIT
# -------------------------------------------------------

def split_data(
    X,
    y,
    test_size=0.2,
    random_state=42
):

    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state
    )

# -------------------------------------------------------
# EVALUATION
# -------------------------------------------------------

def evaluate_model(
    model,
    X_test,
    y_test
):

    predictions = model.predict(
        X_test
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    return {

        "R2": round(r2, 4),

        "RMSE": round(rmse, 4),

        "MAE": round(mae, 4)
    }

# -------------------------------------------------------
# LINEAR REGRESSION
# -------------------------------------------------------

def train_linear_regression(
    X_train,
    y_train
):

    pipeline = Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            LinearRegression()
        )
    ])

    pipeline.fit(
        X_train,
        y_train
    )

    return pipeline

# -------------------------------------------------------
# RANDOM FOREST
# -------------------------------------------------------

def train_random_forest(
    X_train,
    y_train
):

    pipeline = Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            RandomForestRegressor(
                random_state=42
            )
        )
    ])

    params = {

        "model__n_estimators":
            [100, 200],

        "model__max_depth":
            [5, 10, None],

        "model__min_samples_split":
            [2, 5]
    }

    grid = GridSearchCV(
        pipeline,
        params,
        cv=3,
        scoring="r2",
        n_jobs=-1
    )

    grid.fit(
        X_train,
        y_train
    )

    return grid.best_estimator_

# -------------------------------------------------------
# GRADIENT BOOSTING
# -------------------------------------------------------

def train_gradient_boosting(
    X_train,
    y_train
):

    pipeline = Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            GradientBoostingRegressor(
                random_state=42
            )
        )
    ])

    params = {

        "model__n_estimators":
            [100, 200],

        "model__learning_rate":
            [0.05, 0.1],

        "model__max_depth":
            [3, 5]
    }

    grid = GridSearchCV(
        pipeline,
        params,
        cv=3,
        scoring="r2",
        n_jobs=-1
    )

    grid.fit(
        X_train,
        y_train
    )

    return grid.best_estimator_

# -------------------------------------------------------
# CROSS VALIDATION
# -------------------------------------------------------

def calculate_cv_score(
    model,
    X,
    y
):

    scores = cross_val_score(
        model,
        X,
        y,
        cv=5,
        scoring="r2"
    )

    return round(
        scores.mean(),
        4
    )

# -------------------------------------------------------
# TRAIN ALL MODELS
# -------------------------------------------------------

def train_models(df):

    logger.info(
        "Training Models..."
    )

    X, y = prepare_data(df)

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = split_data(X, y)

    models = {}

    results = []

    # Linear Regression

    lr = train_linear_regression(
        X_train,
        y_train
    )

    lr_metrics = evaluate_model(
        lr,
        X_test,
        y_test
    )

    lr_cv = calculate_cv_score(
        lr,
        X,
        y
    )

    results.append({

        "Model":
            "Linear Regression",

        **lr_metrics,

        "CV":
            lr_cv
    })

    models["Linear Regression"] = lr

    # Random Forest

    rf = train_random_forest(
        X_train,
        y_train
    )

    rf_metrics = evaluate_model(
        rf,
        X_test,
        y_test
    )

    rf_cv = calculate_cv_score(
        rf,
        X,
        y
    )

    results.append({

        "Model":
            "Random Forest",

        **rf_metrics,

        "CV":
            rf_cv
    })

    models["Random Forest"] = rf

    # Gradient Boosting

    gb = train_gradient_boosting(
        X_train,
        y_train
    )

    gb_metrics = evaluate_model(
        gb,
        X_test,
        y_test
    )

    gb_cv = calculate_cv_score(
        gb,
        X,
        y
    )

    results.append({

        "Model":
            "Gradient Boosting",

        **gb_metrics,

        "CV":
            gb_cv
    })

    models["Gradient Boosting"] = gb

    results_df = pd.DataFrame(
        results
    )

    best_row = results_df.loc[
        results_df["R2"].idxmax()
    ]

    best_model_name = best_row["Model"]

    best_model = models[
        best_model_name
    ]

    logger.info(
        f"Best Model: {best_model_name}"
    )

    return (
        best_model,
        results_df,
        X,
        y
    )

# -------------------------------------------------------
# SAVE MODEL
# -------------------------------------------------------

def save_model(
    model,
    path=MODEL_PATH
):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    joblib.dump(
        model,
        path
    )

    logger.info(
        f"Model saved at {path}"
    )

# -------------------------------------------------------
# LOAD MODEL
# -------------------------------------------------------

def load_model(
    path=MODEL_PATH
):

    return joblib.load(path)

# -------------------------------------------------------
# PREDICT
# -------------------------------------------------------

def predict(
    model,
    input_data
):

    return model.predict(
        input_data
    )

# -------------------------------------------------------
# NEXT DAY FORECAST
# -------------------------------------------------------

def next_day_forecast(
    model,
    X
):

    latest = X.iloc[-1:]

    prediction = model.predict(
        latest
    )[0]

    return round(
        prediction,
        4
    )

# -------------------------------------------------------
# NEXT WEEK FORECAST
# -------------------------------------------------------

def next_week_forecast(
    model,
    X
):

    latest = X.iloc[-1:]

    forecasts = []

    for _ in range(7):

        pred = model.predict(
            latest
        )[0]

        forecasts.append(pred)

    return pd.DataFrame({

        "Day":
            range(1, 8),

        "Forecast_CO2":
            forecasts
    })

# -------------------------------------------------------
# MONTHLY FORECAST
# -------------------------------------------------------

def monthly_forecast(
    model,
    X,
    days=30
):

    latest = X.iloc[-1:]

    forecasts = []

    for day in range(days):

        pred = model.predict(
            latest
        )[0]

        forecasts.append(pred)

    return pd.DataFrame({

        "Day":
            range(1, days + 1),

        "Forecast_CO2":
            forecasts
    })

# -------------------------------------------------------
# FEATURE IMPORTANCE
# -------------------------------------------------------

def feature_importance(
    model,
    feature_names
):

    try:

        estimator = (
            model.named_steps["model"]
        )

        if hasattr(
            estimator,
            "feature_importances_"
        ):

            return pd.DataFrame({

                "Feature":
                    feature_names,

                "Importance":
                    estimator.feature_importances_

            }).sort_values(
                "Importance",
                ascending=False
            )

    except Exception:
        pass

    return pd.DataFrame()

# -------------------------------------------------------
# COMPLETE PIPELINE
# -------------------------------------------------------

def train_and_save(df):

    (
        best_model,
        results,
        X,
        y
    ) = train_models(df)

    save_model(best_model)

    return {

        "model":
            best_model,

        "results":
            results,

        "X":
            X,

        "y":
            y
    }

# -------------------------------------------------------
# TEST
# -------------------------------------------------------

if __name__ == "__main__":

    print(
        "Steel Industry Prediction Module Loaded"
    )
