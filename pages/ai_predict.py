import streamlit as st

from components.previsao_ia import trainAi
from components.sidebar import sidebar

sidebar()
st.header("Previsao de dados com IA")
trainAi()