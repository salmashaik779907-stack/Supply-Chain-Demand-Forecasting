import pandas as pd

RAW_PATH = r".\data\raw\supply_chain_dataset1.csv"
FORECAST_PATH = r".\outputs\inventory_risk_analysis.csv"
OUTPUT_PATH = r".\outputs\supply_chain_summary.csv"

raw = pd.read_csv(RAW_PATH)
df = pd.read_csv(FORECAST_PATH)

summary = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Total SKUs",
        "Total Warehouses",
        "Total Suppliers",
        "Total Regions",
        "Average Predicted Demand",
        "Average Inventory Level",
        "Medium Risk Records",
        "High Risk Records",
        "Total Recommended Order"
    ],
    "Value": [
        len(df),
        raw["SKU_ID"].nunique(),
        raw["Warehouse_ID"].nunique(),
        raw["Supplier_ID"].nunique(),
        raw["Region"].nunique(),
        df["Predicted_Demand"].mean(),
        df["Inventory_Level"].mean(),
        (df["Stockout_Risk"] == "MEDIUM").sum(),
        (df["Stockout_Risk"] == "HIGH").sum(),
        df["Recommended_Order"].sum()
    ]
})

summary.to_csv(OUTPUT_PATH, index=False)

print("===== SUPPLY CHAIN SUMMARY =====")
print(summary.to_string(index=False))
print("\nSaved to:", OUTPUT_PATH)
