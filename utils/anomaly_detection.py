# utils/anomaly_detection.py

import pandas as pd
import numpy as np
import logging

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# -----------------------------------------------------
# LOGGER
# -----------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -----------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------

DEFAULT_CONTAMINATION = 0.02
DEFAULT_WINDOW = 96
DEFAULT_MULTIPLIER = 1.5

# -----------------------------------------------------
# PREPARE FEATURES
# -----------------------------------------------------

def prepare_features(df):

    features = [

        "Usage_kWh",

        "CO2(tCO2)",

        "Lagging_Current_Reactive.Power_kVarh",

        "Leading_Current_Reactive_Power_kVarh",

        "Lagging_Current_Power_Factor",

        "Leading_Current_Power_Factor"
    ]

    available = [

        col
        for col in features
        if col in df.columns
    ]

    X = df[available].copy()

    X = X.fillna(0)

    return X

# -----------------------------------------------------
# ISOLATION FOREST
# -----------------------------------------------------

def isolation_forest_detection(
    df,
    contamination=DEFAULT_CONTAMINATION
):

    data = df.copy()

    X = prepare_features(data)

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        contamination=contamination,
        random_state=42
    )

    data["Anomaly"] = model.fit_predict(
        X_scaled
    )

    data["Anomaly_Flag"] = np.where(
        data["Anomaly"] == -1,
        "Anomaly",
        "Normal"
    )

    data["Anomaly_Score"] = (
        model.decision_function(
            X_scaled
        )
    )

    return data

# -----------------------------------------------------
# USAGE SPIKES
# -----------------------------------------------------

def detect_usage_spikes(
    df,
    window=DEFAULT_WINDOW,
    multiplier=DEFAULT_MULTIPLIER
):

    rolling = (

        df["Usage_kWh"]

        .rolling(
            window,
            min_periods=1
        )

        .median()

    )

    return (
        df["Usage_kWh"]
        >
        rolling * multiplier
    )

# -----------------------------------------------------
# CO2 SPIKES
# -----------------------------------------------------

def detect_co2_spikes(
    df,
    window=DEFAULT_WINDOW,
    multiplier=DEFAULT_MULTIPLIER
):

    rolling = (

        df["CO2(tCO2)"]

        .rolling(
            window,
            min_periods=1
        )

        .median()

    )

    return (
        df["CO2(tCO2)"]
        >
        rolling * multiplier
    )

# -----------------------------------------------------
# REACTIVE POWER SPIKES
# -----------------------------------------------------

def detect_reactive_power_spikes(
    df,
    window=DEFAULT_WINDOW,
    multiplier=DEFAULT_MULTIPLIER
):

    reactive = (

        df[
            "Lagging_Current_Reactive.Power_kVarh"
        ]

        +

        df[
            "Leading_Current_Reactive_Power_kVarh"
        ]

    )

    rolling = (

        reactive

        .rolling(
            window,
            min_periods=1
        )

        .median()

    )

    return (
        reactive
        >
        rolling * multiplier
    )

# -----------------------------------------------------
# POWER FACTOR DEVIATION
# -----------------------------------------------------

def detect_power_factor_anomaly(df):

    return (

        (
            df[
                "Lagging_Current_Power_Factor"
            ] < 80
        )

        |

        (
            df[
                "Leading_Current_Power_Factor"
            ] < 80
        )

    )

# -----------------------------------------------------
# ROOT CAUSE ANALYSIS
# -----------------------------------------------------

def identify_root_cause(row):

    causes = []

    if row["Usage_Spike"]:
        causes.append(
            "Usage Spike"
        )

    if row["CO2_Spike"]:
        causes.append(
            "CO2 Spike"
        )

    if row["Reactive_Spike"]:
        causes.append(
            "Reactive Power"
        )

    if row["PF_Anomaly"]:
        causes.append(
            "Power Factor"
        )

    if len(causes) == 0:
        return "Normal"

    return ", ".join(causes)

# -----------------------------------------------------
# SEVERITY SCORE
# -----------------------------------------------------

def calculate_severity(df):

    severity = (

        df["Usage_Spike"].astype(int)

        +

        df["CO2_Spike"].astype(int)

        +

        df["Reactive_Spike"].astype(int)

        +

        df["PF_Anomaly"].astype(int)

    )

    return severity * 25

# -----------------------------------------------------
# ALERT LEVELS
# -----------------------------------------------------

def generate_alert_level(score):

    if score >= 75:
        return "Critical"

    elif score >= 50:
        return "High"

    elif score >= 25:
        return "Medium"

    return "Low"

