import pandas as pd

INPUT_PATH = r".\outputs\demand_forecasts.csv"
OUTPUT_PATH = r".\outputs\inventory_risk_analysis.csv"

df = pd.read_csv(INPUT_PATH)

df["Days_of_Inventory"] = (
    df["Inventory_Level"] /
    df["Predicted_Demand"].clip(lower=0.1)
)

df["Stockout_Risk"] = "LOW"

df.loc[df["Days_of_Inventory"] < 7, "Stockout_Risk"] = "MEDIUM"
df.loc[df["Days_of_Inventory"] < 3, "Stockout_Risk"] = "HIGH"

df["Recommended_Order"] = (
    df["Predicted_Demand"] *
    df["Supplier_Lead_Time_Days"]
    - df["Inventory_Level"]
).clip(lower=0)

df.to_csv(OUTPUT_PATH, index=False)

print("===== INVENTORY RISK ANALYSIS =====")
print("HIGH risk:", (df["Stockout_Risk"] == "HIGH").sum())
print("MEDIUM risk:", (df["Stockout_Risk"] == "MEDIUM").sum())
print("LOW risk:", (df["Stockout_Risk"] == "LOW").sum())
print("Average days of inventory:", df["Days_of_Inventory"].mean())
print("Total recommended order:", df["Recommended_Order"].sum())
print("Saved to:", OUTPUT_PATH)
