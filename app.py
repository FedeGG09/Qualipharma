import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
import os
from document_analysis import *  # Importa todas las funciones del análisis de documentos

# Configuración de la aplicación
st.set_page_config(page_title="🤗💬 HugChat")

# Barra lateral
with st.sidebar:
    st.title('🤗💬 HugChat')

# Almacenamiento de respuestas generadas por el LLM
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Mostrar o limpiar mensajes del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Función para generar respuestas del LLM
def generate_response(prompt_input, email, passwd):
    # Login en Hugging Face
    sign = Login(email, passwd)
    cookies = sign.login()
    # Crear ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    for dict_message in st.session_state.messages:
        string_dialogue = "You are a helpful assistant."
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    prompt = f"{string_dialogue} {prompt_input} Assistant: "
    return chatbot.chat(prompt)

# Funcionalidades adicionales para la carga y análisis de documentos
def load_manual(tokens_referencia):
    st.write("Cargando y vectorizando manual...")
    ruta_manual = cargar_y_vectorizar_manual(uploaded_reference_file, reference_file_type, tokens_referencia)
    st.write(f"Manual vectorizado y guardado en {ruta_manual}")

def compare_documents():
    st.write("Comparando documentos...")
    texto_comparar = extraer_texto_pdf(uploaded_compare_file)
    texto_referencia = extraer_texto_pdf(uploaded_reference_file)
    diferencias = encontrar_diferencias(texto_comparar, texto_referencia)
    
    if diferencias:
        diferencias_vectorizadas = vectorizar_y_tokenizar_diferencias(diferencias, tokens_referencia, uploaded_compare_file.name, uploaded_reference_file.name)
        st.success("Las diferencias entre los documentos han sido encontradas y vectorizadas.")
        
        # Mostrar diferencias
        st.header("Diferencias Encontradas")
        diferencias_tabla = []
        for diferencia in diferencias:
            diferencias_tabla.append([diferencia[0], diferencia[1], diferencia[2], diferencia[3]])
        st.table(diferencias_tabla)
    else:
        st.info("No se encontraron diferencias entre los documentos.")

def verify_file_compliance(tokens_referencia):
    st.write("Verificando cumplimiento del archivo...")
    # Lógica de verificación de cumplimiento aquí

# Menú de opciones
st.sidebar.header("Opciones")
option = st.sidebar.selectbox("Selecciona una opción", ["Comparar Documentos", "Cargar y Vectorizar Manual", "Verificar Cumplimiento de Archivo"])

if option == "Comparar Documentos":
    compare_documents()
elif option == "Cargar y Vectorizar Manual":
    tokens_referencia = tokenizar_lineamientos([extraer_texto_pdf(uploaded_reference_file)])
    load_manual(tokens_referencia)
elif option == "Verificar Cumplimiento de Archivo":
    tokens_referencia = tokenizar_lineamientos([extraer_texto_pdf(uploaded_reference_file)])
    verify_file_compliance(tokens_referencia)

# Interfaz Streamlit (continuación)
st.title("Herramienta de Análisis de Documentos")

# Cargar archivo de referencia
st.header("Cargar Manual de Referencia")
uploaded_reference_file = st.file_uploader("Subir archivo de referencia", type=["pdf", "txt", "docx"])
if uploaded_reference_file:
    reference_file_type = uploaded_reference_file.name.split(".")[-1]
    st.success(f"Archivo de referencia {uploaded_reference_file.name} cargado con éxito.")

# Cargar archivo a comparar
st.header("Cargar Documento a Comparar")
uploaded_compare_file = st.file_uploader("Subir archivo a comparar", type=["pdf", "txt", "docx"])
if uploaded_compare_file:
    compare_file_type = uploaded_compare_file.name.split(".")[-1]
    st.success(f"Archivo a comparar {uploaded_compare_file.name} cargado con éxito.")

if uploaded_reference_file and uploaded_compare_file:
    tokens_referencia = tokenizar_lineamientos([extraer_texto_pdf(uploaded_reference_file)])
    
    referencia_vectorizada_csv = cargar_y_vectorizar_manual(uploaded_reference_file, reference_file_type, tokens_referencia)
    if referencia_vectorizada_csv:
        st.success("El manual de referencia ha sido vectorizado y almacenado.")

    texto_comparar = extraer_texto_pdf(uploaded_compare_file)
    texto_referencia = extraer_texto_pdf(uploaded_reference_file)
    diferencias = encontrar_diferencias(texto_comparar, texto_referencia)
    
    if diferencias:
        diferencias_vectorizadas = vectorizar_y_tokenizar_diferencias(diferencias, tokens_referencia, uploaded_compare_file.name, uploaded_reference_file.name)
        st.success("Las diferencias entre los documentos han sido encontradas y vectorizadas.")
        
        # Mostrar diferencias
        st.header("Diferencias Encontradas")
        diferencias_tabla = []
        for diferencia in diferencias:
            diferencias_tabla.append([diferencia[0], diferencia[1], diferencia[2], diferencia[3]])
        st.table(diferencias_tabla)
    else:
        st.info("No se encontraron diferencias entre los documentos.")

