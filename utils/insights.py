# utils/insights.py

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
# EMISSION INSIGHTS
# ----------------------------------------------------

def generate_emission_insights(df):

    insights = []

    if "CO2(tCO2)" not in df.columns:
        return insights

    total_emissions = df["CO2(tCO2)"].sum()

    avg_emissions = df["CO2(tCO2)"].mean()

    insights.append(
        f"Total carbon emissions reached {total_emissions:,.2f} tCO₂."
    )

    insights.append(
        f"Average emission per observation was {avg_emissions:.4f} tCO₂."
    )

    if "Date" in df.columns:

        temp = df.copy()

        temp["Date"] = pd.to_datetime(
            temp["Date"],
            errors="coerce"
        )

        temp = temp.dropna(
            subset=["Date"]
        )

        if len(temp) > 0:

            monthly = (
                temp
                .set_index("Date")
                .resample("ME")
                ["CO2(tCO2)"]
                .sum()
                .to_frame()
            )

            if len(monthly) > 1:

                growth = (
                    monthly["CO2(tCO2)"]
                    .pct_change()
                    .mean()
                    * 100
                )

                insights.append(
                    f"Average monthly emission change was {growth:.2f}%."
                )

    return insights


# ----------------------------------------------------
# LOAD TYPE INSIGHTS
# ----------------------------------------------------

def generate_load_type_insights(df):

    insights = []

    if "Load_Type" not in df.columns:
        return insights

    load_summary = (
        df.groupby("Load_Type")["CO2(tCO2)"]
        .sum()
    )

    if len(load_summary) == 0:
        return insights

    top_load = load_summary.idxmax()

    contribution = (
        load_summary.max()
        / load_summary.sum()
        * 100
    )

    insights.append(
        f"{top_load} contributed {contribution:.1f}% of total emissions."
    )

    return insights


# ----------------------------------------------------
# ENERGY INSIGHTS
# ----------------------------------------------------

def generate_energy_insights(df):

    insights = []

    if "Usage_kWh" not in df.columns:
        return insights

    total_energy = df["Usage_kWh"].sum()

    avg_energy = df["Usage_kWh"].mean()

    peak_energy = df["Usage_kWh"].max()

    insights.append(
        f"Total energy consumption reached {total_energy:,.0f} kWh."
    )

    insights.append(
        f"Average energy usage was {avg_energy:.2f} kWh."
    )

    insights.append(
        f"Peak energy demand reached {peak_energy:.2f} kWh."
    )

    return insights


# ----------------------------------------------------
# CARBON INTENSITY INSIGHTS
# ----------------------------------------------------

def generate_carbon_intensity_insights(df):

    insights = []

    if (
        "Usage_kWh" not in df.columns
        or "CO2(tCO2)" not in df.columns
    ):
        return insights

    total_energy = df["Usage_kWh"].sum()

    total_co2 = df["CO2(tCO2)"].sum()

    if total_energy == 0:
        return insights

    intensity = total_co2 / total_energy

    insights.append(
        f"Carbon intensity was {intensity:.6f} tCO₂ per kWh."
    )

    if intensity > 0.0006:

        insights.append(
            "Carbon intensity exceeds the preferred efficiency threshold."
        )

    else:

        insights.append(
            "Carbon intensity remains within efficient operating levels."
        )

    return insights


# ----------------------------------------------------
# WEEKDAY INSIGHTS
# ----------------------------------------------------

def generate_weekday_insights(df):

    insights = []

    if "Day_of_week" not in df.columns:
        return insights

    weekday_usage = (
        df.groupby("Day_of_week")["Usage_kWh"]
        .sum()
    )

    if len(weekday_usage) == 0:
        return insights

    peak_day = weekday_usage.idxmax()

    insights.append(
        f"Peak energy consumption occurred on {peak_day}."
    )

    return insights


# ----------------------------------------------------
# POWER FACTOR INSIGHTS
# ----------------------------------------------------

