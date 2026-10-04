import pandas as pd
import joblib

DATA_PATH = r".\data\processed\processed_supply_chain.csv"
MODEL_PATH = r".\models\demand_forecasting_model.pkl"
OUTPUT_PATH = r".\outputs\demand_forecasts.csv"

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["Demand_Forecast", "Date"])

model = joblib.load(MODEL_PATH)

df["Predicted_Demand"] = model.predict(X)

df["Forecast_Error"] = (
    df["Demand_Forecast"] - df["Predicted_Demand"]
).abs()

df.to_csv(OUTPUT_PATH, index=False)

print("===== FORECAST GENERATED =====")
print("Rows:", len(df))
print("Average predicted demand:", df["Predicted_Demand"].mean())
print("Minimum predicted demand:", df["Predicted_Demand"].min())
print("Maximum predicted demand:", df["Predicted_Demand"].max())
print("Saved to:", OUTPUT_PATH)
