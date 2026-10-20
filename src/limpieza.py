import pandas as pd
import numpy as np

def limpiar_1(df, nombre):
    df = df.copy()

    # 1. Filtrar por pedidos entregados y eliminar fechas de entrega nulas
    df = df[df['order_status'] == 'delivered']
    df = df.dropna(subset=['order_delivered_customer_date'])
    
    # 2. Verificar consistencia temporal (compra anterior a la entrega)
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])
    
    df = df[df['order_purchase_timestamp'] < df['order_delivered_customer_date']]
    
    # 3. Asegurar payment_value > 0 y rellenar nulos
    df = df[df['payment_value'] > 0]
    df['payment_type'] = df['payment_type'].fillna('not_defined').str.lower().str.strip()
    df['review_score'] = df['review_score'].fillna(0)
    
    # 4. Estandarizar textos de ubicación
    df['customer_city'] = df['customer_city'].str.lower().str.strip()
    df['customer_state'] = df['customer_state'].str.lower().str.strip()
    
    # 5. Columnas derivadas
    df['delivery_days'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
    df['is_late'] = (df['order_delivered_customer_date'] > df['order_estimated_delivery_date']).astype(int)
    
    return df

def limpiar_2(df, nombre):
    df = df.copy()

    # 1. Normalizar categoría y rellenar vacíos
    df['product_category_name'] = df['product_category_name'].str.lower().str.strip().fillna('desconocido')
    
    # 2. Eliminar registros con peso menor/igual a 0 o dimensiones nulas
    df = df[df['product_weight_g'] > 0]
    df = df.dropna(subset=['product_length_cm', 'product_height_cm', 'product_width_cm'])
    
    # 3. Estandarizar textos del vendedor
    df['seller_city'] = df['seller_city'].str.lower().str.strip()
    df['seller_state'] = df['seller_state'].str.lower().str.strip()
    
    # 4. Columnas derivadas
    df['freight_ratio'] = df.apply(lambda row: row['freight_value'] / row['price'] if row['price'] > 0 else 0, axis=1)
    df['is_heavy'] = (df['product_weight_g'] >= 5000).astype(int) # >= 5 kg
    
    return df

def limpiar_3(df, nombre):
    df = df.copy()

    # 1. Estandarizar ciudades y estados de los vendedores
    df['seller_city'] = df['seller_city'].str.lower().str.strip()
    df['seller_state'] = df['seller_state'].str.lower().str.strip()
    
    # 2. Filtrar filas con IDs válidos (si existieran nulos)
    df = df.dropna(subset=['seller_id', 'product_id'])
    
    return df

def limpiar_4(df, nombre):
    df = df.copy()

    # --- LIMPIEZA PARA EL DATAFRAME DE LA CONSULTA 4 (FACT TABLE) ---
    
    # 1. Filtrar solo pedidos entregados y asegurar montos positivos
    df = df[df['order_status'] == 'delivered']
    df = df[df['price'] >= 0]
    
    # 2. Columna derivada del valor total del ítem
    df['total_item_value'] = df['price'] + df['freight_value']
    
    return df
