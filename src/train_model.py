import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor
import joblib
import numpy as np

DATA_PATH = r".\data\processed\processed_supply_chain.csv"
MODEL_PATH = r".\models\demand_forecasting_model.pkl"

df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["Demand_Forecast", "Date"])
y = df["Demand_Forecast"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = np.sqrt(mean_squared_error(y_test, predictions))

print("===== DEMAND FORECASTING MODEL =====")
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
print("MAE:", mae)
print("RMSE:", rmse)

joblib.dump(model, MODEL_PATH)

print("\nModel saved to:", MODEL_PATH)
