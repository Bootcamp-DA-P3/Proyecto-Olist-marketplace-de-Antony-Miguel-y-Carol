-- DATAFRAME 4 · Tabla de hechos
-- Tablas: ALL
--
-- GRANO DECLARADO: Nivel de línea de pedido (order_id + order_item_id).
-- Columna clave: Claves foráneas hacia las dimensiones de clientes, productos y vendedores.

SELECT 
    oi.order_id,
    oi.order_item_id,
    o.customer_id,
    c.customer_unique_id,
    oi.product_id,
    oi.seller_id,
    o.order_purchase_timestamp,
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value) AS total_item_value
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered';