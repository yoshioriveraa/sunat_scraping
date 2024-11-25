import sqlite3
import pandas as pd

# Función para leer datos de la base de datos SQLite
def read_data_sql(PATH=r'bdd/database.db'):
    """
    Lee datos desde una base de datos SQLite y devuelve dos DataFrames.
    """
    conn = sqlite3.connect(PATH)
    df1 = pd.read_sql("SELECT * FROM tabla1", conn)
    df2 = pd.read_sql("SELECT * FROM tabla2", conn)
    conn.close()
    return df1, df2


# Función para limpiar columnas de los DataFrames
def clean_column_names(df, replace_colon=False):
    """
    Limpia y estandariza los nombres de las columnas de un DataFrame.
    """
    df.columns = (
        df.columns.str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace(":", "" if replace_colon else ":", regex=False)
    )
    return df

# Función para transformar los datos del DataFrame df2
def transform_df2(df2):
    """
    Realiza transformaciones específicas en el DataFrame df2.
    """
    # Dividir 'tipo_de_documento' en 'tipo' y 'resto'
    df2['tipo'] = df2['tipo_de_documento'].apply(lambda x: x.split(' ', 1)[0])
    df2['resto'] = df2['tipo_de_documento'].apply(lambda x: x.split(' ', 1)[1])

    # Dividir 'resto' en 'numero_de_documento' y 'nombre_completo'
    df2['numero_de_documento'] = df2['resto'].apply(lambda x: x.split(' - ', 1)[0])
    df2['nombre_completo'] = df2['resto'].apply(lambda x: x.split(' - ', 1)[1])

    # Eliminar columnas innecesarias
    df2 = df2.drop(columns=['tipo_de_documento', 'resto'])

    # Renombrar columnas
    df2 = df2.rename(columns={'tipo': 'tipo_de_documento'})

    # Limpiar texto en 'estado_del_contribuyente'
    df2["estado_del_contribuyente"] = df2["estado_del_contribuyente"].str.replace(
        r"\nFecha de Baja:.*", "", regex=True
    ).str.strip()

    # Convertir fechas al formato estándar ISO
    date_columns = ["fecha_de_inscripción", "fecha_de_inicio_de_actividades"]
    for col in date_columns:
        df2[col] = pd.to_datetime(df2[col], format="%d/%m/%Y", errors="coerce")

    # Ordenar y renombrar columnas
    columns_order = [
        "tipo_contribuyente", "tipo_de_documento", "numero_de_documento", 
        "nombre_completo", "nombre_comercial", "fecha_de_inscripción", 
        "fecha_de_inicio_de_actividades", "estado_del_contribuyente", 
        "condición_del_contribuyente", "domicilio_fiscal", 
        "sistema_emisión_de_comprobante", "actividad_comercio_exterior", 
        "sistema_contabilidad", "actividad(es)_económica(s)", 
        "comprobantes_de_pago_c/aut._de_impresión_(f._806_u_816)", 
        "sistema_de_emisión_electrónica", "emisor_electrónico_desde", 
        "comprobantes_electrónicos", "afiliado_al_ple_desde", "padrones"
    ]
    df2 = df2[columns_order]

    # Renombrar columnas para mayor claridad
    rename_columns = {
        'fecha_de_inscripción': 'fecha_inscripcion',
        'fecha_de_inicio_de_actividades': 'fecha_inicio_actividades',
        'estado_del_contribuyente': 'estado',
        'condición_del_contribuyente': 'condicion',
        'sistema_emisión_de_comprobante': 'emision_comprobante',
        'actividad_comercio_exterior': 'comercio_exterior',
        'sistema_contabilidad': 'contabilidad',
        'actividad(es)_económica(s)': 'actividad_economica',
        'comprobantes_de_pago_c/aut._de_impresión_(f._806_u_816)': 'comprobantes_impresos',
        'sistema_de_emisión_electrónica': 'emision_electronica',
        'emisor_electrónico_desde': 'emisor_electronico_desde',
        'comprobantes_electrónicos': 'comprobantes_electronicos',
        'afiliado_al_ple_desde': 'afiliado_ple_desde',
        'tipo_de_documento': 'tipo_documento',
        'numero_de_documento': 'documento',
        'nombre_completo': 'nombre'
    }
    df2 = df2.rename(columns=rename_columns)
    return df2

# Función para guardar los datos limpios en la base de datos
def save_data_sql(df1, df2, PATH=r'bdd/database.db'):
    """
    Guarda los DataFrames limpios en las tablas correspondientes en SQLite.
    """
    conn = sqlite3.connect(PATH)
    df1.to_sql('tabla1', conn, if_exists='replace', index=False)
    df2.to_sql('tabla2', conn, if_exists='replace', index=False)
    conn.close()
    print("Datos limpios guardados correctamente en la base de datos.")