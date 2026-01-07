# sorteo.py
import os
import random
import pandas as pd
from datetime import datetime


def mezclar_equipos(equipos):
    """Mezcla los equipos y elimina uno si hay número impar."""
    random.shuffle(equipos)
    if len(equipos) % 2 != 0:
        equipos.pop()
    return equipos

def crear_sorteo(equipos):
    """Crea los partidos aleatorios y asigna jugadores local/visitante."""
    equipos = mezclar_equipos(equipos)
    partidos = []

    for i in range(0, len(equipos), 2):
        # Asignar aleatoriamente quién es local y quién visitante
        if random.choice([True, False]):
            jugador_local, jugador_visitante = "Jugador 1", "Jugador 2"
        else:
            jugador_local, jugador_visitante = "Jugador 2", "Jugador 1"

        partidos.append({
            "Local": equipos[i],
            "Jugador Local": jugador_local,
            "Goles Local": None,
            "Visitante": equipos[i + 1],
            "Jugador Visitante": jugador_visitante,
            "Goles Visitante": None,
            "Tiempo Extra Local": None,
            "Tiempo Extra Visitante": None,
            "Penales Local": None,
            "Penales Visitante": None,
            "Ganador": None
        })

    return partidos

def procesar_partido(partido, goles_local, goles_visitante,
                     extra_local=None, extra_visitante=None,
                     penales_local=None, penales_visitante=None):
    """
    Aplica toda la lógica del partido, incluyendo tiempo extra y penales.
    - Mantiene 'Goles Local'/'Goles Visitante' como los goles en los 90'.
    - Guarda 'Tiempo Extra ...' y 'Penales ...' por separado.
    - Determina el ganador usando totales (90' + extra) y penales si aplica,
      pero SIN mutar los campos de los 90'.
    - Los parámetros extra_* y penales_* pueden ser None si no se jugaron.
    """

    # Asegurar tipos: si son None dejamos None (no los convertimos a 0 aquí)
    gl_90 = goles_local
    gv_90 = goles_visitante

    # Totales para decidir ganador (no para sobrescribir los 90')
    total_local = gl_90 if gl_90 is not None else 0
    total_visitante = gv_90 if gv_90 is not None else 0

    # Si hubo tiempo extra (explicitado como número), sumarlo a los totales
    if extra_local is not None and extra_visitante is not None:
        total_local += extra_local
        total_visitante += extra_visitante

    # Si después del extra sigue empate y hubo penales, decidir por penales
    ganador = None
    if total_local == total_visitante:
        # Si se proporcionaron penales válidos, usarlos
        if penales_local is not None and penales_visitante is not None:
            if penales_local > penales_visitante:
                ganador = partido["Local"]
            elif penales_visitante > penales_local:
                ganador = partido["Visitante"]
            else:
                ganador = "Empate"
        else:
            # Si no hubo penales y sigue el empate, declarar empate
            ganador = "Empate"
    else:
        # Decidir por quien tenga mayor total (90' + extra si aplica)
        ganador = partido["Local"] if total_local > total_visitante else partido["Visitante"]

    # Actualizar partido SIN modificar gl_90/gv_90
    partido.update({
        "Goles Local": gl_90,
        "Goles Visitante": gv_90,
        "Tiempo Extra Local": extra_local,
        "Tiempo Extra Visitante": extra_visitante,
        "Penales Local": penales_local,
        "Penales Visitante": penales_visitante,
        "Ganador": ganador
    })

    return partido

def registrar_resultado(partidos, indice, goles_local, goles_visitante,
                        extra_local=None, extra_visitante=None,
                        penales_local=None, penales_visitante=None):

    """Actualiza un partido dentro de la lista de partidos."""
    partidos[indice] = procesar_partido(
        partidos[indice],
        goles_local, goles_visitante,
        extra_local, extra_visitante,
        penales_local, penales_visitante
    )
    return partidos


def guardar_resultados(partidos):
    """Guarda los resultados en Excel con las mismas columnas del original."""
    columnas = [
        "Local", "Jugador Local", "Goles Local",
        "Visitante", "Jugador Visitante", "Goles Visitante",
        "Tiempo Extra Local", "Tiempo Extra Visitante",
        "Penales Local", "Penales Visitante", "Ganador"
    ]
    df = pd.DataFrame(partidos, columns=columnas)

    fecha_actual = datetime.now().strftime("%d_%m_%y")
    ruta_directorio = r"A:\PES\Resultados"
    ruta_archivo = os.path.join(ruta_directorio, f"Partidos_{fecha_actual}.xlsx")
    df.to_excel(ruta_archivo, index=False)

    return ruta_archivo


def calcular_victorias(partidos):
    """Cuenta las victorias de cada jugador."""
    victorias = {"Jugador 1": 0, "Jugador 2": 0}

    for p in partidos:
        if p["Ganador"] == p["Local"]:
            victorias[p["Jugador Local"]] += 1
        elif p["Ganador"] == p["Visitante"]:
            victorias[p["Jugador Visitante"]] += 1

    return victorias

import os
from PIL import Image

def obtener_escudo(nombre_equipo):
    """Devuelve la ruta del escudo si existe, o None."""
    base_path = os.path.join(r"A:\PES", "images")
    for ext in [".png", ".jpg", ".jpeg", ".webp"]:
        posible = os.path.join(base_path, f"{nombre_equipo}{ext}")
        if os.path.exists(posible):
            return posible
    return None
