import streamlit as st
import pandas as pd

from agents.coordinator_agent import CoordinatorAgent
from simulation.environment import SupplyChainEnvironment


# ==========================================
# PAGE SETUP
# ==========================================

st.set_page_config(
    page_title="SupplyChain Swarm",
    page_icon="🚚",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.markdown(
    """
    <div style="text-align:center; padding:10px 0 25px 0;">
        <h1>🚚 SupplyChain Swarm</h1>
        <p style="font-size:18px;">
            Multi-Agent Supply Chain Intelligence Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.write(
    "An AI-based multi-agent system that forecasts demand, "
    "analyzes inventory, evaluates supplier risk, and "
    "recommends procurement decisions."
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    return pd.read_csv(
        "data/raw/supply_chain_data.csv"
    )


data = load_data()


# ==========================================
# SUPPLIERS
# ==========================================

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


# ==========================================
# SIDEBAR CONTROLS
# ==========================================

st.sidebar.header("⚙️ Simulation Controls")

product = st.sidebar.selectbox(
    "Select Product",
    sorted(data["product"].unique())
)

scenario = st.sidebar.selectbox(
    "Select Scenario",
    [
        "Normal",
        "Demand Shock",
        "Supplier Delay",
        "Cost Increase",
        "Combined Crisis"
    ]
)


# ==========================================
# SELECT PRODUCT DATA
# ==========================================

product_data = data[
    data["product"] == product
].copy()


# ==========================================
# CREATE ENVIRONMENT
# ==========================================

environment = SupplyChainEnvironment()


if scenario == "Demand Shock":

    environment.apply_demand_shock(40)


elif scenario == "Supplier Delay":

    environment.apply_supplier_delay(
        "Supplier_A",
        5
    )


elif scenario == "Cost Increase":

    environment.apply_cost_increase(
        "Supplier_C",
        20
    )


elif scenario == "Combined Crisis":

    environment.apply_demand_shock(40)

    environment.apply_supplier_delay(
        "Supplier_A",
        5
    )

    environment.apply_cost_increase(
        "Supplier_C",
        20
    )


# ==========================================
# RUN SUPPLYCHAIN SWARM
# ==========================================

coordinator = CoordinatorAgent()

result = coordinator.run(
    product_data,
    suppliers,
    environment
)


# ==========================================
# SCENARIO INFORMATION
# ==========================================

st.info(
    f"📌 Current Scenario: **{scenario}**"
)


if scenario == "Normal":

    st.write(
        "Normal supply-chain conditions."
    )

elif scenario == "Demand Shock":

    st.write(
        "Customer demand has increased by 40%."
    )

elif scenario == "Supplier Delay":

    st.write(
        "Supplier A is experiencing a 5-day delivery delay."
    )

elif scenario == "Cost Increase":

    st.write(
        "Supplier C's cost has increased by 20%."
    )

elif scenario == "Combined Crisis":

    st.write(
        "Demand increased by 40%, Supplier A has a "
        "5-day delay, and Supplier C's cost increased by 20%."
    )


# ==========================================
# SUPPLY CHAIN OVERVIEW
# ==========================================



st.markdown(
    """
    <h2 style="text-align:center;">
        📊 Supply Chain Overview
    </h2>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📈 Predicted Demand",
        f"{result['adjusted_demand']:.2f} units"
    )

with col2:
    st.metric(
        "📦 Current Inventory",
        f"{result['inventory']['current_inventory']} units"
    )

with col3:
    st.metric(
        "⚠️ Stockout Risk",
        result["inventory"]["stockout_risk"]
    )

with col4:
    st.metric(
        "🚚 Recommended Order",
        f"{result['procurement']['quantity']} units"
    )

# ==========================================
# INVENTORY ANALYSIS
# ==========================================

st.header("📦 Inventory Analysis")

inventory = result["inventory"]


inventory_df = pd.DataFrame({

    "Metric": [
        "Current Inventory",
        "Predicted Demand",
        "Safety Stock",
        "Lead-Time Demand",
        "Reorder Point",
        "Stockout Risk",
        "Recommended Order"
    ],

    "Value": [

        inventory["current_inventory"],

        inventory["predicted_demand"],

        inventory["safety_stock"],

        inventory["lead_time_demand"],

        inventory["reorder_point"],

        inventory["stockout_risk"],

        inventory["recommended_order"]
    ]
})


st.dataframe(
    inventory_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# SUPPLIER RISK ANALYSIS
# ==========================================

st.header("🚚 Supplier Risk Analysis")


supplier_table = []


for supplier in result["suppliers"]:

    supplier_table.append({

        "Supplier":
            supplier["supplier"],

        "Unit Cost":
            f"₹{supplier['unit_cost']:.2f}",

        "Lead Time":
            f"{supplier['lead_time']} days",

        "Reliability":
            f"{supplier['reliability'] * 100:.0f}%",

        "Risk Score":
            supplier["risk_score"],

        "Risk Level":
            supplier["risk_level"]
    })


supplier_df = pd.DataFrame(
    supplier_table
)


st.dataframe(
    supplier_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# SUPPLIER DECISION SCORES
# ==========================================

st.header("📈 Supplier Decision Scores")

score_rows = []

for name, data in suppliers.items():

    cost = data["unit_cost"]
    lead_time = data["lead_time"]
    reliability = data["reliability"]

    # Same scoring logic used by Procurement Agent
    cost_score = cost

    lead_time_score = lead_time * 50

    reliability_penalty = (
        1 - reliability
    ) * 1000

    decision_score = (
        cost_score
        + lead_time_score
        + reliability_penalty
    )

    score_rows.append({
        "Supplier": name,
        "Unit Cost": cost,
        "Lead Time": lead_time,
        "Reliability": reliability * 100,
        "Decision Score": round(
            decision_score,
            2
        )
    })


score_df = pd.DataFrame(score_rows)


st.dataframe(
    score_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# AGENT WORKFLOW
# ==========================================

st.header("🤖 Agent Workflow")


st.markdown(
    """
    **Demand Agent**  
    ↓  
    Forecasts future demand  

    **Inventory Agent**  
    ↓  
    Calculates stockout risk and reorder quantity  

    **Supplier Risk Agent**  
    ↓  
    Evaluates supplier cost, lead time and reliability  

    **Procurement Agent**  
    ↓  
    Selects supplier and recommends order  

    **Final Explainable Decision**
    """
)


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "SupplyChain Swarm | Multi-Agent AI Simulation"
)
