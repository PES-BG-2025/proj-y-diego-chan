#%%
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#%%
#"""AREA DE CONEXION A BASE DE DATOS SQLITE3"""
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
#""" FUNCIONES AUXILIARES PARA FILTRAR Y AGRUPAR GASTOS """
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

#"""DEFINICIÓN DE LA INTERFAZ DE USUARIO CON STREAMLIT"""
# Inicializar la base de datos
inicializar_base_de_datos()

# Cargar todos los gastos una vez (para gráfica global)
todos_los_gastos_df = cargar_todos_los_gastos()

# Categorías predefinidas
CATEGORIAS = ["Consumo diario", "Ocio", "Transporte", "Salud", "Educación","Vestuario"]

# Título
st.title("📊 GASTOCONTROLLER5000") #comando los modificadaores de streamlite son los que tiene st

# Formulario para agregar gasto
st.header("➕ Agregar Nuevo Gasto")
with st.form("Formulario de Gasto"):
    col1, col2 = st.columns(2)
    with col1:
        producto = st.text_input("Producto", placeholder="Ej. Café, Gasolina...")
    with col2:
        categoria = st.selectbox("Categoría", options=CATEGORIAS)

    col3, col4 = st.columns(2)
    with col3:
        monto = st.number_input("Monto", min_value=0.0, step=0.01, format="%.2f")
    with col4:
        fecha = st.date_input("Fecha", value=datetime.today())

    enviado = st.form_submit_button("💾 Guardar")
    if enviado:
        if producto and monto > 0:
            guardar_gasto(producto, categoria, monto, str(fecha))
            # Recargar datos globales después de guardar
            todos_los_gastos_df = cargar_todos_los_gastos()
            st.success("✅ Gasto guardado!")
        else:
            st.warning("⚠️ Por favor, complete el producto y el monto.")

# st.markdown("---")
"---"

# 🥧 Gráfica de pastel: TOTAL DE TODOS LOS TIEMPOS (sin filtros)
st.subheader("🥧 Distribución Total de Gastos por Categoría")
if not todos_los_gastos_df.empty:
    totales_por_categoria = todos_los_gastos_df.groupby('categoria')['monto'].sum()
    fig_pastel, ax_pastel = plt.subplots(figsize=(6, 6))
    ax_pastel.pie(totales_por_categoria, labels=totales_por_categoria.index, autopct='%1.1f%%', startangle=140)
    ax_pastel.set_title("Distribución Global (Todo el historial)")
    ax_pastel.axis('equal')
    st.pyplot(fig_pastel)
else:
    st.info("No hay datos históricos para mostrar.")
    
st.markdown("---")

# 🔍 Filtros y análisis temporal (solo aquí usamos filtros)
#st.header("🔍 Análisis Temporal (por fechas)")
'''
### 🔍 Análisis Temporal (por fechas)
'''
# Fechas por defecto: último mes
hoy = datetime.today()
fecha_inicio_predeterminada = (hoy - timedelta(days=30)).date()

col1, col2, col3 = st.columns(3)
with col1:
    fecha_inicio = st.date_input("Fecha de inicio", value=fecha_inicio_predeterminada)
with col2:
    fecha_fin = st.date_input("Fecha de fin", value=hoy.date())
with col3:
    categoria_seleccionada = st.selectbox("Filtro de categoría", options=["Todas"] + CATEGORIAS)

# Botón para aplicar filtro
if st.button("📊 Actualizar Gráficos Temporales"):
    gastos_filtrados_df = filtrar_gastos(
        str(fecha_inicio),
        str(fecha_fin),
        categoria_seleccionada if categoria_seleccionada != "Todas" else None
    )
else:
    # Por defecto: último mes, todas las categorías
    gastos_filtrados_df = filtrar_gastos(
        str(fecha_inicio_predeterminada),
        str(hoy.date()),
        None
    )

# Selector de periodo
periodo = st.radio("📈 Agrupar por periodo:", ["Semanal", "Mensual", "Anual"], horizontal=True)

# Gráfico de barras temporal
st.subheader("📉 Gastos a lo largo del tiempo (Gráfico de Barras)")
if not gastos_filtrados_df.empty:
    df_agrupado = agrupar_por_periodo(gastos_filtrados_df, periodo)
    fig_barras, ax_barras = plt.subplots(figsize=(10, 5))
    df_agrupado.plot(kind='bar', stacked=True, ax=ax_barras)
    ax_barras.set_title(f"Gastos por {periodo} (Filtrado)")
    ax_barras.set_ylabel("Monto (Q)")
    ax_barras.legend(title="Categoría")
    plt.xticks(rotation=45)
    st.pyplot(fig_barras)
else:
    st.info("No hay datos para mostrar con los filtros seleccionados.")

# Tabla y métricas del análisis temporal
st.header("📋 Gastos Filtrados (Análisis Temporal)")
if not gastos_filtrados_df.empty:
    st.dataframe(gastos_filtrados_df[['producto', 'categoria', 'monto', 'fecha']].reset_index(drop=True))
    total = gastos_filtrados_df['monto'].sum()
    promedio = gastos_filtrados_df['monto'].mean()
    st.metric("💰 Total Gastos (Filtrado)", f"Q{total:,.2f}")
    st.metric("📈 Promedio por Gasto", f"Q{promedio:,.2f}")
else:
    st.write("No hay gastos que coincidan con los filtros seleccionados.")