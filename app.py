import streamlit as st
from document_analysis import (
    extraer_texto_pdf, 
    extraer_texto_docx, 
    leer_archivo_texto, 
    encontrar_diferencias, 
    vectorizar_y_tokenizar_diferencias, 
    tokenizar_lineamientos, 
    almacenar_reglas_vectorizadas, 
    cargar_y_vectorizar_manual
)

# Función para procesar documentos
def procesar_documentos(uploaded_reference_file, uploaded_compare_file, reference_file_type, compare_file_type):
    texto_referencia = extraer_texto(reference_file_type, uploaded_reference_file)
    texto_comparar = extraer_texto(compare_file_type, uploaded_compare_file)
    
    tokens_referencia = tokenizar_lineamientos([texto_referencia])
    diferencias = encontrar_diferencias(texto_comparar, texto_referencia)
    
    if diferencias:
        diferencias_vectorizadas = vectorizar_y_tokenizar_diferencias(diferencias, tokens_referencia, uploaded_compare_file.name, uploaded_reference_file.name)
        st.success("Las diferencias entre los documentos han sido encontradas y vectorizadas.")
        
        st.header("Diferencias Encontradas")
        diferencias_tabla = []
        for diferencia in diferencias:
            diferencias_tabla.append([diferencia[0], diferencia[1], diferencia[2], diferencia[3]])
        st.table(diferencias_tabla)
    else:
        st.info("No se encontraron diferencias entre los documentos.")

# Función para extraer texto según el tipo de archivo
def extraer_texto(file_type, file):
    if file_type == "pdf":
        return extraer_texto_pdf(file)
    elif file_type == "docx":
        return extraer_texto_docx(file)
    elif file_type == "txt":
        return leer_archivo_texto(file)
    return ""

# Función para cargar y vectorizar el manual
def load_manual(tokens_referencia):
    almacenar_reglas_vectorizadas(tokens_referencia)
    st.success("Manual cargado y vectorizado con éxito.")

# Función para verificar cumplimiento de archivo
def verify_file_compliance(tokens_referencia, uploaded_compare_file, compare_file_type):
    texto_comparar = extraer_texto(compare_file_type, uploaded_compare_file)
    tokens_comparar = tokenizar_lineamientos([texto_comparar])
    
    diferencias = encontrar_diferencias(texto_comparar, " ".join(tokens_referencia))
    
    if diferencias:
        diferencias_vectorizadas = vectorizar_y_tokenizar_diferencias(diferencias, tokens_referencia, uploaded_compare_file.name, "Manual de Referencia")
        
        st.success("El documento ha sido analizado para verificar el cumplimiento.")
        
        st.header("Resultados de Verificación de Cumplimiento")
        cumple = True
        for diferencia in diferencias_vectorizadas:
            st.subheader(diferencia["seccion"])
            st.write(f"**Contenido en el Manual:** {diferencia['contenido_referencia']}")
            st.write(f"**Contenido en el Documento:** {diferencia['contenido_documento']}")
            st.write(f"**Tipo de Diferencia:** {diferencia['tipo']}")
            st.write(f"**Recomendación:** {diferencia['recomendacion']}")
            cumple = False
        
        if cumple:
            st.success("El documento cumple con todas las normativas establecidas en el manual de referencia.")
        else:
            st.error("El documento no cumple con las normativas establecidas en el manual de referencia.")
    else:
        st.success("El documento cumple con todas las normativas establecidas en el manual de referencia.")

# Interfaz Streamlit
st.title("Qualipharma - Analytics Town")

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

# Actualizar la interfaz de usuario para el análisis detallado
st.sidebar.header("Opciones")
option = st.sidebar.selectbox("Selecciona una opción", ["Comparar Documentos", "Cargar y Vectorizar Manual", "Verificar Cumplimiento de Archivo"])

if option == "Comparar Documentos":
    if st.button("Procesar Documentos"):
        if uploaded_reference_file and uploaded_compare_file:
            procesar_documentos(uploaded_reference_file, uploaded_compare_file, reference_file_type, compare_file_type)
        else:
            st.warning("Por favor, carga ambos archivos para comparar.")
elif option == "Cargar y Vectorizar Manual":
    if st.button("Cargar y Vectorizar"):
        if uploaded_reference_file:
            tokens_referencia = tokenizar_lineamientos([extraer_texto(reference_file_type, uploaded_reference_file)])
            load_manual(tokens_referencia)
        else:
            st.warning("Por favor, carga un archivo de referencia.")
elif option == "Verificar Cumplimiento de Archivo":
    if st.button("Verificar Cumplimiento"):
        if uploaded_reference_file and uploaded_compare_file:
            tokens_referencia = tokenizar_lineamientos([extraer_texto(reference_file_type, uploaded_reference_file)])
            verify_file_compliance(tokens_referencia, uploaded_compare_file, compare_file_type)
        else:
            st.warning("Por favor, carga ambos archivos para verificar el cumplimiento.")
