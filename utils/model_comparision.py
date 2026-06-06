
import pandas as pd
import numpy as np

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
    GradientBoostingRegressor,
    ExtraTreesRegressor,
    AdaBoostRegressor
)

class ModelComparison:

    def compare(self, X, y):

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        models = {
            "Linear Regression": LinearRegression(),
            "Ridge": Ridge(),
            "Lasso": Lasso(),
            "Random Forest": RandomForestRegressor(random_state=42),
            "Extra Trees": ExtraTreesRegressor(random_state=42),
            "Gradient Boosting": GradientBoostingRegressor(random_state=42),
            "AdaBoost": AdaBoostRegressor(random_state=42)
        }

        results = []

        for name, model in models.items():

            model.fit(X_train, y_train)

            pred = model.predict(X_test)

            results.append({
                "Model": name,
                "R2": r2_score(y_test, pred),
                "MAE": mean_absolute_error(y_test, pred),
                "RMSE": np.sqrt(
                    mean_squared_error(y_test, pred)
                )
            })

        return pd.DataFrame(results).sort_values(
            "R2",
            ascending=False
        )
