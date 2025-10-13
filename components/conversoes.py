import streamlit as st
import pandas as pd
# usando o stringIO para que o pandas possa ler o arquivo em memoria como se fosse
# um arquivo real
from io import StringIO 
from components.dowload_button import dowload_button
from tools.convert_files import *
import os 
import json

# quebrar mais essa função
def componente_conversoes(uploaded_file=None):
    st.subheader("Conversões")
    st.write("Aqui você pode converter seus dados para diferentes formatos.")
    st.write("Suba seu(s) arquivo(s) e divirta-se!")
    if uploaded_file:
        try:
            # Obtém a extensão do arquivo
            file_name = uploaded_file.name if hasattr(uploaded_file, "name") else "arquivo_convertido"
            file_extension = os.path.splitext(file_name)[1].lower()  # Obtém a extensão em minúsculas

            # Lê o conteúdo do arquivo como bytes
            file_content = uploaded_file.read()

            # Handling baseado na extensão do arquivo
            if file_extension == ".csv":
                df = pd.read_csv(StringIO(file_content.decode("utf-8")))
                st.write("Pré-visualização do arquivo CSV:")
                st.write(df)
            elif file_extension in [".xls", ".xlsx"]:
                df = pd.read_excel(uploaded_file)
                st.write("Pré-visualização do arquivo Excel:")
                st.write(df)
            elif file_extension == ".json":
                data = json.loads(file_content.decode("utf-8"))
                st.write("Pré-visualização do arquivo JSON:")
                st.json(data)
            elif file_extension == ".html":
                json_content = file_content.decode("utf-8")
                st.write("Pré-visualização do arquivo HTML:")
                st.markdown(json_content, unsafe_allow_html=True)
            else:
                
                st.warning(f"Tipo de arquivo '{file_extension}' não suportado para visualização.")

            # Seleção de formato de conversão
            st.write("Para qual formato você deseja converter seus dados?")
            option = st.selectbox(
                "Selecione o formato de conversão", 
                (
                    "CSV para Excel", 
                    "CSV para HTML", 
                    "CSV para JSON", 
                    "Excel para CSV", 
                    "Excel para HTML", 
                    "HTML para Excel", 
                    "JSON para CSV"
                ),
            )
            nome_sem_extensao = file_name.split(".",1)[0]

            if st.button("Converter"):
                if option == "CSV para Excel" and file_extension == ".csv":
                    try:
                        # Converte CSV para Excel
                        excel_file = convert_csv_to_excel(StringIO(file_content.decode("utf-8")))
                        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        dowload_button(excel_file, nome_sem_extensao + ".xlsx", mime)
                    except Exception as e:
                        st.error(f"Erro ao converter CSV para Excel: {e}")
                
                elif option == "CSV para HTML" and file_extension == ".csv":
                    try:
                        # Converte CSV para HTML
                        html_content = convert_csv_to_html(StringIO(file_content.decode("utf-8")))
                        mime = "text/html"
                        dowload_button(html_content, nome_sem_extensao + ".html", mime)
                    except Exception as e:
                        st.error(f"Erro ao converter CSV para HTML: {e}")
                
                elif option == "CSV para JSON" and file_extension == ".csv":
                    try:
                        # Converte CSV para JSON
                        json_content = convert_csv_to_json(StringIO(file_content.decode("utf-8")))
                        mime = "application/json"
                        dowload_button(json_content, nome_sem_extensao + ".json", mime)
                    except Exception as e:
                        st.error(f"Erro ao converter CSV para JSON: {e}")
                
                elif option == "Excel para CSV" and file_extension in [".xls", ".xlsx"]:
                    try:
                        # Converte Excel para CSV
                        csv_file = convert_excel_to_csv(uploaded_file)
                        mime = "text/csv"
                        
                        dowload_button(csv_file, nome_sem_extensao + ".csv", mime)
                    except Exception as e:
                                    st.error(f"Erro ao converter Excel para CSV: {e}")
                elif option == "HTML para Excel" and file_extension == ".html":
                    try:
                        # Converte HTML para Excel usando Aspose.Cells
                        excel_file = convert_html_to_excel(uploaded_file)
                        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        dowload_button(excel_file, nome_sem_extensao + ".xlsx", mime)
                    except Exception as e:
                        st.error(f"Erro ao converter HTML para Excel: {e}")             
                else:
                    st.warning("Conversão ainda não implementada para este formato ou tipo de arquivo.")
                    st.warning("Ou você selecionou para converter para o mesmo tipo do arquivo de origem.")
        except pd.errors.EmptyDataError:
            st.error("O arquivo enviado está vazio ou não possui dados válidos.")
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")