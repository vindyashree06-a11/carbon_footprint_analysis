# utils/esg.py

import pandas as pd
import numpy as np
import logging

# ----------------------------------------------------
# LOGGER
# ----------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ----------------------------------------------------
# TOTAL EMISSIONS
# ----------------------------------------------------

def total_emissions(df):

    return float(
        df["CO2(tCO2)"].sum()
    )

# ----------------------------------------------------
# CARBON INTENSITY
# ----------------------------------------------------

def carbon_intensity(df):

    total_energy = (
        df["Usage_kWh"]
        .sum()
    )

    if total_energy == 0:
        return 0

    return (
        df["CO2(tCO2)"].sum()
        /
        total_energy
    )

# ----------------------------------------------------
# TARGET EMISSIONS
# ----------------------------------------------------

def target_emissions(
    current_emissions,
    reduction_target=15
):

    return (
        current_emissions
        *
        (1 - reduction_target / 100)
    )

# ----------------------------------------------------
# REDUCTION %
# ----------------------------------------------------

def reduction_percentage(
    current,
    target
):

    if current == 0:
        return 0

    return (
        (
            current - target
        )
        /
        current
        * 100
    )

# ----------------------------------------------------
# SUSTAINABILITY PROGRESS
# ----------------------------------------------------

def sustainability_progress(
    current,
    target
):

    if current == 0:
        return 100

    progress = (
        target
        /
        current
    ) * 100

    return round(
        progress,
        2
    )

# ----------------------------------------------------
# ESG STATUS
# ----------------------------------------------------

def traffic_light_status(
    current,
    target
):

    ratio = current / target

    if ratio <= 1.00:
        return "Green"

    elif ratio <= 1.15:
        return "Yellow"

    return "Red"

# ----------------------------------------------------
# ESG SCORE
# ----------------------------------------------------

def calculate_esg_score(
    df,
    target_reduction=15
):

    current = total_emissions(df)

    target = target_emissions(
        current,
        target_reduction
    )

    intensity = carbon_intensity(df)

    score = 100

    # Carbon Intensity Penalty

    score -= min(
        intensity * 1000,
        30
    )

    # Emission Penalty

    if current > target:
        excess = (
            (current - target)
            / current
        ) * 100

        score -= excess

    score = max(
        0,
        min(score, 100)
    )

    return round(score, 2)

# ----------------------------------------------------
# ESG RATING
# ----------------------------------------------------

def sustainability_rating(
    score
):

    if score >= 90:
        return "AAA"

    elif score >= 80:
        return "AA"

    elif score >= 70:
        return "A"

    elif score >= 60:
        return "BBB"

    elif score >= 50:
        return "BB"

    elif score >= 40:
        return "B"

    return "CCC"

# ----------------------------------------------------
# ESG KPI SUMMARY
# ----------------------------------------------------

def esg_summary(
    df,
    target_reduction=15
):

    current = total_emissions(df)

    target = target_emissions(
        current,
        target_reduction
    )

    score = calculate_esg_score(
        df,
        target_reduction
    )

    rating = sustainability_rating(
        score
    )

    status = traffic_light_status(
        current,
        target
    )

    progress = sustainability_progress(
        current,
        target
    )

    return {

        "Current_Emissions":
            round(current, 2),

        "Target_Emissions":
            round(target, 2),

        "Reduction_Percentage":
            round(
                reduction_percentage(
                    current,
                    target
                ),
                2
            ),

        "Carbon_Intensity":
            round(
                carbon_intensity(df),
                6
            ),

        "ESG_Score":
            score,

        "ESG_Rating":
            rating,

        "Status":
            status,

        "Progress":
            progress
    }

# ----------------------------------------------------
# LOAD TYPE ESG ANALYSIS
# ----------------------------------------------------

def load_type_esg(df):

    result = (

        df.groupby("Load_Type")

        .agg(

            Energy=(
                "Usage_kWh",
                "sum"
            ),

            Emissions=(
                "CO2(tCO2)",
                "sum"
            )

        )

        .reset_index()

    )

    result["Carbon_Intensity"] = (

        result["Emissions"]

        /

        result["Energy"]

    )

    return result

# ----------------------------------------------------
# MONTHLY ESG TREND
# ----------------------------------------------------

