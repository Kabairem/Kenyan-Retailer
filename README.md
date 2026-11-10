## Repository Structure
# CAPSTONE PROJECT

## Kenyan-Retailer - Comprehensive Milestones README

**Dataset:** `soko_fresh_csv.zip` 
**Role:** Business Intelligence / Data Analyst  
**Author:** Anthony Kariuki (Cohort 7)  
**Project GitHub Repository:** [Kenyan-Retailer Repository](https://github.com/Kabairem/Kenyan-Retailer.git)

---

## Executive Summary

This repository contains a complete, end-to-end Data Science and Analytics solution for a growing Kenyan retail chain operating multiple branches across counties. The project integrates transactional logs, customer demographics, outlet performance metrics, payment channels (M-Pesa, Cash, Card), and macroeconomic indicators to deliver actionable business intelligence, relational database management, statistical hypothesis testing, and predictive demand forecasting.

---

## Data fies
├── customers.csv          # Customer demographic data & loyalty tiers

├── employees.csv          # Employee and management hierarchy data

├── outlets.csv            # Retail branch master data (location, region, county)

├── outlet_targets.csv     # Quarterly branch revenue targets

├── products.csv           # Product catalog, categories, and cost/unit pricing

├── suppliers.csv          # Supplier master records

├── orders.csv             # Transaction header records (dates, status, channels)

├── order_items.csv        # Transaction line items (quantities, prices, discounts)

├── payments.csv           # Payment transactions (M-Pesa references, methods, amounts)

├── data_cleaning.py       # Python pandas script for data hygiene and feature engineering

├── statistical_analysis.py# Hypothesis testing (Welch's t-tests for promotions & payments)

├── demand_forecasting.py  # Time-aware demand forecasting model (RMSE & MAPE evaluation)

└── README.md              # Project documentation and reproduction instructions


---

## Summary of the Eight Capstone Milestones

### 1. Problem Framing and Data Acquisition
* **Business Objectives:** Investigated sales drivers, seasonal trends, customer segmentation (churn risk), promotional effectiveness, and inventory demand forecasting.
* **Success Metrics:** Total Net Revenue, Average Order Value (AOV), M-Pesa adoption rate, RMSE, and MAPE.
* **Data Sources:** Transactional retail CSVs combined with macroeconomic contextual indicators from the Kenya National Bureau of Statistics (KNBS).

### 2. Data Cleaning and Preparation (`pandas`)
* **Data Hygiene:** Handled missing values (imputing delivery fees and discounts with 0, and unassigned loyalty tiers with Bronze), standardized timestamps, and normalized text formatting.
* **Feature Engineering:** Calculated net line-item revenue (`quantity * unit_price * (1 - discount_pct / 100)`).

### 3. Exploratory Data Analysis (EDA) & Key Findings
* **Category Dominance:** *Fresh Produce* and *Dairy* account for over 50% of total retail revenue.
* **Seasonality:** Pronounced sales surges aligned with end-of-month salary cycles and December holiday shopping.
* **Payment Preferences:** Mobile money via **M-Pesa** accounts for over 75% of customer transactions.

### 4. SQL Analytics & Relational Modeling (`PostgreSQL`)
* **Relational Schema:** Enforced primary and foreign key constraints across master and transactional tables.
* **Advanced Queries:** Implemented multi-table joins, window functions (`LAG()`) for month-over-month growth rates, and RFM (Recency, Frequency, Monetary) scoring via `NTILE()` window partitions to classify customer churn risk.

### 5. Statistical Analysis & Hypothesis Testing (`scipy.stats`)
* **Promotional Impact:** Welch's t-test confirmed that promotional discounts yield a statistically significant positive uplift in basket size ($p < 0.05$, mean revenue KES 1,190 vs. KES 821).
* **Payment Methods:** Evaluated spending behavior across M-Pesa and Cash, verifying parity in individual transaction values.

### 6. Predictive Model (Demand Forecasting)
* **Time-Aware Split:** Chronologically split data (training on 2025, validating on 2026) to prevent data leakage.
* **Evaluation:** Compared a historical mean baseline against a trend-extrapolation model using RMSE and MAPE metrics.

### 7. Dashboard and Storytelling (`Power BI`)
* **Executive Overview:** 3-page interactive report tracking total revenue (**KES 29.58M**), AOV (**KES 986.02**), branch target attainment, and customer loyalty tiers.

### 8. Documentation & Reproducibility
* **Repository:** Fully reproducible GitHub repository hosted at [Kenyan-Retailer Repository](https://github.com/Kabairem/Kenyan-Retailer.git).

---

## Getting Started & Reproduction Instructions

### Prerequisites
* Python 3.9+ with `pandas`, `numpy`, `scipy`, and `scikit-learn` installed.
* PostgreSQL (for SQL relational analytics).
* Power BI Desktop (for dashboard visualization).

### Steps
Step 1: Clone the Repository
git clone [https://github.com/Kabairem/Kenyan-Retailer.git](https://github.com/Kabairem/Kenyan-Retailer.git)
cd Kenyan-Retailer

Step 2: Run Data Cleaning Pipeline
python data_cleaning.py

Step 3: Run Statistical Hypothesis Tests
python statistical_analysis.py

Step 4: Run Demand Forecasting Model
python demand_forecasting.py

## DETAILED MILESTEPS

## Milestone 1: Problem Framing and Data Acquisition

### Business Problem & Objectives
The retailer lacked a unified, data-driven view of operations across its branch network. This capstone establishes an integrated pipeline to answer four strategic business questions:

1. Sales Drivers & Seasonality: Which products, branches, and payment methods drive sales and seasonal trends?

2. Customer Segmentation: Who are the high-value customers, and which segments show signs of churn?

3. Promotional Effectiveness: Do promotional campaigns (such as discounts) have a statistically significant impact on sales?

4. Demand Forecasting: What is the projected product demand for upcoming months to optimize inventory management across branches?
   
### Key Performance Indicators (KPIs) & Success Metrics
1. Financial & Sales Metrics: Total Revenue, Average Order Value (AOV), Profit Margins, and Payment Transaction Adoption Rates (e.g., M-Pesa adoption).

2. Customer Metrics: Customer Purchase Rate, Churn Rate, and Loyalty Tier Distribution.

3. Model Performance Metrics: Root Mean Squared Error (RMSE) and Mean Absolute Percentage Error (MAPE) for demand forecasting models.

### Data Inventory & Sources
1. Data Inventory & Sources
Primary Dataset (orders.csv, order_items.csv, customers.csv, products.csv, outlets.csv, payments.csv, suppliers.csv, outlet_targets.csv, employees.csv): A simulated 12-to-18-month transactional dataset reflecting Kenyan retail operations.

2. Contextual Dataset: Public Kenyan macroeconomic indicators (such as Kenya National Bureau of Statistics [KNBS] Consumer Price Index [CPI] and inflation rates).
   

## Milestone 2: Data Cleaning and Preparation
To clean the data I used the below scripts to handle missing values, standardize data types and text formats (such as standardizing payment methods like M-Pesa), remove anomalies, and generate essential features like net line-item revenue.

### 1. Python Data Cleaning Pipeline (data_cleaning.py)
import pandas as pd
import numpy as np

def clean_and_prepare_data():
    print("Starting Data Cleaning Pipeline...")

    # Load raw datasets
    customers = pd.read_csv('customers.csv')
    employees = pd.read_csv('employees.csv')
    order_items = pd.read_csv('order_items.csv')
    orders = pd.read_csv('orders.csv')
    outlet_targets = pd.read_csv('outlet_targets.csv')
    outlets = pd.read_csv('outlets.csv')
    payments = pd.read_csv('payments.csv')
    products = pd.read_csv('products.csv')
    suppliers = pd.read_csv('suppliers.csv')

    # 1. Clean Orders
    # Convert date columns to datetime
    orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
    orders['delivered_at'] = pd.to_datetime(orders['delivered_at'], errors='coerce')
    
    # Impute missing delivery fees with median or 0 where appropriate
    orders['delivery_fee'] = orders['delivery_fee'].fillna(0.0)
    
    # Standardize categorical columns
    orders['status'] = orders['status'].str.strip().str.title()
    orders['channel'] = orders['channel'].str.strip().str.title()

    # 2. Clean Order Items & Calculate Revenue Features
    order_items['discount_pct'] = order_items['discount_pct'].fillna(0.0)
    # Calculate net line item revenue
    order_items['net_revenue'] = (
        order_items['quantity'] * order_items['unit_price'] * (1 - order_items['discount_pct'] / 100.0)
    )

    # 3. Clean Payments
    payments['paid_at'] = pd.to_datetime(payments['paid_at'], errors='coerce')
    # Standardize payment method names
    payments['payment_method'] = (
        payments['payment_method']
        .str.strip()
        .str.title()
        .replace({'M-Pesa': 'M-Pesa', 'Card': 'Card', 'Cash': 'Cash', 'Refund': 'Refund'})
    )

    # 4. Clean Customers & Products
    customers['signup_date'] = pd.to_datetime(customers['signup_date'], errors='coerce')
    customers['loyalty_tier'] = customers['loyalty_tier'].fillna('Bronze').str.strip().str.title()

    products['is_active'] = products['is_active'].fillna(True).astype(bool)
    products['cost_price'] = products['cost_price'].fillna(products['unit_price'] * 0.7) # fallback imputation

    # 5. Merge and export cleaned datasets
    print("Data cleaning complete. Exporting processed files...")
    
    # Save cleaned outputs if needed for downstream modeling
    orders.to_csv('cleaned_orders.csv', index=False)
    order_items.to_csv('cleaned_order_items.csv', index=False)
    payments.to_csv('cleaned_payments.csv', index=False)
    
    print("All preprocessing steps executed successfully!")

if __name__ == '__main__':
    clean_and_prepare_data()

### PostgreSQL Data Ingestion & Cleaning Script (schema_and_clean.sql)
-- =====================================================
-- KENYAN RETAILER CAPSTONE: DATABASE SCHEMA & CLEANING
-- =====================================================

-- Drop tables if re-running script
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS outlets CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS employees CASCADE;

-- 1. Create Dimension & Master Tables
CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(255),
    supplier_type VARCHAR(100),
    county VARCHAR(100),
    contact_email VARCHAR(255)
);

CREATE TABLE outlets (
    outlet_id INT PRIMARY KEY,
    outlet_name VARCHAR(255),
    outlet_type VARCHAR(100),
    county VARCHAR(100),
    region VARCHAR(100),
    town VARCHAR(100),
    opened_on DATE
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    full_name VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255),
    county VARCHAR(100),
    signup_date DATE,
    referred_by INT,
    loyalty_tier VARCHAR(50)
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    supplier_id INT REFERENCES suppliers(supplier_id),
    unit_price NUMERIC(10,2),
    cost_price NUMERIC(10,2),
    is_active BOOLEAN
);

-- 2. Create Transactional Tables
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    outlet_id INT REFERENCES outlets(outlet_id),
    rider_id INT,
    order_date TIMESTAMP,
    status VARCHAR(50),
    channel VARCHAR(50),
    delivery_fee NUMERIC(10,2),
    delivered_at TIMESTAMP
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    unit_price NUMERIC(10,2),
    discount_pct NUMERIC(5,2)
);

CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    payment_method VARCHAR(50),
    amount NUMERIC(10,2),
    paid_at TIMESTAMP,
    mpesa_ref VARCHAR(100)
);

-- =====================================================
-- DATA CLEANING & STANDARDIZATION QUERIES
-- =====================================================

-- Standardize payment methods (fixing casing inconsistencies for M-Pesa, Cash, Card)
UPDATE payments
SET payment_method = INITCAP(TRIM(payment_method));

-- Handle missing delivery fees by defaulting to 0
UPDATE orders
SET delivery_fee = 0.00
WHERE delivery_fee IS NULL;

-- Standardize loyalty tiers
UPDATE customers
SET loyalty_tier = INITCAP(TRIM(loyalty_tier))
WHERE loyalty_tier IS NOT NULL;

-- View to compute clean net revenue per order item
CREATE OR REPLACE VIEW vw_order_item_revenues AS
- Select order_id, product_id, quantity, unit_price, discount_pct,
       (quantity * unit_price * (1 - COALESCE(discount_pct, 0) / 100.0)) AS net_revenue
FROM order_items;


## Milestone 3: Exploratory Data Analysis - EDA.
### Exploratory Data Analysis & Key Findings Report
#### 1.Distributions & Sales Breakdown by Product Category
Observation: Revenue is heavily concentrated in daily essentials and grocery items. Fresh Produce is the top-performing category, generating over KES 9.53M in net revenue, followed by Dairy (KES 5.28M), Cooking Essentials (KES 2.61M), and Cereals & Grains (KES 2.52M).

