import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações do pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.display.float_format = '{:.2f}'.format

# Carregar os DataFrames
df_gols = pd.read_parquet(r"pullebyte-analises/DataSet Project/football-transfermarkt-dataset-01/parquet/appearances.parquet")
df_vitorias = pd.read_parquet(r"pullebyte-analises/DataSet Project/football-transfermarkt-dataset-01/parquet/club_games.parquet")

# Filtrar os dados
df_filtrado = df_gols[(df_gols['player_club_id'] == 418) & (df_gols['competition_id'] == 'CL')]
df_balanceado = df_filtrado[df_filtrado['goals'] != 0]

# Exibir o DataFrame filtrado no Streamlit
st.write("DataFrame Filtrado (real_madrid):")
st.dataframe(df_balanceado)

# Fazer o merge dos DataFrames com base na coluna 'game_id'
df_merged = pd.merge(df_balanceado, df_vitorias, on='game_id', how='inner')
df_vitorias_com_gols = df_merged[df_merged['is_win'] == 1]
total_partidas = df_merged['game_id'].nunique()
partidas_ganhas_com_gols = df_vitorias_com_gols['game_id'].nunique()
percentual_ganhas_com_gols = (partidas_ganhas_com_gols / total_partidas) * 100


# Exibir o DataFrame resultante do merge no Streamlit
st.write("DataFrame Resultante do Merge:")
st.dataframe(df_merged)

coluna = 'goals' 

plt.figure(figsize=(10, 6))
sns.violinplot(data=df_balanceado, x=coluna)
plt.title(f'Violinplot da Coluna {coluna}')
plt.xlabel(coluna)

st.pyplot(plt)


pivot_table = pd.DataFrame({
    'Total de Partidas': [total_partidas],
    'Partidas Ganhas com Gols': [partidas_ganhas_com_gols],
    'Percentual de Partidas Ganhas com Gols': [percentual_ganhas_com_gols]
})

# Exibir a pivot_table no Streamlit
st.write("Pivot Table com a Porcentagem de Partidas Ganhas com Gols dos Jogadores do Real Madrid:")
st.dataframe(pivot_table)
# Calcular a mediana da coluna
def mostrar_Mediana(df_balanceado, coluna):
    mediana = df_balanceado[coluna].median()
    st.write(f"A mediana da coluna {coluna} é: {mediana}")
    return mediana

# Mostrar a mediana
mostrar_Mediana(df_balanceado, coluna)
