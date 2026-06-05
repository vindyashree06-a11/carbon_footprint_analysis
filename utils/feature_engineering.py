# utils/feature_engineering.py

import pandas as pd
import numpy as np
import logging

# =====================================================
# LOGGER
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# =====================================================
# REQUIRED COLUMNS
# =====================================================

REQUIRED_COLUMNS = [
    "Usage_kWh",
    "Lagging_Current_Reactive.Power_kVarh",
    "Leading_Current_Reactive_Power_kVarh",
    "CO2(tCO2)",
    "Lagging_Current_Power_Factor",
    "Leading_Current_Power_Factor"
]


# =====================================================
# HELPER
# =====================================================

def column_exists(df, column):
    return column in df.columns


# =====================================================
# DATE FEATURES
# =====================================================

def create_date_features(df):

    if not column_exists(df, "Date"):
        return df

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Quarter"] = df["Date"].dt.quarter
    df["Day"] = df["Date"].dt.day

    df["Week"] = (
        df["Date"]
        .dt.isocalendar()
        .week
        .astype("Int64")
    )

    df["DayOfYear"] = (
        df["Date"]
        .dt.dayofyear
    )

    return df


# =====================================================
# TOTAL POWER CONSUMPTION
# =====================================================

def create_total_power_consumption(df):

    required = [
        "Usage_kWh",
        "Lagging_Current_Reactive.Power_kVarh",
        "Leading_Current_Reactive_Power_kVarh"
    ]

    if not all(col in df.columns for col in required):
        return df

    df["Total_Power_Consumption"] = (

        df["Usage_kWh"]

        +

        df["Lagging_Current_Reactive.Power_kVarh"]

        +

        df["Leading_Current_Reactive_Power_kVarh"]

    )

    return df


# =====================================================
# REACTIVE POWER RATIO
# =====================================================

def create_reactive_power_ratio(df):

    required = [
        "Usage_kWh",
        "Lagging_Current_Reactive.Power_kVarh",
        "Leading_Current_Reactive_Power_kVarh"
    ]

    if not all(col in df.columns for col in required):
        return df

    reactive = (

        df["Lagging_Current_Reactive.Power_kVarh"]

        +

        df["Leading_Current_Reactive_Power_kVarh"]

    )

    df["Reactive_Power_Ratio"] = (

        reactive

        /

        (df["Usage_kWh"] + 1e-6)

    )

    return df


# =====================================================
# CARBON INTENSITY
# =====================================================

def create_carbon_intensity(df):

    required = [
        "CO2(tCO2)",
        "Usage_kWh"
    ]

    if not all(col in df.columns for col in required):
        return df

    df["Carbon_Intensity"] = (

        df["CO2(tCO2)"]

        /

        (df["Usage_kWh"] + 1e-6)

    )

    return df


# =====================================================
# ROLLING EMISSIONS
# =====================================================

def create_rolling_emissions(df):

    if not column_exists(df, "CO2(tCO2)"):
        return df

    if column_exists(df, "Date"):

        df = df.sort_values(
            by="Date"
        )

    df["Rolling_7_Day_Emission"] = (

        df["CO2(tCO2)"]

        .rolling(
            window=7,
            min_periods=1
        )

        .mean()

    )

    df["Rolling_30_Day_Emission"] = (

        df["CO2(tCO2)"]

        .rolling(
            window=30,
            min_periods=1
        )

        .mean()

    )

    return df


# =====================================================
# ENERGY EFFICIENCY INDEX
# =====================================================

def create_energy_efficiency_index(df):

    required = [
        "Usage_kWh",
        "CO2(tCO2)"
    ]

    if not all(col in df.columns for col in required):
        return df

    df["Energy_Efficiency_Index"] = (

        df["Usage_kWh"]

        /

        (df["CO2(tCO2)"] + 1e-6)

    )

    return df


# =====================================================
# PEAK LOAD FLAG
# =====================================================

def create_peak_load_flag(df):

    if not column_exists(df, "Usage_kWh"):
        return df

    threshold = (
        df["Usage_kWh"]
        .quantile(0.95)
    )

    df["Peak_Load_Flag"] = np.where(
        df["Usage_kWh"] >= threshold,
        1,
        0
    )

    return df


# =====================================================
# WEEKEND FLAG
# =====================================================

def create_weekend_flag(df):

    if column_exists(df, "WeekStatus"):

        df["Weekend_Flag"] = np.where(

            df["WeekStatus"]
            .astype(str)
            .str.lower()
            .str.contains("weekend"),

            1,

            0

        )

    else:

        df["Weekend_Flag"] = 0

    return df


