import pandas as pd

INPUT_PATH = "./outputs/inventory_optimization.csv"
OUTPUT_PATH = "./outputs/what_if_simulation.csv"

df = pd.read_csv(INPUT_PATH)

scenarios = []

for demand_change in [-20, -10, 0, 10, 20]:
    for lead_time_change in [-2, 0, 2]:

        scenario = df.copy()

        scenario["Scenario_Demand"] = (
            scenario["Average_Daily_Demand"]
            * (1 + demand_change / 100)
        )

        scenario["Scenario_Lead_Time"] = (
            scenario["Supplier_Lead_Time_Days"]
            + lead_time_change
        ).clip(lower=1)

        scenario["Scenario_Lead_Time_Demand"] = (
            scenario["Scenario_Demand"]
            * scenario["Scenario_Lead_Time"]
        )

        scenario["Scenario_Reorder_Point"] = (
            scenario["Scenario_Lead_Time_Demand"]
            + scenario["Safety_Stock"]
        )

        scenario["Scenario_Inventory_Gap"] = (
            scenario["Scenario_Reorder_Point"]
            - scenario["Inventory_Level"]
        )

        scenario["Scenario_Order"] = (
            scenario["Scenario_Inventory_Gap"]
            .clip(lower=0)
        )

        scenario["Demand_Change_Percent"] = demand_change
        scenario["Lead_Time_Change_Days"] = lead_time_change

        scenarios.append(
            scenario[
                [
                    "SKU_ID",
                    "Warehouse_ID",
                    "Demand_Change_Percent",
                    "Lead_Time_Change_Days",
                    "Scenario_Demand",
                    "Scenario_Lead_Time",
                    "Scenario_Reorder_Point",
                    "Scenario_Inventory_Gap",
                    "Scenario_Order"
                ]
            ]
        )

result = pd.concat(
    scenarios,
    ignore_index=True
)

numeric_columns = [
    "Scenario_Demand",
    "Scenario_Lead_Time",
    "Scenario_Reorder_Point",
    "Scenario_Inventory_Gap",
    "Scenario_Order"
]

result[numeric_columns] = (
    result[numeric_columns].round(2)
)

result.to_csv(
    OUTPUT_PATH,
    index=False
)

print("=" * 60)
print("WHAT-IF INVENTORY SIMULATION")
print("=" * 60)

print(
    f"Scenarios generated : "
    f"{result[['Demand_Change_Percent', 'Lead_Time_Change_Days']].drop_duplicates().shape[0]}"
)

print(
    f"Simulation rows     : "
    f"{len(result):,}"
)

print(
    f"Maximum demand case : "
    f"{result['Scenario_Demand'].max():.2f}"
)

print(
    f"Maximum order need  : "
    f"{result['Scenario_Order'].max():.2f}"
)

print()
print(f"Saved: {OUTPUT_PATH}")