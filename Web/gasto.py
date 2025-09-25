import streamlit as st 
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os

# Proyecto GastoController5000
# Cargamos librerias, tkinter, flet
# Comenzaremos definiendo funciones 


# nombre del archivo donde se guardaran los gastos (en formato CSV)
AG = 'gastos.csv'

# Función para cargar gastos
def load_expenses():
    if os.path.exists(AG):
        df = pd.read_csv(AG)
        df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce')
        return df
    else:
        return pd.DataFrame(columns=['Producto', 'Categoria', 'Monto', 'Fecha'])

# Función para guardar gastos
def save_expenses(df):  # Recibe un DataFrame df que contiene los registros de gastos 
    df.to_csv(AG, index=False)     # Exporta el DataFrama a un archivo CSV; AG


# Función para actualizar gráfico
def update_pie_chart(df):
    df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce')
    category_expenses = df.dropna(subset=['Monto']).groupby('Categoria')['Monto'].sum()

    fig, ax = plt.subplots(figsize=(6, 6))
    if not category_expenses.empty:
        ax.pie(category_expenses, labels=category_expenses.index, autopct='%1.1f%%', startangle=140)
        ax.set_title("Distribución de gasto por categoría")
        ax.axis('igual')
    else:
        ax.text(0, 0, "No hay datos de gastos disponibles", horizontalalignment='center', verticalalignment='center')
        ax.set_title("Distribución de gasto por categoría")
        
    st.pyplot(fig)


# Cargar datos iniciales
if 'expenses_df' not in st.session_state:
    st.session_state.expenses_df = load_expenses()

# Título de la app
st.title("📊 Aplicación web de seguimiento de gastos")

# Formulario para agregar gasto
st.header("➕ Agregar nuevo gasto")

CATEGORIAS = ["Consumo diario", "Ocio", "Transporte", "Salud", "Educación"]

with st.form("form_gasto"):
    producto = st.text_input("Producto")
    categoria = st.selectbox("Categoria", options = CATEGORIAS)
    monto = st.number_input("Monto", min_value=0.0, step=0.01, format="%.2f")
    fecha = st.date_input("Fecha")

    submitted = st.form_submit_button("Agregar gastos")

    if submitted:
        if producto and monto > 0:
            new_expense = pd.DataFrame([{
                'Producto': producto,
                'Categoria': categoria,
                'Monto': monto,
                'Fecha': str(fecha)
            }])
            st.session_state.expenses_df = pd.concat([st.session_state.expenses_df, new_expense], ignore_index=True)
            save_expenses(st.session_state.expenses_df)
            st.success("✅ Gasto agregado exitosamente!")
        else:
            st.error("❌ Por favor, rellene todos los campos correctamente.")

# Mostrar gráfico actualizado
st.header("📈 Distribución de gastos")
update_pie_chart(st.session_state.expenses_df)

# Mostrar tabla de datos (opcional)
st.header("📋 Todos los gastos")
st.dataframe(st.session_state.expenses_df)


# %%
