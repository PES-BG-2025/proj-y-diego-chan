#%%
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#%%
"""AREA DE CONEXION A BASE DE DATOS SQLITE3"""
# Nombre del archivo de la base de datos
ARCHIVO_BD = 'gastos.db'

# Inicializar la base de datos y crear la tabla si no existe, si existe no hace nada
def inicializar_base_de_datos():
    conexion = sqlite3.connect(ARCHIVO_BD) # Conectar a la base de datos (o crearla si no existe)
    cursor = conexion.cursor() # Crear un cursor para ejecutar comandos SQL
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            monto REAL NOT NULL,
            fecha TEXT NOT NULL
        )
    ''')
    conexion.commit() # Guardar los cambios
    conexion.close() # Cerrar la conexión
#%%
# Guardar un nuevo gasto
def guardar_gasto(producto, categoria, monto, fecha):
    conexion = sqlite3.connect(ARCHIVO_BD)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO gastos (producto, categoria, monto, fecha)
        VALUES (?, ?, ?, ?)
    ''', (producto, categoria, monto, fecha))
    conexion.commit()
    conexion.close()
#%%
# Cargar todos los gastos (sin filtros) para mostrar el pie general.
def cargar_todos_los_gastos():
    conexion = sqlite3.connect(ARCHIVO_BD)
    df = pd.read_sql_query("SELECT * FROM gastos", conexion)
    conexion.close()
    return df
#%%
""" FUNCIONES AUXILIARES PARA FILTRAR Y AGRUPAR GASTOS """
# Filtrar gastos por fechas y categoría
def filtrar_gastos(fecha_inicio, fecha_fin, categoria=None):
    conexion = sqlite3.connect(ARCHIVO_BD)
    consulta = "SELECT * FROM gastos WHERE fecha BETWEEN ? AND ?"
    parametros = [fecha_inicio, fecha_fin]
    if categoria and categoria != "Todas":
        consulta += " AND categoria = ?"
        parametros.append(categoria)
    df = pd.read_sql_query(consulta, conexion, params=parametros)
    conexion.close()
    return df

# Agrupar gastos por periodo (semanal, mensual, anual)
def agrupar_por_periodo(df, periodo='Mensual'):
    df['fecha'] = pd.to_datetime(df['fecha'])
    if periodo == 'Semanal':
        df['periodo'] = df['fecha'].dt.to_period('W').apply(lambda r: r.start_time)
    elif periodo == 'Mensual':
        df['periodo'] = df['fecha'].dt.to_period('M').apply(lambda r: r.start_time)
    elif periodo == 'Anual':
        df['periodo'] = df['fecha'].dt.to_period('Y').apply(lambda r: r.start_time)
    else:
        df['periodo'] = df['fecha']  # Diario

    agrupado = df.groupby(['periodo', 'categoria'])['monto'].sum().unstack(fill_value=0)
    return agrupado

"""DEFINICIÓN DE LA INTERFAZ DE USUARIO CON STREAMLIT"""
# Inicializar la base de datos
inicializar_base_de_datos()

# Cargar todos los gastos una vez (para gráfica global)
todos_los_gastos_df = cargar_todos_los_gastos()

# Categorías predefinidas
CATEGORIAS = ["Consumo diario", "Ocio", "Transporte", "Salud", "Educación","Vestuario"]

# Título
st.title("📊 GASTOCONTROLLER5000") #comando los modificadaores de streamlite son los que tiene st