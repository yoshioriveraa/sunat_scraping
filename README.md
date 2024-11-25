# Proyecto de Scraping y Limpieza de Datos

Este proyecto permite realizar scraping de datos desde un sitio web público utilizando Selenium, procesar los datos obtenidos, limpiarlos utilizando Pandas y almacenarlos en una base de datos SQLite.

## Estructura del Proyecto
- **clean.py**: Contiene funciones para la limpieza de los datos obtenidos.
- **conexion.py**: Maneja la conexión a la base de datos SQLite.
- **scraper.py**: Realiza el scraping de datos desde el sitio web.
- **table.py**: Contiene funciones relacionadas con las tablas de la base de datos.
- **main.py**: Script principal que orquesta todo el proceso.

## Requisitos
1. Python 3.x
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
