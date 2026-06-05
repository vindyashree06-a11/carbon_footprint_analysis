# utils/preprocessing.py

import pandas as pd
import numpy as np
import logging

# ---------------------------------------------------
# LOGGER
# ---------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------
# REQUIRED COLUMNS
# ---------------------------------------------------

REQUIRED_COLUMNS = [
    "Usage_kWh",
    "Lagging_Current_Reactive.Power_kVarh",
    "Leading_Current_Reactive_Power_kVarh",
    "CO2(tCO2)",
    "Lagging_Current_Power_Factor",
    "Leading_Current_Power_Factor",
    "NSM",
    "WeekStatus",
    "Day_of_week",
    "Load_Type",
    "Date"
]

# ---------------------------------------------------
# VALIDATE DATASET
# ---------------------------------------------------

def validate_dataset(df):

    missing_cols = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    return {
        "valid": len(missing_cols) == 0,
        "missing_columns": missing_cols
    }

# ---------------------------------------------------
# PARSE DATE
# ---------------------------------------------------

def parse_dates(df):

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    return df

# ---------------------------------------------------
# DATA TYPES
# ---------------------------------------------------

def convert_data_types(df):

    numeric_cols = [
        "Usage_kWh",
        "Lagging_Current_Reactive.Power_kVarh",
        "Leading_Current_Reactive_Power_kVarh",
        "CO2(tCO2)",
        "Lagging_Current_Power_Factor",
        "Leading_Current_Power_Factor",
        "NSM"
    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df

# ---------------------------------------------------
# MISSING VALUES
# ---------------------------------------------------

def handle_missing_values(df):

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns

    categorical_cols = df.select_dtypes(
        exclude=np.number
    ).columns

    for col in numeric_cols:

        df[col] = df[col].fillna(
            df[col].median()
        )

    for col in categorical_cols:

        if not df[col].mode().empty:

            df[col] = df[col].fillna(
                df[col].mode()[0]
            )

    return df

# ---------------------------------------------------
# DUPLICATES
# ---------------------------------------------------

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    logger.info(
        f"Removed {removed} duplicate rows."
    )

    return df, removed

# ---------------------------------------------------
# OUTLIERS
# ---------------------------------------------------

def detect_outliers_iqr(df):

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns

    report = {}

    for col in numeric_cols:

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        count = len(
            df[
                (df[col] < lower)
                |
                (df[col] > upper)
            ]
        )

        report[col] = count

    return report

# ---------------------------------------------------
# QUALITY REPORT
# ---------------------------------------------------

def generate_quality_report(df):

    return {

        "rows":
            len(df),

        "columns":
            len(df.columns),

        "missing_values":
            int(
                df.isnull()
                .sum()
                .sum()
            ),

        "duplicate_rows":
            int(
                df.duplicated()
                .sum()
            ),

        "memory_mb":
            round(
                df.memory_usage(
                    deep=True
                ).sum()
                / 1024**2,
                2
            )
    }

# ---------------------------------------------------
# WEEKLY SUMMARY
# ---------------------------------------------------

def weekly_usage_summary(df):

    if "Date" not in df.columns:

        return pd.DataFrame()

    return (

        df.groupby(
            pd.Grouper(
                key="Date",
                freq="W"
            )
        )

        ["Usage_kWh"]

        .sum()

        .reset_index()

    )

# ---------------------------------------------------
# LOAD TYPE SUMMARY
# ---------------------------------------------------

def load_type_summary(df):

    return (

        df.groupby("Load_Type")

        .agg(

            Total_Usage=(
                "Usage_kWh",
                "sum"
            ),

            Avg_Usage=(
                "Usage_kWh",
                "mean"
            ),

            Total_CO2=(
                "CO2(tCO2)",
                "sum"
            )

        )

        .reset_index()

    )

# ---------------------------------------------------
# CARBON SUMMARY
# ---------------------------------------------------

def carbon_summary(df):

    return {

        "total_emission":
            round(
                df["CO2(tCO2)"].sum(),
                4
            ),

        "average_emission":
            round(
                df["CO2(tCO2)"].mean(),
                4
            ),

        "max_emission":
            round(
                df["CO2(tCO2)"].max(),
                4
            ),

        "min_emission":
            round(
                df["CO2(tCO2)"].min(),
                4
            )
    }

# ---------------------------------------------------
# MAIN PREPROCESSING FUNCTION
# ---------------------------------------------------

def preprocess_data(df):

    """
    Main preprocessing pipeline.
    Returns cleaned dataframe.
    """

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    validation = validate_dataset(df)

    if not validation["valid"]:

        raise ValueError(
            f"Missing Columns: "
            f"{validation['missing_columns']}"
        )

    df = parse_dates(df)

    df = convert_data_types(df)

    df = handle_missing_values(df)

    df, duplicates_removed = (
        remove_duplicates(df)
    )

    quality_report = (
        generate_quality_report(df)
    )

    logger.info(
        f"Duplicates Removed: "
        f"{duplicates_removed}"
    )

    logger.info(
        f"Quality Report: "
        f"{quality_report}"
    )

    logger.info(
        "Preprocessing Completed Successfully"
    )

    return df

# ---------------------------------------------------
# TEST
# ---------------------------------------------------

if __name__ == "__main__":

    print(
        "Steel Industry Preprocessing Module Loaded"
    )
