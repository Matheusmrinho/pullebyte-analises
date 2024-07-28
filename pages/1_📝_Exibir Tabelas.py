import streamlit as st
import pandas as pd

@st.cache_data
def load_data(file_path):
    return pd.read_parquet(file_path)

@st.cache_data
def merge_data(keyStats_df, attacking_df, defending_df, attempts_df, goalkepping_df, goals_df, distribution_df):
    keyStats_df['club'] = keyStats_df['club'].str.lower()
    attacking_df['club'] = attacking_df['club'].str.lower()
    defending_df['club'] = defending_df['club'].str.lower()
    attempts_df['club'] = attempts_df['club'].str.lower()
    goalkepping_df['club'] = goalkepping_df['club'].str.lower()
    goals_df['club'] = goals_df['club'].str.lower()
    distribution_df['club'] = distribution_df['club'].str.lower()

    jogadores_ataque_df = pd.merge(keyStats_df, attacking_df, on=['player_name', 'club'], how='left', suffixes=('_keyStats', '_attacking'))
    jogadores_defesa_df = pd.merge(jogadores_ataque_df, defending_df, on=['player_name', 'club'], how='left', suffixes=('_ataque', '_defesa'))
    jogadores_attempts_df = pd.merge(jogadores_defesa_df, attempts_df, on=['player_name', 'club'], how='left', suffixes=('_defesa', '_tentativas'))
    jogadores_goalkepping_df = pd.merge(jogadores_attempts_df, goalkepping_df, on=['player_name', 'club'], how='left', suffixes=('_tentativas', '_goalkepping'))
    jogadores_goals_df = pd.merge(jogadores_goalkepping_df, goals_df, on=['player_name', 'club'], how='left', suffixes=('_goalkepping', '_gols'))
    time_completo_df = pd.merge(jogadores_goals_df, distribution_df, on=['player_name', 'club'], how='left', suffixes=('_gols', '_distribuicao'))

    return time_completo_df

@st.cache_data
def filter_data(time_completo_df, club_id):
    return time_completo_df[time_completo_df['club_id'] == club_id]

keyStats_df = load_data(r"DataSet Project\merge-data-by-clubs\merge-data-by-clubs.parquet")
attacking_df = load_data(r"DataSet Project\ucl-matches-dataset-02\parquet\attacking.parquet")
defending_df = load_data(r"DataSet Project\ucl-matches-dataset-02\parquet\defending.parquet")
attempts_df = load_data(r"DataSet Project\ucl-matches-dataset-02\parquet\attempts.parquet")
goalkepping_df = load_data(r"DataSet Project\ucl-matches-dataset-02\parquet\goalkeeping.parquet")
goals_df = load_data(r"DataSet Project\ucl-matches-dataset-02\parquet\goals.parquet")
distribution_df = load_data(r"DataSet Project\ucl-matches-dataset-02\parquet\distributon.parquet")

time_completo_df = merge_data(keyStats_df, attacking_df, defending_df, attempts_df, goalkepping_df, goals_df, distribution_df)

club_id_map = {
    'man. city': 281,
    'losc': 1082,
    'inter': 46,
    'salzburg': 1004, # Não tem
    'sheriff': 1005, # Não tem
    'young boys': 1006, # Não tem
    'malmo': 1007 # Não tem
}

time_completo_df['club_id'] = time_completo_df.apply(
    lambda row: club_id_map.get(row['club'], row['club_id']), axis=1
)


club_data = {
    'Real Madrid': filter_data(time_completo_df, 418),
    'Liverpool': filter_data(time_completo_df, 31),
    'Villarreal': filter_data(time_completo_df, 1050),
    'Man City': filter_data(time_completo_df, 281),
    'Benfica': filter_data(time_completo_df, 294),
    'Atlético Madrid': filter_data(time_completo_df, 13),
    'Bayern Munich': filter_data(time_completo_df, 27),
    'Chelsea': filter_data(time_completo_df, 631),
    'LOSC': filter_data(time_completo_df, 1082),
    'Inter': filter_data(time_completo_df, 46),
    'Salzburg': filter_data(time_completo_df, 1004),
    'Ajax': filter_data(time_completo_df, 610),
    'Paris Saint-Germain': filter_data(time_completo_df, 583),
    'Sporting CP': filter_data(time_completo_df, 1062),
    'Juventus': filter_data(time_completo_df, 506),
    'Manchester United': filter_data(time_completo_df, 1519),
    'Barcelona': filter_data(time_completo_df, 131),
    'Club Brugge': filter_data(time_completo_df, 2282),
    'Sheriff': filter_data(time_completo_df, 1005),
    'Wolfsburg': filter_data(time_completo_df, 82),
    'Dynamo Kyiv': filter_data(time_completo_df, 338),
    'Sevilla': filter_data(time_completo_df, 368),
    'Shakhtar Donetsk': filter_data(time_completo_df, 660),
    'Zenit': filter_data(time_completo_df, 964),
    'Porto': filter_data(time_completo_df, 720),
    'Milan': filter_data(time_completo_df, 5),
    'Dortmund': filter_data(time_completo_df, 16),
    'Young Boys': filter_data(time_completo_df, 1006),
    'Malmo': filter_data(time_completo_df, 1007),
    'RB Leipzig': filter_data(time_completo_df, 23826),
    'Besiktas': filter_data(time_completo_df, 114),
    'Atalanta': filter_data(time_completo_df, 800)
}

for name, df in club_data.items():
    club_data[name] = df.drop_duplicates(subset=['player_name'])

st.write('## Visualização dos dataframes de clubes')
st.write('Dados da UCL completos')
st.dataframe(time_completo_df)
st.write('Dados do Inter de Milão')
st.dataframe(club_data['Inter'])
