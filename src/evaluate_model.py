import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

df = pd.read_csv("outputs/demand_forecasts.csv")

actual = df["Demand_Forecast"]
predicted = df["Predicted_Demand"]

mae = mean_absolute_error(actual, predicted)
rmse = np.sqrt(mean_squared_error(actual, predicted))

print("\n===== MODEL EVALUATION =====")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")

evaluation = pd.DataFrame({
    "Metric": ["MAE", "RMSE"],
    "Value": [mae, rmse]
})

evaluation.to_csv("outputs/model_evaluation.csv", index=False)

print("\nSaved: outputs/model_evaluation.csv")