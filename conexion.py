import sqlite3

def save_to_sqlite(df_1, df_2, db_name='bdd\\database.db'):
    """
    Guarda los DataFrames en una base de datos SQLite.

    :param df_1: Primer DataFrame a guardar
    :param df_2: Segundo DataFrame a guardar
    :param db_name: Nombre del archivo de la base de datos (por defecto es 'database.db')
    """
    # Conectar a la base de datos SQLite (se crea si no existe)
    conn = sqlite3.connect(db_name)
    
    try:
        if df_1 is not None and df_2 is not None:
            try:
                # Intenta guardar en la base de datos si ambos DataFrames tienen datos
                df_1.to_sql('bdd\\tabla1', conn, if_exists='replace', index=False)
                df_2.to_sql('bdd\\tabla2', conn, if_exists='replace', index=False)
            except Exception as e:
                print(f"Error al guardar los DataFrames: {e}")
        else:
            print("No se obtuvieron datos, no se guardará nada.")

        
        print("DataFrames guardados exitosamente en la base de datos.")
    except Exception as e:
        print(f"Ocurrió un error al guardar los DataFrames: {e}")
    finally:
        # Cerrar la conexión a la base de datos
        conn.close()

# Ejemplo de uso
# save_to_sqlite(df_1, df_2)
