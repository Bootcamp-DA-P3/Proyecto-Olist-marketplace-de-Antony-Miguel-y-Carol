-- DATAFRAME 3 · Vendedores y popularidad
-- Tablas: sellers, order_items, products
--
-- GRANO DECLARADO: Una fila por cada combinación de seller_id y product_id.
-- Columna clave: seller_id y product_id.

SELECT 
    s.seller_id,
    LOWER(TRIM(s.seller_city)) AS seller_city,
    LOWER(TRIM(s.seller_state)) AS seller_state,
    p.product_id,
    COUNT(oi.order_id) AS total_units_sold,
    SUM(oi.price) AS total_revenue,
    AVG(oi.price) AS avg_product_price
FROM sellers s
JOIN order_items oi ON s.seller_id = oi.seller_id
JOIN products p ON oi.product_id = p.product_id
GROUP BY s.seller_id, s.seller_city, s.seller_state, p.product_id;