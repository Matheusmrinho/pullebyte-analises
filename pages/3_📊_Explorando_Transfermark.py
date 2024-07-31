import pandas as pd
import streamlit as st

# Função para carregar dados
def load_data(file_path):
    return pd.read_parquet(file_path)

def filter_data(data_frame, filter_by, item_filtro):
    return data_frame[data_frame[filter_by] == item_filtro]
 

# Carregar os dados
games_df = load_data(r'DataSet Project/football-transfermarkt-dataset-01/parquet/games.parquet')
# games_df = filter_data(games_df, 'season', '2021')
games_df = filter_data(games_df, 'competition_id', 'CL')
# game_events_df = load_data(r'DataSet Project/football-transfermarkt-dataset-01/parquet/game_events.parquet')
# players_df = load_data(r'DataSet Project/football-transfermarkt-dataset-01/parquet/players.parquet')
funcao = lambda x,: [filter_data(games_df, 'home_club_id', x), filter_data(games_df, 'away_club_id', x)]


games_by_clubs = {
    'Real Madrid': funcao(418),'Liverpool': funcao(31), 'Villarreal': funcao(1050),'Man. City': funcao(281),
    'Benfica': funcao(294),'Atlético Madrid': funcao(13),'Bayern Munich': funcao(27),'Chelsea': funcao(631),
    'LOSC': funcao(1082),'Inter': funcao(46),'Salzburg': funcao(1004),'Ajax': funcao(610), 'Paris Saint-Germain': funcao(583),
    'Sporting CP': funcao(1062),'Juventus': funcao(506), 'Manchester United': funcao(1519), 'Barcelona': funcao(131),
    'Club Brugge': funcao(2282),'Sheriff': funcao(1005),'Wolfsburg': funcao(82),'Dynamo Kyiv': funcao(338),
    'Sevilla': funcao(368),'Shakhtar Donetsk': funcao(660),'Zenit': funcao(964),'Porto': funcao(720),'Milan': funcao(5),
    'Dortmund': funcao(16),'Young Boys': funcao(1006),'Malmo': funcao(1007),'RB Leipzig': funcao(23826),'Besiktas': funcao(114),
    'Atalanta': funcao(800),
}


# st.dataframe(games_by_clubs)
# for i in games_by_clubs.keys():
#      for j in range(0,2):
#          games_by_clubs[i][j] = games_by_clubs[i][j].merge(game_events_df, on='game_id').merge(players_df, on='player_id')

# st.dataframe(games_by_clubs['Chelsea'][0])
games_df = filter_data(games_df,'season',2021)