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
    # Convertir datos a texto en formato CSV
    datos_texto = datos.to_csv(index=False)

    important_prompt= "Eres un analista de datos experto en criminologia y estadistica. Tu tarea es responder a las preguntas de los usuarios en base al dataset proporcionado"

    # Crear el mensaje para DeepSeek-R1
    mensaje = f"""
    Contexto:
    Tengo un dataset ordenado por fechas y con las siguientes columnas:
    
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

    Analiza siempre al dataset y la descripcion de las columnas que te proporcioné.
    """

    # Consultar a DeepSeek-R1 en Ollama
    respuesta = ollama.chat(model="llama3.2", messages=[{"role": "system", "content": important_prompt}
                                                           ,{"role": "user", "content": mensaje}])
    
    return respuesta['message']['content']

# Función para ejecutar el chat en consola
def chat():
    print("\n💬 Homicidios 2024 - Septiembre")
    print("Escribe 'salir' para terminar la conversación.\n")

    # Cargar datos desde Google Sheets
    datos = conectar_google_sheets()
    print("📊 Datos cargados correctamente.\n")

    print(datos.head(5))

    while True:
        pregunta = input("Tú: ")

        if pregunta.lower() in ["salir", "exit", "quit"]:
            print("Asistente: Hasta luego. 👋")
            break

        respuesta = generar_respuesta(pregunta, datos)
        print(f"Asistente: {respuesta}\n")

# Ejecutar el chat
if __name__ == "__main__":
    chat()
