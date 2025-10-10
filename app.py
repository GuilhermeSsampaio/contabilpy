import streamlit as st
from dotenv import load_dotenv
import os

from components.sidebar import sidebar
load_dotenv()
# streamlit: name="Home" icon="🏡"
st.header("_:blue[ContabiliPy]_ - velocidade na contabilidade", divider=True)

sidebar()