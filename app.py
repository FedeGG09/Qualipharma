import streamlit as st
from document_analysis import *

# Interfaz Streamlit
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

# Funciones
def compare_documents():
    if uploaded_reference_file and uploaded_compare_file:
        texto_comparar = extraer_texto_pdf(uploaded_compare_file) if compare_file_type == "pdf" else extraer_texto_docx(uploaded_compare_file) if compare_file_type == "docx" else leer_archivo_texto(uploaded_compare_file)
        texto_referencia = extraer_texto_pdf(uploaded_reference_file) if reference_file_type == "pdf" else extraer_texto_docx(uploaded_reference_file) if reference_file_type == "docx" else leer_archivo_texto(uploaded_reference_file)
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
    if uploaded_reference_file:
        tokens_referencia = tokenizar_lineamientos([extraer_texto_pdf(uploaded_reference_file) if reference_file_type == "pdf" else extraer_texto_docx(uploaded_reference_file) if reference_file_type == "docx" else leer_archivo_texto(uploaded_reference_file)])
        load_manual(tokens_referencia)
elif option == "Verificar Cumplimiento de Archivo":
    if uploaded_reference_file:
        tokens_referencia = tokenizar_lineamientos([extraer_texto_pdf(uploaded_reference_file) if reference_file_type == "pdf" else extraer_texto_docx(uploaded_reference_file) if reference_file_type == "docx" else leer_archivo_texto(uploaded_reference_file)])
        verify_file_compliance(tokens_referencia)
    else:
        st.info("No se encontraron diferencias entre los documentos.")

