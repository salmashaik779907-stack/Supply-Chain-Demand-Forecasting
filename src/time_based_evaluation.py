import pandas as pd
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

DATA_PATH = "./data/processed/processed_supply_chain.csv"
MODEL_PATH = "./models/demand_forecasting_model.pkl"
OUTPUT_PATH = "./outputs/time_based_evaluation.csv"

df = pd.read_csv(DATA_PATH)

df["Date"] = pd.to_datetime(df["Date"])

df = df.sort_values("Date").reset_index(drop=True)

X = df.drop(
    columns=["Demand_Forecast", "Date"]
)

y = df["Demand_Forecast"]

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

model = joblib.load(MODEL_PATH)

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)

results = pd.DataFrame({
    "Metric": [
        "Time-Based MAE",
        "Time-Based RMSE"
    ],
    "Value": [
        mae,
        rmse
    ]
})

results.to_csv(
    OUTPUT_PATH,
    index=False
)

print("=" * 60)
print("TIME-BASED MODEL EVALUATION")
print("=" * 60)

print(
    f"Training rows : {len(X_train):,}"
)

print(
    f"Testing rows  : {len(X_test):,}"
)

print(
    f"Test start    : "
    f"{df['Date'].iloc[split_index].date()}"
)

print(
    f"MAE           : {mae:.4f}"
)

print(
    f"RMSE          : {rmse:.4f}"
)

print()
print(f"Saved: {OUTPUT_PATH}")