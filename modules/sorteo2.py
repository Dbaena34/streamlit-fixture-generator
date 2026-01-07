# =========================
# 📁 Archivo: sorteo.py
# =========================
import os
import random
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------
# 🔹 Función 1: Cargar y mezclar equipos
# -----------------------------------------------------------
def preparar_equipos():
    equipos = [
        "Arsenal", "Aston Villa", "Chelsea", "Liverpool", "Manchester City", "Manchester United",
        "Tottenham", "West Ham", "Bayer Leverkusen", "Bayern Múnich", "Borussia Dortmund", "Milán",
        "Inter de Milán", "Juventus", "Roma", "Nápoli", "Atlético de Madrid", "Real Madrid", 
        "Barcelona", "PSG", "Inglaterra", "Portugal", "España", "Francia", "Holanda", "Italia", 
        "Alemania", "Brasil", "Argentina", "Colombia", "Newcastle", "Atalanta", "Betis", "Benfica",
        "Flamengo", "Bélgica"
    ]

    random.shuffle(equipos)
    if len(equipos) % 2 != 0:
        equipos.pop()
    return equipos

# -----------------------------------------------------------
# 🔹 Función 2: Jugar los partidos (modo terminal)
# -----------------------------------------------------------
def jugar_partidos(equipos):
    partidos = []
    victorias = {"Jugador 1": 0, "Jugador 2": 0}
    salir = False

    for i in range(0, len(equipos), 2):
        if salir:
            break

        local, visitante = random.choice(
            [("Jugador 1", "Jugador 2"), ("Jugador 2", "Jugador 1")]
        )

        print(f"\n{equipos[i]} (Local - {local}) vs. {equipos[i+1]} (Visitante - {visitante})")
        print("Para salir, escriba 'salir' cuando se le solicite un resultado.")
        
        goles_1 = goles_2 = None
        extra_1 = extra_2 = penales_1 = penales_2 = None

        while True:
            goles_1 = input(f"Ingrese los goles de {equipos[i]}: ")
            if goles_1.lower() == 'salir':
                salir = True
                break
            goles_2 = input(f"Ingrese los goles de {equipos[i+1]}: ")
            if goles_2.lower() == 'salir':
                salir = True
                break

            try:
                goles_1 = int(goles_1)
                goles_2 = int(goles_2)
            except ValueError:
                print("⚠️ Entrada inválida. Ingrese un número entero.")
                continue

            # Tiempo extra
            if goles_1 == goles_2:
                print("Empate! Se jugará tiempo extra.")
                while True:
                    extra_1 = input(f"Ingrese los goles de {equipos[i]} en tiempo extra: ")
                    if extra_1.lower() == 'salir':
                        salir = True
                        break
                    extra_2 = input(f"Ingrese los goles de {equipos[i+1]} en tiempo extra: ")
                    if extra_2.lower() == 'salir':
                        salir = True
                        break
                    
                    try:
                        extra_1 = int(extra_1)
                        extra_2 = int(extra_2)
                    except ValueError:
                        print("⚠️ Entrada inválida. Ingrese un número entero.")
                        continue

                    goles_1 += extra_1
                    goles_2 += extra_2

                    # Penales
                    if goles_1 == goles_2:
                        print("Sigue el empate! Se jugarán penales.")
                        while True:
                            penales_1 = input(f"Ingrese los penales convertidos por {equipos[i]}: ")
                            if penales_1.lower() == 'salir':
                                salir = True
                                break
                            penales_2 = input(f"Ingrese los penales convertidos por {equipos[i+1]}: ")
                            if penales_2.lower() == 'salir':
                                salir = True
                                break
                            
                            try:
                                penales_1 = int(penales_1)
                                penales_2 = int(penales_2)
                            except ValueError:
                                print("⚠️ Entrada inválida. Ingrese un número entero.")
                                continue
                            
                            if penales_1 > penales_2:
                                goles_1 += 1
                            else:
                                goles_2 += 1
                            break
                    break
            break

        if salir:
            break
        
        # Determinar ganador
        if goles_1 > goles_2:
            ganador = equipos[i]
            victorias[local] += 1
        elif goles_2 > goles_1:
            ganador = equipos[i+1]
            victorias[visitante] += 1
        else:
            ganador = "Empate"

        partido = {
            "Local": equipos[i], "Jugador Local": local, "Goles Local": goles_1,
            "Visitante": equipos[i+1], "Jugador Visitante": visitante, "Goles Visitante": goles_2,
            "Tiempo Extra Local": extra_1, "Tiempo Extra Visitante": extra_2,
            "Penales Local": penales_1, "Penales Visitante": penales_2,
            "Ganador": ganador
        }
        partidos.append(partido)

    return pd.DataFrame(partidos), victorias


# -----------------------------------------------------------
# 🔹 Función 3: Guardar resultados en Excel
# -----------------------------------------------------------
def guardar_resultados(df, victorias):
    fecha_actual = datetime.now().strftime("%d_%m_%y")
    ruta_directorio = os.path.join(os.path.expanduser("~"), "Desktop")
    ruta_archivo = os.path.join(ruta_directorio, f"Partidos_{fecha_actual}.xlsx")
    df.to_excel(ruta_archivo, index=False)
    return ruta_archivo


# -----------------------------------------------------------
# 🔹 Función 4: Mostrar resumen
# -----------------------------------------------------------
def mostrar_resumen(df, victorias, ruta):
    print("\n🏆 RONDA FINALIZADA 🏆")
    print("📊 Resultados finales:")
    for _, partido in df.iterrows():
        print(f"{partido['Local']} ({partido['Goles Local']}) vs. {partido['Visitante']} ({partido['Goles Visitante']}) → 🏅 Ganador: {partido['Ganador']}")
    print(f"\n📊 Total de victorias: {victorias}")
    if victorias['Jugador 1'] != victorias['Jugador 2']:
        print(f"🎖️ El jugador con más victorias fue: {max(victorias, key=victorias.get)}")
    else:
        print("🎖️ Hubo un empate en las victorias.")
    print(f"\n📂 Partidos guardados en: {ruta}")
