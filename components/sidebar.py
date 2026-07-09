import streamlit as st

def sidebar():
    st.sidebar.title("Navegação")
    st.sidebar.page_link("app.py", label="Home", icon=":material/home:")
    st.sidebar.page_link("pages/manipular_tabelas.py", label="Manipulação de arquivos", icon=":material/folder_open:")
    st.sidebar.page_link("pages/agent.py", label="ContabilAi", icon=":material/smart_toy:")
    st.sidebar.page_link("pages/ai_predict.py", label="Análise de dados com IA", icon=":material/insights:")