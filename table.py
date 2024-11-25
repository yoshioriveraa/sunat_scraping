# Funciones relacionadas con la creación de DataFrames.
import pandas as pd

def create_dataframe(ruc_nombre, ubicacion_estado, fecha_consulta):
    ruc = ruc_nombre[0].split(": ")[1]  
    nombre_completo = ruc_nombre[1]  
    ubicacion = ubicacion_estado[0].split(": ")[1]  
    estado = ubicacion_estado[1].split(": ")[1]  
    fecha = fecha_consulta[0].split(": ")[1]  

    data = {
        'RUC': [ruc],
        'Nombre Completo': [nombre_completo],
        'Ubicación': [ubicacion],
        'Estado': [estado],
        'Fecha de Consulta': [fecha]
    }

    return pd.DataFrame(data)



