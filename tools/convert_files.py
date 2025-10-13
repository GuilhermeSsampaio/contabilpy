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
    print(f"Arquivo convertido com sucesso para Excel.")
    return output

# ver sobre o lines e o orient
def convert_csv_to_json(input_file):
    readed_file = pd.read_csv(input_file)
    json_content = readed_file.to_json(orient="records", lines=False, indent=4, force_ascii=False)
    print(f"Arquivo convertido com sucesso para JSON.")
    print(f"conteudo: {json_content}")  # Verifique se os caracteres especiais estão corretos
    return json_content

def convert_csv_to_html(input_file):
    readed_file = pd.read_csv(input_file)
    html_content = readed_file.to_html(index=False)
    print(f"Arquivo convertido com sucesso para HTML.")
    return html_content

def convert_excel_to_csv(input_file):
     # Lê o arquivo CSV enviado
    readed_file = pd.read_excel(input_file)
    
    output = BytesIO()
    readed_file.to_excel(output, index=False) 
    output.seek(0)
    print(f"Arquivo convertido com sucesso para csv.")
    return output

def convert_excel_to_html(input_file):
    readed_file = pd.read_excel(input_file)
    
    html_content = readed_file.to_html(index=False) 
    print(f"Arquivo convertido com sucesso para html.")
    return html_content

def convert_html_to_excel(input_file):
    pass


def convert_json_to_csv(input_file):
    pass

def convert_html_to_csv(input_file):
    pass



