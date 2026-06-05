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

    """
    Validate required columns.
    """

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
# PARSE DATE COLUMN
# ---------------------------------------------------

def parse_dates(df):

    """
    Convert Date column to datetime.
    """

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    return df

# ---------------------------------------------------
# REMOVE DUPLICATES
# ---------------------------------------------------

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    removed = before - after

    logger.info(
        f"Removed {removed} duplicate rows."
    )

    return df, removed

# ---------------------------------------------------
# HANDLE MISSING VALUES
# ---------------------------------------------------

def handle_missing_values(df):

    """
    Numerical -> Median
    Categorical -> Mode
    """

    missing_before = (
        df.isnull()
        .sum()
        .sum()
    )

    num_cols = df.select_dtypes(
        include=np.number
    ).columns

    cat_cols = df.select_dtypes(
        exclude=np.number
    ).columns

    for col in num_cols:

        df[col] = df[col].fillna(
            df[col].median()
        )

    for col in cat_cols:

        if not df[col].mode().empty:

            df[col] = df[col].fillna(
                df[col].mode()[0]
            )

    missing_after = (
        df.isnull()
        .sum()
        .sum()
    )

    logger.info(
        f"Missing values fixed: "
        f"{missing_before - missing_after}"
    )

    return df

# ---------------------------------------------------
# CONVERT DATA TYPES
# ---------------------------------------------------

def convert_data_types(df):

    """
    Ensure correct dtypes.
    """

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
# OUTLIER DETECTION
# ---------------------------------------------------

def detect_outliers_iqr(df):

    """
    Detect outliers using IQR.
    """

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns

    outlier_report = {}

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

        outlier_report[col] = count

    return outlier_report

# ---------------------------------------------------
# REMOVE OUTLIERS
# ---------------------------------------------------

def remove_outliers_iqr(df):

    """
    Remove IQR outliers.
    """

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns

    cleaned = df.copy()

    for col in numeric_cols:

        q1 = cleaned[col].quantile(0.25)
        q3 = cleaned[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        cleaned = cleaned[
            (cleaned[col] >= lower)
            &
            (cleaned[col] <= upper)
        ]

    logger.info(
        f"Rows after outlier removal: {len(cleaned)}"
    )

    return cleaned

# ---------------------------------------------------
# DATA QUALITY REPORT
# ---------------------------------------------------

def generate_quality_report(df):

    """
    Generate dataset quality metrics.
    """

    report = {

        "rows": len(df),

        "columns": len(df.columns),

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

    return report

# ---------------------------------------------------
# WEEKLY SUMMARY
# ---------------------------------------------------

def weekly_usage_summary(df):

    if "Date" not in df.columns:

        return pd.DataFrame()

    weekly = (

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

    return weekly

# ---------------------------------------------------
# LOAD TYPE SUMMARY
# ---------------------------------------------------

def load_type_summary(df):

    summary = (

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

    return summary

# ---------------------------------------------------
# EMISSION SUMMARY
# ---------------------------------------------------

def carbon_summary(df):

    total_emission = (
        df["CO2(tCO2)"]
        .sum()
    )

    avg_emission = (
        df["CO2(tCO2)"]
        .mean()
    )

    max_emission = (
        df["CO2(tCO2)"]
        .max()
    )

    min_emission = (
        df["CO2(tCO2)"]
        .min()
    )

    return {

        "total_emission":
            round(total_emission, 4),

        "average_emission":
            round(avg_emission, 4),

        "max_emission":
            round(max_emission, 4),

        "min_emission":
            round(min_emission, 4)
    }

# ---------------------------------------------------
# COMPLETE PIPELINE
# ---------------------------------------------------

def preprocess_data(df):

    """
    Complete preprocessing pipeline.
    """

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

    outlier_report = (
        detect_outliers_iqr(df)
    )

    quality_report = (
        generate_quality_report(df)
    )

    return {

        "data": df,

        "duplicates_removed":
            duplicates_removed,

        "outlier_report":
            outlier_report,

        "quality_report":
            quality_report
    }

# ---------------------------------------------------
# MAIN TEST
# ---------------------------------------------------

if __name__ == "__main__":

    print(
        "Steel Industry Preprocessing Module Loaded"
    )
