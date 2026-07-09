import streamlit as st
st.set_page_config(page_title="ContabiliPy | Manipulação", page_icon="logo.png", layout="wide")
import pandas as pd
from components.sidebar import sidebar
from components.conversoes import componente_conversoes
from components.dashboards import gerar_dashboard
from components.extracoes import extrair_dados
from components.juncoes import juntar_tabelas
from components.relatorios import gerar_relatorio

sidebar()
st.header("Manipulação de tabelas")
# Upload do arquivo
uploaded_files = st.file_uploader(
        "Suba o(s) arquivo(s) que deseja manipular",
        type=["csv", "txt", "html", "xlsx", "json"],
        accept_multiple_files=True
    )
conversoes, extracoes, juncoes, relatorios, dashboards = st.tabs(["Conversões", "Extrações", "Junções", "Relatórios", "Dashboards"])


from components.help_modal import render_help

with conversoes:
    render_help(
        "Como funciona a Conversão?",
        "Transforme seus arquivos instantaneamente! Suportamos **Excel (.xlsx), CSV, JSON e HTML**.\n\n"
        "Basta escolher o formato desejado e o sistema cuidará da formatação. Se você subiu vários arquivos de uma vez, "
        "todos serão convertidos em lote e os botões de download aparecerão na tela.",
        "conversoes"
    )
    componente_conversoes(uploaded_files)
with extracoes:
    render_help(
        "Como usar Extrações e Filtros",
        "Você pode **Ocultar colunas** desmarcando-as na lista acima da tabela.\n\n"
        "Para **Filtrar dados**, escolha uma coluna e use os operadores lógicos matemáticos:\n"
        "- `>` (Maior que)\n- `<` (Menor que)\n- `==` (Exatamente Igual a)\n- `!=` (Diferente de)\n\n"
        "*(Dica: Se a coluna for de texto, use `==` ou `!=`)*.",
        "extracoes"
    )
    extrair_dados(uploaded_files)
with juncoes:
    render_help(
        "Diferença entre Merge e Concat",
        "**Merge (Mesclar)**: Funciona como o `PROCV` do Excel. Ele une as colunas de duas tabelas lado a lado baseando-se em uma "
        "coluna em comum (ex: cruzar uma tabela de Vendas com uma de Clientes usando o campo `ID_Cliente`).\n\n"
        "**Concat (Empilhar)**: Coloca os dados de uma tabela embaixo da outra. Ideal para juntar relatórios mensais "
        "diferentes que possuem as mesmas colunas (ex: Janeiro + Fevereiro).",
        "juncoes"
    )
    juntar_tabelas(uploaded_files)
with relatorios:
    render_help(
        "Gerador de Laudos Analíticos",
        "Essa seção escaneia os seus dados e gera um \"Raio-X\" completo em formato de texto. "
        "Ele detalha os tipos das colunas, dados nulos, amostras e fornece a contagem exata da sua base.\n\n"
        "Você pode fazer o download desse laudo em formato `.txt` para envio por e-mail ou auditorias.",
        "relatorios"
    )
    gerar_relatorio(uploaded_files)
with dashboards:
    render_help(
        "Criando Dashboards Interativos",
        "Selecione o tipo de gráfico (Barras, Linha, Área, Pizza, Dispersão ou Histograma) e plote suas colunas numéricas "
        "e categóricas na tela.\n\n"
        "**Dica de ouro:** Os gráficos são interativos (motor Plotly). Você pode passar o mouse para ver os números reais, "
        "dar zoom em áreas específicas e até clicar no ícone de câmera no canto do gráfico para salvá-lo como imagem `.png`!",
        "dashboards"
    )
    gerar_dashboard(uploaded_files)
