class SupplyChainEnvironment:

    def __init__(self):
        self.demand_multiplier = 1.0
        self.supplier_changes = {}

    def apply_demand_shock(self, percentage):
        self.demand_multiplier = 1 + (percentage / 100)

    def apply_supplier_delay(self, supplier, days):
        self.supplier_changes.setdefault(supplier, {})
        self.supplier_changes[supplier]["delay_days"] = days

    def apply_cost_increase(self, supplier, percentage):
        self.supplier_changes.setdefault(supplier, {})
        self.supplier_changes[supplier]["cost_multiplier"] = (
            1 + (percentage / 100)
        )

    def modify_demand(self, demand):
        return demand * self.demand_multiplier

    def modify_suppliers(self, suppliers):

        modified_suppliers = {}

        for name, data in suppliers.items():

            modified_suppliers[name] = data.copy()

            changes = self.supplier_changes.get(
                name, {}
            )

            # Supplier-specific delay
            modified_suppliers[name]["lead_time"] += (
                changes.get("delay_days", 0)
            )

            # Supplier-specific cost
            modified_suppliers[name]["unit_cost"] *= (
                changes.get("cost_multiplier", 1.0)
            )

        return modified_suppliers