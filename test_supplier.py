from agents.supplier_agent import SupplierAgent


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


agent = SupplierAgent()

results = agent.analyze(suppliers)

print("\n===== SUPPLIER RISK AGENT =====")

for supplier in results:
    print(
        f"{supplier['supplier']} | "
        f"Cost: {supplier['unit_cost']} | "
        f"Lead Time: {supplier['lead_time']} days | "
        f"Reliability: {supplier['reliability']} | "
        f"Risk: {supplier['risk_score']} "
        f"({supplier['risk_level']})"
    )