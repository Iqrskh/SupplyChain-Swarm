from agents.inventory_agent import InventoryAgent


agent = InventoryAgent()

result = agent.analyze(
    current_inventory=100,
    predicted_demand=41.17,
    lead_time=4
)

print("\n===== INVENTORY AGENT =====")
print(f"Current Inventory: {result['current_inventory']}")
print(f"Predicted Demand: {result['predicted_demand']}")
print(f"Safety Stock: {result['safety_stock']}")
print(f"Lead-Time Demand: {result['lead_time_demand']}")
print(f"Reorder Point: {result['reorder_point']}")
print(f"Stockout Risk: {result['stockout_risk']}")
print(f"Recommended Order: {result['recommended_order']} units")