Insight: Staple food items drive foot traffic and basket sizes across all outlets, making inventory stability in fresh produce and dairy critical to overall branch profitability.

#### 2.Temporal Trends & Seasonality
Observation: Transaction volumes and revenue exhibit pronounced upward growth and cyclical monthly peaks. Sales spike significantly at the end of each calendar year, peaking sharply in December 2025 (KES 2.49M) and continuing strong growth through mid-2026, reaching KES 3.29M in June 2026.

Insight: Seasonality strongly correlates with end-of-month salary disbursement cycles in Kenya and holiday shopping periods, requiring dynamic staffing and inventory pre-positioning ahead of peak days.

#### 3.Regional & County Differences
Observation: Performance varies significantly across counties and urban centers. Nairobi and its surrounding metropolitan zones (including Kiambu and Nakuru) capture the highest aggregate sales, driven by high-density urban branches (Soko Fresh Kilimani and Syokimau).

Insight: Urban stores excel in high-frequency convenience transactions, whereas peri-urban and regional supermarkets (such as Sagana and Gilgil) boast higher average basket sizes per transaction.

#### 4.Customer Segmentation (Loyalty Tiers)
Observation: The customer base is segmented into Bronze, Silver, and Gold loyalty tiers. Bronze tier customers generate the largest share of total transaction volume (KES 15.43M), followed by Silver (KES 7.75M) and Gold (KES 3.40M).

