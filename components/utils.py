import streamlit as st
import pandas as pd
import os

def selecionar_arquivo(uploaded_files, key_suffix=""):
    """
    Componente reutilizável (DRY) para selecionar um arquivo da lista.
    Retorna o arquivo selecionado ou None.
    """
    if not uploaded_files:
        st.info("Nenhum arquivo disponível. Faça o upload acima.")
        return None
        
    file_names = [f.name for f in uploaded_files]
    selected_name = st.selectbox("Selecione o arquivo para operar:", file_names, key=f"select_file_{key_suffix}")
    
    for f in uploaded_files:
        if f.name == selected_name:
            return f
    return None

def carregar_dataframe(uploaded_file):
    """
    Carrega o arquivo selecionado em um DataFrame Pandas (SOLID).
    Retorna o DataFrame ou None se o formato não for suportado.
    """
    if not uploaded_file:
        return None
        
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    
    try:
        # Resetar ponteiro em caso de leituras múltiplas
        uploaded_file.seek(0)
        
        if file_extension == ".csv":
            df = pd.read_csv(uploaded_file)
            return df
        elif file_extension in [".xls", ".xlsx"]:
            df = pd.read_excel(uploaded_file)
            return df
        else:
            st.error(f"Formato {file_extension} não é tabular (CSV/Excel). Não é possível carregar como tabela.")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar DataFrame: {e}")
        return None
