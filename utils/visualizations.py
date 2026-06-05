# utils/visualizations.py

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------
# CARBON EMISSION TREND
# -----------------------------------------------------

def carbon_emission_trend(df):

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"]
    )

    daily = (

        temp.groupby("Date")
        ["CO2(tCO2)"]

        .sum()

        .reset_index()

    )

    fig = px.line(
        daily,
        x="Date",
        y="CO2(tCO2)",
        title="Carbon Emission Trend"
    )

    fig.update_layout(
        height=500
    )

    return fig

# -----------------------------------------------------
# MONTHLY EMISSION FORECAST
# -----------------------------------------------------

def monthly_forecast_chart(
    forecast_df
):

    fig = px.line(
        forecast_df,
        x="Day",
        y="Forecast_CO2",
        markers=True,
        title="Monthly Emission Forecast"
    )

    fig.update_layout(
        height=500
    )

    return fig

# -----------------------------------------------------
# ENERGY USAGE TREND
# -----------------------------------------------------

def energy_usage_trend(df):

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"]
    )

    daily = (

        temp.groupby("Date")
        ["Usage_kWh"]

        .sum()

        .reset_index()

    )

    fig = px.line(
        daily,
        x="Date",
        y="Usage_kWh",
        title="Energy Usage Trend"
    )

    return fig

# -----------------------------------------------------
# CO2 DISTRIBUTION
# -----------------------------------------------------

def co2_distribution(df):

    fig = px.histogram(
        df,
        x="CO2(tCO2)",
        nbins=40,
        title="CO₂ Distribution"
    )

    return fig

# -----------------------------------------------------
# CARBON INTENSITY TREND
# -----------------------------------------------------

def carbon_intensity_trend(df):

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"]
    )

    daily = (

        temp.groupby("Date")

        .agg({

            "CO2(tCO2)": "sum",

            "Usage_kWh": "sum"

        })

        .reset_index()

    )

    daily["Carbon_Intensity"] = (

        daily["CO2(tCO2)"]

        /

        daily["Usage_kWh"]

    )

    fig = px.line(
        daily,
        x="Date",
        y="Carbon_Intensity",
        title="Carbon Intensity Trend"
    )

    return fig

# -----------------------------------------------------
# LOAD TYPE COMPARISON
# -----------------------------------------------------

def load_type_comparison(df):

    summary = (

        df.groupby("Load_Type")

        .agg({

            "Usage_kWh": "sum",

            "CO2(tCO2)": "sum"

        })

        .reset_index()

    )

    fig = px.bar(
        summary,
        x="Load_Type",
        y="CO2(tCO2)",
        color="Load_Type",
        title="Load Type Emission Comparison"
    )

    return fig

# -----------------------------------------------------
# ESG SCORE GAUGE
# -----------------------------------------------------

def esg_gauge(score):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score,

            title={
                "text":
                "ESG Score"
            },

            gauge={

                "axis": {
                    "range": [0, 100]
                },

                "steps": [

                    {
                        "range": [0, 50],
                        "color": "red"
                    },

                    {
                        "range": [50, 75],
                        "color": "yellow"
                    },

                    {
                        "range": [75, 100],
                        "color": "green"
                    }
                ]
            }
        )
    )

    fig.update_layout(
        height=400
    )

    return fig

# -----------------------------------------------------
# ANOMALY SCATTER
# -----------------------------------------------------

def anomaly_scatter(df):

    if "Anomaly_Flag" not in df.columns:

        return go.Figure()

    fig = px.scatter(

        df,

        x="Usage_kWh",

        y="CO2(tCO2)",

        color="Anomaly_Flag",

        hover_data=[
            "Alert_Level"
        ],

        title="Anomaly Detection Scatter"
    )

    return fig

# -----------------------------------------------------
# ENERGY HEATMAP
# -----------------------------------------------------

def energy_heatmap(df):

    heatmap = pd.pivot_table(

        df,

        values="Usage_kWh",

        index="Day_of_week",

        columns="Load_Type",

        aggfunc="mean"

    )

    fig = px.imshow(

        heatmap,

        text_auto=True,

        aspect="auto",

        title="Energy Usage Heatmap"

    )

    return fig

# -----------------------------------------------------
# FEATURE IMPORTANCE
# -----------------------------------------------------

