
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
    #Eliminar Partidos que no se jugaron,["Ganador"]=="-" o esta vacio directamente Eliminar toda la fila
    df_total=df_total[df_total["Ganador"]!="-"]
    df_total=df_total[df_total["Ganador"]!=""]
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
