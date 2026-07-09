import streamlit as st
import pandas as pd
from components.utils import selecionar_arquivo, carregar_dataframe
import plotly.express as px

def render_chart(df, tipo_grafico, eixo_x, eixo_y):
    # Trata caso nulo ou vazio
    if not eixo_x or not eixo_y:
        st.warning("Selecione os eixos.")
        return
        
    try:
        if tipo_grafico == "Barras":
            st.bar_chart(df.set_index(eixo_x)[eixo_y])
        elif tipo_grafico == "Linhas":
            st.line_chart(df.set_index(eixo_x)[eixo_y])
        elif tipo_grafico == "Área":
            st.area_chart(df.set_index(eixo_x)[eixo_y])
        elif tipo_grafico == "Dispersão":
            st.scatter_chart(df.set_index(eixo_x)[eixo_y])
        elif tipo_grafico == "Pizza":
            fig = px.pie(df, names=eixo_x, values=eixo_y)
            st.plotly_chart(fig, use_container_width=True)
        elif tipo_grafico == "Histograma":
            fig = px.histogram(df, x=eixo_y)
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico: {e}")

def gerar_dashboard(uploaded_files=None):
    st.subheader("Dashboards e Visualizações")
    st.write("Crie painéis interativos combinando métricas (KPIs) e diversos gráficos na mesma tela.")
    
    selected_file = selecionar_arquivo(uploaded_files, key_suffix="dashboards")
    
    if selected_file:
        df = carregar_dataframe(selected_file)
        
        if df is not None:
            st.markdown("---")
            
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            
            if not numeric_cols:
                st.warning("O arquivo selecionado não possui colunas numéricas para montar métricas.")
                return
                
            # Seção de Métricas (KPIs)
            st.markdown("### 🎯 Métricas Principais (Somas)")
            kpi_cols = st.columns(3)
            
            for i in range(min(3, len(numeric_cols))):
                col_name = numeric_cols[i]
                total = df[col_name].sum()
                with kpi_cols[i]:
                    st.metric(label=f"Total: {col_name}", value=f"{total:,.2f}")
                    
            st.markdown("---")
            
            # Seção de Gráficos do Dashboard
            st.markdown("### 📊 Gráficos Personalizados")
            
            col1, col2 = st.columns(2)
            
            opcoes_graficos = ["Barras", "Linhas", "Área", "Dispersão", "Pizza", "Histograma"]
            
            with col1:
                st.markdown("**Painel 1**")
                tipo_1 = st.selectbox("Tipo de Gráfico", opcoes_graficos, key="t1")
                eixo_x_1 = st.selectbox("Eixo X (Categorias/Rótulos)", df.columns, key="x1", index=0)
                eixo_y_1 = st.selectbox("Eixo Y (Valores Numéricos)", numeric_cols, key="y1", index=0)
                render_chart(df, tipo_1, eixo_x_1, eixo_y_1)
                
            with col2:
                st.markdown("**Painel 2**")
                tipo_2 = st.selectbox("Tipo de Gráfico", opcoes_graficos, key="t2", index=1)
                eixo_x_2 = st.selectbox("Eixo X (Categorias/Rótulos)", df.columns, key="x2", index=min(1, len(df.columns)-1))
                eixo_y_2 = st.selectbox("Eixo Y (Valores Numéricos)", numeric_cols, key="y2", index=min(1, len(numeric_cols)-1))
                render_chart(df, tipo_2, eixo_x_2, eixo_y_2)