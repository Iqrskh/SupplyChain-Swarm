from agents.procurement_agent import ProcurementAgent


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


agent = ProcurementAgent()

result = agent.decide(
    order_quantity=188,
    suppliers=suppliers
)

print("\n===== PROCUREMENT AGENT =====")

print(f"Decision: {result['decision']}")
print(f"Supplier: {result['supplier']}")
print(f"Quantity: {result['quantity']} units")
print(f"Estimated Cost: ₹{result['estimated_cost']}")

print("\nReason:")
print(result["reason"])