import pandas as pd

from agents.coordinator_agent import CoordinatorAgent


# Load data
data = pd.read_csv(
    "data/raw/supply_chain_data.csv"
)

# Select one product
product_data = data[
    data["product"] == "Laptop"
].copy()


# Supplier information
suppliers = {
    "Supplier_A": {
        "unit_cost": 500,
        "lead_time": 4,
        "reliability": 0.95
    },
    "Supplier_B": {
        "unit_cost": 470,
        "lead_time": 6,
        "reliability": 0.88
    },
    "Supplier_C": {
        "unit_cost": 530,
        "lead_time": 3,
        "reliability": 0.97
    }
}


# Create Coordinator
coordinator = CoordinatorAgent()

# Run the swarm
result = coordinator.run(
    product_data,
    suppliers
)


print("\n===================================")
print("       SUPPLYCHAIN SWARM")
print("===================================")

print("\n--- DEMAND AGENT ---")
print(
    f"Forecast: "
    f"{result['demand']['forecast']:.2f} units"
)

print(
    f"MAE: "
    f"{result['demand']['mae']:.2f}"
)

print("\n--- INVENTORY AGENT ---")

inventory = result["inventory"]

print(
    f"Current Inventory: "
    f"{inventory['current_inventory']}"
)

print(
    f"Stockout Risk: "
    f"{inventory['stockout_risk']}"
)

print(
    f"Recommended Order: "
    f"{inventory['recommended_order']} units"
)

print("\n--- SUPPLIER AGENT ---")

for supplier in result["suppliers"]:
    print(
        f"{supplier['supplier']} | "
        f"Risk: {supplier['risk_score']} "
        f"({supplier['risk_level']})"
    )

print("\n--- PROCUREMENT AGENT ---")

procurement = result["procurement"]

print(
    f"Selected Supplier: "
    f"{procurement['supplier']}"
)

print(
    f"Order Quantity: "
    f"{procurement['quantity']} units"
)

print(
    f"Estimated Cost: "
    f"₹{procurement['estimated_cost']}"
)

print("\nReason:")
print(procurement["reason"])

print("\n===================================")