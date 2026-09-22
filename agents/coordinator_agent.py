from agents.demand_agent import DemandAgent
from agents.inventory_agent import InventoryAgent
from agents.supplier_agent import SupplierAgent
from agents.procurement_agent import ProcurementAgent


class CoordinatorAgent:

    def __init__(self):
        self.demand_agent = DemandAgent()
        self.inventory_agent = InventoryAgent()
        self.supplier_agent = SupplierAgent()
        self.procurement_agent = ProcurementAgent()

    def run(self, product_data, suppliers, environment=None):

        # ==========================================
        # 1. DEMAND FORECASTING
        # ==========================================

        demand_result = self.demand_agent.analyze(
            product_data
        )

        predicted_demand = demand_result["forecast"]

        # Apply demand shock
        if environment:
            predicted_demand = environment.modify_demand(
                predicted_demand
            )

        # ==========================================
        # 2. MODIFY SUPPLIERS FOR CURRENT SCENARIO
        # ==========================================

        if environment:
            active_suppliers = environment.modify_suppliers(
                suppliers
            )
        else:
            active_suppliers = suppliers

        # ==========================================
        # 3. SUPPLIER RISK ANALYSIS
        # ==========================================

        supplier_results = self.supplier_agent.analyze(
            active_suppliers
        )

        # ==========================================
        # 4. GET CURRENT INVENTORY
        # ==========================================

        current_inventory = int(
            product_data["inventory"].iloc[-1]
        )

        # ==========================================
        # 5. DETERMINE LEAD TIME
        # ==========================================

        base_lead_time = int(
            product_data["lead_time"].iloc[-1]
        )

        # Find the largest supplier delay
        # for planning purposes
        max_delay = 0

        if environment:
            for changes in environment.supplier_changes.values():

                delay = changes.get(
                    "delay_days",
                    0
                )

                max_delay = max(
                    max_delay,
                    delay
                )

        planning_lead_time = (
            base_lead_time + max_delay
        )

        # ==========================================
        # 6. INVENTORY ANALYSIS
        # ==========================================

        inventory_result = self.inventory_agent.analyze(
            current_inventory=current_inventory,
            predicted_demand=predicted_demand,
            lead_time=planning_lead_time
        )

        order_quantity = inventory_result[
            "recommended_order"
        ]

        # ==========================================
        # 7. PROCUREMENT DECISION
        # ==========================================

        procurement_result = self.procurement_agent.decide(
            order_quantity=order_quantity,
            suppliers=active_suppliers
        )

        # ==========================================
        # 8. RETURN COMPLETE SWARM RESULT
        # ==========================================

        return {

            "demand": demand_result,

            "adjusted_demand": predicted_demand,

            "inventory": inventory_result,

            "suppliers": supplier_results,

            "procurement": procurement_result
        }