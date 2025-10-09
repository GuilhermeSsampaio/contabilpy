import streamlit as st
import pandas as pd
from io import StringIO  # Importa StringIO do módulo io

from components.conversoes import componente_conversoes

st.header("Manipulação de tabelas")

conversoes, extracoes, juncoes, relatorios, graficos, dashboards = st.tabs(["Conversões", "Extrações", "Junções", "Relatórios", "Gráficos", "Dashboards"])

with conversoes:
    componente_conversoes()