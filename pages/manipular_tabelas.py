import streamlit as st
import pandas as pd
from components.sidebar import sidebar
from components.conversoes import componente_conversoes
from components.dashboards import gerar_dashboard
from components.extracoes import extrair_dados
from components.graficos import plotar_graficos
from components.juncoes import juntar_tabelas
from components.relatorios import gerar_relatorio

sidebar()
st.header("Manipulação de tabelas")
# Upload do arquivo
uploaded_file = st.file_uploader(
        "Suba o(s) arquivo(s) que deseja manipular",
        type=["csv", "txt", "html", "xlsx", "json"]
    )

# atualizar a logica pra multiplos arquivos

# uploaded_files = st.file_uploader(
#         "Suba o(s) arquivo(s) que deseja manipular",
#         type=["csv", "txt", "html", "xlsx", "json"],
#         accept_multiple_files=True
        
#     )
conversoes, extracoes, juncoes, relatorios, graficos, dashboards = st.tabs(["Conversões", "Extrações", "Junções", "Relatórios", "Gráficos", "Dashboards"])


with conversoes:
    componente_conversoes(uploaded_file=uploaded_file)
with extracoes:
    extrair_dados()
with juncoes:
    juntar_tabelas()
with relatorios:
    gerar_relatorio()
with graficos:
    plotar_graficos()
with dashboards:
    gerar_dashboard()
    
