import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SupplyTrack",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# COLOR SYSTEM
# ============================================================

BG = "#07111f"
SIDEBAR = "#0b1728"
PANEL = "#0d1d30"
TEXT = "#e8f1f8"
MUTED = "#91a7b8"

CYAN = "#62d9ff"
ORANGE = "#ffb347"
GREEN = "#7ee081"
RED = "#ff6b6b"
PURPLE = "#b084ff"
YELLOW = "#f7d154"

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    forecast = pd.read_csv(
        "./outputs/inventory_risk_analysis.csv"
    )

    raw = pd.read_csv(
        "./data/raw/supply_chain_dataset1.csv"
    )

    raw["Date"] = pd.to_datetime(raw["Date"])
    forecast["Date"] = pd.to_datetime(forecast["Date"])

    identifiers = raw[
        [
            "Date",
            "SKU_ID",
            "Warehouse_ID",
            "Supplier_ID",
            "Region"
        ]
    ].copy()

    df = forecast.copy()

    for column in [
        "SKU_ID",
        "Warehouse_ID",
        "Supplier_ID",
        "Region"
    ]:

        if column not in df.columns:
            df[column] = identifiers[column].values

    return df, raw


try:

    df, raw = load_data()

except Exception as e:

    st.error("Unable to load project data.")
    st.code(str(e))
    st.stop()

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {BG};
        color: {TEXT};
    }}

    section[data-testid="stSidebar"] {{
        background-color: {SIDEBAR};
        border-right: 1px solid #19314a;
    }}

    section[data-testid="stSidebar"] * {{
        color: {TEXT};
    }}

    .main-title {{
        font-size: 38px;
        font-weight: 800;
        letter-spacing: 2px;
        color: {TEXT};
        margin-bottom: 0;
    }}

    .subtitle {{
        color: {MUTED};
        font-size: 15px;
        margin-top: 3px;
        margin-bottom: 25px;
    }}

    .metric-card {{
        background: {PANEL};
        border: 1px solid #19314a;
        border-radius: 12px;
        padding: 18px;
        min-height: 115px;
    }}

    .metric-label {{
        color: {MUTED};
        font-size: 13px;
        margin-bottom: 8px;
    }}

    .metric-value {{
        color: {CYAN};
        font-size: 28px;
        font-weight: 750;
    }}

    .section-title {{
        color: {TEXT};
        font-size: 20px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 10px;
    }}

    .status-box {{
        background: {PANEL};
        border: 1px solid #19314a;
        border-radius: 10px;
        padding: 12px 16px;
    }}

    .status-online {{
        color: {GREEN};
        font-weight: 600;
    }}

    .status-label {{
        color: {MUTED};
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📦 SUPPLYTRACK</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Supply Chain Demand Forecasting & Inventory Management</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## CONTROL PANEL")

st.sidebar.markdown("### Filters")

regions = ["All"] + sorted(
    df["Region"].dropna().astype(str).unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "Region",
    regions
)

warehouses = ["All"] + sorted(
    df["Warehouse_ID"].dropna().astype(str).unique().tolist()
)

selected_warehouse = st.sidebar.selectbox(
    "Warehouse",
    warehouses
)

skus = ["All"] + sorted(
    df["SKU_ID"].dropna().astype(str).unique().tolist()
)

selected_sku = st.sidebar.selectbox(
    "SKU",
    skus
)

# ============================================================
# FILTER DATA
# ============================================================

filtered = df.copy()

if selected_region != "All":

    filtered = filtered[
        filtered["Region"].astype(str) == selected_region
    ]

if selected_warehouse != "All":

    filtered = filtered[
        filtered["Warehouse_ID"].astype(str) == selected_warehouse
    ]

if selected_sku != "All":

    filtered = filtered[
        filtered["SKU_ID"].astype(str) == selected_sku
    ]

# ============================================================
# KPI CALCULATIONS
# ============================================================

active_skus = filtered["SKU_ID"].nunique()

forecast_demand = filtered["Predicted_Demand"].sum()

inventory = filtered["Inventory_Level"].sum()

risk_records = filtered[
    filtered["Stockout_Risk"].isin(
        ["MEDIUM", "HIGH"]
    )
].shape[0]

reorder_units = filtered["Recommended_Order"].sum()

# ============================================================
# NETWORK SNAPSHOT
# ============================================================

st.markdown(
    '<div class="section-title">Network Snapshot</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">ACTIVE SKUs</div>
            <div class="metric-value">{active_skus:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">FORECAST DEMAND</div>
            <div class="metric-value">{forecast_demand:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">INVENTORY UNITS</div>
            <div class="metric-value">{inventory:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">RISK RECORDS</div>
            <div class="metric-value">{risk_records:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c5:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">REORDER UNITS</div>
            <div class="metric-value">{reorder_units:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# DEMAND SIGNAL
# ============================================================

st.markdown(
    '<div class="section-title">Demand Signal</div>',
    unsafe_allow_html=True
)

demand_chart = (
    filtered
    .groupby("Date", as_index=False)
    .agg(
        Actual_Demand=("Demand_Forecast", "mean"),
        Predicted_Demand=("Predicted_Demand", "mean")
    )
    .sort_values("Date")
)

fig_demand = px.line(
    demand_chart,
    x="Date",
    y=[
        "Actual_Demand",
        "Predicted_Demand"
    ],
    title="Actual vs Predicted Demand",
    color_discrete_map={
        "Actual_Demand": CYAN,
        "Predicted_Demand": ORANGE
    }
)

fig_demand.update_layout(
    paper_bgcolor=PANEL,
    plot_bgcolor=PANEL,
    font_color=TEXT,
    legend_title_text="",
    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    ),
    hovermode="x unified"
)

fig_demand.update_xaxes(
    showgrid=False,
    color=MUTED
)

fig_demand.update_yaxes(
    showgrid=True,
    gridcolor="#19314a",
    color=MUTED
)

st.plotly_chart(
    fig_demand,
    use_container_width=True
)

# ============================================================
# WAREHOUSE LOAD
# ============================================================

st.markdown(
    '<div class="section-title">Warehouse Load</div>',
    unsafe_allow_html=True
)

warehouse_data = (
    filtered
    .groupby("Warehouse_ID", as_index=False)
    .agg(
        Forecast_Demand=(
            "Predicted_Demand",
            "sum"
        ),
        Inventory_Level=(
            "Inventory_Level",
            "sum"
        )
    )
)

fig_warehouse = px.bar(
    warehouse_data,
    x="Warehouse_ID",
    y=[
        "Forecast_Demand",
        "Inventory_Level"
    ],
    barmode="group",
    title="Demand vs Inventory by Warehouse",
    color_discrete_map={
        "Forecast_Demand": CYAN,
        "Inventory_Level": ORANGE
    }
)

fig_warehouse.update_layout(
    paper_bgcolor=PANEL,
    plot_bgcolor=PANEL,
    font_color=TEXT,
    legend_title_text="",
    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    )
)

fig_warehouse.update_xaxes(
    showgrid=False,
    color=MUTED
)

fig_warehouse.update_yaxes(
    showgrid=True,
    gridcolor="#19314a",
    color=MUTED
)

st.plotly_chart(
    fig_warehouse,
    use_container_width=True
)

# ============================================================
# REGIONAL DEMAND
# ============================================================

st.markdown(
    '<div class="section-title">Regional Demand</div>',
    unsafe_allow_html=True
)

region_data = (
    filtered
    .groupby("Region", as_index=False)
    .agg(
        Predicted_Demand=(
            "Predicted_Demand",
            "sum"
        )
    )
    .sort_values(
        "Predicted_Demand",
        ascending=False
    )
)

fig_region = px.bar(
    region_data,
    x="Region",
    y="Predicted_Demand",
    title="Forecast Demand by Region",
    color_discrete_sequence=[
        GREEN
    ]
)

fig_region.update_layout(
    paper_bgcolor=PANEL,
    plot_bgcolor=PANEL,
    font_color=TEXT,
    showlegend=False,
    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    )
)

fig_region.update_xaxes(
    showgrid=False,
    color=MUTED
)

fig_region.update_yaxes(
    showgrid=True,
    gridcolor="#19314a",
    color=MUTED
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)

# ============================================================
# INVENTORY RISK MONITOR
# ============================================================

st.markdown(
    '<div class="section-title">Inventory Risk Monitor</div>',
    unsafe_allow_html=True
)

risk_data = (
    filtered
    .groupby("Stockout_Risk")
    .size()
    .reset_index(
        name="Count"
    )
)

risk_order = [
    "LOW",
    "MEDIUM",
    "HIGH"
]

risk_data["Stockout_Risk"] = pd.Categorical(
    risk_data["Stockout_Risk"],
    categories=risk_order,
    ordered=True
)

risk_data = risk_data.sort_values(
    "Stockout_Risk"
)

fig_risk = px.bar(
    risk_data,
    x="Stockout_Risk",
    y="Count",
    title="Inventory Risk Distribution",
    color="Stockout_Risk",
    color_discrete_map={
        "LOW": GREEN,
        "MEDIUM": ORANGE,
        "HIGH": RED
    }
)

fig_risk.update_layout(
    paper_bgcolor=PANEL,
    plot_bgcolor=PANEL,
    font_color=TEXT,
    showlegend=False,
    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    )
)

fig_risk.update_xaxes(
    showgrid=False,
    color=MUTED
)

fig_risk.update_yaxes(
    showgrid=True,
    gridcolor="#19314a",
    color=MUTED
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)

# ============================================================
# MODEL PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">Forecast Model Performance</div>',
    unsafe_allow_html=True
)

try:

    evaluation = pd.read_csv(
        "./outputs/model_evaluation.csv"
    )

    mae = float(
        evaluation.loc[
            evaluation["Metric"] == "MAE",
            "Value"
        ].iloc[0]
    )

    rmse = float(
        evaluation.loc[
            evaluation["Metric"] == "RMSE",
            "Value"
        ].iloc[0]
    )

    m1, m2 = st.columns(2)

    with m1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">MAE</div>
                <div class="metric-value">{mae:.4f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">RMSE</div>
                <div class="metric-value">{rmse:.4f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

except Exception as e:

    st.warning(
        "Model evaluation file could not be loaded."
    )

# ============================================================
# REPLENISHMENT WATCHLIST
# ============================================================

st.markdown(
    '<div class="section-title">Replenishment Watchlist</div>',
    unsafe_allow_html=True
)

watchlist = (
    filtered[
        filtered["Recommended_Order"] > 0
    ]
    .sort_values(
        "Recommended_Order",
        ascending=False
    )
    [
        [
            "SKU_ID",
            "Warehouse_ID",
            "Region",
            "Predicted_Demand",
            "Inventory_Level",
            "Supplier_Lead_Time_Days",
            "Recommended_Order",
            "Stockout_Risk"
        ]
    ]
    .head(15)
)

st.dataframe(
    watchlist,
    width="stretch",
    hide_index=True
)

# ============================================================
# SYSTEM STATUS
# ============================================================

st.markdown(
    '<div class="section-title">System Status</div>',
    unsafe_allow_html=True
)

s1, s2, s3 = st.columns(3)

with s1:

    st.markdown(
        f"""
        <div class="status-box">
            <span class="status-label">
                Forecast Engine
            </span>
            <br>
            <span class="status-online">
                ● ONLINE
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

with s2:

    st.markdown(
        f"""
        <div class="status-box">
            <span class="status-label">
                Inventory Monitor
            </span>
            <br>
            <span class="status-online">
                ● ONLINE
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

with s3:

    st.markdown(
        f"""
        <div class="status-box">
            <span class="status-label">
                Replenishment Engine
            </span>
            <br>
            <span class="status-online">
                ● ONLINE
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br>
    <center>
        <span style="color:#5f7487;">
            SupplyTrack • Demand Forecasting & Inventory Management
        </span>
    </center>
    """,
    unsafe_allow_html=True
)
