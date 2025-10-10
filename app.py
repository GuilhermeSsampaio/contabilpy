import streamlit as st
from components.sidebar import sidebar
# from dotenv import load_dotenv
# import os
# load_dotenv()

# streamlit: name="Home" icon="🏡"
st.header("_:blue[ContabiliPy]_ - velocidade na contabilidade", divider=True)

sidebar()
st.title("Bem-vindo ao ContabiliPy")
st.write("Sua plataforma de contabilidade automatizada com IA e um arcabouço completo de ferramentas.")
st.write("Escolha uma das opções no menu lateral para começar.")
st.write("Desenvolvido por [@Guilherme Sampaio](https://www.linkedin.com/in/guilhermessampaio)")
