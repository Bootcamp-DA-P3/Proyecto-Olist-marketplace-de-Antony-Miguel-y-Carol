-- DATAFRAME 1 · Actividad de clientes
-- Tablas: customers, orders, order_payments, order_reviews, geolocation
--
-- GRANO DECLARADO: No tiene grano

SELECT 
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_pedidos,
    AVG(r.review_score) AS nota_media_cliente,
    (SELECT COUNT(DISTINCT cust.customer_unique_id) FROM customers cust) AS total_clientes_global
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
GROUP BY c.customer_unique_id, c.customer_city, c.customer_state;