Insight: While Bronze members form the high-volume base of daily shoppers, Silver and Gold customers exhibit higher lifetime value and frequency, representing prime targets for retention campaigns to mitigate churn risk.

## The Five Findings That Matter Most
1. Category Dominance: Fresh Produce and Dairy account for over 50% of total retail revenue, indicating that supply chain disruptions in these two categories pose an immediate risk to store turnover.

2. End-of-Month & Holiday Surges: Sales volume surges by up to 80% during end-of-month cycles and December festive periods, necessitating proactive rostering and working capital allocation.

3. M-Pesa Dominance & Payment Preferences: Mobile money via M-Pesa is the primary payment engine, accounting for over 75% of customer settlements, confirming that system uptime for mobile payments is non-negotiable.

4. Urban vs. Peri-Urban Dynamics: High-density metropolitan branches drive transaction frequency, while regional branches in Mt. Kenya and Rift Valley deliver higher average order values.

5. Loyalty Retention Opportunity: A large proportion of revenue comes from Bronze-tier shoppers, highlighting an opportunity to design targeted upselling and loyalty incentives to transition them into Silver and Gold tiers.
   

  ## Milestone 4: SQL Analytics & RFM Script (sql_analytics_queries.sql) 
  -- =====================================================
    KENYAN RETAILER CAPSTONE: MILESTONE 4 SQL ANALYTICS
-- =====================================================
-- 1. STORE & CATEGORY PERFORMANCE (JOINS & AGGREGATIONS)
-- Calculates total net revenue and order count by outlet and product category
SELECT 
    o.outlet_name,
    o.county,
    p.category,
    SUM(oi.quantity * oi.unit_price * (1 - COALESCE(oi.discount_pct, 0) / 100.0)) AS total_net_revenue,
    COUNT(DISTINCT ord.order_id) AS total_orders
FROM order_items oi
JOIN orders ord ON oi.order_id = ord.order_id
JOIN outlets o ON ord.outlet_id = o.outlet_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY o.outlet_name, o.county, p.category
ORDER BY total_net_revenue DESC;


-- 2. MONTHLY SALES GROWTH & WINDOW FUNCTIONS
-- Computes monthly revenue and uses LAG() to calculate month-over-month growth rate
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', ord.order_date) AS sales_month,
        SUM(oi.quantity * oi.unit_price * (1 - COALESCE(oi.discount_pct, 0) / 100.0)) AS monthly_revenue
    FROM order_items oi
    JOIN orders ord ON oi.order_id = ord.order_id
    GROUP BY DATE_TRUNC('month', ord.order_date)
)
SELECT 
    TO_CHAR(sales_month, 'YYYY-MM') AS month_str,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(LAG(monthly_revenue, 1) OVER (ORDER BY sales_month), 2) AS prev_month_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY sales_month)) 
        / NULLIF(LAG(monthly_revenue, 1) OVER (ORDER BY sales_month), 0) * 100, 2
    ) AS mom_growth_pct
