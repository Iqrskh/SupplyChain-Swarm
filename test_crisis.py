import pandas as pd

from agents.coordinator_agent import CoordinatorAgent
from simulation.environment import SupplyChainEnvironment


# ==========================================
# LOAD DATA
# ==========================================

data = pd.read_csv(
    "data/raw/supply_chain_data.csv"
)

# Select one product
product_data = data[
    data["product"] == "Laptop"
].copy()


# ==========================================
# SUPPLIER INFORMATION
# ==========================================

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


# ==========================================
# CREATE COORDINATOR
# ==========================================

coordinator = CoordinatorAgent()


# ==========================================
# NORMAL SCENARIO
# ==========================================

print("\n")
print("==========================================")
print("          NORMAL SCENARIO")
print("==========================================")


normal_environment = SupplyChainEnvironment()


normal_result = coordinator.run(
    product_data,
    suppliers,
    normal_environment
)


print(
    f"\nPredicted Demand: "
    f"{normal_result['adjusted_demand']:.2f} units"
)

print(
    f"Current Inventory: "
    f"{normal_result['inventory']['current_inventory']} units"
)

print(
    f"Stockout Risk: "
    f"{normal_result['inventory']['stockout_risk']}"
)

print(
    f"Recommended Order: "
    f"{normal_result['procurement']['quantity']} units"
)

print(
    f"Selected Supplier: "
    f"{normal_result['procurement']['supplier']}"
)

print(
    f"Estimated Cost: ₹"
    f"{normal_result['procurement']['estimated_cost']:.2f}"
)


# ==========================================
# COMBINED CRISIS SCENARIO
# ==========================================

print("\n")
print("==========================================")
print("          COMBINED CRISIS")
print("==========================================")


crisis_environment = SupplyChainEnvironment()


# Demand increases by 40%
crisis_environment.apply_demand_shock(40)


# Supplier A experiences a 5-day delay
crisis_environment.apply_supplier_delay(
    "Supplier_A",
    5
)


# Supplier C becomes 20% more expensive
crisis_environment.apply_cost_increase(
    "Supplier_C",
    20
)


# Run coordinator under crisis
crisis_result = coordinator.run(
    product_data,
    suppliers,
    crisis_environment
)


print(
    f"\nAdjusted Demand: "
    f"{crisis_result['adjusted_demand']:.2f} units"
)

print(
    f"Current Inventory: "
    f"{crisis_result['inventory']['current_inventory']} units"
)

print(
    f"Stockout Risk: "
    f"{crisis_result['inventory']['stockout_risk']}"
)

print(
    f"Recommended Order: "
    f"{crisis_result['procurement']['quantity']} units"
)

print(
    f"Selected Supplier: "
    f"{crisis_result['procurement']['supplier']}"
)

print(
    f"Estimated Cost: ₹"
    f"{crisis_result['procurement']['estimated_cost']:.2f}"
)


# ==========================================
# SUPPLIER RISK DURING CRISIS
# ==========================================

print("\n")
print("------ SUPPLIER RISK DURING CRISIS ------")


for supplier in crisis_result["suppliers"]:

    print(
        f"{supplier['supplier']} | "
        f"Cost: ₹{supplier['unit_cost']:.2f} | "
        f"Lead Time: {supplier['lead_time']} days | "
        f"Reliability: {supplier['reliability']} | "
        f"Risk: {supplier['risk_score']} "
        f"({supplier['risk_level']})"
    )


# ==========================================
# FINAL COMPARISON
# ==========================================

print("\n")
print("==========================================")
print("        NORMAL vs CRISIS")
print("==========================================")


print(
    f"\nDemand:"
    f"\n  Normal : "
    f"{normal_result['adjusted_demand']:.2f}"
    f"\n  Crisis : "
    f"{crisis_result['adjusted_demand']:.2f}"
)

print(
    f"\nOrder Quantity:"
    f"\n  Normal : "
    f"{normal_result['procurement']['quantity']}"
    f"\n  Crisis : "
    f"{crisis_result['procurement']['quantity']}"
)

print(
    f"\nSupplier:"
    f"\n  Normal : "
    f"{normal_result['procurement']['supplier']}"
    f"\n  Crisis : "
    f"{crisis_result['procurement']['supplier']}"
)

print(
    f"\nEstimated Cost:"
    f"\n  Normal : ₹"
    f"{normal_result['procurement']['estimated_cost']:.2f}"
    f"\n  Crisis : ₹"
    f"{crisis_result['procurement']['estimated_cost']:.2f}"
)


print("\n")
print("==========================================")
print("       SIMULATION COMPLETED")
print("==========================================")