import pandas as pd
import plotly.graph_objects as go
import streamlit as st

@st.cache_data
def load_data():
    players_valuations_df = pd.read_parquet(
        "DataSet Project/football-transfermarkt-dataset-01/dados_nomalizados/player_valuations_nor.parquet",
        columns=['player_id', 'current_club_id', 'market_value_in_eur']
    )
    games_df = pd.read_parquet(
        "DataSet Project/football-transfermarkt-dataset-01/dados_nomalizados/games.parquet_nor.parquet",
        columns=['home_club_id', 'competition_id', 'season', 'home_club_name']
    )
    players_df = pd.read_parquet(
        "DataSet Project/football-transfermarkt-dataset-01/dados_nomalizados/players_nor.parquet",
        columns=['player_id', 'first_name', 'last_name']
    )
    return players_valuations_df, games_df, players_df

def process_data(players_valuations_df, games_df, players_df):
    merge_club_players = pd.merge(
        players_valuations_df, games_df,
        left_on='current_club_id', right_on='home_club_id',
        how='inner'
    )

    filtrado_league = merge_club_players[merge_club_players['competition_id'] == 'CL']
    colunas_desejadas = ['player_id', 'market_value_in_eur', 'season', 'home_club_name', 'home_club_id']
    filtrado_league = filtrado_league[colunas_desejadas]

    resultado = pd.merge(filtrado_league, players_df, on='player_id', how='inner')
    return resultado[['first_name', 'last_name', 'player_id', 'market_value_in_eur', 'season', 'home_club_name', 'home_club_id']]

def plot_comparison(df, selected_teams, selected_players):
    fig = go.Figure()

    filtered_data = df[df['home_club_name'].isin(selected_teams) & df['last_name'].isin(selected_players)]
    filtered_data = filtered_data.groupby(['home_club_name', 'last_name']).agg({'market_value_in_eur': 'max'}).reset_index()

    for team in selected_teams:
        team_data = filtered_data[filtered_data['home_club_name'] == team]
        fig.add_trace(go.Bar(
            x=team_data['last_name'],
            y=team_data['market_value_in_eur'],
            name=team,
            marker_color='Lightblue' if team == selected_teams[0] else 'Blue'
        ))

    fig.update_layout(
        barmode='group',
        title='Comparação de Valores de Mercado',
        xaxis_title='Jogadores',
        yaxis_title='Valor de Mercado (EUR)',
        xaxis_tickangle=-45
    )

    fig.update_traces(texttemplate='%{y:.2s}', textposition='outside')
    st.plotly_chart(fig)

players_valuations_df, games_df, players_df = load_data()
resultado = process_data(players_valuations_df, games_df, players_df)

season = st.selectbox('Selecione a Temporada:', resultado['season'].unique())

# Filtrar os dados pela temporada selecionada
resultado_filtrado = resultado[resultado['season'] == season]

all_teams = resultado_filtrado['home_club_name'].unique()
selected_teams = st.multiselect('Selecione Times para Comparar:', options=all_teams)

if len(selected_teams) > 0:
    players_in_selection = resultado_filtrado[resultado_filtrado['home_club_name'].isin(selected_teams)]['last_name'].unique()
    selected_players = st.multiselect('Selecione Jogadores:', options=players_in_selection)

    if len(selected_players) > 0:
        plot_comparison(resultado_filtrado, selected_teams, selected_players)
    else:
        st.warning("Selecione pelo menos um jogador.")
else:
    st.warning("Selecione pelo menos um time.")
