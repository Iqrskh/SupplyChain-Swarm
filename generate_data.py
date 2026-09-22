import pandas as pd
import numpy as np

np.random.seed(42)

# Simulation settings
days = 365

products = {
    "Laptop": 40,
    "Smartphone": 70,
    "Headphones": 90,
    "Keyboard": 55,
    "Monitor": 35
}

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

dates = pd.date_range(
    start="2025-01-01",
    periods=days,
    freq="D"
)

records = []

for product, base_demand in products.items():

    inventory = base_demand * 10

    for date in dates:

        # Weekly seasonality
        weekly_factor = 1 + 0.15 * np.sin(
            2 * np.pi * date.dayofweek / 7
        )

        # Random demand variation
        noise = np.random.normal(0, base_demand * 0.12)

        demand = max(
            1,
            int(base_demand * weekly_factor + noise)
        )

        # Select supplier
        supplier_name = np.random.choice(
            list(suppliers.keys())
        )

        supplier = suppliers[supplier_name]

        # Record current state
        records.append({
            "date": date,
            "product": product,
            "demand": demand,
            "inventory": max(0, int(inventory)),
            "supplier": supplier_name,
            "unit_cost": supplier["unit_cost"],
            "lead_time": supplier["lead_time"],
            "supplier_reliability": supplier["reliability"]
        })

        # Basic inventory consumption
        inventory -= demand

        # Replenishment simulation
        if inventory < base_demand * 5:
            inventory += base_demand * 8


df = pd.DataFrame(records)

# Save dataset
output_path = "data/raw/supply_chain_data.csv"

df.to_csv(output_path, index=False)

print("Dataset generated successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output_path}")

print("\nProducts:")
print(df["product"].unique())

print("\nFirst 5 rows:")
print(df.head())