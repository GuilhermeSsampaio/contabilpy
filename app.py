import streamlit as st
st.set_page_config(page_title="ContabiliPy | Home", page_icon="logo.png", layout="wide")
from components.sidebar import sidebar
# from dotenv import load_dotenv
# import os
# load_dotenv()

from components.help_modal import render_help

col1, col2 = st.columns([0.85, 0.15], vertical_alignment="center")
with col1:
    st.header("_:blue[ContabiliPy]_ - velocidade na contabilidade", divider=True)
with col2:
    st.image("logo.png", width=110)

sidebar()
st.title("Bem-vindo ao ContabiliPy")
st.write("Sua plataforma de contabilidade automatizada com IA e um arcabouço completo de ferramentas.")
st.write("Escolha uma das opções no menu lateral para começar.")

# --- Modal de Ajuda ---
texto_ajuda = """
O ContabilPy é dividido em três grandes módulos:

1. **:material/folder_open: Manipulação de Arquivos**: Onde você cruza planilhas (PROCV/Merge), empilha dados, aplica filtros matemáticos e cria dashboards visuais em um clique.
2. **:material/smart_toy: ContabilAi**: Um assistente inteligente via chat que pode ler seus arquivos, responder perguntas sobre estatísticas da sua base e converter arquivos (Excel, CSV, JSON, HTML) automaticamente.
3. **:material/insights: Análise de dados com IA**: Nosso módulo avançado de Data Science. Crie modelos preditivos de Regressão, Classificação (ex: análise de crédito) e Séries Temporais (previsão de vendas futuras).
"""
render_help("Como navegar pelo sistema", texto_ajuda, "home")
# ----------------------

st.write("Desenvolvido por [@Guilherme Sampaio](https://www.linkedin.com/in/guilhermessampaio)")
