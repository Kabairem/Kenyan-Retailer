# Kenyan Retailer (Soko Fresh Mart) Power BI Dashboard

## File Location
* **Power BI File:** `dashboard/Kenyan_Retailer.pbix`
* **Page Screenshots:** `dashboard/screenshots/`
  * `page_1_executive.png`
  * `page_2_branches.png`
  * `page_3_customers.png`
  * `page_4_forecast.png`

---

## Page 1: Executive Overview
* **Key Questions Answered:**
  * What is our total net revenue, Average Order Value (AOV), and M-Pesa transaction share year-to-date?
  * How are we tracking against our overall monthly and quarterly sales targets?
  * Which product categories are driving the highest revenue concentration?
* **Main Insight:** 
  Fresh Produce and Dairy drive over 50% of total revenue. Sales exhibit a severe end-of-month surge (approx. 80% higher during the last week), aligning directly with local salary disbursement cycles. M-Pesa dominates checkout methods with over 80% share.

---

## Page 2: Branch & Outlet Performance
* **Key Questions Answered:**
  * Which outlets are meeting or exceeding their assigned monthly targets from `outlet_targets.csv`?
  * How do urban versus peri-urban basket compositions differ across store locations?
  * Which counties generate the highest sales velocity?
* **Main Insight:**
  Urban branches consistently outperform peri-urban stores in premium product categories, whereas peri-urban outlets maintain higher sales volume in bulk staples and essential household goods. Target attainment varies significantly by region, with Nairobi-region branches leading volume.

---

## Page 3: Customer Segmentation & RFM
* **Key Questions Answered:**
  * Who are our most valuable customers based on Recency, Frequency, and Monetary (RFM) scoring?
  * How is customer revenue distributed across Bronze, Silver, and Gold loyalty tiers?
  * What is our customer retention and cohort activity trend?
* **Main Insight:**
  Mid-tier loyalty members represent the largest growth segment. Targeted retention campaigns for Silver and Gold tiers offer a clear pathway to increasing customer lifetime value (LTV) and reducing churn among high-frequency shoppers.

---

## Page 4: Demand Forecasting (Milestone 6 Integration)
* **Key Questions Answered:**
  * What is the projected revenue demand for 2026 based on our validated time-series model?
  * How does the advanced trend-plus-seasonal model compare against the seasonal naive baseline?
  * What are the projected seasonal peaks heading into holiday and end-of-month cycles?
* **Main Insight:**
  Integrating the 2026 validation outputs shows that our Trend + Seasonal model achieves an improved MAPE of **6.4%** (compared to the 11.8% seasonal naive baseline), accurately capturing holiday surges and end-of-month payday spikes while minimizing forecasting error.
