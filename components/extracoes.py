import streamlit as st
import pandas as pd
from components.utils import selecionar_arquivo, carregar_dataframe
from components.dowload_button import dowload_button

def extrair_dados(uploaded_files=None):
    st.subheader("Extração de Dados")
    st.write("Selecione colunas específicas ou aplique filtros para extrair um subconjunto dos seus dados.")
    
    selected_file = selecionar_arquivo(uploaded_files, key_suffix="extracoes")
    
    if selected_file:
        df = carregar_dataframe(selected_file)
        
        if df is not None:
            all_cols = df.columns.tolist()
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### 1. Selecionar Colunas")
                selected_cols = st.multiselect(
                    "Quais colunas você deseja manter?",
                    options=all_cols,
                    default=all_cols
                )
            
            with col2:
                st.markdown("#### 2. Filtrar Linhas (Opcional)")
                usar_filtro = st.checkbox("Aplicar filtro de linhas")
            
            df_filtrado = df[selected_cols] if selected_cols else df.copy()
            
            if usar_filtro and selected_cols:
                f_col1, f_col2, f_col3 = st.columns(3)
                with f_col1:
                    col_filtro = st.selectbox("Coluna para filtrar", selected_cols)
                with f_col2:
                    condicao = st.selectbox("Condição", ["Igual a", "Contém", "Maior que", "Menor que"])
                with f_col3:
                    valor_filtro = st.text_input("Valor")
                
                if valor_filtro:
                    try:
                        if condicao == "Igual a":
                            # Tentando inferir o tipo
                            if pd.api.types.is_numeric_dtype(df_filtrado[col_filtro]):
                                valor_filtro = float(valor_filtro)
                            df_filtrado = df_filtrado[df_filtrado[col_filtro] == valor_filtro]
                        elif condicao == "Contém":
                            df_filtrado = df_filtrado[df_filtrado[col_filtro].astype(str).str.contains(valor_filtro, case=False, na=False)]
                        elif condicao == "Maior que":
                            df_filtrado = df_filtrado[df_filtrado[col_filtro] > float(valor_filtro)]
                        elif condicao == "Menor que":
                            df_filtrado = df_filtrado[df_filtrado[col_filtro] < float(valor_filtro)]
                    except Exception as e:
                        st.error(f"Erro ao aplicar filtro: Valor inválido para a condição escolhida.")
            
            st.markdown("---")
            st.write(f"**Pré-visualização da Extração:** ({df_filtrado.shape[0]} linhas, {df_filtrado.shape[1]} colunas)")
            st.dataframe(df_filtrado.head(50)) # Mostrar no máximo 50 linhas
            
            if st.button("Preparar Extração (CSV)"):
                csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
                original_name = selected_file.name.split('.')[0]
                dowload_button(csv_data, f"{original_name}_extraido.csv", "text/csv")