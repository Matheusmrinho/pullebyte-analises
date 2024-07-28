import pandas as pd
import unidecode
from fuzzywuzzy import process, fuzz

clubs_data = pd.read_parquet(r'DataSet Project/football-transfermarkt-dataset-01/parquet/clubs.parquet')
keystats_data = pd.read_parquet(r'DataSet Project/ucl-matches-dataset-02/parquet/key_stats.parquet')

clubs_data['name'] = clubs_data['name'].str.lower().apply(unidecode.unidecode)
keystats_data['club'] = keystats_data['club'].str.lower().apply(unidecode.unidecode)

min_similarity = 65

def fuzzy_match(name, choices):
    # match = process.extractOne(name, choices, scorer=fuzz.token_set_ratio)
    match = process.extractOne(name, choices, scorer=fuzz.token_set_ratio)
    print(name, "->",match[0], match[1], choices[match[2]]) # match[2] is the index of the matched string in the choices list match[0] is the matched string match[1] is the similarity score
    print('---')
    return match[0] if match[1] >= min_similarity else None

clubs_data['matched_name'] = clubs_data['name'].apply(lambda x: fuzzy_match(x, keystats_data['club']))
clubs_data.dropna(subset=['matched_name'], inplace=True)

merged_data = pd.merge(keystats_data, clubs_data, left_on='club', right_on='matched_name', how='left').drop_duplicates(subset=['player_name', 'club'])

output_path = r'DataSet Project/merge-data-by-clubs/merge-data-by-clubs.parquet'
merged_data.to_parquet(output_path, index=False)
