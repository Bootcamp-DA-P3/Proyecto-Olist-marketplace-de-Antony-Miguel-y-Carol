-- DATAFRAME 1 · Actividad de clientes
-- Tablas: customers, orders, order_payments, order_reviews, geolocation
--
-- GRANO DECLARADO: Una fila por order_id (nivel de pedido individual).
-- Columna clave: order_id (y agrupado por customer_unique_id para métricas de clientes).

SELECT 
    c.customer_unique_id,
    o.order_id,
    LOWER(TRIM(c.customer_city)) AS customer_city,
    LOWER(TRIM(c.customer_state)) AS customer_state,
    geo.avg_lat AS geolocation_lat,
    geo.avg_lng AS geolocation_lng,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    DATEDIFF(o.order_delivered_customer_date, o.order_purchase_timestamp) AS delivery_days,
    CASE 
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1 
        ELSE 0 
    END AS is_late,
    COALESCE(p.payment_type, 'not_defined') AS payment_type,
    p.payment_installments,
    p.payment_value,
    COALESCE(r.review_score, 0) AS review_score
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
-- Subconsulta para resolver la trampa de la geolocalización (promediando coordenadas por prefijo)
LEFT JOIN (
    SELECT geolocation_zip_code_prefix, 
           AVG(geolocation_lat) AS avg_lat, 
           AVG(geolocation_lng) AS avg_lng
    FROM geolocation
    GROUP BY geolocation_zip_code_prefix
) geo ON c.customer_zip_code_prefix = geo.geolocation_zip_code_prefix
LEFT JOIN (
    SELECT order_id, payment_type, payment_installments, SUM(payment_value) AS payment_value
    FROM order_payments
    WHERE payment_value > 0
    GROUP BY order_id, payment_type, payment_installments
) p ON o.order_id = p.order_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_purchase_timestamp < o.order_delivered_customer_date;