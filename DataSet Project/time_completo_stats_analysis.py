import pandas as pd

keyStats_df = pd.read_parquet(r"Caminho para o arquivo keystats + clubs.parquet")
attacking_df = pd.read_parquet(r"Caminho para o arquivo attacking.parquet")
defending_df = pd.read_parquet(r"Caminho para o arquivo defending.parquet")
attempts_df = pd.read_parquet(r"Caminho para o arquivo attempts.parquet")
goalkepping_df = pd.read_parquet(r"Caminho para o arquivo goalkepping.parquet")
goals_df = pd.read_parquet(r"Caminho para o arquivo goals.parquet")
distribution_df = pd.read_parquet(r"Caminho para o arquivo distribution.parquet")


jogadores_ataque_df = pd.merge(keyStats_df, attacking_df, on='player_name', how='left', suffixes=('_keyStats', '_attacking'))
jogadores_defesa_df = pd.merge(jogadores_ataque_df, defending_df, on='player_name', how='left', suffixes=('_ataque', '_defesa'))
jogadores_attempts_df = pd.merge(jogadores_defesa_df, attempts_df, on='player_name', how='left', suffixes=('_defesa', '_tentativas'))
jogadores_goalkepping_df = pd.merge(jogadores_attempts_df, goalkepping_df, on='player_name', how='left', suffixes=('_tentativas', '_goalkepping'))
jogadores_goals_df = pd.merge(jogadores_goalkepping_df, goals_df, on='player_name', how='left', suffixes=('_goalkepping', '_gols'))
time_completo_df = pd.merge(jogadores_goals_df, distribution_df, on='player_name', how='left', suffixes=('_gols', '_distribuicao'))


real_madrid_df = time_completo_df[time_completo_df['club_id'] == 418]
liverpool_df = time_completo_df[time_completo_df['club_id'] == 31]
villarreal_df = time_completo_df[time_completo_df['club_id'] == 1050]
man_city_df = time_completo_df[time_completo_df['club_keyStats'] == 'man. city']
benfica_df = time_completo_df[time_completo_df['club_id'] == 294]
atletico_df = time_completo_df[time_completo_df['club_id'] == 13]
bayern_df = time_completo_df[time_completo_df['club_id'] == 27]
chelsea_df = time_completo_df[time_completo_df['club_id'] == 631]
losc_df = time_completo_df[time_completo_df['club_keyStats'] == 'losc']
inter_df = time_completo_df[time_completo_df['club_keyStats'] == 'inter']
salzburg_df = time_completo_df[time_completo_df['club_keyStats'] == 'salzburg']
ajax_df = time_completo_df[time_completo_df['club_id'] == 610]
paris_df = time_completo_df[time_completo_df['club_id'] == 583]
sporting_cp_df = time_completo_df[time_completo_df['club_id'] == 1062]
juvents_df = time_completo_df[time_completo_df['club_id'] == 506]
man_united_df = time_completo_df[time_completo_df['club_id'] == 1519]
barcelona_df = time_completo_df[time_completo_df['club_id'] == 131]
club_brugge_df = time_completo_df[time_completo_df['club_id'] == 2282]
sheriff_df = time_completo_df[time_completo_df['club_keyStats'] == 'sheriff']
wolfsburg_df = time_completo_df[time_completo_df['club_id'] == 82]
dynamo_kyiv_df = time_completo_df[time_completo_df['club_id'] == 338]
sevilla_df = time_completo_df[time_completo_df['club_id'] == 368]
shakhtar_donetsk_df = time_completo_df[time_completo_df['club_id'] == 660]
zenit_df = time_completo_df[time_completo_df['club_id'] == 964]
porto_df = time_completo_df[time_completo_df['club_id'] == 720]
milan_df = time_completo_df[time_completo_df['club_id'] == 5]
dortmund_df = time_completo_df[time_completo_df['club_id'] == 16]
young_boys_df = time_completo_df[time_completo_df['club_keyStats'] == 'young boys']
malmo_df = time_completo_df[time_completo_df['club_keyStats'] == 'malmo']
leipzig = time_completo_df[time_completo_df['club_id'] == 23826]
besiktas_df = time_completo_df[time_completo_df['club_id'] == 114]
atlanta_df = time_completo_df[time_completo_df['club_id'] == 800]


time_completo_df = time_completo_df.drop_duplicates(subset=['player_name'])

man_city_df
