# utils/emissions.py

import pandas as pd
import logging

# -----------------------------------------------------
# LOGGER
# -----------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# -----------------------------------------------------
# TOTAL EMISSIONS
# -----------------------------------------------------

def total_emissions(df):
    return float(df["CO2(tCO2)"].sum())


# -----------------------------------------------------
# AVERAGE EMISSIONS
# -----------------------------------------------------

def average_emissions(df):
    return float(df["CO2(tCO2)"].mean())


# -----------------------------------------------------
# DAILY EMISSIONS
# -----------------------------------------------------

def daily_emissions(df):

    if "Date" not in df.columns:
        return pd.DataFrame()

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"],
        errors="coerce"
    )

    temp = temp.dropna(subset=["Date"])

    daily = (
        temp.groupby(
            temp["Date"].dt.date
        )["CO2(tCO2)"]
        .sum()
        .reset_index()
    )

    daily.columns = [
        "Date",
        "Daily_Emissions"
    ]

    return daily


# -----------------------------------------------------
# WEEKLY EMISSIONS
# -----------------------------------------------------

def weekly_emissions(df):

    if "Date" not in df.columns:
        return pd.DataFrame()

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"],
        errors="coerce"
    )

    temp = temp.dropna(subset=["Date"])

    weekly = (
        temp
        .set_index("Date")
        .resample("W")
        ["CO2(tCO2)"]
        .sum()
        .reset_index()
    )

    weekly.columns = [
        "Date",
        "Weekly_Emissions"
    ]

    return weekly


# -----------------------------------------------------
# MONTHLY EMISSIONS
# -----------------------------------------------------

def monthly_emissions(df):

    if "Date" not in df.columns:
        return pd.DataFrame()

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"],
        errors="coerce"
    )

    temp = temp.dropna(subset=["Date"])

    monthly = (
        temp
        .set_index("Date")
        .resample("ME")
        ["CO2(tCO2)"]
        .sum()
        .reset_index()
    )

    monthly.columns = [
        "Date",
        "Monthly_Emissions"
    ]

    return monthly


# -----------------------------------------------------
# YEARLY EMISSIONS
# -----------------------------------------------------

def yearly_emissions(df):

    if "Date" not in df.columns:
        return pd.DataFrame()

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"],
        errors="coerce"
    )

    temp = temp.dropna(subset=["Date"])

    yearly = (
        temp
        .set_index("Date")
        .resample("YE")
        ["CO2(tCO2)"]
        .sum()
        .reset_index()
    )

    yearly.columns = [
        "Date",
        "Annual_Emissions"
    ]

    return yearly


# -----------------------------------------------------
# ANNUALIZED EMISSIONS
# -----------------------------------------------------

def annualized_emissions(df):

    if "Date" not in df.columns:
        return total_emissions(df)

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"],
        errors="coerce"
    )

    temp = temp.dropna(subset=["Date"])

    if temp.empty:
        return 0

    days = max(
        1,
        (
            temp["Date"].max()
            -
            temp["Date"].min()
        ).days
    )

    annualized = (
        total_emissions(temp)
        * 365
        / days
    )

    return round(
        annualized,
        2
    )


# -----------------------------------------------------
# LOAD TYPE CONTRIBUTION
# -----------------------------------------------------

def load_type_emissions(df):

    if "Load_Type" not in df.columns:
        return pd.DataFrame()

    result = (
        df.groupby("Load_Type")
        ["CO2(tCO2)"]
        .sum()
        .reset_index()
        .sort_values(
            "CO2(tCO2)",
            ascending=False
        )
    )

    total = result["CO2(tCO2)"].sum()

    if total > 0:

        result["Contribution_%"] = (
            result["CO2(tCO2)"]
            / total
            * 100
        )

    else:

        result["Contribution_%"] = 0

    return result


# -----------------------------------------------------
# CARBON INTENSITY
# -----------------------------------------------------

def carbon_intensity(df):

    total_energy = (
        df["Usage_kWh"]
        .sum()
    )

    if total_energy <= 0:
        return 0

    return (
        df["CO2(tCO2)"].sum()
        / total_energy
    )


# -----------------------------------------------------
# EMISSION DISTRIBUTION
# -----------------------------------------------------

def emission_distribution(df):

    return {
        "min": float(df["CO2(tCO2)"].min()),
        "max": float(df["CO2(tCO2)"].max()),
        "mean": float(df["CO2(tCO2)"].mean()),
        "median": float(df["CO2(tCO2)"].median()),
        "std": float(df["CO2(tCO2)"].std()),
        "variance": float(df["CO2(tCO2)"].var())
    }


# -----------------------------------------------------
# EMISSION TREND
# -----------------------------------------------------

def emission_growth_rate(df):

    monthly = monthly_emissions(df)

    if len(monthly) < 2:
        return 0

    growth = (
        monthly["Monthly_Emissions"]
        .pct_change()
        .mean()
        * 100
    )

    return round(
        float(growth),
        2
    )


# -----------------------------------------------------
# TOP EMISSION RECORDS
# -----------------------------------------------------

def top_emitters(df, top_n=20):

    return (
        df.sort_values(
            "CO2(tCO2)",
            ascending=False
        )
        .head(top_n)
    )


# -----------------------------------------------------
# EMISSION SUMMARY
# -----------------------------------------------------

def emission_summary(df):

    return {
        "total_emission":
            round(total_emissions(df), 2),

        "average_emission":
            round(average_emissions(df), 4),

        "annualized_emission":
            annualized_emissions(df),

        "carbon_intensity":
            round(
                carbon_intensity(df),
                6
            ),

        "growth_rate":
            emission_growth_rate(df)
    }


# -----------------------------------------------------
# ESG TARGETS
# -----------------------------------------------------

def esg_targets(
    df,
    reduction_target=10
):

    current = total_emissions(df)

    target = (
        current *
        (1 - reduction_target / 100)
    )

    reduction_needed = (
        current - target
    )

    return {
        "current_emissions":
            round(current, 2),

        "target_emissions":
            round(target, 2),

        "reduction_needed":
            round(reduction_needed, 2),

        "target_percent":
            reduction_target
    }


# -----------------------------------------------------
# CARBON SAVINGS
# -----------------------------------------------------

def estimate_carbon_savings(
    current_emissions,
    reduction_percent
):

    savings = (
        current_emissions
        * reduction_percent
        / 100
    )

    future_emissions = (
        current_emissions
        - savings
    )

    return {
        "carbon_saved":
            round(savings, 2),

        "future_emissions":
            round(
                future_emissions,
                2
            )
    }


# -----------------------------------------------------
# EMISSION REPORT
# -----------------------------------------------------

def generate_emission_report(df):

    report = {
        "Total Emissions":
            round(total_emissions(df), 2),

        "Average Emissions":
            round(average_emissions(df), 4),

        "Annualized Emissions":
            annualized_emissions(df),

        "Carbon Intensity":
            round(
                carbon_intensity(df),
                6
            ),

        "Emission Growth Rate":
            emission_growth_rate(df)
    }

    return pd.DataFrame(
        report.items(),
        columns=[
            "Metric",
            "Value"
        ]
    )


# -----------------------------------------------------
# TEST
# -----------------------------------------------------

if __name__ == "__main__":

    print(
        "Steel Industry Emissions Module Loaded"
    )
