import pandas as pd

INPUT_PATH = "./outputs/inventory_optimization.csv"
FORECAST_PATH = "./outputs/future_demand_forecast.csv"
OUTPUT_PATH = "./outputs/stockout_overstock_analysis.csv"

inventory = pd.read_csv(INPUT_PATH)
forecast = pd.read_csv(FORECAST_PATH)

demand = (
    forecast
    .groupby(["SKU_ID", "Warehouse_ID"])
    .agg(
        Forecast_Average_Demand=("Predicted_Demand", "mean"),
        Forecast_Peak_Demand=("Predicted_Demand", "max")
    )
    .reset_index()
)

df = inventory.merge(
    demand,
    on=["SKU_ID", "Warehouse_ID"],
    how="left"
)

df["Days_of_Cover"] = (
    df["Inventory_Level"]
    / df["Forecast_Average_Demand"].clip(lower=0.1)
)

df["Demand_Gap"] = (
    df["Forecast_Peak_Demand"]
    - df["Inventory_Level"]
)

df["Inventory_Status"] = "OPTIMAL"

df.loc[
    df["Days_of_Cover"] < 3,
    "Inventory_Status"
] = "STOCKOUT_RISK"

df.loc[
    df["Days_of_Cover"] > 30,
    "Inventory_Status"
] = "OVERSTOCK"

df.loc[
    (df["Days_of_Cover"] >= 3)
    & (df["Days_of_Cover"] <= 7),
    "Inventory_Status"
] = "LOW_STOCK"

df["Potential_Stockout"] = (
    df["Inventory_Level"]
    < df["Forecast_Peak_Demand"]
)

df["Excess_Inventory"] = (
    df["Inventory_Level"]
    - df["Optimized_Reorder_Point"]
).clip(lower=0)

numeric_columns = [
    "Forecast_Average_Demand",
    "Forecast_Peak_Demand",
    "Days_of_Cover",
    "Demand_Gap",
    "Excess_Inventory"
]

df[numeric_columns] = df[numeric_columns].round(2)

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("=" * 60)
print("STOCKOUT + OVERSTOCK ANALYSIS")
print("=" * 60)

print(f"Total SKU-Warehouse combinations : {len(df):,}")
print(
    f"Stockout risk                    : "
    f"{(df['Inventory_Status'] == 'STOCKOUT_RISK').sum():,}"
)
print(
    f"Low stock                        : "
    f"{(df['Inventory_Status'] == 'LOW_STOCK').sum():,}"
)
print(
    f"Overstock                        : "
    f"{(df['Inventory_Status'] == 'OVERSTOCK').sum():,}"
)
print(
    f"Optimal inventory                : "
    f"{(df['Inventory_Status'] == 'OPTIMAL').sum():,}"
)
print(
    f"Potential stockouts              : "
    f"{df['Potential_Stockout'].sum():,}"
)
print(
    f"Excess inventory units           : "
    f"{df['Excess_Inventory'].sum():,.2f}"
)

print()
print(f"Saved: {OUTPUT_PATH}")