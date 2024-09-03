import streamlit as st

# Configurações da página
st.set_page_config(
    page_title="Pullebyte - Análise de Estatísticas de Futebol",
    layout="wide",
    menu_items={
        'About': "Análise realizada da Champions League com base nos datasets disponíveis no Kaggle referentes às temporadas até 2022."
    },
    initial_sidebar_state="auto",
)

# Logo e título do projeto
st.image('img/logo-text-pullebyte.png', width=280)
st.write("""
    <h2>Sobre o Projeto</h2>
    <p>Este projeto visa analisar dados da UEFA Champions League, focando em estatísticas como marcação de gols, desempenho ofensivo e defensivo, e tipos de formações utilizadas.</p>
    <p>Nesta análise foi utilizado o dataset disponível no Kaggle: <a href='https://www.kaggle.com/datasets/davidcariboo/player-scores?select=game_lineups.csv'>Player Scores</a>.</p>
""", unsafe_allow_html=True)

st.divider()
st.write("""
         <h2>Perguntas que orientam a análise</h2>
         <p>Para guiar a análise dos dados, foram definidas as seguintes perguntas:</p>
        <h3>Pergunta 1</h3>
        <p>Podemos agrupar equipes de futebol com base em estatísticas como eficácia na marcação de gols, desempenho ofensivo e defensivo, tipos de formações mais utilizadas, entre outras, visando identificar seus estilos de jogo?</p>
        <h3>Pergunta 2</h3>
        <p>É possível prever a probabilidade de um time ganhar, perder ou empatar uma partida com base nos dados das estatísticas dos jogadores e times como marcação de gols, eficácia ofensiva e faltas cometidas?
</p>
""", unsafe_allow_html=True)

st.write("</div>", unsafe_allow_html=True)