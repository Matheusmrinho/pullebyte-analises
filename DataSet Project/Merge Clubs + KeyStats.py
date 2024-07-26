import pandas as pd
import unidecode
from fuzzywuzzy import process, fuzz
import time

start_time = time.time()
df_players = pd.read_parquet(r'DataSet Project/football-transfermarkt-dataset-01/parquet/clubs.parquet')
df_keystats = pd.read_parquet(r'DataSet Project/ucl-matches-dataset-02/parquet/key_stats.parquet')
print(f"Tempo de carregamento dos dados: {time.time() - start_time:.2f} segundos")

df_players['name'] = df_players['name'].str.lower().str.strip().apply(unidecode.unidecode)
if 'club' in df_keystats.columns:
    df_keystats['club'] = df_keystats['club'].str.lower().str.strip().apply(unidecode.unidecode)
    merge_key = 'club'
else:
    raise KeyError("Coluna 'club' não encontrada em df_keystats")

min_similarity = 75

def fuzzy_match(name, choices):
    match = process.extractOne(name, choices, scorer=fuzz.token_set_ratio)
    return match[0] if match and match[1] >= min_similarity else None

df_players['matched_name'] = df_players['name'].apply(lambda x: fuzzy_match(x, df_keystats[merge_key]))
df_players.dropna(subset=['matched_name'], inplace=True)

df_combined = pd.merge(df_keystats, df_players, left_on=merge_key, right_on='matched_name', how='left').drop_duplicates(subset=['player_name'])

output_path = r'DataSet Project/merge-data-by-clubs/merge-data-by-clubs.parquet'
df_combined.to_parquet(output_path, index=False)