def generate_power_factor_insights(df):

    insights = []

    if "Lagging_Current_Power_Factor" not in df.columns:
        return insights

    avg_pf = (
        df["Lagging_Current_Power_Factor"]
        .mean()
    )

    insights.append(
        f"Average power factor was {avg_pf:.2f}%."
    )

    if avg_pf < 90:

        insights.append(
            "Reactive power inefficiency may be increasing emissions."
        )

    else:

        insights.append(
            "Power factor performance is healthy."
        )

    return insights


# ----------------------------------------------------
# ESG INSIGHTS
# ----------------------------------------------------

def generate_esg_insights(df):

    insights = []

    if (
        "Usage_kWh" not in df.columns
        or "CO2(tCO2)" not in df.columns
    ):
        return insights

    total_energy = df["Usage_kWh"].sum()

    total_co2 = df["CO2(tCO2)"].sum()

    if total_energy == 0:
        return insights

    intensity = total_co2 / total_energy

    esg_score = max(
        0,
        min(
            100,
            100 - (intensity * 1000)
        )
    )

    insights.append(
        f"Current ESG score is estimated at {esg_score:.0f}/100."
    )

    if esg_score >= 80:

        insights.append(
            "ESG performance is strong."
        )

    elif esg_score >= 60:

        insights.append(
            "ESG performance is acceptable but can improve."
        )

    else:

        insights.append(
            "ESG performance requires immediate improvement."
        )

    return insights


# ----------------------------------------------------
# ANOMALY INSIGHTS
# ----------------------------------------------------

def generate_anomaly_insights(df):

    insights = []

    if "Alert_Level" not in df.columns:
        return insights

    critical = (
        df["Alert_Level"]
        .eq("Critical")
        .sum()
    )

    high = (
        df["Alert_Level"]
        .eq("High")
        .sum()
    )

    insights.append(
        f"{critical} critical alerts were detected."
    )

    insights.append(
        f"{high} high-priority alerts were detected."
    )

    if critical > 0:

        insights.append(
            "Immediate investigation of critical anomalies is recommended."
        )

    return insights


# ----------------------------------------------------
# RECOMMENDATIONS
# ----------------------------------------------------

def generate_recommendations(df):

    recommendations = []

    if (
        "Usage_kWh" not in df.columns
        or "CO2(tCO2)" not in df.columns
    ):
        return recommendations

    intensity = (
        df["CO2(tCO2)"].sum()
        /
        max(df["Usage_kWh"].sum(), 1)
    )

    if intensity > 0.0006:

        recommendations.append(
            "Reduce carbon intensity through process optimization."
        )

    if "Lagging_Current_Power_Factor" in df.columns:

        avg_pf = (
            df["Lagging_Current_Power_Factor"]
            .mean()
        )

        if avg_pf < 90:

            recommendations.append(
                "Install power factor correction systems."
            )

    recommendations.append(
        "Monitor peak load periods and reduce demand spikes."
    )

    recommendations.append(
        "Implement predictive maintenance programs."
    )

    recommendations.append(
        "Increase renewable energy integration."
    )

    recommendations.append(
        "Track ESG performance monthly."
    )

    return recommendations


# ----------------------------------------------------
# COMPLETE INSIGHTS ENGINE
# ----------------------------------------------------

def generate_all_insights(df):

    insights = []

    insights.extend(generate_emission_insights(df))
    insights.extend(generate_load_type_insights(df))
    insights.extend(generate_energy_insights(df))
    insights.extend(generate_carbon_intensity_insights(df))
    insights.extend(generate_weekday_insights(df))
    insights.extend(generate_power_factor_insights(df))
    insights.extend(generate_esg_insights(df))
    insights.extend(generate_anomaly_insights(df))

    return insights


# ----------------------------------------------------
# STREAMLIT WRAPPER
# ----------------------------------------------------

def generate_insights(df):
    return generate_all_insights(df)


# ----------------------------------------------------
# REPORT
# ----------------------------------------------------

def insights_report(df):

    return pd.DataFrame(
        {
            "Insight": generate_all_insights(df)
        }
    )


# ----------------------------------------------------
# TEST
# ----------------------------------------------------

if __name__ == "__main__":

    print(
        "Steel Industry AI Insights Engine Loaded"
    )
