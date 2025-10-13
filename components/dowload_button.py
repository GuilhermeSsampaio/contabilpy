import streamlit as st
def dowload_button(data, file_name, mime):
    st.download_button(
                        label="Baixar arquivo convertido",
                        data=data,
                        file_name=file_name,
                        mime=mime
                    )