import streamlit as st
import pandas as pd

from agents.coordinator_agent import CoordinatorAgent
from simulation.environment import SupplyChainEnvironment

from llm_service import explain_supply_chain
from rag_service import retrieve_documents, answer_with_rag


# =========================================================
# PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="SupplyChain-Swarm",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/raw/supply_chain_data.csv"
    )


data = load_data()


# =========================================================
# SUPPLIERS
# =========================================================

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


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("⚙️ Simulation Control")

    st.divider()

    product = st.selectbox(
        "📦 Select Product",
        sorted(data["product"].unique())
    )

    scenario = st.selectbox(
        "🌪️ Select Scenario",
        [
            "Normal",
            "Demand Shock",
            "Supplier Delay",
            "Cost Increase",
            "Combined Crisis"
        ]
    )

    st.divider()

    st.subheader("🧠 AI Stack")

    st.write("🤖 Agents → Decision Logic")
    st.write("📈 ML → Demand Forecast")
    st.write("📚 RAG → Policy Retrieval")
    st.write("🧠 Llama 3.2 → Explanation")
    st.write("👤 Human → Final Review")

    st.divider()

    st.caption(
        "Academic decision-support simulation"
    )

    st.caption(
        "No real procurement action is performed."
    )


# =========================================================
# HEADER
# =========================================================

st.title("🚚 SupplyChain-Swarm")

st.subheader(
    "LLM-Powered Agentic AI Supply Chain "
    "Decision Support System"
)

st.write(
    "An intelligent multi-agent system for demand forecasting, "
    "inventory analysis, supplier risk evaluation, procurement "
    "recommendations, RAG-based knowledge retrieval, and local "
    "LLM-generated explanations."
)

st.caption(
    "🤖 Agentic AI   •   📈 Machine Learning   •   "
    "🧠 Llama 3.2   •   📚 RAG   •   🛡️ Responsible AI"
)

st.divider()


# =========================================================
# PRODUCT DATA
# =========================================================

product_data = data[
    data["product"] == product
].copy()


# =========================================================
# SCENARIO ENVIRONMENT
# =========================================================

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


# =========================================================
# RUN AGENTIC SYSTEM
# =========================================================

coordinator = CoordinatorAgent()


result = coordinator.run(
    product_data,
    suppliers,
    environment
)


inventory = result["inventory"]

procurement = result["procurement"]


selected_supplier = procurement.get(
    "selected_supplier",
    "N/A"
)

order_quantity = procurement.get(
    "quantity",
    0
)

estimated_cost = procurement.get(
    "estimated_cost",
    0
)


# =========================================================
# LLM
# =========================================================

try:

    llm_explanation = explain_supply_chain(
        result
    )

    llm_ok = True

    llm_error = ""


except Exception as e:

    llm_explanation = (
        "The local LLM could not generate an explanation. "
        "Please start Ollama and make sure "
        "llama3.2:3b is available."
    )

    llm_ok = False

    llm_error = str(e)


# =========================================================
# RAG
# =========================================================

rag_query = (
    f"Explain the supply chain decision for the "
    f"{scenario} scenario, including inventory risk, "
    f"supplier evaluation, procurement, and crisis management."
)


try:

    retrieved_documents = retrieve_documents(
        rag_query,
        top_k=2
    )

    rag_error = ""


except Exception as e:

    retrieved_documents = []

    rag_error = str(e)


# =========================================================
# SCENARIO DESCRIPTION
# =========================================================

scenario_descriptions = {

    "Normal":
        "Normal supply-chain conditions.",

    "Demand Shock":
        "Customer demand has increased by 40%.",

    "Supplier Delay":
        "Supplier A is experiencing a 5-day delivery delay.",

    "Cost Increase":
        "Supplier C's cost has increased by 20%.",

    "Combined Crisis":
        "Demand increased by 40%, Supplier A has a "
        "5-day delay, and Supplier C's cost increased "
        "by 20%."
}


# =========================================================
# CURRENT SCENARIO
# =========================================================

st.info(
    f"""
    **Current Scenario:** {scenario}

    **Product:** {product}

    {scenario_descriptions[scenario]}
    """
)


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

st.header("📊 Executive Overview")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📈 Predicted Demand",
        f"{result['adjusted_demand']:.2f}",
        "units"
    )


with col2:

    st.metric(
        "📦 Current Inventory",
        f"{inventory['current_inventory']}",
        "units"
    )


with col3:

    st.metric(
        "⚠️ Stockout Risk",
        str(inventory["stockout_risk"])
    )


with col4:

    st.metric(
        "🛒 Recommended Order",
        f"{order_quantity}",
        "units"
    )


st.success(
    f"""
    🎯 **Procurement Recommendation**

    Supplier: **{selected_supplier}**

    Order Quantity: **{order_quantity} units**

    Estimated Cost: **₹{estimated_cost:,.2f}**

    👤 Human review required before real-world action.
    """
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Overview",
        "🤖 AI Intelligence",
        "📦 Inventory",
        "🏭 Suppliers",
        "⚙️ System"
    ]
)


