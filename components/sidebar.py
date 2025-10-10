import streamlit as st

def sidebar():
    st.sidebar.title("Navegação")
    st.sidebar.page_link("app.py", label="🏡 Home")
    st.sidebar.page_link("pages/manipular_tabelas.py", label="📂 Manipulação de arquivos")
    st.sidebar.page_link("pages/agent.py", label="🤖 ContabilAi")
    st.sidebar.page_link("pages/ai_predict.py", label="🎲 Análise de dados com IA")