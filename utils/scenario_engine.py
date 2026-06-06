
import pandas as pd

class ScenarioEngine:

    def __init__(self, baseline_usage, baseline_emission):
        self.baseline_usage = baseline_usage
        self.baseline_emission = baseline_emission

    def simulate(
        self,
        energy_change=0,
        power_factor_change=0,
        reactive_power_change=0,
        production_growth=0,
        renewable_adoption=0
    ):

        future_usage = self.baseline_usage * (1 + energy_change / 100)
        future_usage *= (1 + production_growth / 100)

        future_emission = (
            self.baseline_emission *
            (future_usage / self.baseline_usage)
        )

        future_emission *= (
            1 - (renewable_adoption / 100) * 0.50
        )

        projected_esg = max(
            0,
            min(100, 100 - future_emission * 100)
        )

        return {
            "future_usage": future_usage,
            "future_emission": future_emission,
            "projected_esg": projected_esg,
            "power_factor_change": power_factor_change,
            "reactive_power_change": reactive_power_change
        }
