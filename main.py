from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import subprocess
import threading

app = FastAPI()

# Função para rodar o Streamlit em uma thread separada
def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true", "--server.address=0.0.0.0"])

# Inicia o Streamlit em uma thread
thread = threading.Thread(target=run_streamlit, daemon=True)
thread.start()

@app.get("/")
def redirect_to_streamlit():
    # Redireciona para o Streamlit
    return RedirectResponse(url="https://contabil-py.squareweb.app:8501")
