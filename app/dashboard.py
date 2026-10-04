import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SupplyTrack Control Tower",
    page_icon="📦",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    risk = pd.read_csv(
        "./outputs/inventory_risk_analysis.csv"
    )

    forecast = pd.read_csv(
        "./outputs/future_demand_forecast.csv"
    )

    optimization = pd.read_csv(
        "./outputs/inventory_optimization.csv"
    )

    stock_analysis = pd.read_csv(
        "./outputs/stockout_overstock_analysis.csv"
    )

    sku = pd.read_csv(
        "./outputs/sku_demand_analysis.csv"
    )

    warehouse = pd.read_csv(
        "./outputs/warehouse_demand_analysis.csv"
    )

    what_if = pd.read_csv(
        "./outputs/what_if_simulation.csv"
    )

    evaluation = pd.read_csv(
        "./outputs/time_based_evaluation.csv"
    )

    raw = pd.read_csv(
        "./data/raw/supply_chain_dataset1.csv"
    )

    risk["Date"] = pd.to_datetime(risk["Date"])

    forecast["Date"] = pd.to_datetime(
        forecast["Date"]
    )

    return (
        risk,
        forecast,
        optimization,
        stock_analysis,
        sku,
        warehouse,
        what_if,
        evaluation,
        raw
    )


(
    risk,
    forecast,
    optimization,
    stock_analysis,
    sku,
    warehouse,
    what_if,
    evaluation,
    raw
) = load_data()

# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #07111f;
        color: #e8f1f8;
    }

    section[data-testid="stSidebar"] {
        background-color: #0b1728;
    }

    .tower {
        background-color: #0d1d30;
        padding: 24px;
        border: 1px solid #183550;
        border-radius: 12px;
        margin-bottom: 20px;
    }

    .tower-title {
        font-size: 30px;
        font-weight: 700;
        color: #62d9ff;
    }

    .tower-subtitle {
        color: #8da6bb;
        font-size: 14px;
    }

    .section-title {
        font-size: 21px;
        font-weight: 600;
        color: #e8f1f8;
        margin-top: 25px;
    }

    .status {
        padding: 12px;
        background-color: #0d1d30;
        border-left: 4px solid #62d9ff;
        border-radius: 6px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="tower">
        <div class="tower-title">
            SUPPLYTRACK
        </div>

        <div class="tower-subtitle">
            Supply Chain Demand Forecasting & Inventory Management
        </div>

        <br>

        <div>
            CONTROL TOWER / NETWORK OPERATIONS
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("CONTROL TOWER")

regions = ["All"] + sorted(
    raw["Region"].unique().tolist()
)

warehouses = ["All"] + sorted(
    raw["Warehouse_ID"].unique().tolist()
)

skus = ["All"] + sorted(
    raw["SKU_ID"].unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "Region",
    regions
)

selected_warehouse = st.sidebar.selectbox(
    "Warehouse",
    warehouses
)

selected_sku = st.sidebar.selectbox(
    "SKU",
    skus
)

# ============================================================
# FILTER FORECAST DATA
# ============================================================

filtered = forecast.copy()

if selected_region != "All":
    filtered = filtered[
        filtered["Region"] == selected_region
    ]

if selected_warehouse != "All":
    filtered = filtered[
        filtered["Warehouse_ID"]
        == selected_warehouse
    ]

if selected_sku != "All":
    filtered = filtered[
        filtered["SKU_ID"]
        == selected_sku
    ]

# ============================================================
# KPI ROW
# ============================================================

total_demand = filtered[
    "Predicted_Demand"
].sum()

avg_inventory = filtered[
    "Inventory_Level"
].mean()

risk_count = len(
    stock_analysis[
        stock_analysis["Inventory_Status"]
        != "OPTIMAL"
    ]
)

reorder_units = optimization[
    "Recommended_Order"
].sum()

active_skus = filtered[
    "SKU_ID"
].nunique()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "ACTIVE SKUs",
    f"{active_skus:,}"
)

c2.metric(
    "FORECAST DEMAND",
    f"{total_demand:,.0f}"
)

c3.metric(
    "AVG INVENTORY",
    f"{avg_inventory:,.0f}"
)

c4.metric(
    "RISK RECORDS",
    f"{risk_count:,}"
)

c5.metric(
    "REORDER UNITS",
    f"{reorder_units:,.0f}"
)

# ============================================================
# DEMAND SIGNAL
# ============================================================

st.markdown(
    '<div class="section-title">DEMAND SIGNAL</div>',
    unsafe_allow_html=True
)

daily = (
    filtered
    .groupby("Date")["Predicted_Demand"]
    .sum()
    .reset_index()
)

