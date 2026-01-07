# app.py
import streamlit as st
import pandas as pd
import io
from modules import sorteo as sor
from PIL import Image

import streamlit as st


# Cargar el logo (ruta relativa al directorio desde donde ejecutas streamlit)
logo = Image.open("images/Logo.png")

# Debe ser la PRIMERA llamada a Streamlit
st.set_page_config(page_title="🎲 Torneo de PES", page_icon=logo, layout="wide")


# 🎨 Fuentes y estilo retro
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# 💅 Tema visual personalizado
st.markdown("""
    <style>
    /* Fondo tipo estadio nocturno */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top, #0a0f24 0%, #000000 80%);
        
    }

    @keyframes glow-bg {
        0% {background: radial-gradient(circle at top, #0a0f24 0%, #000000 80%);}
        100% {background: radial-gradient(circle at top, #1a237e 0%, #000000 85%);}
    }

    /* Fuentes y colores */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        color: #00b0ff !important;
        
    }

    div.stButton > button {
        background: linear-gradient(90deg, #004ba0 0%, #d50000 100%);
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        box-shadow: 0px 0px 5px #2196f3;
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 10px #ff1744;
    }

    textarea, input, select {
        background-color: #121212 !important;
        color: #e0e0e0 !important;
        border-radius: 8px !important;
        border: 1px solid #303f9f !important;
    }

    </style>
""", unsafe_allow_html=True)

col9,col10=st.columns(2)

with col9:
    st.title("🏆 Torneo de PES")
    st.info("Este Proyecto es Patrocinado Por Azucar Manuelita, La mejor azucar del pais")
with col10:
    st.image(logo, width=120)


equipos_default = [
    "Arsenal", "Aston Villa", "Chelsea", "Liverpool", "Manchester City", "Manchester United",
    "Tottenham", "West Ham", "Bayer Leverkusen", "Bayern Múnich", "Borussia Dortmund", "Milán",
    "Inter de Milán", "Juventus", "Roma", "Nápoli", "Atlético de Madrid", "Real Madrid", 
    "Barcelona", "PSG", "Inglaterra", "Portugal", "España", "Francia", "Holanda", "Italia", 
    "Alemania", "Brasil", "Argentina", "Colombia", "Newcastle", "Atalanta", "Betis", "Benfica",
    "Flamengo", "Bélgica","Suiza","Dinamarca","Polonia","Serbia","Marruecos","Uruguay", "Atletico Nacional","A tu Eleccion"
]

st.divider()
col1, col2 = st.columns(2)

with col1:
    # ----- INPUT: equipos -----
    st.header("⚙️ Equipos participantes")
    equipos_text = st.text_area("Introduce los equipos (uno por línea):", value="\n".join(equipos_default), height=100)
    equipos = [e.strip() for e in equipos_text.splitlines() if e.strip()]

# ----- Session state -----
if "partidos" not in st.session_state:
    st.session_state.partidos = None
if "indice_partido" not in st.session_state:
    st.session_state.indice_partido = None
if "last_saved_path" not in st.session_state:
    st.session_state.last_saved_path = None

with col2:
    st.subheader("Realizar Sorteo")
    # ----- Botón para sortear -----
    if st.button("🎲 Realizar Sorteo"):
        if len(equipos) < 2:
            st.error("Necesitas al menos 2 equipos para hacer un sorteo.")
        else:
            st.session_state.partidos = sor.crear_sorteo(equipos)
            st.session_state.indice_partido = 0
            st.success("✅ Sorteo creado. Comienza el primer partido abajo.")

st.divider()

# ----- Mostrar partido actual -----
if st.session_state.partidos and st.session_state.indice_partido is not None:
    idx = st.session_state.indice_partido
    partido = st.session_state.partidos[idx]
    local = partido["Local"]
    visitante = partido["Visitante"]
    jugador_local = partido["Jugador Local"]
    jugador_visitante = partido["Jugador Visitante"]

    st.header(f"⚽ Partido {idx + 1} de {len(st.session_state.partidos)}")
    col3, col4 = st.columns(2)
    # Rutas a los avatares
    avatar_j1 = "images/Jugador 1.png"  # ajusta la ruta según tu carpeta
    avatar_j2 = "images/Jugador 2.png"

    # ---- LADO LOCAL ----
    with col3:
        escudo_local = sor.obtener_escudo(local)
        if escudo_local:
            col5, col6=st.columns(2)
            with col5:
                st.image(escudo_local, width=120)
            with col6:
                st.image(avatar_j1 if jugador_local == "Jugador 1" else avatar_j2, width=100)
        else:
            st.text("🏳️ Sin escudo")
        st.subheader(f"{local} ({jugador_local})")
        goles_local_str = st.selectbox(
            f"Goles - {local}",
            options=["–"] + [str(i) for i in range(0, 11)],
            key=f"golesL_{idx}"
        )

    # ---- LADO VISITANTE ----
    with col4:
        escudo_visit = sor.obtener_escudo(visitante)
        if escudo_visit:
            col7, col8=st.columns(2)
            with col7:
                st.image(escudo_visit, width=120)
            with col8:
                st.image(avatar_j1 if jugador_visitante == "Jugador 1" else avatar_j2, width=100)
        else:
            st.text("🏳️ Sin escudo")
        st.subheader(f"{visitante} ({jugador_visitante})")
        goles_visit_str = st.selectbox(
            f"Goles - {visitante}",
            options=["–"] + [str(i) for i in range(0, 11)],
            key=f"golesV_{idx}"
        )


    extra_local = extra_visit = penales_local = penales_visit = None

    # Solo proceder si ambos tienen un valor válido (no “–”)
    if goles_local_str != "–" and goles_visit_str != "–":
        goles_local = int(goles_local_str)
        goles_visit = int(goles_visit_str)

        # Mostrar tiempo extra solo si hay empate
        if goles_local == goles_visit:
            st.info("⚔️ Empate en los 90 minutos — se jugará tiempo extra.")
            with col3:
                extra_local_str = st.selectbox(
                    f"Tiempo extra - {local}",
                    options=["–"] + [str(i) for i in range(0, 6)],
                    key=f"extraL_{idx}"
                )
            with col4:
                extra_visit_str = st.selectbox(
                    f"Tiempo extra - {visitante}",
                    options=["–"] + [str(i) for i in range(0, 6)],
                    key=f"extraV_{idx}"
                )

            if extra_local_str != "–" and extra_visit_str != "–":
                extra_local = int(extra_local_str)
                extra_visit = int(extra_visit_str)

                # Si sigue empate, mostrar penales
                if extra_local == extra_visit:
                    st.warning("😬 Sigue el empate — se jugarán penales.")
                    with col3:
                        penales_local_str = st.selectbox(
                            f"Penales - {local}",
                            options=["–"] + [str(i) for i in range(0, 11)],
                            key=f"penalesL_{idx}"
                        )
                    with col4:
                        penales_visit_str = st.selectbox(
                            f"Penales - {visitante}",
                            options=["–"] + [str(i) for i in range(0, 11)],
                            key=f"penalesV_{idx}"
                        )

                    if penales_local_str != "–" and penales_visit_str != "–":
                        penales_local = int(penales_local_str)
                        penales_visit = int(penales_visit_str)
    else:
        goles_local = goles_visit = None

   # Botones para registrar o finalizar
    col_guardar, col_finalizar = st.columns(2)
    
    if goles_local is None or goles_visit is None:
        st.warning("⚠️ Debes ingresar al menos los goles de los 90 minutos.")
    else:
        # Si hay empate en 90 y no se han definido extras, detener
        if goles_local == goles_visit and extra_local is None and extra_visit is None:
            st.warning("⚠️ El partido está empatado, ingresa el resultado del tiempo extra.")
        elif goles_local == goles_visit and extra_local == extra_visit and penales_local is None and penales_visit is None:
            st.warning("⚠️ Ingrese el resultado de los penales para desempatar.")
        else:
            st.session_state.partidos = sor.registrar_resultado(
                st.session_state.partidos, idx,
                goles_local, goles_visit,
                extra_local, extra_visit,
                penales_local, penales_visit
            )
            st.session_state.indice_partido += 1
            st.rerun()

    with col_guardar:
        if st.button("💾 Registrar resultado"):
            st.session_state.partidos = sor.registrar_resultado(
            st.session_state.partidos, idx,
            goles_local, goles_visit,
            extra_local, extra_visit,
            penales_local, penales_visit
            )

            # Pasar al siguiente partido
            st.session_state.indice_partido += 1
            st.rerun()
            if st.session_state.indice_partido >= len(st.session_state.partidos):
                st.session_state.indice_partido = None
                st.success("🏁 ¡Todos los partidos fueron jugados!")

    with col_finalizar:
        if st.button("🏁 Finalizar torneo aquí"):
            # Marcar los partidos restantes como no jugados
            for i in range(st.session_state.indice_partido, len(st.session_state.partidos)):
                p = st.session_state.partidos[i]
                p.update({
                    "Goles Local": None,
                    "Goles Visitante": None,
                    "Tiempo Extra Local": None,
                    "Tiempo Extra Visitante": None,
                    "Penales Local": None,
                    "Penales Visitante": None,
                    "Ganador": None
                })
            st.session_state.indice_partido = None
            st.info("✅ El torneo se cerró en este punto. Los partidos restantes se marcaron como no jugados.")



