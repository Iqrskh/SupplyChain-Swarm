from models.forecasting import DemandForecaster


class DemandAgent:

    def __init__(self):
        self.forecaster = DemandForecaster()

    def analyze(self, data):

        results = self.forecaster.train(data)

        forecast = self.forecaster.predict_next(data)

        return {
            "forecast": forecast,
            "mae": results["mae"],
            "rmse": results["rmse"],
            "message": (
                f"Forecasted demand for next period: "
                f"{forecast:.2f} units"
            )
        }