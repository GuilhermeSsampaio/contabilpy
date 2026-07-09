import streamlit as st

from components.previsao_ia import trainAi
from components.sidebar import sidebar

sidebar()
st.header("Previsão de Dados com Inteligência Artificial")

uploaded_files = st.file_uploader(
    "Suba os arquivos que deseja usar para treinamento",
    type=["csv", "txt", "html", "xlsx", "json"],
    accept_multiple_files=True
)

trainAi(uploaded_files)