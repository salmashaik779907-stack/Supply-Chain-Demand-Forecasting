import pandas as pd

DATA_PATH = r".\data\raw\supply_chain_dataset1.csv"

df = pd.read_csv(DATA_PATH)

print("===== SUPPLY CHAIN DATASET =====")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== TARGET SUMMARY =====")
print(df["Demand_Forecast"].describe())

print("\n===== UNIQUE VALUES =====")
for column in ["SKU_ID", "Warehouse_ID", "Supplier_ID", "Region"]:
    print(f"{column}: {df[column].nunique()}")

print("\n===== DATE RANGE =====")
print("Start:", df["Date"].min())
print("End:", df["Date"].max())

print("\nDataset inspection completed successfully!")