FROM monthly_sales
ORDER BY sales_month;


-- 3. CUSTOMER RFM (RECENCY, FREQUENCY, MONETARY) SEGMENTATION
-- Uses window functions and aggregates to score customers for targeted retention
WITH customer_rfm AS (
    SELECT 
        c.customer_id,
        c.full_name,
        -- Recency: Days since last order relative to dataset max date (2026-06-30)
        DATE_PART('day', TIMESTAMP '2026-06-30 23:59:59' - MAX(ord.order_date)) AS recency_days,
        -- Frequency: Total distinct orders placed
        COUNT(DISTINCT ord.order_id) AS frequency,
        -- Monetary: Total net spend
        SUM(oi.quantity * oi.unit_price * (1 - COALESCE(oi.discount_pct, 0) / 100.0)) AS monetary_value
    FROM customers c
    JOIN orders ord ON c.customer_id = ord.customer_id
    JOIN order_items oi ON ord.order_id = oi.order_id
    GROUP BY c.customer_id, c.full_name
),
rfm_scored AS (
    SELECT 
        customer_id,
        full_name,
        recency_days,
        frequency,
        monetary_value,
        NTILE(5) OVER (ORDER BY recency_days ASC) AS r_score, -- Lower days = better (reverse score or keep raw)
        NTILE(5) OVER (ORDER BY frequency DESC) AS f_score,
        NTILE(5) OVER (ORDER BY monetary_value DESC) AS m_score
    FROM customer_rfm
)
SELECT 
    customer_id,
    full_name,
    recency_days,
    frequency,
    ROUND(monetary_value, 2) AS monetary_value,
    (r_score + f_score + m_score) AS total_rfm_score,
    CASE 
        WHEN (r_score + f_score + m_score) >= 12 THEN 'Champions (Gold Tier)'
        WHEN (r_score + f_score + m_score) >= 8 THEN 'Loyal / Potential (Silver Tier)'
        ELSE 'At-Risk / Churning (Bronze Tier)'
    END AS customer_segment
FROM rfm_scored
ORDER BY total_rfm_score DESC;


## Milestone 5: Statistical Analysis & Hypothesis Testing Script (statistical_analysis.py)
import pandas as pd
import numpy as np
from scipy import stats

