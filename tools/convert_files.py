import pandas as pd
from io import BytesIO

# função de conversao de um unico arquivo, criar a multipla
def convert_csv_to_excel(input_file):
    # Lê o arquivo CSV enviado
    readed_file = pd.read_csv(input_file)
    
    # Cria um objeto BytesIO para armazenar o arquivo Excel em memória
    output = BytesIO()
    readed_file.to_excel(output, index=False, engine='openpyxl')  # Usa o engine 'openpyxl' para Excel
    output.seek(0)  # Retorna o ponteiro para o início do arquivo em memória
    print(f"Arquivo convertido com sucesso para Excel.:")
    return output

def convert_excel_to_csv(input_file):
    pass

def convert_json_to_csv(input_file):
    pass

def convert_csv_to_json(input_file):
    pass

def convert_html_to_csv(input_file):
    pass

def convert_csv_to_html(input_file):
    pass

def convert_excel_to_html(input_file):
    pass

def convert_html_to_(input_file):
    pass

