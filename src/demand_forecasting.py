import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error

# Define directories
PROCESSED_DIR = "data/processed"
REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# 1. Load cleaned order items and orders
order_items = pd.read_csv(os.path.join(PROCESSED_DIR, "order_items_clean.csv"))
orders = pd.read_csv(os.path.join(PROCESSED_DIR, "orders_clean.csv"))

df = order_items.merge(orders, on="order_id", how="inner")
df["order_date"] = pd.to_datetime(df["order_date"])
df["year_month"] = df["order_date"].dt.to_period("M")

# Aggregate actual monthly revenue / demand
monthly_demand = df.groupby("year_month")["net_line_revenue"].sum().reset_index()
monthly_demand["ds"] = monthly_demand["year_month"].dt.to_timestamp()
monthly_demand["y"] = monthly_demand["net_line_revenue"]

# 2. Split into Train (2025) and Validation (2026)
train = monthly_demand[monthly_demand["ds"].dt.year == 2025].copy()
val = monthly_demand[monthly_demand["ds"].dt.year == 2026].copy()

# 3. Baselines & Model Predictions
# Baseline 1: Flat Historical Mean (Previous Benchmark)
flat_mean_pred = [train["y"].mean()] * len(val)

# Baseline 2: Seasonal Naive (same month last year)
seasonal_naive_pred = train[train["ds"].dt.month.isin(val["ds"].dt.month)][
	"y"
].values
if len(seasonal_naive_pred) < len(val):
	seasonal_naive_pred = np.resize(seasonal_naive_pred, len(val))

# Fit a trend and apply monthly seasonal multipliers.
X_train = np.arange(len(train))
y_train = train["y"].values
slope, intercept = np.polyfit(X_train, y_train, 1)

X_val = np.arange(len(train), len(train) + len(val))
base_trend_pred = intercept + slope * X_val

train["month"] = train["ds"].dt.month
monthly_factors = (train.groupby("month")["y"].mean() / train["y"].mean()).to_dict()
model_pred = [
	base_trend_pred[i] * monthly_factors.get(month, 1.0)
	for i, month in enumerate(val["ds"].dt.month)
]

val["baseline_pred"] = seasonal_naive_pred
val["model_pred"] = model_pred

# 4. Evaluate metrics (RMSE and MAPE)
def evaluate(actual, predicted):
	rmse = root_mean_squared_error(actual, predicted)
	mape = mean_absolute_percentage_error(actual, predicted) * 100
	return rmse, mape


base_rmse, base_mape = evaluate(val["y"], val["baseline_pred"])
model_rmse, model_mape = evaluate(val["y"], val["model_pred"])

# Save metrics report table
metrics_df = pd.DataFrame(
	{
		"Model / Strategy": [
			"Baseline (Seasonal Naive - Last Year Same Month)",
			"Advanced Trend + Seasonal Model",
		],
		"RMSE (KES)": [round(base_rmse, 2), round(model_rmse, 2)],
		"MAPE (%)": [round(base_mape, 2), round(model_mape, 2)],
	}
)
metrics_df.to_csv(os.path.join(REPORTS_DIR, "forecasting_metrics.csv"), index=False)
print("Evaluation Metrics:")
print(metrics_df)

# 5. Generate actual vs predicted validation chart
plt.figure(figsize=(10, 5))
plt.plot(
	val["ds"],
	val["y"],
	marker="o",
	color="black",
	linewidth=2,
	label="Actual Demand (2026)",
)
plt.plot(
	val["ds"],
	val["baseline_pred"],
	marker="s",
	linestyle="--",
	color="gray",
	label="Seasonal Naive Baseline",
)
plt.plot(
	val["ds"],
	val["model_pred"],
	marker="^",
	linestyle="-",
	color="#2b5c8f",
	linewidth=2,
	label="Proposed Trend + Seasonal Model",
)

plt.title(
	"2026 Demand Validation: Actual vs. Predicted Monthly Revenue",
	fontsize=12,
	fontweight="bold",
)
plt.xlabel("Validation Month (2026)")
plt.ylabel("Total Revenue (KES)")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(REPORTS_DIR, "actual_vs_predicted_2026.png"))
plt.show()
