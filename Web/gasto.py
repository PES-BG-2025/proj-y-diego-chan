#%%
# #import tkinter as tk
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os

# Proyecto GastoController5000
# Cargamos librerias, tkinter, flet
# Comenzaremos definiendo funciones 
#%%
# nombre del archivo donde se guardaran los gastos (en formato CSV)
BDG = 'gastos.csv' 

# Función que cargara los datos de gastos desde el archivo CSV
def load_expenses(): 
    """Carga los datos de gastos desde el archivo CSV si existe; 
    si no existe, crea una tabla vacía con las columnas necesarias."""

    # Declaramos que vamos a usar una variable global llamada "expenses_df"
    # (esto significa que la variable existirá fuera de la función también)
    global expenses_df 

    #verificamos si el archivo "expenses.csv existe en la carpeta actual"
    if os.path.exists(BDG):
        # Si el archivo SÍ existe:
        #   -lo leemos con pandas y lo guardamos en la variable "expenses_df"
        expenses_df = pd.read_csv(BDG)

        #Aseguramos que la columna "Amount" (monto) contenga números
        #   - pd.to_numeric convierte los valores a números
        #   - errors='coerce' significa: si hay algo que no es número (como texto),
        #       cámbialo a "valor nulo" en vez de fallar
        expenses_df['Amount'] = pd.to_numeric(expenses_df['Amount'], errors='coerce')

    else:
        # Si el archivo no existe: 
        #   - creamos un dataframe vacío (una tabla sin filas)
        #   - pero con las columnas que necesitamos: 'Product', 'Category', 'Amount', 'Date'
        expenses_df = pd.DataFrame(columns=['Product', 'Category', 'Amount', 'Date'])


#%% 
load_expenses()



# %%
