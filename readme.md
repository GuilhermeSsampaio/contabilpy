# ContabiliPy 🚀

Bem-vindo ao **ContabiliPy**, sua plataforma de contabilidade automatizada com IA e um arcabouço completo de ferramentas. Este projeto foi criado com o intuito de acelerar e facilitar as rotinas contábeis utilizando Inteligência Artificial e automações baseadas em Python.

## 🎯 Funcionalidades Principais

- **Agente de IA (ContAi):** Um assistente inteligente alimentado pelo modelo Gemini (via biblioteca `agno`). O agente é capaz de interagir com o usuário, interpretar intenções e realizar tarefas automáticas, como converter arquivos CSV para Excel a partir das suas solicitações no chat.
- **Manipulação de Tabelas:** Uma interface rica no Streamlit que conta com abas de diversas funcionalidades:
  - 🔄 **Conversões:** Converta arquivos de forma rápida (CSV para Excel, JSON, HTML, etc.).
  - 📥 **Extrações:** Extraia dados de diferentes formatos de arquivo.
  - 🔗 **Junções:** Junte múltiplas tabelas para análises mais aprofundadas.
  - 📊 **Relatórios & Gráficos:** Gere insights visuais e documentos sumarizados dos seus dados.
  - 📈 **Dashboards:** Crie painéis interativos com as informações processadas.
- **Upload Múltiplo:** Suporte para o upload de diversos tipos de arquivos (`.csv`, `.txt`, `.html`, `.xlsx`, `.json`).

## 🛠️ Tecnologias Utilizadas

- **[Python](https://www.python.org/)** - Linguagem principal.
- **[Streamlit](https://streamlit.io/)** - Framework para construção de toda a interface web.
- **[Pandas](https://pandas.pydata.org/)** - Biblioteca principal para manipulação e análise de dados.
- **[Agno](https://github.com/agno-ai/agno) & Google Gemini** - Utilizados para construir e prover o agente de Inteligência Artificial.
- **Docker & Docker Compose** - Para facilitar a conteinerização e deploy da aplicação.

## ⚙️ Pré-requisitos

Para rodar o projeto localmente, certifique-se de ter o Python (3.10+) instalado. Você também precisará configurar suas credenciais do Google Gemini API.

1. Crie uma pasta oculta `.streamlit` na raiz do projeto.
2. Dentro dela, crie um arquivo chamado `secrets.toml`.
3. Adicione sua chave de API:
```toml
GOOGLE_API_KEY = "sua-chave-api-aqui"
```

## 🚀 Como Executar

Você pode executar o projeto de duas formas: nativamente usando Python ou via Docker.

### Opção 1: Usando Python (Virtual Environment)

1. Clone o repositório.
2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```
3. Ative o ambiente virtual:
   - **Windows:** `venv\Scripts\activate`
   - **Linux/Mac:** `source venv/bin/activate`
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Rode a aplicação:
   ```bash
   streamlit run app.py
   ```

### Opção 2: Usando Docker

1. Certifique-se de que o Docker e o Docker Compose estão instalados e rodando.
2. Execute o comando:
   ```bash
   docker-compose up --build
   ```
3. Acesse a aplicação no seu navegador: `http://localhost:8501`.

## 📂 Estrutura do Projeto

- `/agent` - Contém a lógica de configuração e inicialização do agente de IA (ContAi).
- `/components` - Componentes reutilizáveis do Streamlit (como a barra lateral, gráficos, dashbords, conversões).
- `/pages` - As diferentes páginas da aplicação Streamlit (Agente, Manipulação de tabelas, etc.).
- `/tools` - Funções utilitárias como conversores de arquivos (`convert_csv_to_excel`, etc.).
- `app.py` - O arquivo principal de entrada (Home) da aplicação.
- `requirements.txt` - Lista de dependências do projeto.
- `Dockerfile` & `docker-compose.yaml` - Arquivos de configuração para o Docker.

## 👨‍💻 Desenvolvedor
Desenvolvido por **Guilherme Sampaio**  
[LinkedIn](https://www.linkedin.com/in/guilhermessampaio)
