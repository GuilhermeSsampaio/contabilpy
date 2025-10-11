import sys
import os
import pandas as pd
from components.sidebar import sidebar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import streamlit as st
from agent.ContAi import contAgent
from agno.agent import RunEvent
import tempfile
from tools.convert_files import convert_csv_to_excel
import io
import json

# quebrar esse arquivo grande em partes menores
# entender minuciosamente o fluxo de dados
# melhorar UX para casos de uso específicos
# expandir funcionalidades do agente

sidebar()
st.title("ContAi")
st.write("Agente de IA que automatiza seus B.Os")

# Inicializar histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Armazenar dados de arquivos convertidos para posterior download
if "converted_files" not in st.session_state:
    st.session_state.converted_files = {}

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Se for uma mensagem do assistente com botão de download
        if message.get("file_download"):
            file_info = message["file_download"]
            if file_info["file_name"] in st.session_state.converted_files:
                st.download_button(
                    label="Baixar Excel",
                    data=st.session_state.converted_files[file_info["file_name"]],
                    file_name=file_info["file_name"],
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem e suba seus arquivos.", accept_file=True, file_type=[".csv", ".txt", ".xlsx"]):
    # salvar texto do prompt
    prompt_text = prompt.text or ""
    st.session_state.messages.append({"role": "user", "content": prompt_text})

    # salvar arquivos enviados em um diretório temporário e adicionar caminhos ao prompt_text
    saved_paths = []
    uploaded_csv_files = []  # Lista específica para arquivos CSV
    
    if prompt.files:
        save_dir = os.path.join(tempfile.gettempdir(), "contabilipy_uploads")
        os.makedirs(save_dir, exist_ok=True)
        for file in prompt.files:
            save_path = os.path.join(save_dir, file.name)
            # garantir que o ponteiro esteja no início
            try:
                file.seek(0)
            except Exception:
                raise Exception("Não foi possível resetar o ponteiro do arquivo.")
            with open(save_path, "wb") as f:
                f.write(file.read())
            saved_paths.append(save_path)
            
            # Manter lista específica de arquivos CSV
            if file.name.endswith(".csv"):
                uploaded_csv_files.append(save_path)
                df = pd.read_csv(save_path)
                st.markdown(f"**Arquivo CSV enviado:** {file.name}")
                st.write(df)
            else:
                st.markdown(f"Arquivo enviado: {file.name} — salvo em {save_path}")

    # anexa os paths ao texto para que o agente saiba dos arquivos locais
    if saved_paths:
        prompt_text += "\n\nArquivos salvos:\n" + "\n".join(saved_paths)
        
        # Se o pedido for para converter para Excel e só tiver um CSV, vamos ajudar o agente
        if ("converte" in prompt_text.lower() or "excel" in prompt_text.lower() or "transforme" in prompt_text.lower()) and len(uploaded_csv_files) == 1:
            prompt_text += f"\n\nO arquivo a ser convertido é: {uploaded_csv_files[0]}"

    # Agora executar o agente (stream) normalmente
    with st.chat_message("assistant"):
        message_container = st.container()
        with message_container:
            response_placeholder = st.empty()
            full_response = ""
            file_download_info = None
            tool_args = {}  # Armazenar argumentos da ferramenta entre eventos
            converted_files_in_session = {}  # Para armazenar arquivos convertidos nesta sessão
            using_fallback = False  # Indicador de que estamos usando o fallback automático
            converted_file_name = None  # Nome do arquivo que foi convertido

            # Verificar se não há texto mas há um arquivo CSV (tentativa automática de conversão)
            if not prompt.text and len(uploaded_csv_files) == 1:
                st.info("Detectamos um arquivo CSV sem instruções específicas. Deseja convertê-lo para Excel?")
                
                if st.button("Sim, converter para Excel"):
                    file_path = uploaded_csv_files[0]
                    try:
                        output_bytes = convert_csv_to_excel(file_path)
                        file_name = os.path.splitext(os.path.basename(file_path))[0] + ".xlsx"
                        st.session_state.converted_files[file_name] = output_bytes.getvalue()
                        
                        st.success(f"Arquivo {file_name} convertido com sucesso!")
                        st.download_button(
                            label=f"Baixar {file_name}",
                            data=output_bytes.getvalue(),
                            file_name=file_name,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        )
                        
                        full_response = f"Converti o arquivo {os.path.basename(file_path)} para Excel. O download está disponível acima."
                        response_placeholder.markdown(full_response)
                        
                        # Adicionar resposta ao histórico
                        message_data = {"role": "assistant", "content": full_response, "file_download": {"file_name": file_name}}
                        st.session_state.messages.append(message_data)
                        # return  # Encerra o processamento aqui
                    except Exception as e:
                        st.error(f"Erro ao converter arquivo: {str(e)}")
            
            # Usar um modo de conversão direta se for um pedido claro de conversão e houver apenas um CSV
            auto_convert = False
            if (("converte" in prompt_text.lower() or "excel" in prompt_text.lower() or 
                  "transforme" in prompt_text.lower()) and len(uploaded_csv_files) == 1):
                auto_convert = True
                file_path = uploaded_csv_files[0]
                try:
                    output_bytes = convert_csv_to_excel(file_path)
                    file_name = os.path.splitext(os.path.basename(file_path))[0] + ".xlsx"
                    st.session_state.converted_files[file_name] = output_bytes.getvalue()
                    
                    st.success(f"Arquivo {file_name} convertido com sucesso!")
                    st.download_button(
                        label=f"Baixar {file_name}",
                        data=output_bytes.getvalue(),
                        file_name=file_name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                    
                    full_response = f"Converti o arquivo {os.path.basename(file_path)} para Excel. O download está disponível abaixo."
                    converted_file_name = file_name
                    converted_files_in_session[file_name] = output_bytes.getvalue()
                    file_download_info = {"file_name": file_name}
                    using_fallback = True  # Marcar que já estamos usando o fallback
                    
                    # Atualizar a resposta imediatamente
                    response_placeholder.markdown(full_response)
                except Exception as e:
                    st.error(f"Erro ao converter arquivo: {str(e)}")
                    auto_convert = False  # Falha na conversão automática, tentar com o agente
            
            # Se não for auto_convert ou se auto_convert falhar, passar para o agente
            if not auto_convert:
                # passar a string (prompt_text) para o agente, não o objeto prompt
                for chunk in contAgent.run(prompt_text, stream=True):
                    # Verificar evento e processar de acordo
                    if chunk.event == RunEvent.run_content:
                        # Não adicionar conteúdo do agente se já estamos em modo de fallback
                        if not using_fallback:
                            full_response += chunk.content
                            response_placeholder.markdown(full_response)
                    elif chunk.event == RunEvent.tool_call_started and not using_fallback:
                        # Verificar se é uma chamada para converter CSV para Excel
                        if chunk.tool.tool_name == "converter_csv_para_excel":
                            # Não mostrar debug em modo de produção
                            # st.write("Args da ferramenta:", chunk.tool.tool_args)
                            
                            if "file_path" in chunk.tool.tool_args:
                                file_path = chunk.tool.tool_args["file_path"]
                                # Verificar se o caminho existe
                                if os.path.exists(file_path):
                                    st.info(f"Convertendo arquivo: {file_path}")
                                    # Armazenar argumentos para uso posterior
                                    tool_args = chunk.tool.tool_args
                                else:
                                    # Se tiver apenas um arquivo CSV, sugerir este sem mostrar aviso
                                    if len(uploaded_csv_files) == 1:
                                        tool_args = {"file_path": uploaded_csv_files[0]}
                            else:
                                # Se tiver apenas um arquivo CSV, usar sem mostrar aviso
                                if len(uploaded_csv_files) == 1:
                                    tool_args = {"file_path": uploaded_csv_files[0]}
                    elif chunk.event == RunEvent.tool_call_completed and not using_fallback:
                        if chunk.tool.tool_name == "converter_csv_para_excel":
                            # Lidar com diferentes tipos de resultado
                            result = chunk.tool.result
                            
                            # Converter string para dicionário se necessário
                            if isinstance(result, str):
                                try:
                                    result = json.loads(result)
                                except json.JSONDecodeError:
                                    # Se não for JSON, assumir resultado simples
                                    result = {"success": True, "message": result}
                            
                            # Se ainda não for um dict após a tentativa de conversão, criar um dict
                            if not isinstance(result, dict):
                                result = {"success": True, "message": str(result)}
                            
                            # Verificar se temos um caminho de arquivo
                            file_path = result.get("file_path") or tool_args.get("file_path")
                            
                            # Último recurso: se não há caminho e só existe um CSV, usar ele
                            if not file_path and len(uploaded_csv_files) == 1:
                                file_path = uploaded_csv_files[0]
                            
                            if file_path and os.path.exists(file_path):
                                try:
                                    output_bytes = convert_csv_to_excel(file_path)
                                    file_name = os.path.splitext(os.path.basename(file_path))[0] + ".xlsx"
                                    # Armazenar para posterior download
                                    st.session_state.converted_files[file_name] = output_bytes.getvalue()
                                    converted_files_in_session[file_name] = output_bytes.getvalue()
                                    file_download_info = {"file_name": file_name}
                                    converted_file_name = file_name
                                    
                                    # Limpar a resposta anterior do agente se ela estiver pedindo um arquivo
                                    if "especifique" in full_response.lower() or "qual arquivo" in full_response.lower():
                                        full_response = f"Converti o arquivo {os.path.basename(file_path)} para Excel. O download está disponível."
                                    else:
                                        # Adicionar mensagem sobre o download no full_response
                                        full_response += f"\n\nO arquivo '{file_name}' está pronto para download."
                                    
                                    # Atualizar a resposta
                                    response_placeholder.markdown(full_response)
                                    
                                    # Mostrar botão de download imediatamente
                                    st.success(f"Arquivo {file_name} convertido com sucesso!")
                                    st.download_button(
                                        label=f"Baixar {file_name}",
                                        data=output_bytes.getvalue(),
                                        file_name=file_name,
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    )
                                except Exception as e:
                                    full_response += f"\nErro ao processar arquivo para download: {str(e)}"
                                    st.error(f"Erro ao processar arquivo: {str(e)}")
                            else:
                                # Só mostrar erro se não estivermos em fallback
                                if not using_fallback and len(uploaded_csv_files) == 0:
                                    error_msg = f"\nErro: Não foi possível determinar o caminho do arquivo. Por favor, envie um arquivo CSV."
                                    full_response += error_msg
                                    st.error(error_msg)

            # Se já tivermos convertido um arquivo via fallback, não exibir resposta potencialmente confusa do agente
            if using_fallback and converted_file_name:
                message_data = {
                    "role": "assistant", 
                    "content": f"Converti o arquivo para Excel. O arquivo '{converted_file_name}' está disponível para download.",
                    "file_download": {"file_name": converted_file_name}
                }
            else:
                # Adicionar resposta ao histórico
                message_data = {"role": "assistant", "content": full_response}
                if file_download_info:
                    message_data["file_download"] = file_download_info
            
            # Adicionar a mensagem ao histórico
            st.session_state.messages.append(message_data)