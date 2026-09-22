from simulation.environment import SupplyChainEnvironment


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


print("\n===== NORMAL CONDITIONS =====")

environment = SupplyChainEnvironment()

normal_suppliers = environment.modify_suppliers(
    suppliers
)

print(normal_suppliers)


print("\n===== DEMAND SHOCK =====")

environment = SupplyChainEnvironment()

environment.apply_demand_shock(40)

normal_demand = 41.17

new_demand = environment.modify_demand(
    normal_demand
)

print(f"Original Demand: {normal_demand:.2f}")
print(f"New Demand: {new_demand:.2f}")


print("\n===== SUPPLIER DELAY =====")

environment = SupplyChainEnvironment()

environment.apply_supplier_delay(5)

delayed_suppliers = environment.modify_suppliers(
    suppliers
)

for name, data in delayed_suppliers.items():
    print(
        f"{name}: "
        f"Lead Time = {data['lead_time']} days"
    )


print("\n===== COST INCREASE =====")

environment = SupplyChainEnvironment()

environment.apply_cost_increase(20)

expensive_suppliers = environment.modify_suppliers(
    suppliers
)

for name, data in expensive_suppliers.items():
    print(
        f"{name}: "
        f"Cost = ₹{data['unit_cost']:.2f}"
    )


print("\n===== COMBINED CRISIS =====")

environment = SupplyChainEnvironment()

environment.apply_demand_shock(40)
environment.apply_supplier_delay(5)
environment.apply_cost_increase(20)

crisis_demand = environment.modify_demand(
    normal_demand
)

crisis_suppliers = environment.modify_suppliers(
    suppliers
)

print(f"Crisis Demand: {crisis_demand:.2f}")

for name, data in crisis_suppliers.items():
    print(
        f"{name}: "
        f"Cost = ₹{data['unit_cost']:.2f}, "
        f"Lead Time = {data['lead_time']} days"
    )