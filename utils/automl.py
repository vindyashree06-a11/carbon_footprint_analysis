
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso
)

from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

class AutoMLEngine:

    def __init__(self):

        self.models = {
            "Linear Regression": LinearRegression(),
            "Ridge": Ridge(),
            "Lasso": Lasso(),
            "Random Forest": RandomForestRegressor(
                random_state=42
            ),
            "Gradient Boosting": GradientBoostingRegressor(
                random_state=42
            )
        }

    def train_all(
        self,
        X,
        y
    ):

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.2,
                random_state=42
            )
        )

        results = []

        best_score = -999
        best_model = None

        for name, model in self.models.items():

            model.fit(X_train, y_train)

            pred = model.predict(X_test)

            r2 = r2_score(y_test, pred)
            mae = mean_absolute_error(y_test, pred)
            rmse = mean_squared_error(
                y_test,
                pred
            ) ** 0.5

            results.append([
                name,
                r2,
                mae,
                rmse
            ])

            if r2 > best_score:

                best_score = r2
                best_model = model

        return (
            pd.DataFrame(
                results,
                columns=[
                    "Model",
                    "R2",
                    "MAE",
                    "RMSE"
                ]
            ),
            best_model
        )
