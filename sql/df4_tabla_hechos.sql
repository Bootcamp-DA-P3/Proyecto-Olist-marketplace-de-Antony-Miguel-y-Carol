-- DATAFRAME 4 · Tabla de hechos
-- Tablas: ALL
--
-- GRANO DECLARADO: No tiene grano

SELECT 
    -- Identificadores principales
    o.order_id,
    oi.order_item_id,
    c.customer_unique_id,
    c.customer_id,
    s.seller_id,
    p.product_id,
    
    -- Dimensiones de fecha y tiempo
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    
    -- Dimensiones geográficas y de categoría
    c.customer_city,
    c.customer_state,
    s.seller_city,
    s.seller_state,
    p.product_category_name,
    
    -- Estado y logística
    o.order_status,
    
    -- Métricas / Hechos (Valores numéricos)
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value) AS total_item_value,
    
    -- Información de pago (tomando la cuota y tipo principal o agregada)
    op.payment_type,
    op.payment_installments,
    op.payment_value,
    
    -- Información de satisfacción del cliente
    orv.review_score,
    orv.review_creation_date

FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN sellers s ON oi.seller_id = s.seller_id
-- LEFT JOIN para asegurar que no se pierdan pedidos si falta algún pago o reseña en los datos de muestra
LEFT JOIN (
    SELECT order_id, payment_type, payment_installments, payment_value,
           ROW_NUMBER() OVER(PARTITION BY order_id ORDER BY payment_sequential) as rn
    FROM order_payments
) op ON o.order_id = op.order_id AND op.rn = 1
LEFT JOIN order_reviews orv ON o.order_id = orv.order_id;