# ----- Si todos los partidos fueron jugados -----
if st.session_state.partidos and st.session_state.indice_partido is None:
    st.header("📊 Resultados Finales")

    columnas = [
        "Local", "Jugador Local", "Goles Local",
        "Visitante", "Jugador Visitante", "Goles Visitante",
        "Tiempo Extra Local", "Tiempo Extra Visitante",
        "Penales Local", "Penales Visitante", "Ganador"
    ]
    df_final = pd.DataFrame(st.session_state.partidos, columns=columnas)
    st.dataframe(df_final)

    # Resumen de victorias
    vict = sor.calcular_victorias(st.session_state.partidos)
    st.subheader("🏅 Resumen de victorias")
    st.write(vict)
    if vict["Jugador 1"] > vict["Jugador 2"]:
        st.success("🥇 El jugador con más victorias fue **Jugador 1**")
    elif vict["Jugador 2"] > vict["Jugador 1"]:
        st.success("🥇 El jugador con más victorias fue **Jugador 2**")
    else:
        st.info("🤝 Hubo un empate en las victorias.")

    # Guardar resultados
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📂 Guardar resultados en disco"):
            try:
                ruta = sor.guardar_resultados(st.session_state.partidos)
                st.session_state.last_saved_path = ruta
                st.success(f"✅ Resultados guardados en: {ruta}")
            except Exception as e:
                st.error(f"Error guardando archivo: {e}")

    with col2:
        buffer = io.BytesIO()
        try:
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df_final.to_excel(writer, sheet_name="Partidos", index=False)
            buffer.seek(0)
            st.download_button(
                "⬇️ Descargar Excel",
                data=buffer,
                file_name="Partidos_streamlit.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"No se pudo crear el archivo para descargar: {e}")

st.subheader("ℹ️ Sobre esta aplicación")
st.markdown("""
Esta aplicación permite gestionar un torneo de PES (Pro Evolution Soccer) de manera sencilla e intuitiva. Algunas de las características incluyen:

- Registro de resultados de partidos.
- Visualización de estadísticas de jugadores.
- Descarga de resultados en formato Excel.

¡Disfruta de la experiencia de torneo!
""")

