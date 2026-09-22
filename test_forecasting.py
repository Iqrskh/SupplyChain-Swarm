import pandas as pd

from agents.demand_agent import DemandAgent


data = pd.read_csv(
    "data/raw/supply_chain_data.csv"
)

product_data = data[
    data["product"] == "Laptop"
].copy()

agent = DemandAgent()

result = agent.analyze(product_data)

print("\n===== DEMAND FORECASTING AGENT =====")
print(f"Forecast: {result['forecast']:.2f} units")
print(f"MAE: {result['mae']:.2f}")
print(f"RMSE: {result['rmse']:.2f}")

print("\nAgent Decision:")
print(result["message"])