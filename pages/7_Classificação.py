import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample
import streamlit as st
import numpy as np

# Carregar os dados
players = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/dados_nomalizados/players_nor.parquet')
appearances = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/dados_nomalizados/apperances_nor.parquet')
clubs = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/dados_nomalizados/club_nor.parquet')
games = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/dados_nomalizados/games.parquet_nor.parquet')
def rename_column(df, old_name, new_name):
    """
    Renomeia uma coluna em um DataFrame do Pandas.

    Parâmetros:
    df (pd.DataFrame): O DataFrame a ser modificado.
    old_name (str): O nome atual da coluna.
    new_name (str): O novo nome da coluna.

    Retorna:
    pd.DataFrame: O DataFrame com a coluna renomeada.
    """
    df = df.rename(columns={old_name: new_name})
    return df
players2 = rename_column(players, 'name', 'player_name')
def player_stats(player_name, season):
    
    df = appearances.merge(games, on=['game_id'], how='left')
    df = df[df['player_name'] == player_name]
    df = df[df['season'] == season]
    
    if (df.shape[0] == 0):
        Out = [(np.nan, player_name, season, 0, 0, 0, 0, 0, 0, 0, 0)]
        out_df = pd.DataFrame(data=Out, columns=['player_id', 'player_name', 'season', 'goals', 'games',
                                                 'assists', 'minutes_played', 'goals_for', 'goals_against', 'clean_sheet', 'goals_per_minute'])
        return out_df
    
    else:
        
        df["goals_for"] = df.apply(lambda row: row['home_club_goals'] if row['home_club_id'] == row['player_club_id'] 
                      else row['away_club_goals'] if row['away_club_id'] == row['player_club_id'] 
                      else np.nan, axis=1)
        df["goals_against"] = df.apply(lambda row: row['away_club_goals'] if row['home_club_id'] == row['player_club_id'] 
                      else row['home_club_goals'] if row['away_club_id'] == row['player_club_id'] 
                      else np.nan, axis=1)
        df['clean_sheet'] = df.apply(lambda row: 1 if row['goals_against'] == 0
                      else 0 if row['goals_against'] > 0
                      else np.nan, axis=1)
        
        df = df.groupby(['player_id', "player_name", "season"], as_index=False).agg({'goals': 'sum', 'game_id': 'nunique', 
                                                                      'assists': 'sum', 'minutes_played': 'sum', 'goals_for': 'sum',
                                                                      'goals_against': 'sum', 'clean_sheet': 'sum'})
        
        df['goals_per_minute'] = df['goals'] / df['minutes_played']
        out_df = df.rename(columns={'game_id': 'games'})
        
        return out_df

def club_stats(club_name, season):
    
    # Filtrar jogos onde o clube é o time da casa ou o visitante
    df = games[(games['home_club_name'] == club_name) | (games['away_club_name'] == club_name)]
    df = df[df['season'] == season]
    
    if df.shape[0] == 0:
        # Se não houver jogos, retornar zeros para os gols e partidas
        Out = [(club_name, season, 0, 0, 0)]
        out_df = pd.DataFrame(data=Out, columns=['club_name', 'season', 'goals_for', 'goals_against', 'matches'])
        return out_df
    
    else:
        # Calcular gols feitos
        df['goals_for'] = df.apply(lambda row: row['home_club_goals'] if row['home_club_name'] == club_name 
                                   else row['away_club_goals'], axis=1)
        
        # Calcular gols sofridos
        df['goals_against'] = df.apply(lambda row: row['away_club_goals'] if row['home_club_name'] == club_name 
                                       else row['home_club_goals'], axis=1)
        
        # Somar os gols feitos e sofridos
        total_goals_for = df['goals_for'].sum()
        total_goals_against = df['goals_against'].sum()
        
        # Contar o número de partidas
        total_matches = df.shape[0]
        
        # Criar o DataFrame de saída com os resultados agregados
        out_df = pd.DataFrame({
            'club_name': [club_name],
            'season': [season],
            'goals_for': [total_goals_for],
            'goals_against': [total_goals_against],
            'matches': [total_matches]
        })
        
        return out_df
def determine_result(row):
    if row['home_club_goals'] > row['away_club_goals']:
        return 'win'
    elif row['home_club_goals'] < row['away_club_goals']:
        return 'lose'
    else:
        return 'draw'

# Criar a coluna 'result' no DataFrame 'games'
games['result'] = games.apply(determine_result, axis=1)

# Merge dos DataFrames appearances e games
combined_df = pd.merge(appearances, games, on='game_id')

# Pré-processamento dos dados
# Remover colunas que possam estar vazando informações sobre a variável alvo
features = ['yellow_cards', 'red_cards', 'goals', 'assists', 'minutes_played']
X = combined_df[features]
y = combined_df['result']  # Variável alvo

# Balanceamento das classes
df = pd.concat([X, y], axis=1)
draw = df[df.result == 'draw']
lose = df[df.result == 'lose']
win = df[df.result == 'win']

# Upsample minority classes
draw_upsampled = resample(draw, replace=True, n_samples=len(win), random_state=42)
lose_upsampled = resample(lose, replace=True, n_samples=len(win), random_state=42)

# Combine majority class with upsampled minority classes
df_upsampled = pd.concat([win, draw_upsampled, lose_upsampled])

X = df_upsampled[features]
y = df_upsampled['result']

# Normalização dos dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Divisão dos dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Treinamento do modelo de regressão logística multinomial
model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
model.fit(X_train, y_train)

# Validação cruzada
cv_scores = cross_val_score(model, X_scaled, y, cv=5)
print("Validação Cruzada - Acurácia Média:", cv_scores.mean())

y_pred = model.predict(X_test)
print("Acurácia:", accuracy_score(y_test, y_pred))
print("Relatório de Classificação:\n", classification_report(y_test, y_pred))


y_prob = model.predict_proba(X_test)
print("Probabilidades de cada classe:\n", y_prob)