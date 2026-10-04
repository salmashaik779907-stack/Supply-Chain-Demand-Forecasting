import pandas as pd

INPUT_PATH = "./outputs/future_demand_forecast.csv"

df = pd.read_csv(INPUT_PATH)

# SKU-level analysis
sku_analysis = (
    df.groupby("SKU_ID")
    .agg(
        Average_Demand=("Predicted_Demand", "mean"),
        Peak_Demand=("Predicted_Demand", "max"),
        Total_Forecast_Demand=("Predicted_Demand", "sum")
    )
    .reset_index()
    .sort_values(
        "Total_Forecast_Demand",
        ascending=False
    )
)

sku_analysis.to_csv(
    "./outputs/sku_demand_analysis.csv",
    index=False
)

# Warehouse-level analysis
warehouse_analysis = (
    df.groupby("Warehouse_ID")
    .agg(
        Average_Demand=("Predicted_Demand", "mean"),
        Peak_Demand=("Predicted_Demand", "max"),
        Total_Forecast_Demand=("Predicted_Demand", "sum")
    )
    .reset_index()
    .sort_values(
        "Total_Forecast_Demand",
        ascending=False
    )
)

warehouse_analysis.to_csv(
    "./outputs/warehouse_demand_analysis.csv",
    index=False
)

print("=" * 60)
print("SKU + WAREHOUSE DEMAND ANALYSIS")
print("=" * 60)

print(f"SKUs analysed       : {len(sku_analysis)}")
print(f"Warehouses analysed : {len(warehouse_analysis)}")

print()
print("TOP 5 SKUs")
print(
    sku_analysis.head(5).to_string(index=False)
)

print()
print("WAREHOUSE SUMMARY")
print(
    warehouse_analysis.to_string(index=False)
)

print()
print("Saved:")
print("./outputs/sku_demand_analysis.csv")
print("./outputs/warehouse_demand_analysis.csv")