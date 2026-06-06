
import pandas as pd

class InsightEngine:

    def generate(
        self,
        df
    ):

        insights = []

        total_emission = (
            df["CO2(tCO2)"].sum()
        )

        avg_usage = (
            df["Usage_kWh"].mean()
        )

        load_summary = (
            df.groupby("Load_Type")
            ["CO2(tCO2)"]
            .sum()
        )

        highest_load = (
            load_summary.idxmax()
        )

        insights.append(
            f"{highest_load} contributes the highest emissions."
        )

        insights.append(
            f"Total emissions: {total_emission:.2f} tCO₂."
        )

        insights.append(
            f"Average energy usage: {avg_usage:.2f} kWh."
        )

        insights.append(
            "Improving power factor can reduce carbon intensity."
        )

        return insights
