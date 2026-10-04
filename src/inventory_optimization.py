import pandas as pd
import numpy as np

INPUT_PATH = "./outputs/future_demand_forecast.csv"
OUTPUT_PATH = "./outputs/inventory_optimization.csv"

# ============================================================
# LOAD FUTURE FORECAST
# ============================================================

df = pd.read_csv(INPUT_PATH)

df["Date"] = pd.to_datetime(df["Date"])

# ============================================================
# DEMAND STATISTICS
# ============================================================

group_cols = [
    "SKU_ID",
    "Warehouse_ID"
]

stats = (
    df.groupby(group_cols)
    .agg(
        Average_Daily_Demand=(
            "Predicted_Demand",
            "mean"
        ),
        Demand_Std=(
            "Predicted_Demand",
            "std"
        ),
        Supplier_Lead_Time_Days=(
            "Supplier_Lead_Time_Days",
            "first"
        ),
        Inventory_Level=(
            "Inventory_Level",
            "first"
        )
    )
    .reset_index()
)

stats["Demand_Std"] = stats["Demand_Std"].fillna(0)

# ============================================================
# SAFETY STOCK
# ============================================================

SERVICE_Z = 1.65

stats["Safety_Stock"] = (
    SERVICE_Z
    * stats["Demand_Std"]
    * np.sqrt(
        stats["Supplier_Lead_Time_Days"]
    )
)

# ============================================================
# REORDER POINT
# ============================================================

stats["Lead_Time_Demand"] = (
    stats["Average_Daily_Demand"]
    * stats["Supplier_Lead_Time_Days"]
)

stats["Optimized_Reorder_Point"] = (
    stats["Lead_Time_Demand"]
    + stats["Safety_Stock"]
)

# ============================================================
# INVENTORY GAP
# ============================================================

stats["Inventory_Gap"] = (
    stats["Optimized_Reorder_Point"]
    - stats["Inventory_Level"]
)

stats["Recommended_Order"] = (
    stats["Inventory_Gap"]
    .clip(lower=0)
)

# ============================================================
# INVENTORY STATUS
# ============================================================

stats["Inventory_Status"] = "ADEQUATE"

stats.loc[
    stats["Inventory_Gap"] > 0,
    "Inventory_Status"
] = "REORDER"

stats.loc[
    stats["Inventory_Level"]
    < stats["Safety_Stock"],
    "Inventory_Status"
] = "CRITICAL"

# ============================================================
# ROUND VALUES
# ============================================================

numeric_columns = [
    "Average_Daily_Demand",
    "Demand_Std",
    "Safety_Stock",
    "Lead_Time_Demand",
    "Optimized_Reorder_Point",
    "Inventory_Level",
    "Inventory_Gap",
    "Recommended_Order"
]

stats[numeric_columns] = (
    stats[numeric_columns]
    .round(2)
)

# ============================================================
# SAVE
# ============================================================

stats.to_csv(
    OUTPUT_PATH,
    index=False
)

print("=" * 60)
print("INVENTORY OPTIMIZATION")
print("=" * 60)

print(
    f"SKU-Warehouse combinations : {len(stats):,}"
)

print(
    f"Critical combinations      : "
    f"{(stats['Inventory_Status'] == 'CRITICAL').sum():,}"
)

print(
    f"Reorder combinations       : "
    f"{(stats['Inventory_Status'] == 'REORDER').sum():,}"
)

print(
    f"Adequate combinations      : "
    f"{(stats['Inventory_Status'] == 'ADEQUATE').sum():,}"
)

print(
    f"Total safety stock         : "
    f"{stats['Safety_Stock'].sum():,.2f}"
)

print(
    f"Total recommended order    : "
    f"{stats['Recommended_Order'].sum():,.2f}"
)

print()
print(f"Saved: {OUTPUT_PATH}")