
import pandas as pd
import os
import shutil

def pregunta_01():
    import pandas as pd
    import os

    # Crear directorio de salida
    os.makedirs('files/output', exist_ok=True)
    
    # Lectura del archivo
    data = pd.read_csv('files/input/solicitudes_de_credito.csv', sep=';', index_col=0)
    
    # Limpieza inicial
    data = data.dropna()
    
    # Estandarización de texto en columnas categóricas
    data['sexo'] = data['sexo'].str.lower()
    data['tipo_de_emprendimiento'] = data['tipo_de_emprendimiento'].str.lower()
    data['idea_negocio'] = data['idea_negocio'].str.lower()
    data['barrio'] = data['barrio'].str.lower()
    data['línea_credito'] = data['línea_credito'].str.lower()
    
    # Limpieza específica por columna
    data['barrio'] = data['barrio'].str.replace('_', ' ').str.replace('-', ' ')
    data['idea_negocio'] = data['idea_negocio'].str.replace('_', ' ').str.replace('-', ' ')
    data['línea_credito'] = data['línea_credito'].str.replace('_', ' ').str.replace('-', ' ')
    
    # Limpieza de monto del crédito
    data['monto_del_credito'] = data['monto_del_credito'].str.replace('$', '', regex=False)
    data['monto_del_credito'] = data['monto_del_credito'].str.replace(',', '', regex=False)
    data['monto_del_credito'] = data['monto_del_credito'].str.replace('.00', '', regex=False)
    data['monto_del_credito'] = data['monto_del_credito'].str.strip()
    data['monto_del_credito'] = pd.to_numeric(data['monto_del_credito'])
    
    # Procesamiento de fechas
    data['temp_fecha'] = pd.to_datetime(data['fecha_de_beneficio'], 
                                    dayfirst=True, 
                                    format='%d/%m/%Y', 
                                    errors='coerce')
    
    mask_alt_format = data['temp_fecha'].isna()
    if mask_alt_format.any():
        data.loc[mask_alt_format, 'temp_fecha'] = pd.to_datetime(
            data.loc[mask_alt_format, 'fecha_de_beneficio'],
            format='%Y/%m/%d',
            errors='coerce'
        )
    
    data['fecha_de_beneficio'] = data['temp_fecha'].dt.strftime('%Y-%m-%d')
    data = data.drop('temp_fecha', axis=1)
    
    # Eliminar filas con fechas inválidas y duplicados
    data = data.dropna()
    data = data.drop_duplicates()
    
    # Guardar el resultado
    data.to_csv('files/output/solicitudes_de_credito.csv', sep=';')
    
    return data

pregunta_01()