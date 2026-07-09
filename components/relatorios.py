import streamlit as st
import pandas as pd
import io
from components.utils import selecionar_arquivo, carregar_dataframe
from components.dowload_button import dowload_button

def gerar_relatorio(uploaded_files=None):
    st.subheader("Relatórios Estatísticos")
    st.write("Gere um sumário estatístico detalhado do seu conjunto de dados.")
    
    selected_file = selecionar_arquivo(uploaded_files, key_suffix="relatorios")
    
    if selected_file:
        df = carregar_dataframe(selected_file)
        
        if df is not None:
            # Métricas chave
            st.markdown("### Visão Geral")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de Linhas", f"{df.shape[0]:,}")
            with col2:
                st.metric("Total de Colunas", f"{df.shape[1]:,}")
            with col3:
                total_nulos = df.isnull().sum().sum()
                st.metric("Valores Nulos Totais", f"{total_nulos:,}")
                
            st.markdown("---")
            
            # Análise Estatística
            st.markdown("### Estatísticas Descritivas (Apenas Numéricos)")
            numeric_desc = df.describe()
            if not numeric_desc.empty:
                st.dataframe(numeric_desc)
            else:
                st.info("O conjunto de dados não possui colunas numéricas para estatísticas descritivas.")
                
            st.markdown("### Tipos de Dados e Nulos por Coluna")
            # Criando um DF amigável para exibir dtypes e nulos
            info_df = pd.DataFrame({
                'Tipo de Dado': df.dtypes.astype(str),
                'Valores Nulos': df.isnull().sum(),
                '% de Nulos': (df.isnull().sum() / len(df) * 100).round(2).astype(str) + '%'
            })
            st.dataframe(info_df)
            
            st.markdown("---")
            if st.button("Baixar Relatório (TXT)"):
                buffer = io.StringIO()
                buffer.write(f"RELATÓRIO ESTATÍSTICO: {selected_file.name}\n")
                buffer.write("="*50 + "\n\n")
                
                buffer.write("1. VISÃO GERAL\n")
                buffer.write(f"- Total de Linhas: {df.shape[0]}\n")
                buffer.write(f"- Total de Colunas: {df.shape[1]}\n")
                buffer.write(f"- Valores Nulos Totais: {total_nulos}\n\n")
                
                buffer.write("2. INFORMAÇÕES DAS COLUNAS\n")
                buffer.write(info_df.to_string() + "\n\n")
                
                buffer.write("3. ESTATÍSTICAS DESCRITIVAS (Numéricas)\n")
                if not numeric_desc.empty:
                    buffer.write(numeric_desc.to_string() + "\n")
                else:
                    buffer.write("Nenhuma coluna numérica disponível.\n")
                
                txt_data = buffer.getvalue().encode('utf-8')
                dowload_button(txt_data, f"relatorio_{selected_file.name.split('.')[0]}.txt", "text/plain")