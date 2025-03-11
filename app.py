import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import ollama

# Configurar acceso a Google Sheets
def conectar_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Leer credenciales desde el archivo JSON
    creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
    client = gspread.authorize(creds)

    # Abrir la hoja de cálculo (CAMBIA EL NOMBRE A TU HOJA)
    spreadsheet = client.open("data")
    worksheet = spreadsheet.worksheet("data")

    # Convertir los datos en un DataFrame de Pandas
    pd.set_option('display.max_columns', None)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    return df

# Función para generar respuesta con DeepSeek-R1
def generar_respuesta(pregunta, datos):
    # Convertir datos a string para el modelo
    datos_texto = datos.to_csv(index=False)

    important_prompt= "Eres un analista de datos experto en criminologia y estadistica. Tu tarea es responder a las preguntas de los usuarios en base al dataset proporcionado"

    # Crear el mensaje para DeepSeek-R1
    mensaje = f"""
    Contexto:
    Tengo un dataset sobre homicidios en Perú con las siguientes columnas:
    
    - **NRO_CASO**: Número de caso o nombre del caso, (casos que existen) si encuentras casos con el mismo nombre significa que pertenecen al mismo caso
    - **ESTADO_CASO**: Estado del caso (ej. 'PENDIENTE', 'RESUELTO').
    - **TIPO**: Tipo de delito. (ej. 'DELITO CONTRA LA VIDA EL CUERPO Y LA SALUD')
    - **SUBTIPO**: Subtipo del delito (ej. 'HOMICIDIO').
    - **MODALIDAD**: Modalidad del caso (ej. 'SICARIATO','HOMICIDIO CALIFICADO POR PAF').
    - **MOVIL**: Motivo del crimen (ej. 'AJUSTE DE CUENTA').
    - **MEDIO_EMPLEADO**: Arma utilizada en el crimen.
    - **ZONA_CADAVER**: Lugar donde se halló el cadáver.
    - **NRO_DIA**: Día numérico del mes en que ocurrió el caso.
    - **DIA**: Día de la semana del caso.
    - **MES**: Mes del caso.
    - **AÑO**: Año del caso.
    - **HORA**: Hora del caso.
    - **FECHA_HECHO**: Fecha completa del caso.
    - **SITUACION_PERSONA**: Estado de la víctima (ej. 'VICTIMA','PRESUNTO AUTOR').
    - **EDAD**: Edad de la víctima.
    - **ESTADO_CIVIL**: Estado civil de la víctima.
    - **DELINCUENTE**: ¿La víctima era delincuente? (Sí/No).
    - **SEXO**: Género de la víctima.
    - **PAIS_NATAL**: Nacionalidad de la víctima.
    - **DEPARTAMENTO_HECHO**: Departamento donde ocurrió el caso.
    - **PROVINCIA_HECHO**: Provincia donde ocurrió el caso.
    - **DISTRITO_HECHO**: Distrito donde ocurrió el caso.
    - **CONO_HECHO**: Zona de Lima donde ocurrió (Ej. 'Norte', 'Sur', etc.).
    - **UNIDAD_A_CARGO**: Unidad policial a cargo del caso.
    - **NRO_IMPACTOS**: Número de impactos de bala (si aplica).
    - **NRO_PRESUNTOS_AUTORES**: Cantidad de presuntos responsables.
    - **VEHICULO_UTILIZADO**: Tipo de vehículo usado en el crimen (si aplica).
    {datos_texto}

    Pregunta del usuario:
    {pregunta}

    Analiza siempre en base a las columnas que te di, dame la respuesta completa en base a lo que dice la celda.
    """

    # Consultar a DeepSeek-R1 en Ollama
    respuesta = ollama.chat(model="llama3.2", messages=[{"role": "system", "content": important_prompt}
                                                           ,{"role": "user", "content": mensaje}])
    
    return respuesta['message']['content']


# Interfaz de Chat con Streamlit
def main():
    st.title("💬 Homicidios 2024 - Septiembre")
    st.write("Soy un version gratuita y tendré varios errores. ")
    st.write("TE ACONSEJO QUE SEAS BASTANTE EXPLICITO Y ME INDIQUES CON CLARIDAD LO QUE NECESITAS. ")

    # Inicializar sesión de chat si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Cargar datos desde Google Sheets
    datos = conectar_google_sheets()

        # Mostrar los datos en Streamlit
    st.write("Vista previa de los datos:", datos.head(20))

    # Mostrar mensajes anteriores en el chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Entrada de usuario
    pregunta = st.chat_input("Escribe tu pregunta aquí...")

    if pregunta:
        # Agregar la pregunta al historial del chat
        st.session_state.messages.append({"role": "user", "content": pregunta})

        # Mostrar la pregunta en el chat
        with st.chat_message("user"):
            st.markdown(pregunta)

        # Generar respuesta usando la IA y los datos
        respuesta = generar_respuesta(st.session_state.messages, datos)

        # Agregar la respuesta al historial del chat
        st.session_state.messages.append({"role": "assistant", "content": respuesta})

        # Mostrar la respuesta en el chat
        with st.chat_message("assistant"):
            st.markdown(respuesta)

if __name__ == "__main__":
    main()