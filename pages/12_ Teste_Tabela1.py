# import pandas as pd
# import unidecode
# from fuzzywuzzy import process, fuzz
# import time

# start_time = time.time()
# df_players = pd.read_parquet(r'DataSet Project/football-transfermarkt-dataset-01/parquet/clubs.parquet')
# df_keystats = pd.read_parquet(r'DataSet Project/ucl-matches-dataset-02/parquet/key_stats.parquet')
# print(f"Tempo de carregamento dos dados: {time.time() - start_time:.2f} segundos")

# df_players['name'] = df_players['name'].str.lower().str.strip().apply(unidecode.unidecode)
# if 'club' in df_keystats.columns:
#     df_keystats['club'] = df_keystats['club'].str.lower().str.strip().apply(unidecode.unidecode)
#     merge_key = 'club'
# else:
#     raise KeyError("Coluna 'club' não encontrada em df_keystats")

# min_similarity = 75

# def fuzzy_match(name, choices):
#     match = process.extractOne(name, choices, scorer=fuzz.token_set_ratio)
#     return match[0] if match and match[1] >= min_similarity else None

# df_players['matched_name'] = df_players['name'].apply(lambda x: fuzzy_match(x, df_keystats[merge_key]))
# df_players.dropna(subset=['matched_name'], inplace=True)

# # Realizar o merge
# df_combined = pd.merge(df_keystats, df_players, left_on=merge_key, right_on='matched_name', how='left')

# # Verificar as colunas disponíveis
# print(df_combined.columns)

# # Corrigir o nome da coluna, se necessário
# if 'win' not in df_combined.columns:
#     raise KeyError("Coluna 'win' não encontrada em df_combined")

# # Calcular pontos e porcentagem de pontos
# df_combined['points'] = 2 * df_combined['win'] + df_combined['draw']
# df_combined['points_percent'] = df_combined['points'] / (2 * df_combined['games'])

# # Criar tabela dinâmica para visualizar a porcentagem de pontos por clube e temporada
# pivot_table = pd.pivot_table(data=df_combined, index='club_name', columns='season', values='points_percent')
# styled_pivot_table = pivot_table.style.background_gradient().format("{:.2f}")

# # Exibir a tabela dinâmica
# print(styled_pivot_table)
# #data = {
#     'game_id': [2321044, 2486531, 2899571, 2482257, 2368445],
#     'is_win': [1, 1, 0, 0, 1]
# #}

import streamlit as st
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
import os

# Adicionar o caminho do diretório ao sys.path para importar os módulos
sys.path.append(os.path.join(os.getcwd(), 'DataSet Project'))

# Importar o dataframe do módulo time_completo_stats_analysis
from time_completo_stats_analysis import time_completo_df

# Carregar o arquivo club_games.parquet
club_games_df = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/club_games.parquet')

# Verificar as colunas dos dataframes
st.write("Colunas de time_completo_df:", time_completo_df.columns)
st.write("Colunas de club_games_df:", club_games_df.columns)

# Verificar se a coluna 'club_id' existe em ambos os dataframes
if 'club_id' not in time_completo_df.columns or 'club_id' not in club_games_df.columns:
    raise KeyError("A coluna 'club_id' não está presente em um dos dataframes.")

# Mesclar os dataframes com base na chave comum 'club_id'
merged_df = pd.merge(time_completo_df, club_games_df, on='club_id')

# Selecionar as variáveis de interesse
features = ['total_attempts', 'pass_completed', 'balls_recoverd', 'on_target', 'saved']
target = 'is_win'  

# Preparar os dados
X = merged_df[features]
y = merged_df[target]

# Lidar com valores NaN
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

# Dividir os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizar os dados
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Treinar o modelo de regressão logística
model = LogisticRegression()
model.fit(X_train, y_train)

# Fazer previsões
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)

# Avaliar o modelo
st.write("Classification Report:")
st.text(classification_report(y_test, y_pred))
st.write("Confusion Matrix:")
st.text(confusion_matrix(y_test, y_pred))

# Gerar o boxplot
proba_df = pd.DataFrame(y_pred_proba, columns=model.classes_)
proba_df['real'] = y_test.values
proba_df['pred'] = y_pred

plt.figure(figsize=(10, 6))
sns.boxplot(x='real', y=proba_df.columns[1], data=proba_df)
plt.title('Distribuição das Probabilidades Previstas por Resultado Real')
plt.xlabel('Resultado Real')
plt.ylabel('Probabilidade Prevista de Vitória')

# Exibir o boxplot no Streamlit
st.pyplot(plt)