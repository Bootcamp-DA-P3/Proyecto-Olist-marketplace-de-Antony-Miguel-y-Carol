-- DATAFRAME 2 · Catalogo de productos
-- Tablas: products, categoria_traduccion, order_items, sellers
--
-- GRANO DECLARADO: Una fila por ítem dentro de cada pedido (order_id + order_item_id implícito en la relación).
-- Columna clave: product_id combinado con seller_id.

SELECT 
    p.product_id,
    LOWER(TRIM(COALESCE(p.product_category_name, 'desconocido'))) AS product_category_name,
    p.product_weight_g,
    oi.price,
    oi.freight_value,
    -- Columna derivada: ratio de flete respecto al precio
    CASE WHEN oi.price > 0 THEN (oi.freight_value / oi.price) ELSE 0 END AS freight_ratio,
    -- Columna derivada: producto pesado (>= 5 kg / 5000 gramos)
    CASE WHEN p.product_weight_g >= 5000 THEN 1 ELSE 0 END AS is_heavy,
    s.seller_id,
    LOWER(TRIM(s.seller_city)) AS seller_city,
    LOWER(TRIM(s.seller_state)) AS seller_state
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN sellers s ON oi.seller_id = s.seller_id
WHERE p.product_weight_g > 0
  AND p.product_length_cm IS NOT NULL 
  AND p.product_height_cm IS NOT NULL 
  AND p.product_width_cm IS NOT NULL;