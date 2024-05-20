import streamlit as st
from hugchat import hugchat
from hugchat.login import Login
from io import BytesIO
import os
import pandas as pd
import pdfminer.high_level
import spacy
import re
import json
import csv
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from docx import Document
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from fuzzywuzzy import fuzz
from tabulate import tabulate
from transformers import pipeline
from openpyxl import Workbook
import logging
from datetime import datetime

def main():
    st.sidebar.title("Opciones")
    option = st.sidebar.selectbox("Seleccione una opción", ["Comparar documentos", "Cargar y vectorizar manual", "Verificar cumplimiento"])

    if option == "Comparar documentos":
        comparar_documentos()
    elif option == "Cargar y vectorizar manual":
        cargar_y_vectorizar_manual()
    elif option == "Verificar cumplimiento":
        verificar_archivo()

# Instancias de modelos BERT y BART
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad", tokenizer="bert-large-uncased-whole-word-masking-finetuned-squad")

lemmatizer = WordNetLemmatizer()

def cargar_archivo_interactivo():
    uploaded_file = st.file_uploader("Cargar archivo", type=['pdf', 'docx', 'txt', 'csv'])
    if uploaded_file is not None:
        content = uploaded_file.read()
        return BytesIO(content)
    return None

def comparar_documentos():
    documento1_content = cargar_archivo_interactivo()
    if documento1_content is None:
        st.error("No se cargó ningún documento.")
        return
    documento2_content = cargar_archivo_interactivo()
    if documento2_content is None:
        st.error("No se cargó ningún documento.")
        return
    
    # Procesar contenido de documentos
    doc1 = Document(documento1_content)
    doc2 = Document(documento2_content)
    diferencias = encontrar_diferencias(doc1, doc2)
    if diferencias:
        todas_las_diferencias = [diferencia[0] for diferencia in diferencias]
        documento_referencia = documento1_content  # Usar el primer documento como referencia
        vectorizar_y_tokenizar_diferencias(todas_las_diferencias, tokens_referencia, nombre_documento2, documento_referencia)

def verificar_archivo():
    archivo_content = cargar_archivo_interactivo()
    if archivo_content is None:
        st.error("No se cargó ningún archivo.")
        return
    
    tokens_referencia = tokenizar_lineamientos(lineamientos)
    reglas_vectorizadas_nuevo = almacenar_reglas_vectorizadas(archivo_content, tokens_referencia)
    ruta_archivo_csv_nuevo = "archivo_cargado_vectorizado.csv"
    guardar_diccionario_en_csv(reglas_vectorizadas_nuevo, ruta_archivo_csv_nuevo)

    reglas_manual = cargar_diccionario_desde_csv(ruta_manual)
    cumple, resultado = verificar_cumplimiento_diferencias_cargadas(reglas_manual, archivo_content, tokens_referencia)

    st.write(f"Cumple con las normativas: {cumple}.")
    if not cumple:
        st.write("Las siguientes diferencias no cumplen con las normativas:")
        for diferencia in resultado:
            st.write("-", diferencia)

if __name__ == "__main__":
    main()