# -----------------------------------------------------
# RUN COMPLETE ANALYSIS
# -----------------------------------------------------

def run_anomaly_detection(
    df,
    contamination=DEFAULT_CONTAMINATION
):

    logger.info(
        "Running anomaly detection..."
    )

    data = isolation_forest_detection(
        df,
        contamination
    )

    data["Usage_Spike"] = (
        detect_usage_spikes(data)
    )

    data["CO2_Spike"] = (
        detect_co2_spikes(data)
    )

    data["Reactive_Spike"] = (
        detect_reactive_power_spikes(data)
    )

    data["PF_Anomaly"] = (
        detect_power_factor_anomaly(data)
    )

    data["Root_Cause"] = data.apply(
        identify_root_cause,
        axis=1
    )

    data["Severity_Score"] = (
        calculate_severity(data)
    )

    data["Alert_Level"] = (
        data["Severity_Score"]
        .apply(generate_alert_level)
    )

    logger.info(
        "Anomaly detection completed."
    )

    return data

# -----------------------------------------------------
# ALERT SUMMARY
# -----------------------------------------------------

def alert_summary(df):

    summary = {

        "Total_Records":
            len(df),

        "Total_Anomalies":
            int(
                (
                    df["Anomaly_Flag"]
                    == "Anomaly"
                ).sum()
            ),

        "Critical_Alerts":
            int(
                (
                    df["Alert_Level"]
                    == "Critical"
                ).sum()
            ),

        "High_Alerts":
            int(
                (
                    df["Alert_Level"]
                    == "High"
                ).sum()
            ),

        "Medium_Alerts":
            int(
                (
                    df["Alert_Level"]
                    == "Medium"
                ).sum()
            ),

        "Low_Alerts":
            int(
                (
                    df["Alert_Level"]
                    == "Low"
                ).sum()
            )
    }

    return summary

# -----------------------------------------------------
# ROOT CAUSE SUMMARY
# -----------------------------------------------------

def root_cause_summary(df):

    return (

        df["Root_Cause"]

        .value_counts()

        .reset_index()

        .rename(
            columns={
                "index": "Root_Cause",
                "Root_Cause": "Count"
            }
        )

    )

# -----------------------------------------------------
# CRITICAL ALERTS
# -----------------------------------------------------

def critical_alerts(df):

    return (

        df[
            df["Alert_Level"]
            == "Critical"
        ]

        .sort_values(
            "Severity_Score",
            ascending=False
        )

    )

# -----------------------------------------------------
# TOP ANOMALIES
# -----------------------------------------------------

def top_anomalies(
    df,
    top_n=25
):

    return (

        df.sort_values(
            "Severity_Score",
            ascending=False
        )

        .head(top_n)

    )

# -----------------------------------------------------
# EXPORT REPORT
# -----------------------------------------------------

def export_alert_report(df):

    cols = [

        "Anomaly_Flag",

        "Severity_Score",

        "Alert_Level",

        "Root_Cause"
    ]

    available = [

        c for c in cols
        if c in df.columns
    ]

    return df[
        available
    ].copy()

# -----------------------------------------------------
# ESG RISK SCORE
# -----------------------------------------------------

def calculate_esg_risk_score(df):

    critical = (
        df["Alert_Level"]
        == "Critical"
    ).sum()

    high = (
        df["Alert_Level"]
        == "High"
    ).sum()

    medium = (
        df["Alert_Level"]
        == "Medium"
    ).sum()

    score = (

        critical * 5

        +

        high * 3

        +

        medium * 1

    )

    return round(score, 2)

# -----------------------------------------------------
# RECOMMENDATION ENGINE
# -----------------------------------------------------

def generate_recommendations(df):

    recommendations = []

    if df["Usage_Spike"].sum() > 0:

        recommendations.append(
            "Investigate peak energy consumption periods."
        )

    if df["CO2_Spike"].sum() > 0:

        recommendations.append(
            "Review high-emission production activities."
        )

    if df["Reactive_Spike"].sum() > 0:

        recommendations.append(
            "Optimize reactive power compensation systems."
        )

    if df["PF_Anomaly"].sum() > 0:

        recommendations.append(
            "Improve power factor correction equipment."
        )

    if len(recommendations) == 0:

        recommendations.append(
            "No major anomalies detected."
        )

    return recommendations

# -----------------------------------------------------
# TEST
# -----------------------------------------------------

if __name__ == "__main__":

    print(
        "Steel Industry Anomaly Detection Module Loaded"
    )
