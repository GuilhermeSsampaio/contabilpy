import streamlit as st
import pandas as pd
from io import StringIO  # Importa StringIO do módulo io
import sys
import os

from interface.components.conversoes import componente_conversoes
from tools.convert_files import convert_csv_to_excel

st.header("Manipulação de tabelas")

conversoes, extracoes, juncoes, relatorios, graficos, dashboards = st.tabs(["Conversões", "Extrações", "Junções", "Relatórios", "Gráficos", "Dashboards"])

with conversoes:
    componente_conversoes()