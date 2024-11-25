import sqlite3
import pandas as pd

def read_data_sql(PATH = r'sunat\bdd\database.db'):

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(PATH)

    # Leer las tablas en dos DataFrames diferentes
    df1 = pd.read_sql("SELECT * FROM tabla1", conn)
    df2 = pd.read_sql("SELECT * FROM tabla2", conn)
    # Cerrar conexión
    conn.close()

    return df1, df2

def save_data_sql():
    pass

# Guardar los DataFrames limpios en las tablas correspondientes
# df1.to_sql('tabla1', conn, if_exists='replace', index=False)  # Reemplaza la tabla1 con los datos limpios
# df2.to_sql('tabla2', conn, if_exists='replace', index=False)  # Reemplaza la tabla2 con los datos limpios

df1, df2 = read_data_sql()

print(df1)
print(df2)

print("Datos limpios guardados correctamente en la base de datos.")