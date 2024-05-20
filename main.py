def main():
    st.title("Document Analysis Tool")
    st.sidebar.title("Menu")
    
    menu = ["Comparar Documentos", "Cargar y Vectorizar Manual", "Verificar Cumplimiento", "Salir"]
    choice = st.sidebar.selectbox("Seleccione una opción", menu)

    if choice == "Comparar Documentos":
        st.subheader("Comparar Documentos")
        doc1_file = st.file_uploader("Cargar Documento 1 (DOCX)", type=["docx"])
        doc2_file = st.file_uploader("Cargar Documento 2 (DOCX)", type=["docx"])
        
        if st.button("Comparar"):
            if doc1_file and doc2_file:
                doc1_text = extraer_texto_docx(doc1_file)
                doc2_text = extraer_texto_docx(doc2_file)
                diferencias = encontrar_diferencias(doc1_text, doc2_text)
                
                if diferencias:
                    st.write("Diferencias encontradas:")
                    for dif in diferencias:
                        st.write(dif)
                else:
                    st.write("No se encontraron diferencias.")
            else:
                st.write("Por favor, suba ambos documentos.")
    
    elif choice == "Cargar y Vectorizar Manual":
        st.subheader("Cargar y Vectorizar Manual")
        manual_file = st.file_uploader("Cargar Manual (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
        
        if st.button("Cargar y Vectorizar"):
            if manual_file:
                file_type = manual_file.name.split('.')[-1]
                ruta_manual = cargar_y_vectorizar_manual(manual_file, file_type, tokens_referencia)
                if ruta_manual:
                    st.write(f"Manual vectorizado y guardado en {ruta_manual}")
                else:
                    st.write("Error al procesar el manual.")
            else:
                st.write("Por favor, suba un archivo de manual.")

    elif choice == "Verificar Cumplimiento":
        st.subheader("Verificar Cumplimiento")
        manual_csv = st.file_uploader("Cargar Manual Vectorizado (CSV)", type=["csv"])
        verificar_file = st.file_uploader("Cargar Documento para Verificar (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
        
        if st.button("Verificar"):
            if manual_csv and verificar_file:
                reglas_manual = cargar_diccionario_desde_csv(manual_csv)
                file_type = verificar_file.name.split('.')[-1]
                if file_type == "pdf":
                    texto_nuevo = extraer_texto_pdf(verificar_file)
                elif file_type == "txt":
                    texto_nuevo = leer_archivo_texto(verificar_file)
                elif file_type == "docx":
                    texto_nuevo = extraer_texto_docx(verificar_file)
                else:
                    texto_nuevo = None
                
                if texto_nuevo:
                    diferencias = vectorizar_y_tokenizar_diferencias(texto_nuevo, reglas_manual, "documento_verificado", "manual_referencia")
                    if diferencias:
                        st.write("Diferencias encontradas y vectorizadas:")
                        st.write(diferencias)
                    else:
                        st.write("No se encontraron diferencias significativas.")
                else:
                    st.write("Error al extraer texto del documento para verificar.")
            else:
                st.write("Por favor, suba ambos archivos.")

    elif choice == "Salir":
        st.write("Gracias por usar la herramienta.")
    
if __name__ == "__main__":
    main()
