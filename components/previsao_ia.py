import streamlit as st
import pandas as pd
import numpy as np
import datetime
from components.utils import selecionar_arquivo, carregar_dataframe
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, accuracy_score

def treinar_modelo_tradicional(df):
    st.write("### Modelo Tradicional (Regressão ou Classificação)")
    
    colunas = df.columns.tolist()
    
    alvo = st.selectbox("Selecione a Coluna Alvo (O que você quer prever?)", colunas, key="trad_alvo")
    colunas_disponiveis = [c for c in colunas if c != alvo]
    preditoras = st.multiselect("Selecione as Colunas Preditoras (Variáveis de entrada)", colunas_disponiveis, default=colunas_disponiveis, key="trad_pred")
    
    tipo_modelo = st.radio("Tipo de Previsão", ["Regressão (Valores Numéricos)", "Classificação (Categorias/Textos)"], key="trad_tipo")
    
    if preditoras and alvo:
        if st.button("Treinar Modelo", use_container_width=True):
            with st.spinner("Treinando IA... isso pode levar alguns segundos."):
                try:
                    df_clean = df[[alvo] + preditoras].dropna()
                    
                    if df_clean.empty:
                        st.error("Após remover linhas vazias, não sobrou nenhum dado para treinar. Verifique seu arquivo.")
                        return

                    X = pd.get_dummies(df_clean[preditoras], drop_first=True)
                    y = df_clean[alvo]
                    
                    # Split
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    
                    if "Regressão" in tipo_modelo:
                        model = RandomForestRegressor(random_state=42)
                        model.fit(X_train, y_train)
                        preds = model.predict(X_test)
                        r2 = r2_score(y_test, preds)
                        st.success(f"Modelo treinado com sucesso! Margem de Acerto (R²): {r2:.2f}")
                    else:
                        model = RandomForestClassifier(random_state=42)
                        model.fit(X_train, y_train)
                        preds = model.predict(X_test)
                        acc = accuracy_score(y_test, preds)
                        st.success(f"Modelo treinado com sucesso! Acurácia: {acc:.2%}")
                    
                    st.session_state['ia_model'] = model
                    st.session_state['ia_features'] = X.columns.tolist()
                    st.session_state['ia_tipo'] = tipo_modelo
                    st.session_state['ia_alvo'] = alvo
                except Exception as e:
                    st.error(f"Erro ao treinar modelo: {e}")
                    
        # Exibe o Simulador se o modelo estiver carregado e o alvo não mudou
        if 'ia_model' in st.session_state and 'ia_features' in st.session_state and st.session_state.get('ia_alvo') == alvo:
            st.markdown("---")
            st.write("### 🔮 Simulador de Previsão")
            st.write("Digite valores fictícios para simular uma previsão na hora:")
            
            inputs_simulador = {}
            cols = st.columns(3)
            
            for i, feat in enumerate(st.session_state['ia_features']):
                col = cols[i % 3]
                with col:
                    inputs_simulador[feat] = st.number_input(f"{feat}", value=0.0, format="%.2f", key=f"sim_{feat}")
                    
            if st.button("Gerar Previsão", type="primary", use_container_width=True):
                input_df = pd.DataFrame([inputs_simulador])
                pred = st.session_state['ia_model'].predict(input_df)[0]
                
                if "Regressão" in st.session_state['ia_tipo']:
                    st.info(f"O valor estimado para '{alvo}' é: **{pred:,.2f}**")
                else:
                    st.info(f"A categoria prevista para '{alvo}' é: **{pred}**")


def treinar_serie_temporal(df):
    st.write("### Previsão de Séries Temporais")
    st.write("Prevê valores futuros baseados na progressão do seu histórico de datas.")
    
    colunas = df.columns.tolist()
    
    col_data = st.selectbox("Selecione a Coluna contendo as Datas", colunas, key="ts_data")
    col_valor = st.selectbox("Selecione a Coluna de Valor (o que deseja prever)", colunas, key="ts_valor")
    
    periodos = st.number_input("Quantos períodos (dias) futuros deseja prever?", min_value=1, max_value=730, value=30, key="ts_periodos")
    
    if st.button("Gerar Previsão Temporal", use_container_width=True):
        with st.spinner("Analisando série temporal com Random Forest..."):
            try:
                df_ts = df[[col_data, col_valor]].copy()
                # Tenta converter para data. dayfirst=True para formato brasileiro
                df_ts[col_data] = pd.to_datetime(df_ts[col_data], dayfirst=True, errors='coerce')
                df_ts = df_ts.dropna().sort_values(col_data)
                
                if df_ts.empty:
                    st.error("A coluna de datas selecionada não contém datas válidas.")
                    return
                
                # Extrair características da data para a IA entender a passagem do tempo
                df_ts['ano'] = df_ts[col_data].dt.year
                df_ts['mes'] = df_ts[col_data].dt.month
                df_ts['dia'] = df_ts[col_data].dt.day
                df_ts['dia_semana'] = df_ts[col_data].dt.dayofweek
                
                X = df_ts[['ano', 'mes', 'dia', 'dia_semana']]
                y = df_ts[col_valor]
                
                # Random forest é decente em detectar sazonalidades (meses/dias da semana)
                model = RandomForestRegressor(random_state=42)
                model.fit(X, y)
                
                # Gerar dataframe com datas futuras
                ultima_data = df_ts[col_data].max()
                datas_futuras = [ultima_data + datetime.timedelta(days=x) for x in range(1, periodos + 1)]
                
                df_futuro = pd.DataFrame({col_data: datas_futuras})
                df_futuro['ano'] = df_futuro[col_data].dt.year
                df_futuro['mes'] = df_futuro[col_data].dt.month
                df_futuro['dia'] = df_futuro[col_data].dt.day
                df_futuro['dia_semana'] = df_futuro[col_data].dt.dayofweek
                
                X_futuro = df_futuro[['ano', 'mes', 'dia', 'dia_semana']]
                previsoes = model.predict(X_futuro)
                
                df_futuro['Previsão Estimada'] = previsoes
                
                st.markdown("---")
                st.write("### 📈 Resultado da Previsão")
                
                # Preparar gráfico conjunto
                df_hist = df_ts[[col_data, col_valor]].copy()
                df_hist.rename(columns={col_valor: 'Histórico Real'}, inplace=True)
                df_hist.set_index(col_data, inplace=True)
                
                df_prev = df_futuro[[col_data, 'Previsão Estimada']].copy()
                df_prev.set_index(col_data, inplace=True)
                
                grafico_df = pd.concat([df_hist, df_prev])
                st.line_chart(grafico_df)
                
                st.write("Tabela de Valores Previstos:")
                st.dataframe(df_futuro[[col_data, 'Previsão Estimada']].head(10))
                
            except Exception as e:
                st.error(f"Erro ao processar série temporal: {e}. Certifique-se de que a coluna de data tem formato válido e o alvo possui números.")

def trainAi(uploaded_files=None):
    st.write("Treine modelos de Machine Learning (Regressão, Classificação ou Séries Temporais) utilizando seus dados.")
    
    selected_file = selecionar_arquivo(uploaded_files, key_suffix="previsao")
    
    if selected_file:
        df = carregar_dataframe(selected_file)
        if df is not None:
            st.markdown("---")
            
            aba_tradicional, aba_temporal = st.tabs(["📊 Regressão / Classificação", "📈 Séries Temporais"])
            
            with aba_tradicional:
                treinar_modelo_tradicional(df)
                
            with aba_temporal:
                treinar_serie_temporal(df)