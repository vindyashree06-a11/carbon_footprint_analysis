
import pandas as pd

class DigitalTwin:

    def __init__(
        self,
        baseline_usage,
        baseline_emission
    ):

        self.baseline_usage = baseline_usage
        self.baseline_emission = baseline_emission

    def simulate(
        self,
        usage_change=0,
        renewable=0,
        production_growth=0
    ):

        future_usage = (
            self.baseline_usage
            *
            (1 + usage_change / 100)
        )

        future_usage *= (
            1 + production_growth / 100
        )

        future_emission = (
            self.baseline_emission
            *
            (future_usage / self.baseline_usage)
        )

        future_emission *= (
            1 - renewable / 100 * 0.5
        )

        esg_score = max(
            0,
            min(
                100,
                100 - future_emission * 100
            )
        )

        return {
            "future_usage": future_usage,
            "future_emission": future_emission,
            "projected_esg": esg_score
        }
