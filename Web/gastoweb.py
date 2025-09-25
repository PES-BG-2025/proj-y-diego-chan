#%%
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#%%
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