import pandas as pd
from scraper import get_data_from_page
from conexion import save_to_sqlite
import time
import random

def process_dnis(dnis):
    all_df_1 = []
    all_df_2 = []

    for dni in dnis:
        try:
            # Obtener los dataframes para cada DNI
            df_1, df_2 = get_data_from_page(dni)
            
            # Verificar si los dataframes no son None
            if df_1 is not None and df_2 is not None:
                all_df_1.append(df_1)
                all_df_2.append(df_2)
            else:
                print(f"No se pudo obtener datos para el DNI {dni}")

        except Exception as e:
            print(f"Error procesando el DNI {dni}: {e}")
        
        # Espera aleatoria entre solicitudes para evitar bloqueos
        time.sleep(random.uniform(5, 9))  # Espera de 3 a 7 segundos entre cada solicitud
    
    # Verificar si tenemos datos para concatenar
    if all_df_1 and all_df_2:
        try:
            # Concatenar los DataFrames de todos los DNIs
            final_df_1 = pd.concat(all_df_1, ignore_index=True)
            final_df_2 = pd.concat(all_df_2, ignore_index=True)

            return final_df_1, final_df_2
        
        except Exception as e:
            print(f"Error al concatenar los DataFrames: {e}")
            return None, None
    else:
        print("No se encontraron datos para ninguno de los DNIs.")
        return None, None


if __name__ == '__main__':
    # Lista de DNIs a procesar
    df_dnis = pd.read_csv(r'sunat\DNIs\dni.csv')
    dnis_list = df_dnis['dni'].astype('str').to_list()

    final_df_1, final_df_2 = process_dnis(dnis_list)

    save_to_sqlite(final_df_1, final_df_2)