# =====================================================
# SEASONAL USAGE INDEX
# =====================================================

def create_seasonal_usage_index(df):

    if not all(
        col in df.columns
        for col in ["Month", "Usage_kWh"]
    ):
        return df

    monthly_avg = (

        df.groupby("Month")

        ["Usage_kWh"]

        .transform("mean")

    )

    overall_avg = max(
        df["Usage_kWh"].mean(),
        1e-6
    )

    df["Seasonal_Usage_Index"] = (
        monthly_avg / overall_avg
    )

    return df


# =====================================================
# LOAD TYPE ENCODING
# =====================================================

def create_load_type_encoding(df):

    if not column_exists(df, "Load_Type"):
        return df

    df["Load_Type_Encoding"] = (

        df["Load_Type"]

        .astype("category")

        .cat.codes

    )

    return df


# =====================================================
# POWER FACTOR FEATURES
# =====================================================

def create_power_factor_features(df):

    required = [
        "Lagging_Current_Power_Factor",
        "Leading_Current_Power_Factor"
    ]

    if not all(col in df.columns for col in required):
        return df

    df["Average_Power_Factor"] = (

        df["Lagging_Current_Power_Factor"]

        +

        df["Leading_Current_Power_Factor"]

    ) / 2

    df["Power_Factor_Difference"] = abs(

        df["Lagging_Current_Power_Factor"]

        -

        df["Leading_Current_Power_Factor"]

    )

    return df


# =====================================================
# REACTIVE EFFICIENCY
# =====================================================

def create_reactive_efficiency(df):

    required = [
        "Usage_kWh",
        "Lagging_Current_Reactive.Power_kVarh",
        "Leading_Current_Reactive_Power_kVarh"
    ]

    if not all(col in df.columns for col in required):
        return df

    reactive = (

        df["Lagging_Current_Reactive.Power_kVarh"]

        +

        df["Leading_Current_Reactive_Power_kVarh"]

    )

    df["Reactive_Efficiency"] = (

        reactive

        /

        (df["Usage_kWh"] + 1e-6)

    )

    return df


# =====================================================
# LOAD CATEGORY
# =====================================================

def create_load_category(df):

    if not column_exists(df, "Usage_kWh"):
        return df

    q1 = df["Usage_kWh"].quantile(0.33)
    q2 = df["Usage_kWh"].quantile(0.66)

    df["Load_Category"] = pd.cut(
        df["Usage_kWh"],
        bins=[-np.inf, q1, q2, np.inf],
        labels=["Low", "Medium", "High"]
    )

    return df


# =====================================================
# EMISSION CATEGORY
# =====================================================

def create_emission_category(df):

    if not column_exists(df, "CO2(tCO2)"):
        return df

    q1 = df["CO2(tCO2)"].quantile(0.33)
    q2 = df["CO2(tCO2)"].quantile(0.66)

    df["Emission_Category"] = pd.cut(
        df["CO2(tCO2)"],
        bins=[-np.inf, q1, q2, np.inf],
        labels=["Low", "Medium", "High"]
    )

    return df


# =====================================================
# FEATURE REPORT
# =====================================================

def feature_report(df):

    return pd.DataFrame({

        "Feature": df.columns,

        "Data_Type": [
            str(dtype)
            for dtype in df.dtypes
        ],

        "Missing_Values": [
            df[col].isna().sum()
            for col in df.columns
        ]
    })


# =====================================================
# MAIN FEATURE ENGINEERING PIPELINE
# =====================================================

def engineer_features(df):

    logger.info(
        "Starting Feature Engineering..."
    )

    df = create_date_features(df)
    df = create_total_power_consumption(df)
    df = create_reactive_power_ratio(df)
    df = create_carbon_intensity(df)
    df = create_rolling_emissions(df)
    df = create_energy_efficiency_index(df)
    df = create_peak_load_flag(df)
    df = create_weekend_flag(df)
    df = create_seasonal_usage_index(df)
    df = create_load_type_encoding(df)
    df = create_power_factor_features(df)
    df = create_reactive_efficiency(df)
    df = create_load_category(df)
    df = create_emission_category(df)

    logger.info(
        "Feature Engineering Completed"
    )

    return df


# =====================================================
# STREAMLIT COMPATIBILITY FUNCTION
# =====================================================

def create_features(df):
    """
    Used by Streamlit pages:
    from utils.feature_engineering import create_features
    """
    return engineer_features(df)


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print(
        "Steel Industry Feature Engineering Module Loaded"
    )
