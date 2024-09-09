import streamlit as st
import pandas as pd
import pickle as pkl
import numpy as np


def nomescertos(result):
    return 'Vitória' if result == 1 else 'Empate' if result == 0 else 'Derrota'


st.title("🎯 Quem ganha?")
st.subheader("Previsão de Vitória")

model_path = 'model_results.pkl'
with open(model_path, 'rb') as f:
    results = pkl.load(f)
    

valid_models = {name: model_data for name, model_data in results.items() if hasattr(model_data['model'], 'predict')}

if valid_models:
    st.success('Modelos carregados corretamente e prontos para predição.')


    tabela_games = pd.read_parquet('DataSet Project/transfermarkrt-dados-clean/games.parquet')
    home_formations = tabela_games['home_club_formation'].unique().tolist()
    away_formations = tabela_games['away_club_formation'].unique().tolist()


    col1, col2 = st.columns(2)
        
    with col1:
        st.subheader("📊 Features")
        st.write("Insira as informações do jogo para prever o resultado")
            
        minutos_partida = st.number_input('Minutos da partida', min_value=1, value=120)
        gols_total = st.number_input('Gols (total)', min_value=0, value=0)
        assists_total = st.number_input('Assistências (total)', min_value=0, value=0)
        cartoes_amarelos = st.number_input('Cartões amarelos', min_value=0, value=0)
        cartoes_vermelhos = st.number_input('Cartões vermelhos', min_value=0, value=0)
        home_club_formation = st.selectbox('Selecione a formação do time da casa', options=home_formations)
        away_club_formation = st.selectbox('Selecione a formação do time visitante', options=away_formations)

        media_gols_minuto = gols_total / minutos_partida
        media_faltas_jogo = (cartoes_amarelos + cartoes_vermelhos) / minutos_partida
        assists = assists_total


        user_inputs = {
                'media_gols_minuto': media_gols_minuto,
                'media_faltas_jogo': media_faltas_jogo,
                'assists': assists,
                'home_club_formation': home_club_formation,
                'away_club_formation': away_club_formation
            }

        user_inputs_df = pd.DataFrame([user_inputs])

        expected_target = st.selectbox(
                    "Selecione o resultado esperado", 
                    options=[1, 0, -1], 
                    format_func=lambda x: 'Vitória' if x == 1 else 'Empate' if x == 0 else 'Derrota'
                    )
        

    with col2:
        st.subheader("🔮 Previsão")
        if st.button('Prever'):
            for model_name, model_data in valid_models.items():
                model = model_data['model']
                preprocessing_pipeline = model_data['preprocessor']  

                try:

                    X_preprocessed = preprocessing_pipeline.transform(user_inputs_df)

                    pred = model.predict(X_preprocessed)

                    pred_text = nomescertos(pred[0])
                    expected_text = nomescertos(expected_target)

                    if pred[0] == expected_target:
                        st.success(f"{model_name} previu corretamente o resultado esperado: {pred_text}")
                    else:
                        st.error(f"{model_name} previu incorretamente o resultado esperado: {pred_text}")
                    
                except Exception as e:
                    st.error(f"Erro ao processar as entradas com {model_name}: {e}")
else:
    st.error(f"O arquivo {model_path} não foi encontrado. Certifique-se de que o modelo está no caminho correto.")
