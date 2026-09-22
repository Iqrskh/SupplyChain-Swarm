# 🚚 SupplyChain-Swarm

### Multi-Agent Supply Chain Intelligence Platform

SupplyChain-Swarm is a Python-based multi-agent supply-chain simulation system that combines **machine-learning-based demand forecasting** with specialized agents for inventory analysis, supplier risk evaluation, and procurement decision-making.

The system can simulate different supply-chain conditions and generate explainable procurement recommendations through an interactive Streamlit dashboard.

---

## 📌 Project Overview

Modern supply chains face challenges such as:

- Uncertain customer demand
- Inventory shortages
- Excess inventory
- Supplier delays
- Changing supplier costs
- Supplier reliability and risk

SupplyChain-Swarm addresses these challenges using a **multi-agent architecture**, where each agent performs a specialized task and contributes to the final supply-chain decision.

---

## 🎯 Objectives

The main objectives of the project are:

- Forecast future product demand
- Analyze current inventory levels
- Calculate stockout risk
- Determine reorder requirements
- Evaluate supplier risk
- Select suitable suppliers
- Recommend procurement quantities
- Simulate supply-chain crisis scenarios
- Provide explainable decision-making through a dashboard

---

## 🤖 Multi-Agent Architecture

The system contains specialized agents:

### 📈 Demand Agent

Forecasts future demand using historical supply-chain data.

### 📦 Inventory Agent

Analyzes inventory levels, safety stock, lead-time demand, reorder points, and stockout risk.

### ⚠️ Supplier Risk Agent

Evaluates suppliers using factors such as:

- Unit cost
- Lead time
- Reliability
- Risk score

### 🛒 Procurement Agent

Uses supply-chain information to recommend:

- Supplier selection
- Order quantity
- Estimated procurement cost

### 🧠 Coordinator Agent

Coordinates the different agents and produces the final supply-chain decision.

---

## 🔄 System Workflow

```text
Historical Supply Chain Data
            ↓
       Demand Agent
            ↓
      Inventory Agent
            ↓
    Supplier Risk Agent
            ↓
     Procurement Agent
            ↓
     Coordinator Agent
            ↓
 Final Explainable Decision