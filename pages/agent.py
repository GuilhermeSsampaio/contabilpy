import sys
import os
import pandas as pd
from components.sidebar import sidebar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
from agent.ContAi import contAgent
from agno.agent import RunEvent
import tempfile
import json

sidebar()
st.title("ContAi")
st.write("Agente de IA que automatiza seus B.Os contábeis e de análise de dados.")

INITIAL_MESSAGE = {
    "role": "assistant",
    "content": "Olá! Sou o ContAi, seu assistente de IA especializado em automação de tarefas contábeis e análise de dados.\n\nPosso te ajudar convertendo documentos para diversos formatos como **Excel, CSV, JSON e HTML**. \n\nEnvie seus arquivos e me diga como posso ajudar!"
}

if "messages" not in st.session_state:
    st.session_state.messages = [INITIAL_MESSAGE]

col1, col2 = st.columns([0.8, 0.2])
with col2:
    if st.button("🗑️ Limpar Chat"):
        st.session_state.messages = [INITIAL_MESSAGE]
        st.rerun()

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("file_download"):
            file_info = message["file_download"]
            try:
                with open(file_info["file_path"], "rb") as f:
                    data = f.read()
                # Extensões comuns para mime types
                ext = os.path.splitext(file_info["file_name"])[1].lower()
                mime_type = "application/octet-stream"
                if ext == ".xlsx":
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif ext == ".csv":
                    mime_type = "text/csv"
                elif ext == ".json":
                    mime_type = "application/json"
                elif ext == ".html":
                    mime_type = "text/html"
                    
                st.download_button(
                    label=f"Baixar {file_info['file_name']}",
                    data=data,
                    file_name=file_info["file_name"],
                    mime=mime_type
                )
            except Exception:
                pass

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem e suba seus arquivos.", accept_file=True, file_type=[".csv", ".txt", ".xlsx", ".json", ".html"]):
    prompt_text = prompt.text or ""
    
    # Salva o input do usuario na tela e no state
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
        st.markdown(prompt_text)

    saved_paths = []
    
    if prompt.files:
        save_dir = os.path.join(tempfile.gettempdir(), "contabilipy_uploads")
        os.makedirs(save_dir, exist_ok=True)
        for file in prompt.files:
            save_path = os.path.join(save_dir, file.name)
            try:
                file.seek(0)
            except Exception:
                raise Exception("Não foi possível resetar o ponteiro do arquivo.")
            with open(save_path, "wb") as f:
                f.write(file.read())
            saved_paths.append(save_path)
            
            st.markdown(f"**Arquivo recebido e salvo localmente:** {file.name}")

    if saved_paths:
        prompt_text += "\n\nArquivos salvos no meu sistema:\n" + "\n".join(saved_paths)

    with st.chat_message("assistant"):
        message_container = st.container()
        with message_container:
            response_placeholder = st.empty()
            full_response = ""
            
            # Resetar os pendentes antes de rodar a IA
            st.session_state.pending_downloads = []

            for chunk in contAgent.run(prompt_text, stream=True):
                if getattr(chunk, "event", None) == RunEvent.run_content:
                    full_response += getattr(chunk, "content", "")
                    response_placeholder.markdown(full_response)
            
            message_data = {"role": "assistant", "content": full_response}
            
            # Se a tool rodou, ela terá populado o pending_downloads
            if st.session_state.pending_downloads:
                message_data["file_download"] = st.session_state.pending_downloads[-1]
                
            st.session_state.messages.append(message_data)
            
            # Mostra botão de download na rodada atual
            for d in st.session_state.pending_downloads:
                try:
                    with open(d["file_path"], "rb") as f:
                        data = f.read()
                    
                    ext = os.path.splitext(d["file_name"])[1].lower()
                    mime_type = "application/octet-stream"
                    if ext == ".xlsx":
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    elif ext == ".csv":
                        mime_type = "text/csv"
                    elif ext == ".json":
                        mime_type = "application/json"
                    elif ext == ".html":
                        mime_type = "text/html"
                        
                    st.download_button(
                        label=f"Baixar {d['file_name']}",
                        data=data,
                        file_name=d['file_name'],
                        mime=mime_type
                    )
                except Exception as e:
                    st.error(f"Erro ao disponibilizar arquivo: {e}")