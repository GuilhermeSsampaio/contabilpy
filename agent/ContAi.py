from agno.agent import Agent
from agno.models.google import Gemini
import streamlit as st
from tools.convert_files import convert_csv_to_excel
import os
import io

gemini_api_key = st.secrets["GOOGLE_API_KEY"]

# Função wrapper para converter CSV para Excel que o agente poderá chamar
# é como uma interface para avisar o agente sobre a funcionalidade disponível
# a conversao real é feita na função convert_csv_to_excel, na pagina agent.py

def converter_csv_para_excel(file_path):
    """
    Converte um arquivo CSV para Excel
    
    Args:
        file_path (str): Caminho para o arquivo CSV a ser convertido
    
    Returns:
        dict: Dicionário com informações sobre o resultado da conversão
    """
    try:
        if not os.path.exists(file_path):
            return {"success": False, "message": f"Arquivo {file_path} não encontrado"}
        
        if not file_path.lower().endswith('.csv'):
            return {"success": False, "message": f"O arquivo {file_path} não é um CSV"}
        # essa linha somente chama a função de conversão e obtém o arquivo convertido em memória
        # output_bytes = convert_csv_to_excel(file_path)
        file_name = os.path.splitext(os.path.basename(file_path))[0] + ".xlsx"
        
        return {
            "success": True, 
            "file_name": file_name,
            "message": f"Arquivo {file_name} convertido com sucesso"
        }
    except Exception as e:
        return {"success": False, "message": f"Erro ao converter {file_path}: {str(e)}"}

contAgent = Agent(
    name="ContAgent",
    model=Gemini(id="gemini-2.5-flash", api_key=gemini_api_key),
    instructions=[
        "Você é um assistente contábil que ajuda com automação de tarefas",
        "Quando o usuário pedir para converter um arquivo CSV para Excel, identifique o caminho do arquivo nos 'Arquivos salvos' e use a função converter_csv_para_excel",
        "Se o usuário não especificar qual arquivo converter e houver múltiplos CSVs, pergunte qual deles deve ser convertido",
        "Após a conversão, informe ao usuário que o arquivo Excel está disponível para download"
    ],
    tools=[converter_csv_para_excel]
)

# contAgent.cli_app(stream=True)

