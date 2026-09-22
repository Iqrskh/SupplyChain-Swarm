class InventoryAgent:

    def __init__(self, safety_days=3):
        self.safety_days = safety_days

    def analyze(self, current_inventory, predicted_demand, lead_time):
        """
        Analyze inventory and determine whether replenishment is required.
        """

        # Safety stock based on predicted daily demand
        safety_stock = predicted_demand * self.safety_days

        # Expected demand during supplier lead time
        lead_time_demand = predicted_demand * lead_time

        # Reorder point
        reorder_point = lead_time_demand + safety_stock

        # Determine inventory status
        if current_inventory <= safety_stock:
            risk = "HIGH"
        elif current_inventory <= reorder_point:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        # Recommended order quantity
        if current_inventory < reorder_point:
            order_quantity = max(
                0,
                int(reorder_point - current_inventory)
            )
        else:
            order_quantity = 0

        return {
            "current_inventory": current_inventory,
            "predicted_demand": predicted_demand,
            "safety_stock": round(safety_stock, 2),
            "lead_time_demand": round(lead_time_demand, 2),
            "reorder_point": round(reorder_point, 2),
            "stockout_risk": risk,
            "recommended_order": order_quantity
        }