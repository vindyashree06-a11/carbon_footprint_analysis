
import pandas as pd
import numpy as np

from sklearn.ensemble import IsolationForest

class AnomalyDetector:aa

    def __init__(self, contamination=0.05):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42
        )

    def detect(self, df):

        features = [
            "Usage_kWh",
            "CO2(tCO2)",
            "Lagging_Current_Reactive.Power_kVarh",
            "Leading_Current_Reactive_Power_kVarh"
        ]

        temp = df.copy()

        X = temp[features].fillna(0)

        temp["anomaly"] = self.model.fit_predict(X)

        temp["severity_score"] = (
            np.abs(
                X["Usage_kWh"] - X["Usage_kWh"].median()
            )
            /
            (X["Usage_kWh"].std() + 1)
        )

        temp["alert_level"] = np.where(
            temp["anomaly"] == -1,
            "HIGH",
            "NORMAL"
        )

        return temp

    def get_anomalies(self, df):

        result = self.detect(df)

        return result[
            result["anomaly"] == -1
        ]
