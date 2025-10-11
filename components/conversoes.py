import streamlit as st
import pandas as pd
from io import StringIO  # Importa StringIO do módulo io
from tools.convert_files import convert_csv_to_excel
# quebrar mais essa função
def componente_conversoes(uploaded_file=None):
    st.subheader("Conversões")
    st.write("Aqui você pode converter seus dados para diferentes formatos.")
    st.write("Suba seu(s) arquivo(s) e divirta-se!")
    if uploaded_file:
        try:
            # Lê o conteúdo do arquivo como bytes e converte para um DataFrame
            file_content = uploaded_file.read()  # Lê o conteúdo do arquivo
            df = pd.read_csv(StringIO(file_content.decode("utf-8")))  # Decodifica e lê como CSV
            st.write("Pré-visualização do arquivo:")
            st.write(df)
            
            st.write("Para qual formato você deseja converter seus dados?")
            option = st.selectbox(
                "Selecione o formato de conversão", 
                ("CSV para Excel", "Excel para CSV", "JSON para CSV", "CSV para JSON", "Excel para HTML", "HTML para Excel"),
            )
            
            if st.button("Converter"):
                if option == "CSV para Excel":
                    # Converte o arquivo CSV para Excel
                    excel_file = convert_csv_to_excel(StringIO(file_content.decode("utf-8")))
                    
                    # Botão para baixar o arquivo convertido
                    st.download_button(
                        label="Baixar arquivo convertido",
                        data=excel_file,
                        file_name="arquivo_convertido.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("Conversão ainda não implementada para este formato.")
        except pd.errors.EmptyDataError:
            st.error("O arquivo enviado está vazio ou não possui dados válidos.")
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")