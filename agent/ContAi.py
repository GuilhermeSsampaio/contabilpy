from agno.agent import Agent
from agno.models.google import Gemini
import streamlit as st
import os
import tempfile
from tools.convert_files import (
    convert_csv_to_excel, convert_excel_to_csv, convert_csv_to_json,
    convert_json_to_csv, convert_excel_to_html, convert_html_to_excel,
    convert_csv_to_html, convert_html_to_csv
)

gemini_api_key = st.secrets["GOOGLE_API_KEY"]

def converter_documento(file_path, formato_destino):
    """
    Converte um arquivo local para o formato de destino desejado.
    
    Args:
        file_path (str): Caminho absoluto para o arquivo original a ser convertido.
        formato_destino (str): Formato desejado. Pode ser 'excel', 'csv', 'json' ou 'html'.
        
    Returns:
        dict: Resultado da conversão com sucesso e o caminho do novo arquivo gerado.
    """
    try:
        if not os.path.exists(file_path):
            return {"success": False, "message": f"Arquivo {file_path} não encontrado no sistema."}
            
        extensao_origem = os.path.splitext(file_path)[1].lower().replace('.', '')
        nome_base = os.path.splitext(os.path.basename(file_path))[0]
        formato_destino = formato_destino.lower()
        
        ext_map = {'excel': 'xlsx', 'csv': 'csv', 'json': 'json', 'html': 'html'}
        ext_dest = ext_map.get(formato_destino, formato_destino)
        
        novo_nome = f"{nome_base}_convertido.{ext_dest}"
        pasta_temp = os.path.join(tempfile.gettempdir(), "contabilipy_outputs")
        os.makedirs(pasta_temp, exist_ok=True)
        novo_caminho = os.path.join(pasta_temp, novo_nome)
        
        output_data = None
        
        if extensao_origem == 'csv' and formato_destino in ['excel', 'xlsx']:
            output_data = convert_csv_to_excel(file_path).getvalue()
        elif extensao_origem == 'csv' and formato_destino == 'json':
            output_data = convert_csv_to_json(file_path)
        elif extensao_origem == 'csv' and formato_destino == 'html':
            output_data = convert_csv_to_html(file_path)
        elif extensao_origem in ['xlsx', 'xls'] and formato_destino == 'csv':
            output_data = convert_excel_to_csv(file_path)
        elif extensao_origem in ['xlsx', 'xls'] and formato_destino == 'html':
            output_data = convert_excel_to_html(file_path)
        elif extensao_origem == 'html' and formato_destino in ['excel', 'xlsx']:
            output_data = convert_html_to_excel(file_path).getvalue()
        elif extensao_origem == 'json' and formato_destino == 'csv':
            output_data = convert_json_to_csv(file_path)
        elif extensao_origem == 'html' and formato_destino == 'csv':
            output_data = convert_html_to_csv(file_path)
        else:
            return {"success": False, "message": f"Conversão de {extensao_origem} para {formato_destino} não é suportada."}
            
        with open(novo_caminho, 'wb') as f:
            if isinstance(output_data, str):
                f.write(output_data.encode('utf-8'))
            else:
                f.write(output_data)
                
        # Injetar o download para a interface
        if "pending_downloads" not in st.session_state:
            st.session_state.pending_downloads = []
        st.session_state.pending_downloads.append({
            "file_name": novo_nome,
            "file_path": novo_caminho
        })
                
        return {
            "success": True,
            "message": f"Conversão finalizada com sucesso! O arquivo está em: {novo_caminho}",
            "file_path": novo_caminho,
            "file_name": novo_nome
        }
        
    except Exception as e:
        return {"success": False, "message": f"Erro durante a conversão: {str(e)}"}

contAgent = Agent(
    name="ContAgent",
    model=Gemini(id="gemini-2.5-flash", api_key=gemini_api_key),
    instructions=[
        "Você é o ContAi, um assistente de inteligência artificial especializado em automação de tarefas de contabilidade e análise de dados.",
        "Vá direto ao ponto nas suas respostas. Não inicie frases com saudações ('Olá', 'Oi') e não se apresente novamente, EXCETO se o usuário enviar APENAS uma saudação ('oi', 'olá', 'tudo bem?').",
        "Aja como se já estivesse em uma conversa fluída com o usuário.",
        "Sempre que o usuário pedir para converter um ou mais arquivos, encontre o caminho deles listado no seu prompt como 'Arquivos salvos no meu sistema'.",
        "CRÍTICO: Ao usar a ferramenta `converter_documento`, você DEVE usar exatamente os seguintes parâmetros: `file_path` (string com o caminho absoluto do arquivo) e `formato_destino` (string com o formato: excel, csv, json ou html).",
        "Sempre avise o usuário explicitamente quando a conversão for bem sucedida e diga que ele pode baixar o arquivo utilizando o botão fornecido abaixo.",
        "Se o usuário pedir para converter e não anexar o arquivo, solicite que ele faça o upload.",
        "Seja cordial, direto e objetivo."
    ],
    tools=[converter_documento]
)

