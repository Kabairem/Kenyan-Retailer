import os
import zipfile
import numpy as np
import pandas as pd

# Define paths
RAW_ZIP_PATH = "soko_fresh_csv.zip"
EXTRACT_DIR = "data/raw"
CLEAN_DIR = "data/processed"
REPORTS_DIR = "reports"

os.makedirs(EXTRACT_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# 1. Extract raw data if not already extracted
if os.path.exists(RAW_ZIP_PATH):
	with zipfile.ZipFile(RAW_ZIP_PATH, "r") as zip_ref:
		zip_ref.extractall(EXTRACT_DIR)
	print(f"Extracted {RAW_ZIP_PATH} to {EXTRACT_DIR}")

# Load raw datasets (adjust filenames to match your exact CSV headers inside the zip)
# Assuming typical names from your schema: orders.csv, order_items.csv, customers.csv, etc.
try:
	orders_df = pd.read_csv(os.path.join(EXTRACT_DIR, "orders.csv"))
	order_items_df = pd.read_csv(os.path.join(EXTRACT_DIR, "order_items.csv"))
	customers_df = pd.read_csv(os.path.join(EXTRACT_DIR, "customers.csv"))
	payments_df = pd.read_csv(os.path.join(EXTRACT_DIR, "payments.csv"))
except FileNotFoundError:
	# Fallback if files are extracted directly without subfolders
	orders_df = pd.read_csv("orders.csv")
	order_items_df = pd.read_csv("order_items.csv")
	customers_df = pd.read_csv("customers.csv")
	payments_df = pd.read_csv("payments.csv")

audit_logs = []


def profile_data(df, stage_name, table_name):
	"""Helper to record rows, duplicates, nulls, and outliers."""
	row_count = len(df)
	dup_count = df.duplicated().sum()
	null_counts = df.isnull().sum().to_dict()

	# Outlier detection on numeric columns if applicable (e.g. unit_price, quantity)
	outlier_counts = 0
	for col in ["unit_price", "quantity", "amount"]:
		if col in df.columns:
			Q1 = df[col].quantile(0.25)
			Q3 = df[col].quantile(0.75)
			IQR = Q3 - Q1
			lower_bound = Q1 - 1.5 * IQR
			upper_bound = Q3 + 1.5 * IQR
			outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
			outlier_counts += len(outliers)

	audit_logs.append(
		{
			"Table": table_name,
			"Stage": stage_name,
			"Total Rows": row_count,
			"Duplicates": dup_count,
			"Total Nulls": sum(null_counts.values()),
			"Outliers Flagged": outlier_counts,
		}
	)


# --- ORDERS CLEANING ---
profile_data(orders_df, "Before Cleaning", "orders")
orders_df = orders_df.drop_duplicates()
orders_df["order_date"] = pd.to_datetime(orders_df["order_date"], errors="coerce")
orders_df["delivery_fee"] = orders_df["delivery_fee"].fillna(0)
profile_data(orders_df, "After Cleaning", "orders")

# --- ORDER ITEMS CLEANING (Handling Outliers & Quantities) ---
profile_data(order_items_df, "Before Cleaning", "order_items")
order_items_df = order_items_df.drop_duplicates()

# Handle extreme price/quantity outliers using IQR clipping or dropping
for col in ["unit_price", "quantity"]:
	if col in order_items_df.columns:
		Q1 = order_items_df[col].quantile(0.25)
		Q3 = order_items_df[col].quantile(0.75)
		IQR = Q3 - Q1
		lower = Q1 - 1.5 * IQR
		upper = Q3 + 1.5 * IQR
		# Cap extreme values to realistic bounds to preserve data integrity
		order_items_df[col] = np.clip(order_items_df[col], lower, upper)

order_items_df["discount_applied"] = order_items_df["discount_applied"].fillna(0)
# Engineer Net Line Revenue
if "unit_price" in order_items_df.columns and "quantity" in order_items_df.columns:
	order_items_df["net_line_revenue"] = (
		order_items_df["unit_price"]
		* order_items_df["quantity"]
		* (1 - order_items_df["discount_applied"])
	)

profile_data(order_items_df, "After Cleaning", "order_items")

# --- CUSTOMERS & PAYMENTS CLEANING ---
profile_data(customers_df, "Before Cleaning", "customers")
customers_df = customers_df.drop_duplicates()
customers_df["loyalty_tier"] = customers_df["loyalty_tier"].fillna("Bronze")
profile_data(customers_df, "After Cleaning", "customers")

profile_data(payments_df, "Before Cleaning", "payments")
payments_df = payments_df.drop_duplicates()
payments_df["payment_method"] = payments_df["payment_method"].str.strip().str.title()
profile_data(payments_df, "After Cleaning", "payments")

# Save cleaned files
orders_df.to_csv(os.path.join(CLEAN_DIR, "orders_clean.csv"), index=False)
order_items_df.to_csv(os.path.join(CLEAN_DIR, "order_items_clean.csv"), index=False)
customers_df.to_csv(os.path.join(CLEAN_DIR, "customers_clean.csv"), index=False)
payments_df.to_csv(os.path.join(CLEAN_DIR, "payments_clean.csv"), index=False)

# Export Audit Table to reports/
audit_df = pd.DataFrame(audit_logs)
audit_report_path = os.path.join(REPORTS_DIR, "data_cleaning_audit.csv")
audit_df.to_csv(audit_report_path, index=False)

print(f"Data cleaning complete! Audit report saved to {audit_report_path}")
