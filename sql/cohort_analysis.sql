-- Перевірка кількості клієнтів
SELECT 
    COUNT(*) AS total_customers,
FROM customers;

-- Перевірка кількості замовлень
SELECT 
    COUNT(*) AS total_orders,
FROM orders;

-- CLV по клієнтах
SELECT
    o.customer_id,
    COUNT(o.order_id) AS orders_count,
    SUM(o.amount) AS total_revenue,
    AVG(o.amount) AS avg_order_value
FROM orders o
GROUP BY o.customer_id;

-- Клієнти з урахуванням тих, хто не має замовлень
SELECT
    c.customer_id,
    COALESCE(COUNT(o.order_id), 0) AS orders_count,
    COALESCE(SUM(o.amount), 0) AS total_revenue
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id;

-- Сегментація клієнтів
SELECT
    c.customer_id,
    COUNT(o.order_id) AS orders_count,
    CASE
        WHEN COUNT(o.order_id) = 0 THEN 'inactive'
        WHEN COUNT(o.order_id) = 1 THEN 'one_time'
        ELSE 'repeat'
    END AS customer_segment
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id;

-- Дохід по сегментах
SELECT
    customer_segment,
    COUNT(customer_id) AS customers_count,
    SUM(total_revenue) AS total_revenue,
    AVG(total_revenue) AS avg_revenue
FROM (
    SELECT
        c.customer_id,
        SUM(o.amount) AS total_revenue,
        CASE
            WHEN COUNT(o.order_id) = 0 THEN 'inactive'
            WHEN COUNT(o.order_id) = 1 THEN 'one_time'
            ELSE 'repeat'
        END AS customer_segment
    FROM customers c
    LEFT JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
) t
GROUP BY customer_segment;

-- CLV з ранжуванням
SELECT
    customer_id,
    total_revenue,
    NTILE(5) OVER (ORDER BY total_revenue DESC) AS revenue_bucket
FROM (
    SELECT
        c.customer_id,
        COALESCE(SUM(o.amount), 0) AS total_revenue
    FROM customers c
    LEFT JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
) t;

-- Остання покупка клієнта
SELECT
    customer_id,
    MAX(order_date) AS last_order_date
FROM orders
GROUP BY customer_id;

-- Churn-статус
SELECT
    c.customer_id,
    MAX(o.order_date) AS last_order_date,
    CASE
        WHEN MAX(o.order_date) < DATE '2023-04-01' OR MAX(o.order_date) IS NULL
        THEN 'churned'
        ELSE 'active'
    END AS churn_status
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id;

-- Місячний дохід
SELECT
    DATE_TRUNC('month', order_date) AS order_month,
    SUM(amount) AS total_revenue
FROM orders
GROUP BY order_month
ORDER BY order_month;