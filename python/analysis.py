import pandas as pd
import matplotlib.pyplot as plt

customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv")

print(customers.shape)
print(orders.shape)

## clv по клієнтах
clv = (
    orders
    .groupby("customer_id")
    .agg(
        orders_count=("order_id", "count"),
        total_revenue=("amount", "sum"),
        avg_order_value=("amount", "mean")
    )
    .reset_index()
)

print(clv.head())

## Додаємо клієнтів без замовлень
customers_full = customers.merge(
    clv,
    on="customer_id",
    how="left"
)

customers_full[["orders_count", "total_revenue", "avg_order_value"]] = (
    customers_full[["orders_count", "total_revenue", "avg_order_value"]]
    .fillna(0)
)

print(customers_full.head())

## Перша перевірка
print("Total customers:", customers_full.shape[0])
print("Customers with revenue > 0:", (customers_full["total_revenue"] > 0).sum())

## Гістогарама clv 
customers_full["total_revenue"].plot(kind="hist", bins=50)
plt.title("Розподіл доходу на клієнта (CLV)")
plt.xlabel("Total revenue")
plt.ylabel("Customers")
plt.tight_layout()
plt.savefig("images/total_revenue.png", dpi=300)
plt.show()

## Додаємо кумулятивний дохід
customers_full = customers_full.sort_values(
    by="total_revenue",
    ascending=False
)

customers_full["revenue_share"] = (
    customers_full["total_revenue"] / customers_full["total_revenue"].sum()
)

customers_full["cumulative_revenue_share"] = (
    customers_full["revenue_share"].cumsum()
)

## Сегментація клієнтів
def customer_segment(count):
    if count == 0:
        return "inactive"
    elif count == 1:
        return "one_time"
    else:
        return "repeat"

customers_full["customer_segment"] = customers_full["orders_count"].apply(customer_segment)

## Візуалізація сегментів
customers_full["customer_segment"].value_counts().plot(kind="bar")
plt.title("Customers by segment")
plt.tight_layout()
plt.savefig("images/customer_segment.png", dpi=300)
plt.show()

## Pareto
customers_full = customers_full.sort_values(
    by="total_revenue",
    ascending=False
)

customers_full["revenue_share"] = (
    customers_full["total_revenue"] / customers_full["total_revenue"].sum()
)

customers_full["pareto_segment"] = customers_full["cumulative_revenue_share"].apply(
    lambda x: "Top 20%" if x <= 0.8 else "Bottom 80%"
)

## Pareto-графік
plt.figure(figsize=(8,5))
plt.plot(customers_full["cumulative_revenue_share"])
plt.axhline(0.8, color="red", linestyle="--")
plt.title("Pareto analysis (80% доходу)")
plt.xlabel("Клієнти, відсортовані за доходом")
plt.ylabel("Кумулятивна частка доходу")
plt.tight_layout()
plt.savefig("images/pareto.png", dpi=300)
plt.show()

## Підготовка дат
orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["order_month"] = orders["order_date"].dt.to_period("M")

## Коли в останнє була покупка
last_order = (
    orders
    .groupby("customer_id")
    .agg(last_order_date=("order_date", "max"))
    .reset_index()
)

customers_full = customers_full.merge(
    last_order,
    on="customer_id",
    how="left"
)

## churn
cutoff_date = pd.to_datetime("2024-01-01")

customers_full["churn_status"] = customers_full["last_order_date"].apply(
    lambda x: "churned" if pd.isna(x) or x < cutoff_date else "active"
)

## Візуалізація churn
customers_full["churn_status"].value_counts().plot(kind="bar")
plt.title("Churn vs Active customers")
plt.tight_layout()
plt.savefig("images/churn.png", dpi=300)
plt.show()

## Cohort month
first_order = (
    orders
    .groupby("customer_id")
    .agg(cohort_month=("order_month", "min"))
    .reset_index()
)

## Додаємо cohort в orders
orders = orders.merge(
    first_order,
    on="customer_id",
    how="left"
)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
## Рахуємо номер місця
orders["cohort_index"] = (
    orders["order_month"] - orders["cohort_month"]
).apply(lambda x: x.n)

## Створюємо cohort table 
cohort_data = (
    orders
    .groupby(["cohort_month", "cohort_index"])
    .agg(customers=("customer_id", "nunique"))
    .reset_index()
)

## Pivot
cohort_table = cohort_data.pivot(
    index="cohort_month",
    columns="cohort_index",
    values="customers"
)

## Retention
retention = cohort_table.divide(cohort_table[0], axis=0) * 100
retention = retention.round(1)

print(retention)

## Візуалізація
plt.figure(figsize=(12, 6))
plt.imshow(retention, cmap="Blues", aspect="auto")
plt.colorbar(label="Retention %")
plt.xticks(range(len(retention.columns)), retention.columns)
plt.yticks(range(len(retention.index)), retention.index.astype(str))
plt.xlabel("Місяців з першої покупки")
plt.ylabel("Когорта (місяць)")
plt.title("Cohort Retention Analysis")
plt.tight_layout()
plt.savefig("images/retention_cohort.png", dpi=300)
plt.show()

## Дохід по місяцям
orders["order_month"] = orders["order_date"].dt.to_period("M")

revenue_by_month = (
    orders
    .groupby("order_month")
    .agg(total_revenue=("amount", "sum"))
    .reset_index()
)

revenue_by_month["order_month"] = revenue_by_month["order_month"].astype(str)

## Графік доходу по місяцям
plt.figure(figsize=(10, 5))
plt.plot(revenue_by_month["order_month"], revenue_by_month["total_revenue"])
plt.xticks(rotation=45)
plt.title("Дохід у часі")
plt.xlabel("Місяць")
plt.ylabel("Дохід")
plt.tight_layout()
plt.savefig("images/revenue_per_month.png", dpi=300)
plt.show()