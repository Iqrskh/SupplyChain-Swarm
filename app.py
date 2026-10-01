import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

from agents.coordinator_agent import CoordinatorAgent
from simulation.environment import SupplyChainEnvironment

from llm_service import explain_supply_chain
from rag_service import retrieve_documents, answer_with_rag


# =========================================================
# PDF REPORT GENERATION
# =========================================================

def generate_pdf_report(
    result,
    product,
    scenario,
    selected_supplier,
    order_quantity,
    estimated_cost,
    llm_explanation,
    retrieved_documents,
    review_status,
    reviewer_comment
):
    """
    Generate the final SupplyChain-Swarm PDF report.
    The report is available only after human approval.
    """

    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle
        )

    except ImportError:
        raise RuntimeError(
            "ReportLab is not installed. "
            "Run: pip install reportlab"
        )

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )

    styles = getSampleStyleSheet()

    story = []

    inventory = result["inventory"]

    procurement = result["procurement"]

    demand = result.get("demand", {})

    report_id = (
        f"SC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    )

    generated_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # =====================================================
    # TITLE
    # =====================================================

    story.append(
        Paragraph(
            "<b>SupplyChain-Swarm Decision Report</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            "LLM-Powered Agentic AI Supply Chain "
            "Decision Support System",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    story.append(
        Paragraph(
            "<b>1. Basic Information</b>",
            styles["Heading2"]
        )
    )

    basic_data = [
        ["Report ID", report_id],
        ["Generated", generated_at],
        ["Product / SKU", str(product)],
        ["Scenario", str(scenario)],
        ["Review Status", str(review_status)]
    ]

    basic_table = Table(
        basic_data,
        colWidths=[
            55 * mm,
            115 * mm
        ]
    )

    basic_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(basic_table)

    story.append(Spacer(1, 12))

    # =====================================================
    # DEMAND ANALYSIS
    # =====================================================

    story.append(
        Paragraph(
            "<b>2. Demand Analysis</b>",
            styles["Heading2"]
        )
    )

    demand_data = [
        ["Metric", "Value"],

        [
            "Predicted Demand",
            f"{result['adjusted_demand']:.2f} units"
        ],

        [
            "Model Forecast",
            f"{demand.get('forecast', 0):.2f} units"
        ],

        [
            "MAE",
            f"{demand.get('mae', 0):.2f}"
        ],

        [
            "RMSE",
            f"{demand.get('rmse', 0):.2f}"
        ]
    ]

    demand_table = Table(
        demand_data,
        colWidths=[
            70 * mm,
            100 * mm
        ]
    )

    demand_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(demand_table)

    story.append(Spacer(1, 12))

    # =====================================================
    # INVENTORY ANALYSIS
    # =====================================================

    story.append(
        Paragraph(
            "<b>3. Inventory Analysis</b>",
            styles["Heading2"]
        )
    )

    inventory_data = [
        ["Metric", "Value"],

        [
            "Current Inventory",
            str(inventory["current_inventory"])
        ],

        [
            "Predicted Demand",
            str(inventory["predicted_demand"])
        ],

        [
            "Safety Stock",
            f"{inventory['safety_stock']:.2f}"
        ],

        [
            "Lead-Time Demand",
            f"{inventory['lead_time_demand']:.2f}"
        ],

        [
            "Reorder Point",
            f"{inventory['reorder_point']:.2f}"
        ],

        [
            "Stockout Risk",
            str(inventory["stockout_risk"])
        ],

        [
            "Recommended Order",
            f"{inventory['recommended_order']} units"
        ]
    ]

    inventory_table = Table(
        inventory_data,
        colWidths=[
            70 * mm,
            100 * mm
        ]
    )

    inventory_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(inventory_table)

    story.append(Spacer(1, 12))

    # =====================================================
    # SUPPLIER ANALYSIS
    # =====================================================

    story.append(
        Paragraph(
            "<b>4. Supplier Analysis</b>",
            styles["Heading2"]
        )
    )

    supplier_rows = [
        [
            "Supplier",
            "Unit Cost",
            "Lead Time",
            "Reliability",
            "Risk Score",
            "Risk"
        ]
    ]

    for item in result.get("suppliers", []):

        supplier_rows.append([
            str(item.get("supplier", "")),

            f"₹{item.get('unit_cost', 0):.2f}",

            f"{item.get('lead_time', 0)} days",

            f"{item.get('reliability', 0) * 100:.2f}%",

            f"{item.get('risk_score', 0):.2f}",

            str(item.get("risk_level", ""))
        ])

    if len(supplier_rows) > 1:

        supplier_table = Table(
            supplier_rows,
            repeatRows=1,
            colWidths=[
                27 * mm,
                27 * mm,
                25 * mm,
                30 * mm,
                28 * mm,
                25 * mm
            ]
        )

        supplier_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    4
                )
            ])
        )

        story.append(supplier_table)

    story.append(Spacer(1, 5))

    story.append(
        Paragraph(
            "Reliability is represented using the "
            "dataset-derived stockout-rate proxy.",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    # =====================================================
    # PROCUREMENT
    # =====================================================

    story.append(
        Paragraph(
            "<b>5. Procurement Recommendation</b>",
            styles["Heading2"]
        )
    )

    procurement_data = [
        ["Metric", "Value"],

        [
            "Decision",
            str(
                procurement.get(
                    "decision",
                    "N/A"
                )
            )
        ],

        [
            "Supplier",
            str(selected_supplier)
        ],

        [
            "Order Quantity",
            f"{order_quantity} units"
        ],

        [
            "Estimated Cost",
            f"₹{estimated_cost:,.2f}"
        ],

        [
            "Reason",
            str(
                procurement.get(
                    "reason",
                    "N/A"
                )
            )
        ]
    ]

    procurement_table = Table(
        procurement_data,
        colWidths=[
            70 * mm,
            100 * mm
        ]
    )

    procurement_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(procurement_table)

    story.append(Spacer(1, 12))

    # =====================================================
    # LLM EXPLANATION
    # =====================================================

    story.append(
        Paragraph(
            "<b>6. Llama 3.2 Explanation</b>",
            styles["Heading2"]
        )
    )

    explanation = (
        str(llm_explanation)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )

    story.append(
        Paragraph(
            explanation,
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 12))

    # =====================================================
    # RAG SOURCES
    # =====================================================

    story.append(
        Paragraph(
            "<b>7. RAG Knowledge Sources</b>",
            styles["Heading2"]
        )
    )

    if retrieved_documents:

        rag_data = [
            [
                "Knowledge Source",
                "Relevance Score"
            ]
        ]

        for document in retrieved_documents:

            rag_data.append([
                document["filename"],
                f"{document['score']:.3f}"
            ])

        rag_table = Table(
            rag_data,
            colWidths=[
                110 * mm,
                60 * mm
            ]
        )

        rag_table.setStyle(
            TableStyle([
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ])
        )

        story.append(rag_table)

    else:

        story.append(
            Paragraph(
                "No RAG knowledge sources were retrieved.",
                styles["Normal"]
            )
        )

    story.append(Spacer(1, 12))

    # =====================================================
    # HUMAN REVIEW
    # =====================================================

    story.append(
        Paragraph(
            "<b>8. Human Review</b>",
            styles["Heading2"]
        )
    )

    reviewer_comment = (
        reviewer_comment
        if reviewer_comment
        else "No comment provided."
    )

    reviewer_comment = (
        str(reviewer_comment)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )

    review_data = [
        [
            "Review Status",
            str(review_status)
        ],

        [
            "Reviewer Comment",
            reviewer_comment
        ]
    ]

    review_table = Table(
        review_data,
        colWidths=[
            55 * mm,
            115 * mm
        ]
    )

    review_table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),
            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(review_table)

    story.append(Spacer(1, 12))

    # =====================================================
    # RESPONSIBLE AI
    # =====================================================

    story.append(
        Paragraph(
            "<b>9. Responsible AI Notice</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "This is an academic decision-support simulation. "
            "The recommendation does not automatically execute "
            "a real procurement transaction. Human approval is "
            "required before any real-world action.",
            styles["Normal"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


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

    df = pd.read_csv(
        "data/raw/supply_chain_dataset1.csv"
    )

    if "Date" in df.columns:

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

    return df


data = load_data()


# =========================================================
# DATA VALIDATION
# =========================================================

required_columns = [
    "Date",
    "SKU_ID",
    "Warehouse_ID",
    "Supplier_ID",
    "Region",
    "Units_Sold",
    "Inventory_Level",
    "Supplier_Lead_Time_Days",
    "Reorder_Point",
    "Order_Quantity",
    "Unit_Cost",
    "Unit_Price",
    "Promotion_Flag",
    "Stockout_Flag",
    "Demand_Forecast"
]

missing_columns = [
    column
    for column in required_columns
    if column not in data.columns
]

if missing_columns:

    st.error(
        "The dataset is missing required columns:"
    )

    st.write(
        missing_columns
    )

    st.stop()


# =========================================================
# DATASET-DRIVEN SUPPLIERS
# =========================================================

supplier_summary = (
    data
    .groupby("Supplier_ID")
    .agg(
        unit_cost=("Unit_Cost", "mean"),
        lead_time=("Supplier_Lead_Time_Days", "mean"),
        stockout_rate=("Stockout_Flag", "mean")
    )
    .reset_index()
)


suppliers = {}


for _, row in supplier_summary.iterrows():

    supplier_id = str(
        row["Supplier_ID"]
    )

    reliability_proxy = (
        1 - float(
            row["stockout_rate"]
        )
    )

    suppliers[supplier_id] = {

        "unit_cost":
            float(
                row["unit_cost"]
            ),

        "lead_time":
            int(
                round(
                    row["lead_time"]
                )
            ),

        "reliability":
            reliability_proxy
    }


supplier_names = sorted(
    suppliers.keys()
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title(
        "⚙️ Simulation Control"
    )

    st.divider()

    product = st.selectbox(
        "📦 Select Product",
        sorted(
            data["SKU_ID"]
            .astype(str)
            .unique()
        )
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

    st.subheader(
        "🧠 AI Stack"
    )

    st.write(
        "🤖 Agents → Decision Logic"
    )

    st.write(
        "📈 ML → Demand Forecast"
    )

    st.write(
        "📚 RAG → Policy Retrieval"
    )

    st.write(
        "🧠 Llama 3.2 → Explanation"
    )

    st.write(
        "👤 Human → Final Review"
    )

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

st.title(
    "🚚 SupplyChain-Swarm"
)

st.subheader(
    "LLM-Powered Agentic AI Supply Chain "
    "Decision Support System"
)

st.write(
    "An intelligent multi-agent system for demand "
    "forecasting, inventory analysis, supplier risk "
    "evaluation, procurement recommendations, "
    "RAG-based knowledge retrieval, and local "
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
    data["SKU_ID"].astype(str)
    == str(product)
].copy()


product_data = product_data.sort_values(
    by="Date"
).reset_index(
    drop=True
)


# =========================================================
# SCENARIO SUPPLIER SELECTION
# =========================================================

delay_supplier = None

cost_supplier = None


if supplier_names:

    delay_supplier = min(
        supplier_names,
        key=lambda name:
            suppliers[name]["lead_time"]
    )

    cost_supplier = min(
        supplier_names,
        key=lambda name:
            suppliers[name]["unit_cost"]
    )


# =========================================================
# SCENARIO ENVIRONMENT
# =========================================================

environment = (
    SupplyChainEnvironment()
)


if scenario == "Demand Shock":

    environment.apply_demand_shock(
        40
    )


elif scenario == "Supplier Delay":

    if delay_supplier:

        environment.apply_supplier_delay(
            delay_supplier,
            5
        )


elif scenario == "Cost Increase":

    if cost_supplier:

        environment.apply_cost_increase(
            cost_supplier,
            20
        )


elif scenario == "Combined Crisis":

    environment.apply_demand_shock(
        40
    )

    if delay_supplier:

        environment.apply_supplier_delay(
            delay_supplier,
            5
        )

    if cost_supplier:

        environment.apply_cost_increase(
            cost_supplier,
            20
        )


# =========================================================
# RUN AGENTIC SYSTEM
# =========================================================

coordinator = (
    CoordinatorAgent()
)


try:

    result = coordinator.run(
        product_data,
        suppliers,
        environment
    )

    system_error = ""

except Exception as e:

    result = None

    system_error = str(e)


if result is None:

    st.error(
        "The Agentic AI system could not "
        "complete the simulation."
    )

    st.code(
        system_error
    )

    st.stop()


# =========================================================
# EXTRACT RESULTS
# =========================================================

inventory = (
    result["inventory"]
)

procurement = (
    result["procurement"]
)


selected_supplier = (
    procurement.get(
        "supplier",
        "N/A"
    )
)


order_quantity = (
    procurement.get(
        "quantity",
        0
    )
)


estimated_cost = (
    procurement.get(
        "estimated_cost",
        0
    )
)


# =========================================================
# LLM EXPLANATION
# =========================================================

try:

    llm_explanation = (
        explain_supply_chain(
            result
        )
    )

    llm_ok = True

    llm_error = ""

except Exception as e:

    llm_explanation = (
        "The local LLM could not generate "
        "an explanation. Please start Ollama "
        "and make sure llama3.2:3b is available."
    )

    llm_ok = False

    llm_error = str(e)


# =========================================================
# RAG QUERY
# =========================================================

rag_query = (
    f"Explain the supply chain decision for the "
    f"{scenario} scenario, including inventory risk, "
    f"supplier evaluation, procurement, and crisis management."
)


# =========================================================
# RAG RETRIEVAL
# =========================================================

try:

    retrieved_documents = (
        retrieve_documents(
            rag_query,
            top_k=2
        )
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
        (
            f"{delay_supplier} is experiencing "
            "a 5-day delivery delay."
        ),

    "Cost Increase":
        (
            f"{cost_supplier}'s cost has increased "
            "by 20%."
        ),

    "Combined Crisis":
        (
            f"Demand increased by 40%, "
            f"{delay_supplier} has a 5-day delay, "
            f"and {cost_supplier}'s cost increased "
            "by 20%."
        )
}


# =========================================================
# HUMAN REVIEW STATE
# =========================================================

review_key = (
    f"{product}|"
    f"{scenario}|"
    f"{result.get('adjusted_demand', 0)}|"
    f"{order_quantity}|"
    f"{selected_supplier}|"
    f"{estimated_cost}"
)


if (
    st.session_state.get(
        "review_key"
    )
    != review_key
):

    st.session_state.review_key = (
        review_key
    )

    st.session_state.review_status = (
        "Pending"
    )

    st.session_state.reviewer_comment = (
        ""
    )


review_status = (
    st.session_state.review_status
)

reviewer_comment = (
    st.session_state.reviewer_comment
)


# =========================================================
# CURRENT SCENARIO
# =========================================================

st.info(
    f"""
**Current Scenario:** {scenario}

**Product / SKU:** {product}

{scenario_descriptions[scenario]}
"""
)


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

st.header(
    "📊 Executive Overview"
)


col1, col2, col3, col4 = (
    st.columns(4)
)


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
        str(
            inventory["stockout_risk"]
        )
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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "📊 Overview",
        "🤖 AI Intelligence",
        "📦 Inventory",
        "🏭 Suppliers",
        "⚙️ System",
        "👤 Human Review & Report"
    ]
)


# =========================================================
# TAB 1 — OVERVIEW
# =========================================================

with tab1:

    st.subheader(
        "🔄 End-to-End AI Pipeline"
    )


    flow1, flow2, flow3 = (
        st.columns(3)
    )


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
lead time and reliability proxy.
"""
        )


    flow4, flow5, flow6 = (
        st.columns(3)
    )


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

            "Product / SKU",

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
        width="stretch",
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
            width="stretch",
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


    st.subheader(
        "🧠 RAG-Grounded AI Analysis"
    )


    try:

        rag_answer = (
            answer_with_rag(
                rag_query,
                result
            )
        )

        st.write(
            rag_answer
        )


    except Exception as e:

        st.warning(
            f"RAG response could not be generated: {e}"
        )


    st.divider()


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

• Supplier reliability is represented using a
dataset-derived stockout-rate proxy.

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
        width="stretch",
        hide_index=True
    )


    st.subheader(
        "📌 Inventory Indicators"
    )


    a, b, c = (
        st.columns(3)
    )


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

                "Reliability Proxy":
                    f"{item['reliability'] * 100:.2f}%",

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
        width="stretch",
        hide_index=True
    )


    st.caption(
        "Reliability Proxy = 1 − observed supplier stockout rate "
        "in the dataset. It is used as a risk-analysis proxy, "
        "not as a direct supplier reliability measurement."
    )


    st.subheader(
        "🎯 Procurement Decision"
    )


    a, b, c = (
        st.columns(3)
    )


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


    for supplier_name, supplier_data in (
        suppliers.items()
    ):

        cost = (
            supplier_data["unit_cost"]
        )

        lead_time = (
            supplier_data["lead_time"]
        )

        reliability = (
            supplier_data["reliability"]
        )


        decision_score = (

            cost

            + lead_time * 50

            + (1 - reliability) * 1000

        )


        score_rows.append({

            "Supplier":
                supplier_name,

            "Unit Cost":
                round(
                    cost,
                    2
                ),

            "Lead Time":
                lead_time,

            "Reliability Proxy":
                round(
                    reliability * 100,
                    2
                ),

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
        width="stretch",
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
            "reliability proxy and risk."
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

            "Random Forest demand forecasting",

            "Coordinates specialized supply-chain agents",

            "Llama 3.2 through Ollama",

            "Generates natural-language explanations",

            "Retrieves project-specific policy knowledge",

            "Runs Llama 3.2 locally",

            "Grounding, transparency and human review"

        ]

    })


    st.dataframe(
        component_df,
        width="stretch",
        hide_index=True
    )


    st.divider()


    st.subheader(
        "📊 Dataset Information"
    )


    dataset_info = pd.DataFrame({

        "Property": [

            "Dataset File",

            "Rows",

            "Columns",

            "Product Identifier",

            "Supplier Identifier",

            "Demand Column",

            "Inventory Column",

            "Lead Time Column"

        ],

        "Value": [

            "supply_chain_dataset1.csv",

            f"{len(data):,}",

            len(data.columns),

            "SKU_ID",

            "Supplier_ID",

            "Units_Sold",

            "Inventory_Level",

            "Supplier_Lead_Time_Days"

        ]

    })


    st.dataframe(
        dataset_info,
        width="stretch",
        hide_index=True
    )


    st.divider()


    st.subheader(
        "🟢 System Status"
    )


    status1, status2, status3 = (
        st.columns(3)
    )


    with status1:

        st.success(
            "Dataset Loaded"
        )


    with status2:

        if llm_ok:

            st.success(
                "Llama 3.2 Connected"
            )

        else:

            st.warning(
                "Llama 3.2 Unavailable"
            )


    with status3:

        if retrieved_documents:

            st.success(
                "RAG Knowledge Available"
            )

        else:

            st.warning(
                "RAG Knowledge Unavailable"
            )


    st.divider()


    st.caption(
        "SupplyChain-Swarm is an academic decision-support "
        "simulation. Recommendations are simulated and "
        "must be reviewed by a human before any real-world use."
    )


# =========================================================
# TAB 6 — HUMAN REVIEW & REPORT
# =========================================================

with tab6:

    st.subheader(
        "👤 Human Review"
    )

    st.write(
        "The AI recommendation must be reviewed by a human "
        "before the final report is released."
    )

    # =====================================================
    # RECOMMENDATION SUMMARY
    # =====================================================

    review_col1, review_col2, review_col3 = (
        st.columns(3)
    )


    with review_col1:

        st.metric(
            "Recommended Order",
            f"{order_quantity} units"
        )


    with review_col2:

        st.metric(
            "Supplier",
            str(selected_supplier)
        )


    with review_col3:

        st.metric(
            "Estimated Cost",
            f"₹{estimated_cost:,.2f}"
        )


    st.info(
        f"""
**Product / SKU:** {product}

**Scenario:** {scenario}

**Stockout Risk:** {inventory["stockout_risk"]}

**AI Decision:** {
    procurement.get(
        "decision",
        "N/A"
    )
}
"""
    )


    # =====================================================
    # REVIEW STATUS
    # =====================================================

    if review_status == "Pending":

        st.warning(
            "⏳ Review Status: PENDING"
        )

    elif review_status == "Approved":

        st.success(
            "✅ Review Status: APPROVED"
        )

    elif review_status == "Rejected":

        st.error(
            "❌ Review Status: REJECTED"
        )


    # =====================================================
    # REVIEWER COMMENT
    # =====================================================

    reviewer_comment_input = st.text_area(
        "📝 Reviewer Comment",
        value=reviewer_comment,
        placeholder=(
            "Enter a reason for approving or "
            "rejecting this recommendation."
        ),
        height=120
    )


    st.session_state.reviewer_comment = (
        reviewer_comment_input
    )


    # =====================================================
    # APPROVE / REJECT BUTTONS
    # =====================================================

    approve_col, reject_col = (
        st.columns(2)
    )


    with approve_col:

        if st.button(
            "✅ Approve Recommendation",
            type="primary",
            use_container_width=True
        ):

            st.session_state.review_status = (
                "Approved"
            )

            st.session_state.reviewer_comment = (
                reviewer_comment_input
            )

            st.rerun()


    with reject_col:

        if st.button(
            "❌ Reject Recommendation",
            use_container_width=True
        ):

            st.session_state.review_status = (
                "Rejected"
            )

            st.session_state.reviewer_comment = (
                reviewer_comment_input
            )

            st.rerun()


    # =====================================================
    # APPROVED → PDF
    # =====================================================

    if review_status == "Approved":

        st.divider()

        st.subheader(
            "📄 Approved Decision Report"
        )

        st.success(
            "The recommendation has been approved. "
            "The final PDF report is now available."
        )


        try:

            pdf_bytes = generate_pdf_report(

                result=result,

                product=product,

                scenario=scenario,

                selected_supplier=selected_supplier,

                order_quantity=order_quantity,

                estimated_cost=estimated_cost,

                llm_explanation=llm_explanation,

                retrieved_documents=retrieved_documents,

                review_status=review_status,

                reviewer_comment=reviewer_comment

            )


            filename = (
                f"SupplyChain_Report_"
                f"{product}_"
                f"{scenario.replace(' ', '_')}.pdf"
            )


            st.download_button(
                label="📥 Download Approved PDF Report",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True
            )


        except Exception as e:

            st.error(
                "PDF report could not be generated."
            )

            st.code(
                str(e)
            )

            st.info(
                "Make sure ReportLab is installed:"
                "\npip install reportlab"
            )


    # =====================================================
    # REJECTED
    # =====================================================

    elif review_status == "Rejected":

        st.divider()

        st.error(
            "❌ Recommendation rejected."
        )

        st.info(
            "The approved PDF report is not available "
            "because the recommendation was rejected."
        )


    # =====================================================
    # PENDING
    # =====================================================

    else:

        st.divider()

        st.info(
            "Approve the recommendation to unlock "
            "the final PDF report."
        )