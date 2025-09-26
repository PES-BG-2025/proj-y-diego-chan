# 📊 GASTOCONTROLLER5000

Una aplicación sencilla pero poderosa para gestionar y visualizar tus gastos personales. Disponible en dos versiones:


- **Versión Web**: Interfaz moderna con `Streamlit`, base de datos `SQLite` y otra con CSV, gráficos por periodos y filtros avanzados.

---

## 🚀 Versiones Disponibles

### 1. [Versión Web (Streamlit + + CSV/SQLite)](web/)
> Ideal para acceso desde navegador, con más funcionalidades.

- Interfaz web moderna y responsive.
- Base de datos SQLite integrada. (version CSV:Almacena datos en un archivo `gastos.csv`.)
- Filtros por fechas y categorías.
- Gráficos de barras por periodo (semanal/mensual/anual) + gráfico de torta del consumo total en el tiempo.
- Estadísticas rápidas (total, promedio).

---

## 📦 Requisitos

Ambas versiones requieren **Python 3.8 o superior**.

### Para la versión Web:
```bash
pip install -r web/requirements-web.txt
```