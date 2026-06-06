
import numpy as np

def create_features(df):

    df["Total_Power_Consumption"] = (
        df["Usage_kWh"]
    )

    df["Reactive_Power_Ratio"] = (
        df["Lagging_Current_Reactive.Power_kVarh"]
        /
        (
            df["Leading_Current_Reactive_Power_kVarh"]
            + 1
        )
    )

    df["Carbon_Intensity"] = (
        df["CO2(tCO2)"]
        /
        (df["Usage_kWh"] + 1)
    )

    df["Energy_Efficiency_Index"] = (
        df["Usage_kWh"]
        /
        (df["CO2(tCO2)"] + 1)
    )

    df["Peak_Load_Flag"] = np.where(
        df["Usage_kWh"] >
        df["Usage_kWh"].quantile(0.95),
        1,
        0
    )

    return df