# =========================================================
# TAB 1 — OVERVIEW
# =========================================================

with tab1:

    st.subheader(
        "🔄 End-to-End AI Pipeline"
    )


    flow1, flow2, flow3 = st.columns(3)


    with flow1:

        st.info(
            """
            ### 📈 Demand Agent

            Forecasts future demand
            using historical data.
            """
        )


    with flow2:

        st.info(
            """
            ### 📦 Inventory Agent

            Calculates safety stock,
            reorder point and stockout risk.
            """
        )


    with flow3:

        st.info(
            """
            ### 🏭 Supplier Agent

            Evaluates supplier cost,
            lead time and reliability.
            """
        )


    flow4, flow5, flow6 = st.columns(3)


    with flow4:

        st.info(
            """
            ### 🛒 Procurement Agent

            Generates the structured
            procurement recommendation.
            """
        )


    with flow5:

        st.info(
            """
            ### 📚 RAG Layer

            Retrieves relevant
            supply-chain policies.
            """
        )


    with flow6:

        st.info(
            """
            ### 🧠 Llama 3.2

            Generates a grounded
            natural-language explanation.
            """
        )


    st.divider()


    st.subheader(
        "📋 Simulation Summary"
    )


    overview_df = pd.DataFrame({

        "Metric": [

            "Scenario",

            "Product",

            "Adjusted Demand",

            "Current Inventory",

            "Stockout Risk",

            "Selected Supplier",

            "Order Quantity",

            "Estimated Cost"

        ],

        "Value": [

            scenario,

            product,

            f"{result['adjusted_demand']:.2f} units",

            f"{inventory['current_inventory']} units",

            inventory["stockout_risk"],

            selected_supplier,

            f"{order_quantity} units",

            f"₹{estimated_cost:,.2f}"

        ]

    })


    st.dataframe(
        overview_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 2 — AI INTELLIGENCE
# =========================================================

with tab2:

    st.subheader(
        "🤖 AI Supply Chain Intelligence"
    )


    if llm_ok:

        st.success(
            "🟢 Local LLM connected — "
            "Llama 3.2 via Ollama"
        )

    else:

        st.warning(
            "🟠 Local LLM unavailable — "
            "start Ollama."
        )

        with st.expander(
            "Technical Error"
        ):

            st.code(
                llm_error
            )


    st.markdown(
        "### 🧠 AI-Generated Decision Explanation"
    )


    st.write(
        llm_explanation
    )


    st.divider()


    # =====================================================
    # RAG
    # =====================================================

    st.subheader(
        "📚 RAG Knowledge Retrieval"
    )


    st.write(
        "The system retrieves relevant project-specific "
        "policies before generating the grounded AI response."
    )


    if retrieved_documents:

        st.success(
            f"Retrieved {len(retrieved_documents)} "
            "relevant knowledge sources."
        )


        rag_df = pd.DataFrame(

            [

                {

                    "Knowledge Source":
                        document["filename"],

                    "Relevance Score":
                        round(
                            document["score"],
                            3
                        )

                }

                for document
                in retrieved_documents

            ]

        )


        st.dataframe(
            rag_df,
            use_container_width=True,
            hide_index=True
        )


        with st.expander(
            "🔎 View Retrieved Knowledge"
        ):

            for document in retrieved_documents:

                st.markdown(
                    f"### 📄 {document['filename']}"
                )

                st.caption(
                    f"Relevance Score: "
                    f"{document['score']:.3f}"
                )

                st.text(
                    document["content"]
                )

                st.divider()


    else:

        st.warning(
            "No relevant knowledge sources were retrieved."
        )

        if rag_error:

            with st.expander(
                "RAG Error"
            ):

                st.code(
                    rag_error
                )


    # =====================================================
    # RAG + LLM
    # =====================================================

    st.subheader(
        "🧠 RAG-Grounded AI Analysis"
    )


    try:

        rag_answer = answer_with_rag(
            rag_query,
            result
        )


        st.write(
            rag_answer
        )


    except Exception as e:

        st.warning(
            f"RAG response could not be generated: {e}"
        )


    st.divider()


    # =====================================================
    # RESPONSIBLE AI
    # =====================================================

    st.subheader(
        "🛡️ Responsible AI"
    )


    st.info(
        """
        **Human-in-the-loop architecture**

        • AI outputs are simulated decision-support results.

        • Numerical decisions are generated by
        specialized supply-chain agents.

        • The LLM explains the results rather than
        replacing the decision logic.

        • RAG provides project-specific knowledge.

        • Retrieved knowledge sources are visible.

        • The system is instructed not to invent
        supplier, cost, inventory or policy information.

        • No real procurement transaction is
        automatically executed.

        • Final business decisions require human review.
        """
    )


# =========================================================
# TAB 3 — INVENTORY
# =========================================================

with tab3:

    st.subheader(
        "📦 Inventory Analysis"
    )


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


    st.subheader(
        "📌 Inventory Indicators"
    )


    a, b, c = st.columns(3)


    with a:

        st.metric(
            "Reorder Point",
            f"{inventory['reorder_point']:.2f}"
        )


    with b:

        st.metric(
            "Safety Stock",
            f"{inventory['safety_stock']:.2f}"
        )


    with c:

        st.metric(
            "Lead-Time Demand",
            f"{inventory['lead_time_demand']:.2f}"
        )


# =========================================================
# TAB 4 — SUPPLIERS
# =========================================================

with tab4:

    st.subheader(
        "🏭 Supplier Risk Analysis"
    )


    supplier_df = pd.DataFrame(

        [

            {

                "Supplier":
                    item["supplier"],

                "Unit Cost":
                    f"₹{item['unit_cost']:.2f}",

                "Lead Time":
                    f"{item['lead_time']} days",

                "Reliability":
                    f"{item['reliability'] * 100:.0f}%",

                "Risk Score":
                    item["risk_score"],

                "Risk Level":
                    item["risk_level"]

            }

            for item
            in result["suppliers"]

        ]

    )


    st.dataframe(
        supplier_df,
        use_container_width=True,
        hide_index=True
    )


    st.subheader(
        "🎯 Procurement Decision"
    )


    a, b, c = st.columns(3)


    with a:

        st.metric(
            "Selected Supplier",
            selected_supplier
        )


    with b:

        st.metric(
            "Order Quantity",
            f"{order_quantity} units"
        )


    with c:

        st.metric(
            "Estimated Cost",
            f"₹{estimated_cost:,.2f}"
        )


    if procurement.get("reason"):

        st.info(
            procurement["reason"]
        )


    st.subheader(
        "📈 Supplier Decision Scores"
    )


    score_rows = []


    for supplier_name, supplier_data in suppliers.items():

        cost = supplier_data["unit_cost"]

        lead_time = supplier_data["lead_time"]

        reliability = supplier_data["reliability"]


        decision_score = (

            cost

            + lead_time * 50

            + (1 - reliability) * 1000

        )


        score_rows.append({

            "Supplier":
                supplier_name,

            "Unit Cost":
                cost,

            "Lead Time":
                lead_time,

            "Reliability":
                reliability * 100,

            "Decision Score":
                round(
                    decision_score,
                    2
                )

        })


    score_df = pd.DataFrame(
        score_rows
    )


    st.dataframe(
        score_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TAB 5 — SYSTEM
# =========================================================

with tab5:

    st.subheader(
        "🤖 Agentic AI Workflow"
    )


    workflow = [

        (
            "1️⃣",
            "Demand Agent",
            "Forecasts future demand from historical data."
        ),

        (
            "2️⃣",
            "Inventory Agent",
            "Calculates safety stock, reorder point, "
            "stockout risk and order quantity."
        ),

        (
            "3️⃣",
            "Supplier Agent",
            "Evaluates supplier cost, lead time, "
            "reliability and risk."
        ),

        (
            "4️⃣",
            "Procurement Agent",
            "Produces the structured procurement recommendation."
        ),

        (
            "5️⃣",
            "RAG Layer",
            "Retrieves relevant project-specific policies."
        ),

        (
            "6️⃣",
            "Local LLM",
            "Generates a grounded natural-language explanation."
        ),

        (
            "7️⃣",
            "Human Review",
            "Reviews the simulated recommendation "
            "before real-world action."
        )

    ]


    for icon, title, description in workflow:

        with st.expander(
            f"{icon} {title}"
        ):

            st.write(
                description
            )


    st.divider()


    st.subheader(
        "🧩 AI Components"
    )


    component_df = pd.DataFrame({

        "Component": [

            "Machine Learning",

            "Agentic AI",

            "LLM",

            "Generative AI",

            "RAG",

            "Local AI Inference",

            "Responsible AI"

        ],

        "Role": [

            "Demand forecasting",

            "Coordinates specialized supply-chain agents",

            "Llama 3.2 explains system results",

            "Generates natural-language explanations",

            "Retrieves project-specific policies",

            "Runs Llama 3.2 through Ollama",

            "Grounding, transparency and human review"

        ]

    })


    st.dataframe(
        component_df,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    st.subheader(
        "📌 System Status"
    )


    a, b, c, d = st.columns(4)


    with a:

        st.success(
            "✅ Agents Running"
        )


    with b:

        if llm_ok:

            st.success(
                "✅ Local LLM Connected"
            )

        else:

            st.warning(
                "⚠️ LLM Unavailable"
            )


    with c:

        if retrieved_documents:

            st.success(
                "✅ RAG Retrieval Active"
            )

        else:

            st.warning(
                "⚠️ No RAG Sources"
            )


    with d:

        st.success(
            "✅ Simulation Active"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "SupplyChain-Swarm | LLM-Powered Agentic AI "
    "Supply Chain Decision Support System | "
    "Agentic AI • ML • LLM • RAG • Responsible AI"
)