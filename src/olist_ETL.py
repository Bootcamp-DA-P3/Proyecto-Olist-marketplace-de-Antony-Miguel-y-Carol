import pandas as pd

from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from src.limpieza import *

from src.config import (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    CARPETA_SQL,
    CARPETA_DATA,
)

CONSULTAS = {
    # TABLA DE HECHOS.
    "df4_tabla_hechos": "-",

    # DIMENSIONES.
    "df1_actividad_clientes": "-",
    "df2_catalogo_productos": "-",
    "df3_vendedores_popularidad": "-",
}

def crear_engine():
    """Crea el motor de conexión a MySQL con las credenciales del .env."""
    if not DB_USER or not DB_PASSWORD:
        raise RuntimeError(
            "Faltan DB_USER o DB_PASSWORD en el fichero .env. "
            "Copiad .env.example como .env y rellenadlo."
        )
    #url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)


def extraer(engine, nombre):
    """Ejecuta queries/<nombre>.sql y devuelve el resultado como DataFrame."""
    ruta = CARPETA_SQL / f"{nombre}.sql"
    if not ruta.exists():
        raise FileNotFoundError(f"No existe la consulta {ruta}")

    consulta = ruta.read_text(encoding="utf-8").strip().rstrip(";")
    return pd.read_sql(text(consulta), engine)

def comprobar_grano(df, clave, nombre):
    """Detiene el proceso si la consulta no respeta el grano que declara."""
    if clave not in df.columns:
        raise KeyError(f"{nombre}: la consulta no devuelve la columna de grano '{clave}'")

    distintos = df[clave].nunique(dropna=False)
    if distintos != len(df):
        raise ValueError(
            f"{nombre}: {len(df)} filas para {distintos} valores distintos de '{clave}'. "
            "Algo esta multiplicando filas: el JOIN del .sql o una regla de limpieza."
        )

def exportar(df, nombre_csv):
    """Guarda el DataFrame en data/ como CSV."""
    # por si la carpeta no existe todavía
    CARPETA_DATA.mkdir(parents=True, exist_ok=True)
    # Definir la ruta completa del archivo
    ruta_salida = CARPETA_DATA / f"{nombre_csv}.csv"
    # Exportar con index=False y encoding='utf-8-sig'
    df.to_csv(ruta_salida, index=False, encoding="utf-8-sig")
    print(f"Archivo exportado correctamente en: {ruta_salida.resolve()}")
    return ruta_salida

def ejecutar_etl():
    """Recorre todas las consultas. Devuelve {nombre: (filas, ruta del csv)}."""
    engine = crear_engine()
    resultados = {}

    for nombre, clave_de_grano in CONSULTAS.items():
        df = extraer(engine, nombre)
        # comprobar_grano(df, clave_de_grano, f"{nombre} (SQL)")
        if clave_de_grano == "df1_actividad_clientes":
            df = limpiar_1(df, nombre)
        elif clave_de_grano == "df2_catalogo_productos":
            df = limpiar_2(df, nombre)
        elif clave_de_grano == "df3_vendedores_popularidad":
            df = limpiar_3(df, nombre)
        elif clave_de_grano == "df4_tabla_hechos":
            df = limpiar_4(df, nombre)

        # comprobar_grano(df, clave_de_grano, f"{nombre} (tras limpiar)")
        resultados[nombre] = (len(df), exportar(df, nombre))

    return resultados