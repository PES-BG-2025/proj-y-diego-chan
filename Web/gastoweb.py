#%%
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#%%
# Nombre del archivo de la base de datos
ARCHIVO_BD = 'gastos.db'

# Inicializar la base de datos
def inicializar_base_de_datos():
    conexion = sqlite3.connect(ARCHIVO_BD)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            monto REAL NOT NULL,
            fecha TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()
#%%