from agno.agent import Agent
from agno.models.google import Gemini
import streamlit as st
# from tools.convert_files import convert_csv_to_excel
gemini_api_key = st.secrets["GOOGLE_API_KEY"]

contAgent = Agent(
    name="ContAgent",
    model=Gemini(id="gemini-2.0-flash", api_key=gemini_api_key),
    # instructions=["Use sua ferramenta para converter arquivos csv para excel, e mostre o caminho retornado pro user"],
    # tools=[convert_csv_to_excel()]
)

# contAgent.cli_app(stream=True)

