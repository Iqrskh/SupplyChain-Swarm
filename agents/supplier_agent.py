class SupplierAgent:

    def analyze(self, suppliers):
        results = []

        for name, data in suppliers.items():

            # Higher reliability = lower risk
            reliability_risk = (1 - data["reliability"]) * 100

            # Longer delivery = higher risk
            delivery_risk = data["lead_time"] * 5

            # Combined risk score
            risk_score = (
                reliability_risk * 0.6
                + delivery_risk * 0.4
            )

            if risk_score < 15:
                risk_level = "LOW"
            elif risk_score < 25:
                risk_level = "MEDIUM"
            else:
                risk_level = "HIGH"

            results.append({
                "supplier": name,
                "unit_cost": data["unit_cost"],
                "lead_time": data["lead_time"],
                "reliability": data["reliability"],
                "risk_score": round(risk_score, 2),
                "risk_level": risk_level
            })

        return results