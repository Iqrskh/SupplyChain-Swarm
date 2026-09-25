import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


class DemandForecaster:

    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

    def prepare_features(self, df):

        df = df.copy()

        # Support the public supply-chain dataset
        if "Date" in df.columns:
            df["date"] = pd.to_datetime(df["Date"])
        elif "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        else:
            raise ValueError(
                "Dataset must contain either 'Date' or 'date' column."
            )

        # Support the public supply-chain dataset
        if "Units_Sold" in df.columns:
            df["demand"] = df["Units_Sold"]
        elif "demand" not in df.columns:
            raise ValueError(
                "Dataset must contain either 'Units_Sold' or 'demand' column."
            )

        # Calendar features
        df["day_of_week"] = df["date"].dt.dayofweek
        df["day_of_month"] = df["date"].dt.day
        df["month"] = df["date"].dt.month

        # Previous demand
        df["lag_1"] = df["demand"].shift(1)
        df["lag_7"] = df["demand"].shift(7)

        # Rolling average
        df["rolling_7"] = (
            df["demand"]
            .rolling(window=7)
            .mean()
        )

        return df

    def train(self, df):

        df = self.prepare_features(df)

        # Remove rows created by lag/rolling features
        df = df.dropna()

        features = [
            "day_of_week",
            "day_of_month",
            "month",
            "lag_1",
            "lag_7",
            "rolling_7"
        ]

        X = df[features]
        y = df["demand"]

        # Time-based split
        split = int(len(df) * 0.8)

        X_train = X.iloc[:split]
        X_test = X.iloc[split:]

        y_train = y.iloc[:split]
        y_test = y.iloc[split:]

        # Train model
        self.model.fit(X_train, y_train)

        # Predictions
        predictions = self.model.predict(X_test)

        # Evaluation metrics
        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                predictions
            )
        )

        return {
            "mae": mae,
            "rmse": rmse,
            "actual": y_test.values,
            "predicted": predictions
        }

    def predict_next(self, df):

        df = self.prepare_features(df)

        df = df.dropna()

        features = [
            "day_of_week",
            "day_of_month",
            "month",
            "lag_1",
            "lag_7",
            "rolling_7"
        ]

        latest = df[features].iloc[-1:]

        prediction = self.model.predict(latest)

        return float(prediction[0])