def run_statistical_tests():
    print("==================================================")
    print("KENYAN RETAILER CAPSTONE: STATISTICAL ANALYSIS")
    print("==================================================\n")

    # Load data
    orders = pd.read_csv('orders.csv')
    order_items = pd.read_csv('order_items.csv')
    payments = pd.read_csv('payments.csv')

    # ==========================================================
    # HYPOTHESIS 1: Promotional Impact on Basket Size (Revenue)
    # Null Hypothesis (H0): Mean order revenue for discounted orders equals non-discounted orders.
    # Alternate Hypothesis (Ha): Mean order revenue for discounted orders is significantly different.
    # ==========================================================
    order_items['line_revenue'] = (
        order_items['quantity'] * order_items['unit_price'] * (1 - order_items['discount_pct'].fillna(0) / 100.0)
    )
    order_totals = order_items.groupby('order_id').agg(
        total_revenue=('line_revenue', 'sum'),
        has_discount=('discount_pct', lambda x: (x > 0).any())
    ).reset_index()

    discounted = order_totals[order_totals['has_discount']]['total_revenue']
    non_discounted = order_totals[~order_totals['has_discount']]['total_revenue']

    t_stat_1, p_val_1 = stats.ttest_ind(discounted, non_discounted, equal_var=False)

    print("--- HYPOTHESIS 1: Promotional Discounts Impact ---")
    print(f"Mean Revenue (Discounted Orders): KES {discounted.mean():.2f}")
    print(f"Mean Revenue (Non-Discounted Orders): KES {non_discounted.mean():.2f}")
    print(f"Welch's t-test statistic: {t_stat_1:.4f}")
    print(f"p-value: {p_val_1:.4e}")
    if p_val_1 < 0.05:
        print("Conclusion: Reject H0. Discounts have a statistically significant positive impact on order basket size.\n")
    else:
        print("Conclusion: Fail to reject H0.\n")

    # ==========================================================
    # HYPOTHESIS 2: M-Pesa vs. Cash Spending Comparison
    # Null Hypothesis (H0): Mean transaction amounts for M-Pesa and Cash are equal.
    # Alternate Hypothesis (Ha): Mean transaction amounts differ significantly.
    # ==========================================================
    order_payments = payments.merge(orders, on='order_id', how='inner')
    order_payments['payment_method_clean'] = order_payments['payment_method'].str.strip().str.title()

    mpesa_amounts = order_payments[order_payments['payment_method_clean'] == 'M-Pesa']['amount']
    cash_amounts = order_payments[order_payments['payment_method_clean'] == 'Cash']['amount']

    t_stat_2, p_val_2 = stats.ttest_ind(mpesa_amounts, cash_amounts, equal_var=False)

    print("--- HYPOTHESIS 2: Payment Method Spending (M-Pesa vs Cash) ---")
    print(f"Mean Transaction (M-Pesa): KES {mpesa_amounts.mean():.2f}")
    print(f"Mean Transaction (Cash): KES {cash_amounts.mean():.2f}")
    print(f"Welch's t-test statistic: {t_stat_2:.4f}")
    print(f"p-value: {p_val_2:.4e}")
    if p_val_2 < 0.05:
        print("Conclusion: Reject H0. Significant difference exists between M-Pesa and Cash transaction values.")
    else:
        print("Conclusion: Fail to reject H0. There is no statistically significant difference in spending amounts between M-Pesa and Cash customers.")

if __name__ == '__main__':
    run_statistical_tests()

### Summary of Findings & Conclusions
1. Promotional Impact Test:Result: Welch's independent samples t-test yielded a t-statistic of 26.03 with a p-value of 1.34e-147 ($p < 0.05$).
Conclusion: Promotional campaigns and discounts successfully drive higher customer spending. Orders containing discounted items have a significantly higher average revenue (KES 1,190.02) compared to non-discounted orders (KES 821.51), proving that promotions effectively stimulate larger basket sizes.

2. Payment Method Spending Test (M-Pesa vs. Cash): Result: Welch's t-test yielded a p-value of 0.389 ($p > 0.05$).
Conclusion: There is no statistically significant difference in average transaction value between customers paying via M-Pesa (KES 1,103.97) and those paying with Cash (KES 1,122.25). While M-Pesa dominates transaction frequency and total volume, individual basket values remain consistent across both payment methods.


## Milestone 6: Predictive Model Script (demand_forecasting_model.py)
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

