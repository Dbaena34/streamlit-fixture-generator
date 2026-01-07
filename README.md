# ⚽ App de Sorteo de Partidos y Gestión de Resultados

Aplicación desarrollada en **Streamlit** para realizar sorteos automáticos de partidos, asignando de forma aleatoria equipos, jugadores y localías. Permite además registrar resultados en tiempo real y exportarlos a Excel.

---

## 🛠️ Funcionamiento General

La aplicación se ejecuta como una app estándar de Streamlit (`streamlit run app.py`).

- Los equipos y jugadores están previamente definidos dentro del proyecto.
- Se valida que el número de equipos sea **par** para poder generar los enfrentamientos.
- El sorteo asigna:
  - Equipos
  - Jugadores
  - Localía (local / visitante)  
  todo de forma aleatoria, evitando que siempre el mismo jugador quede como local.

Una vez realizado el sorteo:
- Los partidos se muestran en dos columnas (izquierda y derecha).
- Se visualizan las **imágenes de los jugadores** correspondientes.
- Los resultados se ingresan mediante campos numéricos.
- Los datos se **guardan automáticamente**.
- Los partidos pueden exportarse a un archivo **Excel (.xlsx)**.

---

## 📂 Estructura del Proyecto
  ├── app.py
  ├── requirements.txt
  ├── modules/
  │ ├── init.py
  │ └── sorteo.py
  ├── images/
  ├── Resultados/


### Descripción de archivos y carpetas

- **`app.py`**  
  Archivo principal. Maneja la interfaz con Streamlit, muestra los sorteos, imágenes y captura los resultados.

- **`modules/sorteo.py`**  
  Contiene la lógica del sorteo:
  - Aleatoriedad de equipos y jugadores
  - Validación de cantidad par
  - Gestión de fechas y nombres de archivos
  - Preparación de datos para exportación

- **`images/`**  
  Carpeta con las imágenes de los jugadores utilizadas durante el sorteo.

- **`Resultados/`**  
  Carpeta donde se guardan automáticamente los archivos Excel generados.

---

## 🚀 Ejecución del Proyecto

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPO>

2. Instalar dependencias:

  pip install -r requirements.txt

3. Ejecutar la aplicación:

  streamlit run app.py

## 📦 Exportación de Resultados
  -Los partidos sorteados y sus marcadores se exportan en formato Excel (.xlsx).
  -Cada archivo queda almacenado en la carpeta Resultados/.
  -Se evita la sobrescritura utilizando fecha y hora en el nombre del archivo.