def monthly_esg_trend(df):

    if "Date" not in df.columns:
        return pd.DataFrame()

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"]
    )

    monthly = (

        temp.groupby(
            pd.Grouper(
                key="Date",
                freq="M"
            )
        )

        .agg(

            Energy=(
                "Usage_kWh",
                "sum"
            ),

            Emissions=(
                "CO2(tCO2)",
                "sum"
            )

        )

        .reset_index()

    )

    monthly["Carbon_Intensity"] = (

        monthly["Emissions"]

        /

        monthly["Energy"]

    )

    return monthly

# ----------------------------------------------------
# ESG RECOMMENDATIONS
# ----------------------------------------------------

def generate_recommendations(
    df,
    score
):

    recommendations = []

    intensity = carbon_intensity(df)

    if intensity > 0.0006:

        recommendations.append(
            "Reduce carbon intensity through energy optimization."
        )

    if score < 80:

        recommendations.append(
            "Implement aggressive carbon reduction initiatives."
        )

    if df["Usage_kWh"].mean() > (
        df["Usage_kWh"].quantile(0.75)
    ):

        recommendations.append(
            "Investigate excessive energy consumption patterns."
        )

    if (
        "Lagging_Current_Power_Factor"
        in df.columns
    ):

        avg_pf = (
            df[
                "Lagging_Current_Power_Factor"
            ]
            .mean()
        )

        if avg_pf < 90:

            recommendations.append(
                "Improve power factor correction systems."
            )

    if len(recommendations) == 0:

        recommendations.append(
            "Current ESG performance is on track."
        )

    return recommendations

# ----------------------------------------------------
# ESG REPORT
# ----------------------------------------------------

def generate_esg_report(
    df,
    target_reduction=15
):

    summary = esg_summary(
        df,
        target_reduction
    )

    report = pd.DataFrame({

        "Metric": list(
            summary.keys()
        ),

        "Value": list(
            summary.values()
        )

    })

    return report

# ----------------------------------------------------
# ESG BENCHMARKING
# ----------------------------------------------------

def benchmark_esg_score(score):

    if score >= 90:

        return (
            "Industry Leader"
        )

    elif score >= 75:

        return (
            "Above Average"
        )

    elif score >= 60:

        return (
            "Average"
        )

    elif score >= 40:

        return (
            "Below Average"
        )

    return (
        "High Risk"
    )

# ----------------------------------------------------
# NET ZERO ESTIMATION
# ----------------------------------------------------

def estimate_net_zero_years(
    current_emissions,
    annual_reduction_percent
):

    years = 0

    emissions = current_emissions

    while emissions > 1:

        emissions = emissions * (
            1 -
            annual_reduction_percent
            / 100
        )

        years += 1

        if years > 100:
            break

    return years

# ----------------------------------------------------
# ESG DASHBOARD DATA
# ----------------------------------------------------

def dashboard_metrics(
    df,
    target_reduction=15
):

    summary = esg_summary(
        df,
        target_reduction
    )

    return {

        "ESG Score":
            summary["ESG_Score"],

        "Rating":
            summary["ESG_Rating"],

        "Status":
            summary["Status"],

        "Carbon Intensity":
            summary["Carbon_Intensity"],

        "Progress":
            summary["Progress"]
    }

# ----------------------------------------------------
# COMPLETE ESG ENGINE
# ----------------------------------------------------

def run_esg_engine(
    df,
    target_reduction=15
):

    logger.info(
        "Running ESG Engine..."
    )

    summary = esg_summary(
        df,
        target_reduction
    )

    recommendations = (
        generate_recommendations(
            df,
            summary["ESG_Score"]
        )
    )

    report = (
        generate_esg_report(
            df,
            target_reduction
        )
    )

    return {

        "summary":
            summary,

        "recommendations":
            recommendations,

        "report":
            report
    }
# ----------------------------------------------------
# STREAMLIT COMPATIBILITY WRAPPER
# ----------------------------------------------------

def calculate_esg(df, target_reduction=15):
    """
    Compatibility function used by dashboard pages.

    Returns:
    {
        "score": float,
        "rating": str,
        "status": str,
        "progress": float,
        "summary": dict
    }
    """

    summary = esg_summary(
        df,
        target_reduction
    )

    return {

        "score":
            summary["ESG_Score"],

        "rating":
            summary["ESG_Rating"],

        "status":
            summary["Status"],

        "progress":
            summary["Progress"],

        "summary":
            summary
    }
# ----------------------------------------------------
# TEST
# ----------------------------------------------------

if __name__ == "__main__":

    print(
        "Steel Industry ESG Module Loaded"
    )
