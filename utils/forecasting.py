
import pandas as pd
import numpy as np

class CarbonForecaster:

    def __init__(self):
        self.forecast_horizons = [30, 90, 180, 365]

    def moving_average_forecast(
        self,
        series,
        periods=30
    ):

        avg = series.tail(30).mean()

        return pd.DataFrame({
            "Forecast": [avg] * periods
        })

    def generate_forecasts(
        self,
        df,
        target="CO2(tCO2)"
    ):

        forecasts = {}

        for horizon in self.forecast_horizons:

            forecasts[horizon] = (
                self.moving_average_forecast(
                    df[target],
                    horizon
                )
            )

        return forecasts

    def confidence_interval(
        self,
        series,
        confidence=0.95
    ):

        mean = series.mean()
        std = series.std()

        return {
            "lower": mean - (1.96 * std),
            "upper": mean + (1.96 * std)
        }
