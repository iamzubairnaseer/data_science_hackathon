-- Net revenue definition used throughout: valid quantity/price/date only; returned orders contribute zero.
-- 1. Total net revenue
SELECT ROUND(SUM(quantity * unit_price * (1-discount) * (1-returned)),2) AS total_net_revenue
FROM orders
WHERE quantity > 0 AND unit_price > 0 AND date(order_date) IS NOT NULL;

-- 2. Top 10 customers by spending
SELECT c.customer_name, c.city, COUNT(DISTINCT o.order_id) AS number_of_orders,
       ROUND(SUM(o.quantity*o.unit_price*(1-o.discount)*(1-o.returned)),2) AS total_spending
FROM orders o JOIN customers c ON c.customer_id=o.customer_id
WHERE o.quantity>0 AND o.unit_price>0 AND date(o.order_date) IS NOT NULL
GROUP BY c.customer_id,c.customer_name,c.city
ORDER BY total_spending DESC LIMIT 10;

-- 3. Category-wise revenue, order count and quantity sold
SELECT TRIM(LOWER(p.category)) AS category_key,
       ROUND(SUM(o.quantity*o.unit_price*(1-o.discount)*(1-o.returned)),2) AS net_revenue,
       COUNT(DISTINCT o.order_id) AS order_count, SUM(o.quantity) AS quantity_sold
FROM orders o JOIN products p ON p.product_id=o.product_id
WHERE o.quantity>0 AND o.unit_price>0 AND date(o.order_date) IS NOT NULL
GROUP BY TRIM(LOWER(p.category)) ORDER BY net_revenue DESC;

-- 4. Monthly net revenue trend
SELECT strftime('%Y-%m',order_date) AS month,
       ROUND(SUM(quantity*unit_price*(1-discount)*(1-returned)),2) AS net_revenue
FROM orders
WHERE quantity>0 AND unit_price>0 AND date(order_date) IS NOT NULL
GROUP BY month ORDER BY month;

-- 5. Top 5 products by net revenue
SELECT p.product_name,
       ROUND(SUM(o.quantity*o.unit_price*(1-o.discount)*(1-o.returned)),2) AS net_revenue
FROM orders o JOIN products p ON p.product_id=o.product_id
WHERE o.quantity>0 AND o.unit_price>0 AND date(o.order_date) IS NOT NULL
GROUP BY p.product_id,p.product_name ORDER BY net_revenue DESC LIMIT 5;