fig = px.line(
    daily,
    x="Date",
    y="Predicted_Demand",
    template="plotly_dark",
    title="Forecast Demand Timeline"
)

fig.update_layout(
    paper_bgcolor="#07111f",
    plot_bgcolor="#0d1d30"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# NETWORK VIEW
# ============================================================

st.markdown(
    '<div class="section-title">NETWORK VIEW</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:

    warehouse_chart = (
        filtered
        .groupby("Warehouse_ID")
        ["Predicted_Demand"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        warehouse_chart,
        x="Warehouse_ID",
        y="Predicted_Demand",
        template="plotly_dark",
        title="Warehouse Demand Load"
    )

    fig.update_layout(
        paper_bgcolor="#07111f",
        plot_bgcolor="#0d1d30"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    region_chart = (
        filtered
        .groupby("Region")
        ["Predicted_Demand"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        region_chart,
        x="Region",
        y="Predicted_Demand",
        template="plotly_dark",
        title="Regional Demand"
    )

    fig.update_layout(
        paper_bgcolor="#07111f",
        plot_bgcolor="#0d1d30"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# INVENTORY CONTROL
# ============================================================

st.markdown(
    '<div class="section-title">INVENTORY CONTROL</div>',
    unsafe_allow_html=True
)

left, right = st.columns(2)

with left:

    status_chart = (
        stock_analysis
        ["Inventory_Status"]
        .value_counts()
        .reset_index()
    )

    status_chart.columns = [
        "Status",
        "Count"
    ]

    fig = px.bar(
        status_chart,
        x="Status",
        y="Count",
        template="plotly_dark",
        title="Inventory Status"
    )

    fig.update_layout(
        paper_bgcolor="#07111f",
        plot_bgcolor="#0d1d30"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    risk_chart = (
        risk["Stockout_Risk"]
        .value_counts()
        .reset_index()
    )

    risk_chart.columns = [
        "Risk",
        "Count"
    ]

    fig = px.bar(
        risk_chart,
        x="Risk",
        y="Count",
        template="plotly_dark",
        title="Inventory Risk Monitor"
    )

    fig.update_layout(
        paper_bgcolor="#07111f",
        plot_bgcolor="#0d1d30"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ============================================================
# SKU ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">SKU DEMAND ANALYSIS</div>',
    unsafe_allow_html=True
)

st.dataframe(
    sku.head(15),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# REPLENISHMENT WATCHLIST
# ============================================================

st.markdown(
    '<div class="section-title">REPLENISHMENT WATCHLIST</div>',
    unsafe_allow_html=True
)

watchlist = optimization[
    optimization["Recommended_Order"] > 0
].sort_values(
    "Recommended_Order",
    ascending=False
)

st.dataframe(
    watchlist.head(15),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# WHAT-IF SIMULATION
# ============================================================

st.markdown(
    '<div class="section-title">WHAT-IF SIMULATION</div>',
    unsafe_allow_html=True
)

demand_change = st.slider(
    "Demand Change (%)",
    min_value=-20,
    max_value=20,
    value=0,
    step=10
)

lead_change = st.slider(
    "Lead Time Change (Days)",
    min_value=-2,
    max_value=2,
    value=0,
    step=1
)

scenario = what_if[
    (what_if["Demand_Change_Percent"]
     == demand_change)
    &
    (what_if["Lead_Time_Change_Days"]
     == lead_change)
]

if not scenario.empty:

    st.metric(
        "Scenario Order Requirement",
        f"{scenario['Scenario_Order'].sum():,.0f}"
    )

    st.metric(
        "Scenario Reorder Point",
        f"{scenario['Scenario_Reorder_Point'].mean():,.2f}"
    )

# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">FORECAST MODEL PERFORMANCE</div>',
    unsafe_allow_html=True
)

m1, m2 = st.columns(2)

mae = evaluation.loc[
    evaluation["Metric"]
    == "Time-Based MAE",
    "Value"
].iloc[0]

rmse = evaluation.loc[
    evaluation["Metric"]
    == "Time-Based RMSE",
    "Value"
].iloc[0]

m1.metric(
    "TIME-BASED MAE",
    f"{mae:.4f}"
)

m2.metric(
    "TIME-BASED RMSE",
    f"{rmse:.4f}"
)

# ============================================================
# SYSTEM STATUS
# ============================================================

st.markdown(
    '<div class="section-title">SYSTEM STATUS</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="status">
        ● FORECAST ENGINE — ONLINE
    </div>

    <div class="status">
        ● INVENTORY OPTIMIZATION — ONLINE
    </div>

    <div class="status">
        ● REPLENISHMENT ENGINE — ONLINE
    </div>

    <div class="status">
        ● WHAT-IF SIMULATION — ONLINE
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "SupplyTrack | Supply Chain Control Tower"
)