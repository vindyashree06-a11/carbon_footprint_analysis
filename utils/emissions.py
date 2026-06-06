
import pandas as pd

def total_emissions(df):
    return df["CO2(tCO2)"].sum()

def average_emissions(df):
    return df["CO2(tCO2)"].mean()

def daily_emissions(df):

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"]
    )

    return (
        temp.groupby(
            temp["Date"].dt.date
        )["CO2(tCO2)"]
        .sum()
        .reset_index()
    )

def monthly_emissions(df):

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"]
    )

    return (
        temp.groupby(
            temp["Date"].dt.to_period("M")
        )["CO2(tCO2)"]
        .sum()
        .reset_index()
    )
