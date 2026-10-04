import pandas as pd

DATA_PATH = r".\data\raw\supply_chain_dataset1.csv"
OUTPUT_PATH = r".\data\processed\processed_supply_chain.csv"

df = pd.read_csv(DATA_PATH)

df["Date"] = pd.to_datetime(df["Date"])

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df["DayOfWeek"] = df["Date"].dt.dayofweek
df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)

df = pd.get_dummies(
    df,
    columns=["SKU_ID", "Warehouse_ID", "Supplier_ID", "Region"],
    dtype=int
)

df.to_csv(OUTPUT_PATH, index=False)

print("Preprocessing completed!")
print("Shape:", df.shape)
print("Saved to:", OUTPUT_PATH)
