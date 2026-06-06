
import numpy as np
import pandas as pd

class MonteCarloSimulator:

    def __init__(
        self,
        simulations=1000
    ):

        self.simulations = simulations

    def run(
        self,
        baseline_emission
    ):

        results = []

        for _ in range(
            self.simulations
        ):

            random_factor = np.random.normal(
                1.0,
                0.10
            )

            emission = (
                baseline_emission
                *
                random_factor
            )

            results.append(
                emission
            )

        return pd.DataFrame({
            "Emission": results
        })

    def risk_score(
        self,
        simulation_df
    ):

        return (
            simulation_df["Emission"]
            .std()
        )
