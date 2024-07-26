import pandas as pd

keyStats_df = pd.read_parquet(r"DataSet Project\merge-data-by-clubs\merge-data-by-clubs.parquet")
attacking_df = pd.read_parquet(r"DataSet Project\ucl-matches-dataset-02\parquet\attacking.parquet")
defending_df = pd.read_parquet(r"DataSet Project\ucl-matches-dataset-02\parquet\defending.parquet")
attempts_df = pd.read_parquet(r"DataSet Project\ucl-matches-dataset-02\parquet\attempts.parquet")
goalkepping_df = pd.read_parquet(r"DataSet Project\ucl-matches-dataset-02\parquet\goalkeeping.parquet")
goals_df = pd.read_parquet(r"DataSet Project\ucl-matches-dataset-02\parquet\goals.parquet")
distribution_df = pd.read_parquet(r"DataSet Project\ucl-matches-dataset-02\parquet\distributon.parquet")

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

club_id_map = {
    'man. city': 281,
    'losc': 1082,
    'inter': 46,
    'salzburg': 1004,
    'sheriff': 1005,
    'young boys': 1006,
    'malmo': 1007
}

time_completo_df['club_id'] = time_completo_df.apply(
    lambda row: club_id_map.get(row['club'], row['club_id']), axis=1
)

real_madrid_df = time_completo_df[time_completo_df['club_id'] == 418]
liverpool_df = time_completo_df[time_completo_df['club_id'] == 31]
villarreal_df = time_completo_df[time_completo_df['club_id'] == 1050]
man_city_df = time_completo_df[time_completo_df['club_id'] == 281]
benfica_df = time_completo_df[time_completo_df['club_id'] == 294]
atletico_df = time_completo_df[time_completo_df['club_id'] == 13]
bayern_df = time_completo_df[time_completo_df['club_id'] == 27]
chelsea_df = time_completo_df[time_completo_df['club_id'] == 631]
losc_df = time_completo_df[time_completo_df['club_id'] == 1082]
inter_df = time_completo_df[time_completo_df['club_id'] == 46]
salzburg_df = time_completo_df[time_completo_df['club_id'] == 1004]
ajax_df = time_completo_df[time_completo_df['club_id'] == 610]
paris_df = time_completo_df[time_completo_df['club_id'] == 583]
sporting_cp_df = time_completo_df[time_completo_df['club_id'] == 1062]
juvents_df = time_completo_df[time_completo_df['club_id'] == 506]
man_united_df = time_completo_df[time_completo_df['club_id'] == 1519]
barcelona_df = time_completo_df[time_completo_df['club_id'] == 131]
club_brugge_df = time_completo_df[time_completo_df['club_id'] == 2282]
sheriff_df = time_completo_df[time_completo_df['club_id'] == 1005]
wolfsburg_df = time_completo_df[time_completo_df['club_id'] == 82]
dynamo_kyiv_df = time_completo_df[time_completo_df['club_id'] == 338]
sevilla_df = time_completo_df[time_completo_df['club_id'] == 368]
shakhtar_donetsk_df = time_completo_df[time_completo_df['club_id'] == 660]
zenit_df = time_completo_df[time_completo_df['club_id'] == 964]
porto_df = time_completo_df[time_completo_df['club_id'] == 720]
milan_df = time_completo_df[time_completo_df['club_id'] == 5]
dortmund_df = time_completo_df[time_completo_df['club_id'] == 16]
young_boys_df = time_completo_df[time_completo_df['club_id'] == 1006]
malmo_df = time_completo_df[time_completo_df['club_id'] == 1007]
leipzig = time_completo_df[time_completo_df['club_id'] == 23826]
besiktas_df = time_completo_df[time_completo_df['club_id'] == 114]
atlanta_df = time_completo_df[time_completo_df['club_id'] == 800]

club_data = {
    'Real Madrid': real_madrid_df,
    'Liverpool': liverpool_df,
    'Villarreal': villarreal_df,
    'Man City': man_city_df,
    'Benfica': benfica_df,
    'Atlético Madrid': atletico_df,
    'Bayern Munich': bayern_df,
    'Chelsea': chelsea_df,
    'LOSC': losc_df,
    'Inter': inter_df,
    'Salzburg': salzburg_df,
    'Ajax': ajax_df,
    'Paris Saint-Germain': paris_df,
    'Sporting CP': sporting_cp_df,
    'Juventus': juvents_df,
    'Manchester United': man_united_df,
    'Barcelona': barcelona_df,
    'Club Brugge': club_brugge_df,
    'Sheriff': sheriff_df,
    'Wolfsburg': wolfsburg_df,
    'Dynamo Kyiv': dynamo_kyiv_df,
    'Sevilla': sevilla_df,
    'Shakhtar Donetsk': shakhtar_donetsk_df,
    'Zenit': zenit_df,
    'Porto': porto_df,
    'Milan': milan_df,
    'Dortmund': dortmund_df,
    'Young Boys': young_boys_df,
    'Malmo': malmo_df,
    'RB Leipzig': leipzig,
    'Besiktas': besiktas_df,
    'Atalanta': atlanta_df
}

for name, df in club_data.items():
    club_data[name] = df.drop_duplicates(subset=['player_name'])

# df_exibir = club_data['Man City']
# df_exibir