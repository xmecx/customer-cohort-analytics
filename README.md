#  Customer Cohort & Retention Analytics

## Project Description
This project focuses on analyzing customer behavior, Customer Lifetime Value (CLV), retention, churn, and 
overall revenue structure.

The goal is to demonstrate how Python and SQL can be used to generate business insights that support 
retention strategies, VIP customer identification, and revenue growth decisions.
---

##  Data
The project CSV files:

- `customers.csv`
  - `customer_id`
  - registration date
  - demographic attributes (if available)

- `orders.csv`
  - `order_id`
  - `customer_id`
  - `order_date`
  - `amount`

The dataset includes both customers with and without orders.


##  Key Metrics
The following metrics were calculated:

- number of orders per customer
- total revenue per customer (CLV)
- average order value
- revenue share by customer (Pareto 80/20)
- customer churn status
- cohort-based retention
- revenue over time

###  CLV (Customer Lifetime Value)
Calculated:
- number of orders
- total revenue
- average order value per customer


###  Behavioral Segmentation
Customers were segmented into:
- `inactive` — 0 orders
- `one_time` — 1 order
- `repeat` — 2+ orders

###  Pareto (VIP Analysis)
Customers were ranked by revenue to identify:
- VIP customers (top 20%)
- their contribution to total revenue


###  Churn Analysis
Churn was determined based on the date of the last purchase:
- `active` — customer purchased recently
- `churned` — customer inactive beyond a defined threshold period


###  Cohort Retention
Cohort analysis was built based on the month of first purchase:
- monthly retention rates
- heatmap visualization


###  Revenue over Time
Analyzed:
- monthly revenue
- revenue trends over time


##  Tools
- Python
- pandas
- matplotlib
- SQL (aggregation, joins, window functions)

##  Result
This project demonstrates:
- working with multiple related tables
- an end-to-end analytical pipeline
- business-oriented analytical thinking
- integration of Python and SQL for data analysis
