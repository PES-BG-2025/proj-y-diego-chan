# 📊 GASTOCONTROLLER5000

Una aplicación sencilla pero poderosa para gestionar y visualizar tus gastos personales. Disponible en dos versiones:

- **Versión Desktop**: Interfaz gráfica con `tkinter` y almacenamiento en CSV.
- **Versión Web**: Interfaz moderna con `Streamlit`, base de datos `SQLite`, gráficos por periodos y filtros avanzados.

---

## 🚀 Versiones Disponibles

### 1. [Versión Desktop (Tkinter + CSV)](desktop/)
> Ideal para uso local sin servidor.

- Interfaz gráfica simple.
- Almacena datos en un archivo `expenses.csv`.
- Gráfico de torta en tiempo real.

### 2. [Versión Web (Streamlit + SQLite)](web/)
> Ideal para acceso desde navegador, con más funcionalidades.

- Interfaz web moderna y responsive.
- Base de datos SQLite integrada.
- Filtros por fechas y categorías.
- Gráficos de barras por periodo (semanal/mensual/anual) + gráfico de torta del consumo total en el tiempo.
- Estadísticas rápidas (total, promedio).

---

## 📦 Requisitos

Ambas versiones requieren **Python 3.8 o superior**.

### Para la versión Desktop:
```bash
pip install -r desktop/requirements-desktop.txt
```
### Para la versión Web:
```bash
pip install -r web/requirements-web.txt
```