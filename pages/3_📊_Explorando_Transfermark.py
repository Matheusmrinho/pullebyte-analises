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
game_events_df = load_data(r'DataSet Project/football-transfermarkt-dataset-01/parquet/game_events.parquet')
players_df = load_data(r'DataSet Project/football-transfermarkt-dataset-01/parquet/players.parquet')

games_by_clubs = {
    'Real Madrid': [filter_data(games_df, 'home_club_id', 418), filter_data(games_df, 'away_club_id', 418)],
    'Liverpool': [filter_data(games_df, 'home_club_id', 31), filter_data(games_df, 'away_club_id', 31)],
    'Villarreal': [filter_data(games_df, 'home_club_id', 1050), filter_data(games_df, 'away_club_id', 1050)],
    'Man. City': [filter_data(games_df, 'home_club_id', 281), filter_data(games_df, 'away_club_id', 281)],
    'Benfica': [filter_data(games_df, 'home_club_id', 294), filter_data(games_df, 'away_club_id', 294)],
    'Atlético Madrid': [filter_data(games_df, 'home_club_id', 13), filter_data(games_df, 'away_club_id', 13)],
    'Bayern Munich': [filter_data(games_df, 'home_club_id', 27), filter_data(games_df, 'away_club_id', 27)],
    'Chelsea': [filter_data(games_df, 'home_club_id', 631), filter_data(games_df, 'away_club_id', 631)],
    'LOSC': [filter_data(games_df, 'home_club_id', 1082), filter_data(games_df, 'away_club_id', 1082)],
    'Inter': [filter_data(games_df, 'home_club_id', 46), filter_data(games_df, 'away_club_id', 46)],
    'Salzburg': [filter_data(games_df, 'home_club_id', 1004), filter_data(games_df, 'away_club_id', 1004)],
    'Ajax': [filter_data(games_df, 'home_club_id', 610), filter_data(games_df, 'away_club_id', 610)],
    'Paris Saint-Germain': [filter_data(games_df, 'home_club_id', 583), filter_data(games_df, 'away_club_id', 583)],
    'Sporting CP': [filter_data(games_df, 'home_club_id', 1062), filter_data(games_df, 'away_club_id', 1062)],
    'Juventus': [filter_data(games_df, 'home_club_id', 506), filter_data(games_df, 'away_club_id', 506)],
    'Manchester United': [filter_data(games_df, 'home_club_id', 1519), filter_data(games_df, 'away_club_id', 1519)],
    'Barcelona': [filter_data(games_df, 'home_club_id', 131), filter_data(games_df, 'away_club_id', 131)],
    'Club Brugge': [filter_data(games_df, 'home_club_id', 2282), filter_data(games_df, 'away_club_id', 2282)],
    'Sheriff': [filter_data(games_df, 'home_club_id', 1005), filter_data(games_df, 'away_club_id', 1005)],
    'Wolfsburg': [filter_data(games_df, 'home_club_id', 82), filter_data(games_df, 'away_club_id', 82)],
    'Dynamo Kyiv': [filter_data(games_df, 'home_club_id', 338), filter_data(games_df, 'away_club_id', 338)],
    'Sevilla': [filter_data(games_df, 'home_club_id', 368), filter_data(games_df, 'away_club_id', 368)],
    'Shakhtar Donetsk': [filter_data(games_df, 'home_club_id', 660), filter_data(games_df, 'away_club_id', 660)],
    'Zenit': [filter_data(games_df, 'home_club_id', 964), filter_data(games_df, 'away_club_id', 964)],
    'Porto': [filter_data(games_df, 'home_club_id', 720), filter_data(games_df, 'away_club_id', 720)],
    'Milan': [filter_data(games_df, 'home_club_id', 5), filter_data(games_df, 'away_club_id', 5)],
    'Dortmund': [filter_data(games_df, 'home_club_id', 16), filter_data(games_df, 'away_club_id', 16)],
    'Young Boys': [filter_data(games_df, 'home_club_id', 1006), filter_data(games_df, 'away_club_id', 1006)],
    'Malmo': [filter_data(games_df, 'home_club_id', 1007), filter_data(games_df, 'away_club_id', 1007)],
    'RB Leipzig': [filter_data(games_df, 'home_club_id', 23826), filter_data(games_df, 'away_club_id', 23826)],
    'Besiktas': [filter_data(games_df, 'home_club_id', 114), filter_data(games_df, 'away_club_id', 114)],
    'Atalanta': [filter_data(games_df, 'home_club_id', 800), filter_data(games_df, 'away_club_id', 800)],
}

for i in games_by_clubs.keys():
    for j in range(0,2):
        games_by_clubs[i][j] = games_by_clubs[i][j].merge(game_events_df, on='game_id').merge(players_df, on='player_id')

st.dataframe(games_by_clubs['Chelsea'][0])