import streamlit as st
import pandas as pd
from components.utils import carregar_dataframe
from components.dowload_button import dowload_button
from tools.junctions import juntar_dataframes_merge, juntar_dataframes_concat

def juntar_tabelas(uploaded_files=None):
    st.subheader("Relações entre tabelas")
    st.write("Crie relações entre diferentes tabelas (PROCV/Merge) ou empilhe os dados (Concat).")
    
    if not uploaded_files or len(uploaded_files) < 2:
        st.info("Por favor, suba pelo menos DOIS arquivos na seção de upload acima para fazer junções.")
        return
        
    file_names = [f.name for f in uploaded_files]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Tabela A (Esquerda)")
        file_a_name = st.selectbox("Selecione o primeiro arquivo", file_names, key="join_file_a")
    with col2:
        st.markdown("#### Tabela B (Direita)")
        # Seleciona o segundo arquivo por padrão, se houver
        file_b_name = st.selectbox("Selecione o segundo arquivo", file_names, key="join_file_b", index=1 if len(file_names)>1 else 0)
        
    file_a = next(f for f in uploaded_files if f.name == file_a_name)
    file_b = next(f for f in uploaded_files if f.name == file_b_name)
    
    df_a = carregar_dataframe(file_a)
    df_b = carregar_dataframe(file_b)
    
    if df_a is not None and df_b is not None:
        st.markdown("---")
        tipo_juncao = st.radio("Escolha a operação de junção:", ["Merge (PROCV)", "Concatenação (Empilhar)"])
        
        df_resultado = None
        
        if tipo_juncao == "Merge (PROCV)":
            c1, c2, c3 = st.columns(3)
            with c1:
                col_a = st.selectbox("Coluna chave na Tabela A", df_a.columns)
            with c2:
                col_b = st.selectbox("Coluna chave na Tabela B", df_b.columns)
            with c3:
                how = st.selectbox("Tipo de Join", ["inner", "left", "right", "outer"], help="inner: só correspondentes; left: mantém todos da esquerda; right: mantém todos da direita; outer: mantém todos")
                
            if st.button("Executar Merge"):
                try:
                    df_resultado = juntar_dataframes_merge(df_a, df_b, col_a, col_b, how)
                except Exception as e:
                    st.error(f"Erro ao realizar merge: {e}")
                    
        else:
            if st.button("Executar Concatenação"):
                try:
                    # Assumindo empilhamento vertical (axis=0)
                    df_resultado = juntar_dataframes_concat([df_a, df_b], axis=0)
                except Exception as e:
                    st.error(f"Erro ao concatenar: {e}")
                    
        if df_resultado is not None:
            st.success("Junção realizada com sucesso!")
            st.write(f"**Tamanho do resultado:** {df_resultado.shape[0]} linhas, {df_resultado.shape[1]} colunas.")
            st.dataframe(df_resultado.head(50))
            
            csv_data = df_resultado.to_csv(index=False).encode('utf-8')
            nome_arquivo = f"juncao_{file_a_name.split('.')[0]}_{file_b_name.split('.')[0]}.csv"
            dowload_button(csv_data, nome_arquivo, "text/csv")