import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
import os
from document_analysis import *  # Importa todas las funciones del análisis de documentos

# App title
st.set_page_config(page_title="🤗💬 HugChat")

# Sidebar
with st.sidebar:
    st.title('🤗💬 HugChat')

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    for dict_message in st.session_state.messages:
        string_dialogue = "You are a helpful assistant."
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

    prompt = f"{string_dialogue} {prompt_input} Assistant: "
    return chatbot.chat(prompt)

# User-provided prompt
if st.chat_input():
    prompt = st.chat_input()  # Obtén el prompt del input del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            email = st.secrets["email"]  # Asegúrate de agregar tus credenciales en streamlit secrets
            passwd = st.secrets["passwd"] 
            response = generate_response(prompt, email, passwd)
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Funcionalidades adicionales para la carga y análisis de documentos
def load_manual(tokens_referencia):
    st.write("Cargando y vectorizando manual...")
    ruta_manual = cargar_y_vectorizar_manual(tokens_referencia)
    st.write(f"Manual vectorizado y guardado en {ruta_manual}")

def compare_documents():
    st.write("Comparando documentos...")
    comparar_documentos()

def verify_file_compliance(tokens_referencia):
    st.write("Verificando cumplimiento del archivo...")
    verificar_archivo(tokens_referencia)

# Menú de opciones
st.sidebar.header("Opciones")
option = st.sidebar.selectbox("Selecciona una opción", ["Comparar Documentos", "Cargar y Vectorizar Manual", "Verificar Cumplimiento de Archivo"])

if option == "Comparar Documentos":
    compare_documents()
elif option == "Cargar y Vectorizar Manual":
    tokens_referencia = tokenizar_lineamientos(lineamientos)
    load_manual(tokens_referencia)
elif option == "Verificar Cumplimiento de Archivo":
    tokens_referencia = tokenizar_lineamientos(lineamientos)
    verify_file_compliance(tokens_referencia)
