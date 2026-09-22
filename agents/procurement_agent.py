class ProcurementAgent:

    def decide(self, order_quantity, suppliers):

        # No order required
        if order_quantity <= 0:
            return {
                "decision": "No order required",
                "supplier": None,
                "quantity": 0,
                "estimated_cost": 0,
                "reason": "Current inventory is sufficient."
            }

        supplier_scores = []

        # ==========================================
        # CALCULATE SCORE FOR EACH SUPPLIER
        # ==========================================

        for name, data in suppliers.items():

            cost = data["unit_cost"]
            lead_time = data["lead_time"]
            reliability = data["reliability"]

            # Cost component
            cost_score = cost

            # Lead-time component
            lead_time_score = lead_time * 50

            # Reliability penalty
            reliability_penalty = (
                1 - reliability
            ) * 1000

            # Total decision score
            total_score = (
                cost_score
                + lead_time_score
                + reliability_penalty
            )

            supplier_scores.append({
                "supplier": name,
                "cost": cost,
                "lead_time": lead_time,
                "reliability": reliability,
                "score": total_score
            })

        # ==========================================
        # SELECT LOWEST SCORE
        # ==========================================

        supplier_scores.sort(
            key=lambda x: x["score"]
        )

        selected = supplier_scores[0]

        best_supplier = selected["supplier"]

        estimated_cost = (
            order_quantity * selected["cost"]
        )

        # ==========================================
        # FIND COMPARISON SUPPLIERS
        # ==========================================

        other_suppliers = [
            s for s in supplier_scores
            if s["supplier"] != best_supplier
        ]

        # ==========================================
        # GENERATE EXPLANATION
        # ==========================================

        reason = (
            f"{best_supplier} was selected because "
            f"its overall decision score was the lowest "
            f"among the available suppliers. "
            f"It has a unit cost of ₹{selected['cost']:.2f}, "
            f"a lead time of {selected['lead_time']} days, "
            f"and reliability of "
            f"{selected['reliability'] * 100:.0f}%."
        )

        if other_suppliers:

            next_best = other_suppliers[0]

            reason += (
                f" Its score was "
                f"{selected['score']:.1f}, compared with "
                f"{next_best['supplier']}'s score of "
                f"{next_best['score']:.1f}."
            )

        # ==========================================
        # RETURN DECISION
        # ==========================================

        return {
            "decision": "Order recommended",
            "supplier": best_supplier,
            "quantity": order_quantity,
            "estimated_cost": estimated_cost,
            "score": round(selected["score"], 2),
            "reason": reason,
            "supplier_scores": supplier_scores
        }