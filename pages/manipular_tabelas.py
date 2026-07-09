import streamlit as st
import pandas as pd
from components.sidebar import sidebar
from components.conversoes import componente_conversoes
from components.dashboards import gerar_dashboard
from components.extracoes import extrair_dados
from components.juncoes import juntar_tabelas
from components.relatorios import gerar_relatorio

sidebar()
st.header("Manipulação de tabelas")
# Upload do arquivo
uploaded_files = st.file_uploader(
        "Suba o(s) arquivo(s) que deseja manipular",
        type=["csv", "txt", "html", "xlsx", "json"],
        accept_multiple_files=True
    )
conversoes, extracoes, juncoes, relatorios, dashboards = st.tabs(["Conversões", "Extrações", "Junções", "Relatórios", "Dashboards"])


with conversoes:
    componente_conversoes(uploaded_files)
with extracoes:
    extrair_dados(uploaded_files)
with juncoes:
    juntar_tabelas(uploaded_files)
with relatorios:
    gerar_relatorio(uploaded_files)
with dashboards:
    gerar_dashboard(uploaded_files)
