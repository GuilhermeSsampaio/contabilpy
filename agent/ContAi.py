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

def converter_documento(file_path: str, formato_destino: str) -> dict:
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
                
        return {"success": True, "message": f"O arquivo {novo_nome} foi gerado com sucesso. O sistema já criou o botão de download."}
        
    except Exception as e:
        return {"success": False, "message": f"Erro durante a conversão: {str(e)}"}

def analisar_estatisticas_planilha(file_path: str, query_pandas: str = "") -> str:
    """
    Lê um arquivo de dados (Excel, CSV, JSON, HTML) e retorna um resumo estatístico das informações.
    Se o usuário fizer uma pergunta com filtros ("média de quem foi aprovado", "idade maior que 30"), 
    você pode passar uma string no argumento `query_pandas` para filtrar a tabela ANTES de tirar as estatísticas.
    
    Args:
        file_path (str): Caminho absoluto para o arquivo que será lido.
        query_pandas (str, opcional): Uma string no formato aceito pelo pandas.DataFrame.query(). 
                                      Exemplos: "Status_Credito == 'Aprovado'", "Idade > 30 and Renda > 2000".
        
    Returns:
        str: Resumo com os nomes das colunas, amostra dos dados filtrados e as estatísticas matemáticas.
    """
    try:
        import pandas as pd
        if not os.path.exists(file_path):
            return f"Arquivo {file_path} não encontrado."
            
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext == '.xlsx':
            df = pd.read_excel(file_path)
        elif ext == '.json':
            df = pd.read_json(file_path)
        elif ext == '.html':
            df = pd.read_html(file_path)[0]
        else:
            return "Formato não suportado para análise estatística pela IA."
            
        # Aplica o filtro se a IA enviar uma query
        if query_pandas:
            try:
                df = df.query(query_pandas)
            except Exception as e:
                return f"Erro ao aplicar a query '{query_pandas}'. Tente formular de outra forma. Erro técnico: {str(e)}"
                
        if df.empty:
            return "A tabela ficou vazia após aplicar a query. Nenhum dado corresponde ao filtro."
            
        resultado = f"O arquivo possui {df.shape[0]} linhas e {df.shape[1]} colunas.\n\n"
        resultado += f"Colunas:\n{list(df.columns)}\n\n"
        
        resultado += f"Amostra dos Dados (5 primeiras linhas):\n{df.head(5).to_string()}\n\n"
        
        # Describe apenas colunas numéricas
        numericos = df.select_dtypes(include=['number'])
        if not numericos.empty:
            resultado += f"Estatísticas Numéricas (Média, Mínimo, Máximo, etc):\n{numericos.describe().to_string()}\n"
        else:
            resultado += "Não há colunas numéricas neste arquivo para gerar estatísticas matemáticas."
            
        return resultado
    except Exception as e:
        return f"Erro ao analisar arquivo: {str(e)}"

contAgent = Agent(
    name="ContAgent",
    model=Gemini(id="gemini-2.5-flash-lite", api_key=gemini_api_key),
    instructions=[
        "Você é o ContAi, um assistente de inteligência artificial especializado em automação de tarefas de contabilidade e análise de dados.",
        "Vá direto ao ponto nas suas respostas. Não inicie frases com saudações ('Olá', 'Oi') e não se apresente novamente, EXCETO se o usuário enviar APENAS uma saudação ('oi', 'olá', 'tudo bem?').",
        "Aja como se já estivesse em uma conversa fluída com o usuário.",
        "Sempre que o usuário pedir para converter arquivos ou analisar dados, encontre o caminho exato deles listado no seu histórico como '[SISTEMA: Arquivos salvos no meu sistema nesta mensagem:]'.",
        "CRÍTICO: Para usar a ferramenta `analisar_estatisticas_planilha`, você DEVE OBRIGATORIAMENTE passar o parâmetro `file_path`. E caso a pergunta exija filtros (ex: média apenas de aprovados), passe também o parâmetro `query_pandas` (ex: query_pandas=\"Status_Credito == 'Aprovado'\").",
        "Sempre avise o usuário explicitamente quando uma conversão for bem sucedida, MAS NUNCA imprima diretórios ou caminhos do sistema (ex: C:\\Users\\...). Diga apenas que o arquivo está pronto no botão abaixo.",
        "Seja cordial, direto e objetivo."
    ],
    tools=[converter_documento, analisar_estatisticas_planilha]
)
