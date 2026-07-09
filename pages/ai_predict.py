import streamlit as st
st.set_page_config(page_title="ContabiliPy | Previsões", page_icon="logo.png", layout="wide")

from components.previsao_ia import trainAi
from components.sidebar import sidebar
from components.help_modal import render_help

sidebar()
st.header("Previsão de Dados com Inteligência Artificial")

texto_ajuda_predict = """
**Como usar o Módulo Preditivo?**

Esse módulo possui duas ferramentas matemáticas potentes:

1. **Regressão / Classificação**: 
   - *O que faz:* Descobre o padrão de correlação entre várias colunas. 
   - *Exemplos:* Prever o valor de Vendas (Alvo) baseado no Investimento em Marketing (Preditora). Ou prever Análise de Crédito (Aprovado/Recusado).
   
2. **Séries Temporais**:
   - *O que faz:* Analisa uma linha do tempo e tenta adivinhar o comportamento futuro.
   - *Exemplos:* Suba o faturamento diário da empresa de Janeiro a Março, selecione prever 30 dias, e a IA vai desenhar a curva de faturamento esperada para Abril!
"""
render_help("Entenda os Modelos de IA", texto_ajuda_predict, "predict")

uploaded_files = st.file_uploader(
    "Suba os arquivos que deseja usar para treinamento",
    type=["csv", "txt", "html", "xlsx", "json"],
    accept_multiple_files=True
)

trainAi(uploaded_files)