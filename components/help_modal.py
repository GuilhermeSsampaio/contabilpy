import streamlit as st

@st.dialog("Central de Ajuda")
def _show_modal(titulo: str, conteudo: str):
    st.subheader(titulo)
    st.markdown(conteudo)

def render_help(titulo: str, conteudo: str, key: str):
    """
    Componente reutilizável estilo 'React Props'.
    Renderiza um botão discreto e abre o modal quando clicado.
    """
    if st.button("Entenda como funciona", icon=":material/help:", key=f"btn_help_{key}", help="Clique para abrir as instruções"):
        _show_modal(titulo, conteudo)
