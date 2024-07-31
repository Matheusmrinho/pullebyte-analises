from Home import clubs_valuation, get_squad_stats , creating_domestic_dataset, competitions
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import plotly.express as px

club_values = st.selectbox('Select a country', [x for x in competitions.country_name.unique()])
club_values_ES = clubs_valuation(club_values, verbose = True)
club_values_ES['points'] = 2 * club_values_ES.win + club_values_ES.draw
club_values_ES['points_percent'] = club_values_ES.points / (2 * club_values_ES.games)
pivot_table = pd.pivot_table(data=club_values_ES, index='club_name', columns='season', values='points_percent')
norm_values = pivot_table.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)), axis=1).fillna(0)
st.markdown('### Performance dos clubes por temporada')
fig = px.imshow(norm_values, 
                labels=dict(x="Season", y="Club Name", color="Points Percent"),
                x=pivot_table.columns,
                y=pivot_table.index,
                color_continuous_scale='Blues')

fig.update_layout(
    title="Performance por temporada",
    xaxis_title="Temporada",
    yaxis_title="Nome do Clubes",
    coloraxis_colorbar=dict(title="Pontos Percentuais"),
)    
st.plotly_chart(fig)
# Calcular a diferença de valor
# Calcular a diferença de valor
club_values_ES['value_diff'] = club_values_ES.pre_market_value - club_values_ES.post_market_value

# Lista de todos os clubes únicos da liga selecionada
club_list_ES = club_values_ES['club_name'].unique().tolist()
st.markdown('### Valorização dos clubes por temporada')
# Widget para selecionar os clubes a serem comparados
selected_clubs = st.multiselect('Selecione os clubes para comparar', club_list_ES, default=club_list_ES[:3])

# Criar a tabela dinâmica
values_ES = pd.pivot_table(data=club_values_ES, index='club_name', columns='season', values=['points_percent', 'value_diff']).T

# Filtrar os dados para os clubes selecionados
value_diff_data = values_ES[selected_clubs].loc['value_diff'].reset_index()

# Plotar a diferença de valor usando Plotly
fig1 = px.line(value_diff_data, x='season', y=selected_clubs, markers=True, labels={'value': 'Diferença de Valores'}, title='Diferença de valor dos clubes por temporada')

# Exibir o gráfico
st.plotly_chart(fig1)