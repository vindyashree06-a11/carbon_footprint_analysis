# utils/feature_engineering.py

import pandas as pd
import numpy as np
import logging

# -------------------------------------------------------
# LOGGER
# -------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -------------------------------------------------------
# DATE FEATURES
# -------------------------------------------------------

def create_date_features(df):

    """
    Extract date-based features.
    """

    if "Date" not in df.columns:
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
        .astype(int)
    )

    return df


# -------------------------------------------------------
# TOTAL POWER CONSUMPTION
# -------------------------------------------------------

def create_total_power_consumption(df):

    df["Total_Power_Consumption"] = (
        df["Usage_kWh"]
        +
        df["Lagging_Current_Reactive.Power_kVarh"]
        +
        df["Leading_Current_Reactive_Power_kVarh"]
    )

    return df


# -------------------------------------------------------
# REACTIVE POWER RATIO
# -------------------------------------------------------

def create_reactive_power_ratio(df):

    reactive_power = (
        df["Lagging_Current_Reactive.Power_kVarh"]
        +
        df["Leading_Current_Reactive_Power_kVarh"]
    )

    df["Reactive_Power_Ratio"] = (
        reactive_power
        /
        (
            df["Usage_kWh"] + 1
        )
    )

    return df


# -------------------------------------------------------
# CARBON INTENSITY
# -------------------------------------------------------

def create_carbon_intensity(df):

    df["Carbon_Intensity"] = (
        df["CO2(tCO2)"]
        /
        (
            df["Usage_kWh"] + 1
        )
    )

    return df


# -------------------------------------------------------
# ROLLING EMISSIONS
# -------------------------------------------------------

def create_rolling_emissions(df):

    if "Date" in df.columns:

        df = df.sort_values(
            "Date"
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


# -------------------------------------------------------
# ENERGY EFFICIENCY INDEX
# -------------------------------------------------------

def create_energy_efficiency_index(df):

    df["Energy_Efficiency_Index"] = (
        df["Usage_kWh"]
        /
        (
            df["CO2(tCO2)"] + 0.0001
        )
    )

    return df


# -------------------------------------------------------
# PEAK LOAD FLAG
# -------------------------------------------------------

def create_peak_load_flag(df):

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


# -------------------------------------------------------
# WEEKEND FLAG
# -------------------------------------------------------

def create_weekend_flag(df):

    if "WeekStatus" not in df.columns:

        df["Weekend_Flag"] = 0
        return df

    df["Weekend_Flag"] = np.where(
        df["WeekStatus"]
        .astype(str)
        .str.lower()
        .str.contains("weekend"),
        1,
        0
    )

    return df


# -------------------------------------------------------
# SEASONAL USAGE INDEX
# -------------------------------------------------------

def create_seasonal_usage_index(df):

    if "Month" not in df.columns:
        return df

    monthly_avg = (
        df.groupby("Month")
        ["Usage_kWh"]
        .transform("mean")
    )

    overall_avg = (
        df["Usage_kWh"]
        .mean()
    )

    df["Seasonal_Usage_Index"] = (
        monthly_avg /
        overall_avg
    )

    return df


# -------------------------------------------------------
# LOAD TYPE ENCODING
# -------------------------------------------------------

def create_load_type_encoding(df):

    if "Load_Type" not in df.columns:
        return df

    df["Load_Type_Encoding"] = (
        df["Load_Type"]
        .astype("category")
        .cat.codes
    )

    return df


# -------------------------------------------------------
# POWER FACTOR FEATURES
# -------------------------------------------------------

def create_power_factor_features(df):

    df["Average_Power_Factor"] = (
        df["Lagging_Current_Power_Factor"]
        +
        df["Leading_Current_Power_Factor"]
    ) / 2

    df["Power_Factor_Difference"] = (
        abs(
            df["Lagging_Current_Power_Factor"]
            -
            df["Leading_Current_Power_Factor"]
        )
    )

    return df


# -------------------------------------------------------
# REACTIVE POWER EFFICIENCY
# -------------------------------------------------------

def create_reactive_efficiency(df):

    total_reactive = (
        df["Lagging_Current_Reactive.Power_kVarh"]
        +
        df["Leading_Current_Reactive_Power_kVarh"]
    )

    df["Reactive_Efficiency"] = (
        total_reactive
        /
        (
            df["Usage_kWh"] + 1
        )
    )

    return df


# -------------------------------------------------------
# LOAD CATEGORY
# -------------------------------------------------------

def create_load_category(df):

    q1 = df["Usage_kWh"].quantile(0.33)
    q2 = df["Usage_kWh"].quantile(0.66)

    conditions = [

        df["Usage_kWh"] <= q1,

        (
            (df["Usage_kWh"] > q1)
            &
            (df["Usage_kWh"] <= q2)
        ),

        df["Usage_kWh"] > q2
    ]

    choices = [
        "Low",
        "Medium",
        "High"
    ]

    df["Load_Category"] = np.select(
        conditions,
        choices,
        default="Medium"
    )

    return df


# -------------------------------------------------------
# EMISSION CATEGORY
# -------------------------------------------------------

def create_emission_category(df):

    q1 = df["CO2(tCO2)"].quantile(0.33)
    q2 = df["CO2(tCO2)"].quantile(0.66)

    conditions = [

        df["CO2(tCO2)"] <= q1,

        (
            (df["CO2(tCO2)"] > q1)
            &
            (df["CO2(tCO2)"] <= q2)
        ),

        df["CO2(tCO2)"] > q2
    ]

    choices = [
        "Low",
        "Medium",
        "High"
    ]

    df["Emission_Category"] = np.select(
        conditions,
        choices,
        default="Medium"
    )

    return df


# -------------------------------------------------------
# FEATURE REPORT
# -------------------------------------------------------

def feature_report(df):

    return pd.DataFrame({

        "Feature": df.columns,

        "Data_Type": [
            str(dtype)
            for dtype in df.dtypes
        ],

        "Missing_Values": [
            df[col].isnull().sum()
            for col in df.columns
        ]
    })


# -------------------------------------------------------
# COMPLETE FEATURE PIPELINE
# -------------------------------------------------------

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


# -------------------------------------------------------
# TEST
# -------------------------------------------------------

if __name__ == "__main__":

    print(
        "Steel Industry Feature Engineering Module Loaded"
    )
