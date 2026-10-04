import pandas as pd
import joblib

# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = "./data/raw/supply_chain_dataset1.csv"
MODEL_PATH = "./models/demand_forecasting_model.pkl"
OUTPUT_PATH = "./outputs/future_demand_forecast.csv"

df = pd.read_csv(DATA_PATH)

df["Date"] = pd.to_datetime(df["Date"])

# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(MODEL_PATH)

# ============================================================
# FEATURE ENGINEERING
# ============================================================

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df["DayOfWeek"] = df["Date"].dt.dayofweek
df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)

categorical_columns = [
    "SKU_ID",
    "Warehouse_ID",
    "Supplier_ID",
    "Region"
]

df_encoded = pd.get_dummies(
    df,
    columns=categorical_columns,
    dtype=int
)

# ============================================================
# MATCH MODEL FEATURES
# ============================================================

feature_columns = model.get_booster().feature_names

for column in feature_columns:

    if column not in df_encoded.columns:
        df_encoded[column] = 0

X = df_encoded[feature_columns]

# ============================================================
# GENERATE BASE FORECAST
# ============================================================

df["Predicted_Demand"] = model.predict(X)

# ============================================================
# FUTURE FORECAST
# ============================================================

last_date = df["Date"].max()

future_dates = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=30,
    freq="D"
)

latest_records = (
    df.sort_values("Date")
    .groupby(
        ["SKU_ID", "Warehouse_ID"],
        as_index=False
    )
    .tail(1)
)

future_rows = []

for _, row in latest_records.iterrows():

    for future_date in future_dates:

        future_rows.append(
            {
                "Date": future_date,
                "SKU_ID": row["SKU_ID"],
                "Warehouse_ID": row["Warehouse_ID"],
                "Supplier_ID": row["Supplier_ID"],
                "Region": row["Region"],
                "Inventory_Level": row["Inventory_Level"],
                "Supplier_Lead_Time_Days": row[
                    "Supplier_Lead_Time_Days"
                ],
                "Reorder_Point": row["Reorder_Point"],
                "Order_Quantity": row["Order_Quantity"],
                "Unit_Cost": row["Unit_Cost"],
                "Unit_Price": row["Unit_Price"],
                "Promotion_Flag": row["Promotion_Flag"],
                "Stockout_Flag": row["Stockout_Flag"],
                "Units_Sold": row["Units_Sold"]
            }
        )

future_df = pd.DataFrame(future_rows)

# ============================================================
# FUTURE FEATURES
# ============================================================

future_df["Year"] = future_df["Date"].dt.year
future_df["Month"] = future_df["Date"].dt.month
future_df["Day"] = future_df["Date"].dt.day
future_df["DayOfWeek"] = future_df["Date"].dt.dayofweek
future_df["WeekOfYear"] = (
    future_df["Date"]
    .dt.isocalendar()
    .week
    .astype(int)
)

future_encoded = pd.get_dummies(
    future_df,
    columns=categorical_columns,
    dtype=int
)

for column in feature_columns:

    if column not in future_encoded.columns:
        future_encoded[column] = 0

future_X = future_encoded[feature_columns]

# ============================================================
# PREDICTION
# ============================================================

future_df["Predicted_Demand"] = model.predict(
    future_X
)

future_df["Predicted_Demand"] = (
    future_df["Predicted_Demand"]
    .clip(lower=0)
)

# ============================================================
# SAVE
# ============================================================

future_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("=" * 60)
print("FUTURE DEMAND FORECAST")
print("=" * 60)
print(f"Last historical date : {last_date.date()}")
print(
    f"Forecast start       : "
    f"{future_dates.min().date()}"
)
print(
    f"Forecast end         : "
    f"{future_dates.max().date()}"
)
print(
    f"Forecast rows        : "
    f"{len(future_df):,}"
)
print(
    f"Average demand       : "
    f"{future_df['Predicted_Demand'].mean():.2f}"
)
print()
print(f"Saved: {OUTPUT_PATH}")