
import pandas as pd
import numpy as np

def load_dataset(path):
    df = pd.read_csv(path)
    return df

def clean_dataset(df):
    df = df.drop_duplicates()

    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    return df

def validate_dataset(df):
    required = [
        "Usage_kWh",
        "CO2(tCO2)",
        "Load_Type"
    ]

    missing = [
        col for col in required
        if col not in df.columns
    ]

    return missing
