import pandas as pd
import numpy as np

def limpiar_1(df, nombre):
    df = df.copy()
    
    # Rellenar valores nulos en la nota media con 0 (clientes sin reseñas)
    if 'nota_media_cliente' in df.columns:
        df['nota_media_cliente'] = df['nota_media_cliente'].fillna(0)
        
    # Estandarizar columnas de texto (ciudades y estados)
    if 'customer_city' in df.columns:
        df['customer_city'] = df['customer_city'].str.strip().str.lower()
        
    if 'customer_state' in df.columns:
        df['customer_state'] = df['customer_state'].str.strip().str.upper()
        
    # Asegurar tipos numéricos enteros
    if 'total_pedidos' in df.columns:
        df['total_pedidos'] = df['total_pedidos'].astype(int)
        
    if 'total_clientes_global' in df.columns:
        df['total_clientes_global'] = df['total_clientes_global'].astype(int)
        
    return df

def limpiar_2(df, nombre):
    df = df.copy()
    
    # Normalizar nombres de columnas
    df.columns = [c.strip().lower().replace(' ', '_').replace('ó', 'o').replace('í', 'i').replace('ú', 'u') for c in df.columns]
    
    # Limpieza de fechas (conversión a datetime)
    fecha_cols = [c for c in df.columns if 'fecha' in c or 'timestamp' in c or 'purchase' in c]
    for col in fecha_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        
    # Limpieza de estados y ciudades
    if 'estado_cliente' in df.columns:
        df['estado_cliente'] = df['estado_cliente'].astype(str).str.upper().str.strip()
    if 'ciudad_cliente' in df.columns:
        df['ciudad_cliente'] = df['ciudad_cliente'].astype(str).str.lower().str.strip()
    if 'estado' in df.columns:
        df['estado'] = df['estado'].astype(str).str.lower().str.strip()
        
    return df

def limpiar_3(df, nombre):
    df = df.copy()
    
    # Normalizar textos de ubicación y categoría
    if 'seller_city_clean' in df.columns:
        df['seller_city_clean'] = df['seller_city_clean'].astype(str).str.lower().str.strip()
    if 'seller_state_clean' in df.columns:
        df['seller_state_clean'] = df['seller_state_clean'].astype(str).str.upper().str.strip()
    if 'product_category_name' in df.columns:
        df['product_category_name'] = df['product_category_name'].fillna('desconocido').astype(str).str.lower().str.strip()
        
    # Conversión y redondeo de columnas numéricas
    metricas = {
        'unidades_vendidas_producto': int,
        'pedidos_distintos_producto': int,
        'ingreso_total_producto': float,
        'ranking_producto_en_vendedor': int
    }
    
    for col, dtype in metricas.items():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            if dtype == int:
                df[col] = df[col].astype(int)
            else:
                df[col] = df[col].round(2)
                
    return df


def limpiar_4(df, nombre):
    df = df.copy()
    
    # 1. Conversión de fechas y marcas de tiempo
    date_cols = [c for c in df.columns if 'timestamp' in c or 'date' in c]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        
    # 2. Tipado y redondeo de métricas monetarias
    monetary_cols = ['price', 'freight_value', 'total_item_value', 'payment_value']
    for col in monetary_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).round(2)
            
    # 3. Tipado de métricas enteras
    int_cols = ['order_item_id', 'payment_installments', 'review_score']
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
    # 4. Normalización de textos, categorías y estados geográficos
    text_cols = ['customer_city', 'customer_state', 'seller_city', 'seller_state', 'product_category_name', 'order_status', 'payment_type']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            if 'state' in col:
                df[col] = df[col].str.upper()
            else:
                df[col] = df[col].str.lower()
                # Reemplazar nulos textuales por NaN de Pandas
                df[col] = df[col].replace(['nan', 'none', 'nat', 'null'], np.nan)
                
    # 5. Imputación de valores por defecto lógicos para análisis y dashboards
    if 'product_category_name' in df.columns:
        df['product_category_name'] = df['product_category_name'].fillna('sin_categoria')
    if 'payment_type' in df.columns:
        df['payment_type'] = df['payment_type'].fillna('desconocido')
        
    return df
