
import os
import re
import glob
import time
import requests,random
import pandas as pd
from googletrans import Translator

def limpiar_fecha(fecha_timestamp):
        # Formato seguro para nombre de archivo
        return fecha_timestamp.strftime("%Y-%m-%d_%H-%M")

#   Unificar Resultados
# ----------------------------
def unificar_resultados(ruta):
    archivos_xlsx = glob.glob(os.path.join(ruta, "*.xlsx"))
    lista_df = [pd.read_excel(f) for f in archivos_xlsx]
    df_total = pd.concat(lista_df, ignore_index=True)
    return df_total

# ----------------------------
#   Formatear Fecha y Hora
# ----------------------------
def formatear_fecha_hora(df):
    df['FechaHora'] = pd.to_datetime(df['FechaHora'], errors='coerce')
    df['Fecha'] = df['FechaHora'].dt.date
    df['Hora'] = df['FechaHora'].dt.strftime('%H:%M')
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M').dt.time
    df['Hora'] = df['Hora'].apply(lambda x: x.strftime('%H:%M') if pd.notnull(x) else x)
    columnas = ['Fecha', 'Hora'] + [col for col in df.columns if col not in ['Fecha', 'Hora', 'FechaHora']]
    df = df[columnas]
    df = df.sort_values(by=['Fecha', 'Hora']).reset_index(drop=True)
    return df

# ----------------------------
#   Eliminar Duplicados
# ----------------------------
def eliminar_duplicados(df):
    df = df.drop_duplicates(subset=['Fecha', 'Hora', 'Equipo1', 'Jugador1', 'Equipo2', 'Jugador2'], keep='last')
    return df

# ----------------------------
#   Guardar CSV
# ----------------------------
def guardar_resultado_unificado(df, mes, año, mes_n):
    nombre_archivo = f'Resumen_{mes}_{año}.csv'
    ruta_salida1 = fr"2_Resultados\\{mes_n}_{mes}_{año}\\Resumen"
    ruta_salida2 = fr"3_Trabajo_Datos\\Resumenes"
    os.makedirs(ruta_salida1, exist_ok=True)
    os.makedirs(ruta_salida2, exist_ok=True)
    df.to_csv(os.path.join(ruta_salida1, nombre_archivo), index=False, encoding='utf-8-sig')
    df.to_csv(os.path.join(ruta_salida2, nombre_archivo), index=False, encoding='utf-8-sig')