def run_demand_forecasting_model():
    print("==================================================")
    print("KENYAN RETAILER CAPSTONE: PREDICTIVE MODEL (MILSTONE 6)")
    print("==================================================\n")

    # Load cleaned data
    orders = pd.read_csv('orders.csv')
    order_items = pd.read_csv('order_items.csv')

    # Aggregate monthly total quantity demanded across all branches
    df = order_items.merge(orders, on='order_id', how='inner')
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['year_month'] = df['order_date'].dt.to_period('M')

    monthly_demand = df.groupby('year_month')['quantity'].sum().reset_index()
    monthly_demand['year_month_str'] = monthly_demand['year_month'].astype(str)

    # Time-Aware Train/Validation Split
    # Train: Year 2025 (Months 1 - 12)
    # Validation: Year 2026 (Months 1 - 6)
    train = monthly_demand[monthly_demand['year_month'].dt.year == 2025]
    val = monthly_demand[monthly_demand['year_month'].dt.year == 2026].copy()

    print(f"Training Set Periods: {train['year_month_str'].min()} to {train['year_month_str'].max()} ({len(train)} months)")
    print(f"Validation Set Periods: {val['year_month_str'].min()} to {val['year_month_str'].max()} ({len(val)} months)\n")

    # 1. Simple Baseline Model (Historical Mean Persistence)
    baseline_value = train['quantity'].mean()
    val['baseline_pred'] = baseline_value

    # 2. Predictive Trend Model (Linear Regression / Trend Extrapolation)
    z = np.polyfit(range(len(train)), train['quantity'], 1)
    p = np.poly1d(z)
    val['model_pred'] = p(range(len(train), len(train) + len(val)))

    # 3. Evaluation Metrics
    rmse_baseline = np.sqrt(mean_squared_error(val['quantity'], val['baseline_pred']))
    mape_baseline = mean_absolute_percentage_error(val['quantity'], val['baseline_pred'])

    rmse_model = np.sqrt(mean_squared_error(val['quantity'], val['model_pred']))
    mape_model = mean_absolute_percentage_error(val['quantity'], val['model_pred'])

    print("--- MODEL PERFORMANCE EVALUATION ---")
    print(f"Baseline Model -> RMSE: {rmse_baseline:.2f} | MAPE: {mape_baseline*100:.2f}%")
    print(f"Trend Model    -> RMSE: {rmse_model:.2f} | MAPE: {mape_model*100:.2f}%")

    # Error Analysis
    val['error'] = val['quantity'] - val['model_pred']
    val['abs_error_pct'] = (abs(val['error']) / val['quantity']) * 100
    
    print("\n--- VALIDATION COMPARISON ---")
    print(val[['year_month_str', 'quantity', 'model_pred', 'abs_error_pct']].to_string(index=False))

    print("\n--- ERROR ANALYSIS: WHAT THE MODEL GETS WRONG ---")
    print("1. Holiday & End-of-Month Surges: The trend model underestimates extreme spikes (such as December holiday shopping and massive mid-2026 retail growth).")
    print("2. Exogenous Shocks: Unanticipated promotional campaigns or local supply bottlenecks create residual errors that linear trend models cannot capture.")

if __name__ == '__main__':
    run_demand_forecasting_model()

### Key Components for Your Milestone Submission
Train/Validation Split: Implemented a strict time-aware split using historical 2025 monthly data for training and 2026 data for validation to prevent data leakage.

#### Models Compared:
Simple Baseline: Historical mean demand persistence.
Predictive Model: Linear trend extrapolation model capturing long-term retail expansion.

#### Evaluation Metrics:
RMSE (Root Mean Squared Error): Measures absolute magnitude of forecast errors.
MAPE (Mean Absolute Percentage Error): Evaluates relative percentage deviation.

#### What the Model Gets Wrong (Error Analysis):
The model struggles with unmodelled exogenous spikes (e.g., December festive demand surges and promotional blitzes) because it relies solely on historical linear trajectory without external economic indicators (like CPI or holiday flags).

## Milestone 7: Power BI Dashboard & Storytelling Architecture
### Dashboard Structure & Page Layout
#### Page 1: Executive Summary & Core KPIs
Card Metrics: Total Net Revenue (KES 29.58M), Total Orders (30,000), Average Order Value (KES 986.02), and M-Pesa Adoption Rate (75.26%).
Visuals: Monthly revenue trend line (highlighting December festive surges and 2026 growth), payment method breakdown donut chart, and top 10 revenue-generating product categories (Fresh Produce and Dairy leading).

#### Page 2: Branch & Regional Performance
Slicers: County (Nairobi, Kiambu, Nakuru, etc.), Outlet Type (Supermarket, Kiosk), and Date Range.
Visuals: Geographic map of retail branches sized by revenue, and a clustered bar chart comparing Actual Revenue vs. Target (outlet_targets.csv) across branches.

#### Page 3: Customer Segmentation & Demand Forecasting
Visuals: Customer RFM loyalty tier breakdown (Bronze, Silver, Gold) and 6-month forward demand projections comparing actual 
vs. trend model forecasts.

### Essential DAX Measures for Your Power BI Model
-- 1. Total Net Revenue
Total Revenue = SUMX(
    'order_items', 
    'order_items'[quantity] * 'order_items'[unit_price] * (1 - DIVIDE(COALESCE('order_items'[discount_pct], 0), 100))
)

-- 2. Total Orders
Total Orders = DISTINCTCOUNT('orders'[order_id])

-- 3. Average Order Value (AOV)
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)

-- 4. M-Pesa Revenue Share (%)
M-Pesa Revenue Share = DIVIDE(
    CALCULATE([Total Revenue], 'payments'[payment_method] = "M-Pesa"),
    [Total Revenue],
    0
)
 
    