def feature_importance_chart(
    feature_df
):

    fig = px.bar(

        feature_df.head(15),

        x="Importance",

        y="Feature",

        orientation="h",

        title="Feature Importance"

    )

    return fig

# -----------------------------------------------------
# WEEKLY EMISSIONS
# -----------------------------------------------------

def weekly_emission_analysis(df):

    temp = df.copy()

    temp["Date"] = pd.to_datetime(
        temp["Date"]
    )

    weekly = (

        temp.groupby(
            pd.Grouper(
                key="Date",
                freq="W"
            )
        )

        ["CO2(tCO2)"]

        .sum()

        .reset_index()

    )

    fig = px.bar(

        weekly,

        x="Date",

        y="CO2(tCO2)",

        title="Weekly Emissions"

    )

    return fig

# -----------------------------------------------------
# SUSTAINABILITY DASHBOARD
# -----------------------------------------------------

def sustainability_progress_chart(
    current,
    target
):

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            name="Current",

            x=["Emissions"],

            y=[current]

        )

    )

    fig.add_trace(

        go.Bar(

            name="Target",

            x=["Emissions"],

            y=[target]

        )

    )

    fig.update_layout(

        title="Sustainability Progress",

        barmode="group",

        height=500

    )

    return fig

# -----------------------------------------------------
# EMISSION CONTRIBUTION PIE
# -----------------------------------------------------

def emission_contribution_pie(df):

    summary = (

        df.groupby("Load_Type")

        ["CO2(tCO2)"]

        .sum()

        .reset_index()

    )

    fig = px.pie(

        summary,

        names="Load_Type",

        values="CO2(tCO2)",

        hole=0.5,

        title="Emission Contribution"

    )

    return fig

# -----------------------------------------------------
# ENERGY VS CO2
# -----------------------------------------------------

def energy_vs_emission(df):

    fig = px.scatter(

        df,

        x="Usage_kWh",

        y="CO2(tCO2)",

        color="Load_Type",

        size="Usage_kWh",

        title="Energy vs CO₂"

    )

    return fig

# -----------------------------------------------------
# POWER FACTOR ANALYSIS
# -----------------------------------------------------

def power_factor_chart(df):

    fig = px.histogram(

        df,

        x="Lagging_Current_Power_Factor",

        nbins=30,

        title="Power Factor Distribution"

    )

    return fig

# -----------------------------------------------------
# LOAD PROFILE
# -----------------------------------------------------

def load_profile_chart(df):

    profile = (

        df.groupby("Load_Type")

        ["Usage_kWh"]

        .mean()

        .reset_index()

    )

    fig = px.bar(

        profile,

        x="Load_Type",

        y="Usage_kWh",

        color="Load_Type",

        title="Average Load Profile"

    )

    return fig

# -----------------------------------------------------
# MONTHLY CARBON ANALYSIS
# -----------------------------------------------------

def monthly_carbon_analysis(df):

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

        ["CO2(tCO2)"]

        .sum()

        .reset_index()

    )

    fig = px.area(

        monthly,

        x="Date",

        y="CO2(tCO2)",

        title="Monthly Carbon Analysis"

    )

    return fig

# -----------------------------------------------------
# ESG TREND
# -----------------------------------------------------

def esg_trend_chart(df):

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

        .agg({

            "CO2(tCO2)": "sum",

            "Usage_kWh": "sum"

        })

        .reset_index()

    )

    monthly["ESG_Index"] = (

        100

        -

        (
            monthly["CO2(tCO2)"]

            /

            monthly["Usage_kWh"]

            * 1000
        )
    )

    fig = px.line(

        monthly,

        x="Date",

        y="ESG_Index",

        markers=True,

        title="ESG Trend"

    )

    return fig

# -----------------------------------------------------
# DASHBOARD KPI CARD DATA
# -----------------------------------------------------

def dashboard_kpis(df):

    return {

        "Total Energy":
            round(
                df["Usage_kWh"].sum(),
                2
            ),

        "Total Emissions":
            round(
                df["CO2(tCO2)"].sum(),
                2
            ),

        "Average Emissions":
            round(
                df["CO2(tCO2)"].mean(),
                4
            ),

        "Carbon Intensity":
            round(
                (
                    df["CO2(tCO2)"].sum()
                    /
                    df["Usage_kWh"].sum()
                ),
                6
            )
    }