# --------------------------
# Función Principal de Análisis
# --------------------------
def analizar_resultados(ruta_carpeta, nombre_archivo=None, exportar=False, mes=None, año=None):
    
    dic_equipos, dic_jugadores = cargar_diccionarios()

    # Leer archivo CSV
    if nombre_archivo is None:
        archivos = [f for f in os.listdir(ruta_carpeta) if f.endswith('.csv')]
        if len(archivos) == 0:
            raise FileNotFoundError("No se encontraron archivos CSV en la carpeta.")
        elif len(archivos) > 1:
            raise ValueError(f"Hay más de un archivo CSV en la carpeta: {archivos}")
        else:
            nombre_archivo = archivos[0]
    
    ruta = os.path.join(ruta_carpeta, nombre_archivo)
    df = pd.read_csv(ruta)

    # Verificar columnas
    for col in ['Goles1', 'Goles2']:
        if col not in df.columns:
            raise ValueError(f"Falta la columna '{col}' en el archivo.")

    # --------------------------
    # Cálculo de columnas
    # --------------------------
    df['Resultado'] = df.apply(lambda x: 
        'Gana Equipo1' if x['Goles1'] > x['Goles2'] 
        else 'Gana Equipo2' if x['Goles1'] < x['Goles2'] 
        else 'Empate', axis=1)
    
    df['Team_Ganador'] = df.apply(lambda x:
        x['Equipo1'] if x['Goles1'] > x['Goles2']
        else x['Equipo2'] if x['Goles1'] < x['Goles2']
        else 'Empate', axis=1)
    
    df['Jugador_Ganador'] = df.apply(lambda x:
        x['Jugador1'] if x['Goles1'] > x['Goles2']
        else x['Jugador2'] if x['Goles1'] < x['Goles2']
        else 'Empate', axis=1)

    df['DiferenciaGoles'] = abs(df['Goles1'] - df['Goles2'])
    df['TotalGoles'] = df['Goles1'] + df['Goles2']
    df['Marcador_Ordenado'] = df[['Goles1', 'Goles2']].min(axis=1).astype(str) + '-' + df[['Goles1', 'Goles2']].max(axis=1).astype(str)
    df['SoloFecha'] = pd.to_datetime(df['Fecha']).dt.date
    df['PartidoNro'] = df.index + 1
    df['ResultadoCodificado'] = df['Resultado'].map({'Empate': 0, 'Gana Equipo1': 1, 'Gana Equipo2': 2})
    

    # --------------------------
    # Unión con diccionarios
    # --------------------------
    df = df.merge(dic_equipos, left_on='Equipo1', right_on='Equipo', how='left').rename(columns={'Equipo_ID': 'Equipo_x_ID'})
    df = df.merge(dic_equipos, left_on='Equipo2', right_on='Equipo', how='left').rename(columns={'Equipo_ID': 'Equipo_y_ID'})
    df = df.merge(dic_jugadores, left_on='Jugador1', right_on='Jugador', how='left').rename(columns={'Jugador_ID': 'Jugador_x_ID'})
    df = df.merge(dic_jugadores, left_on='Jugador2', right_on='Jugador', how='left').rename(columns={'Jugador_ID': 'Jugador_y_ID'})
    
    # --------------------------
    # IDs Ganador y Perdedor
    # --------------------------
    df['ID_Jugador_Ganador'] = df.apply(lambda x:
        x['Jugador_x_ID'] if x['Jugador_Ganador'] == x['Jugador1']
        else x['Jugador_y_ID'] if x['Jugador_Ganador'] == x['Jugador2']
        else 0, axis=1)

    df['ID_Team_Ganador'] = df.apply(lambda x:
        x['Equipo_x_ID'] if x['Team_Ganador'] == x['Equipo1']
        else x['Equipo_y_ID'] if x['Team_Ganador'] == x['Equipo2']
        else 0, axis=1)

    # Perdedor
    df['Team_Perdedor'] = df.apply(lambda x:
        x['Equipo2'] if x['Goles1'] > x['Goles2']
        else x['Equipo1'] if x['Goles1'] < x['Goles2']
        else 'Empate', axis=1)

    df['Jugador_Perdedor'] = df.apply(lambda x:
        x['Jugador2'] if x['Goles1'] > x['Goles2']
        else x['Jugador1'] if x['Goles1'] < x['Goles2']
        else 'Empate', axis=1)

    df['ID_Team_Perdedor'] = df.apply(lambda x:
        x['Equipo_x_ID'] if x['Team_Perdedor'] == x['Equipo1']
        else x['Equipo_y_ID'] if x['Team_Perdedor'] == x['Equipo2']
        else 0, axis=1)

    df['ID_Jugador_Perdedor'] = df.apply(lambda x:
        x['Jugador_x_ID'] if x['Jugador_Perdedor'] == x['Jugador1']
        else x['Jugador_y_ID'] if x['Jugador_Perdedor'] == x['Jugador2']
        else 0, axis=1)

    # --------------------------
    # Eliminar columnas duplicadas y ordenar
    # --------------------------
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.sort_values(by=['Fecha', 'Hora']).reset_index(drop=True)

    # --------------------------
    # Resumen resultados
    # --------------------------
    resumen_resultados = df['Resultado'].value_counts()

    # --------------------------
    # Exportar si se solicita
    # --------------------------
    if exportar:
        if mes is None or año is None:
            raise ValueError("Para exportar debes especificar mes y año.")
        
        nombre_csv = f"Total_{mes}_{año}.csv"
        ruta_salida = r"3_Trabajo_Datos\Totales"
        os.makedirs(ruta_salida, exist_ok=True)
        ruta_completa = os.path.join(ruta_salida, nombre_csv)
        df.to_csv(ruta_completa, index=False, encoding='utf-8-sig')
        print(f"✅ Archivo exportado: {ruta_completa}")

    return df, resumen_resultados
