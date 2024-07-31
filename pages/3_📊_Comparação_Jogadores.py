import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go

def load_data(file_path):
    return pd.read_parquet(file_path)

def filter_data(time_completo_df, club_id):
    return time_completo_df[time_completo_df['club_id'] == club_id]

def get_player_data(df, player_name):
    return df[df['player_name'] == player_name]

def calculate_attributes(df):
    df['min_per_goal'] = df.apply(
        lambda row: row['minutes_played'] / row['goals_goalkepping'] if row['goals_goalkepping'] > 0 else np.nan,
        axis=1
    )
    return df

def convert_minutes_to_hours(df, attribute):
    df[attribute] = df[attribute] / 60
    return df

def plot_player_comparison(player1, player2, attributes, player1_name, player2_name, attribute_labels):
    valid_attributes = [attr for attr in attributes if not pd.isna(player1[attr]) and not pd.isna(player2[attr])]
    labels = [attribute_labels[attr] for attr in valid_attributes]
    values1 = [player1[attr] for attr in valid_attributes]
    values2 = [player2[attr] for attr in valid_attributes]

    if not labels: 
        st.write("Não há atributos válidos para comparação.")
        return

    # Dividir minutos jogados por 60 para converter em horas jogadas
    if 'minutes_played' in valid_attributes:
        index = valid_attributes.index('minutes_played')
        values1[index] /= 60
        values2[index] /= 60
        labels[index] = 'Horas jogadas'

    fig = go.Figure(data=[
        go.Bar(name=player1_name, x=labels, y=values1),
        go.Bar(name=player2_name, x=labels, y=values2)
    ])

    fig.update_layout(
        title='Comparação de Atributos entre Jogadores',
        xaxis_title='Atributos',
        yaxis_title='Valores',
        barmode='group'
    )

    st.plotly_chart(fig)

attribute_labels = {
    'match_played_keyStats': 'Partidas jogadas',
    'goals_goalkepping': 'Quantidade de goals',
    'assists_keyStats': 'Assistências',
    'min_per_goal': 'Goals por minuto',
    'minutes_played': 'Minutos jogados',
    'saved': 'Defesas',
    'conceded': 'Gols sofridos'
}

time_completo_df = load_data('DataSet Project/merge-data-by-clubs/merge-time-completo.parquet')

time_completo_df = calculate_attributes(time_completo_df)

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

st.title('Comparação de Jogadores')

club1 = st.selectbox('Selecione o primeiro time', list(club_data.keys()), index=0)
club2 = st.selectbox('Selecione o segundo time', list(club_data.keys()), index=1)

position_filter = st.selectbox('Selecione a posição dos jogadores', ['Todos', 'Forward', 'Midfielder', 'Defender', 'Goalkeeper'])

def filter_players_by_position(df, position):
    if position == 'Todos':
        return df['player_name'].tolist()
    else:
        return df[df['position'] == position]['player_name'].tolist()

players_club1 = filter_players_by_position(club_data[club1], position_filter)
players_club2 = filter_players_by_position(club_data[club2], position_filter)

player1_name = st.selectbox('Selecione o jogador do primeiro time', players_club1, index=0 if players_club1 else None)
player2_name = st.selectbox('Selecione o jogador do segundo time', players_club2, index=0 if players_club2 else None)

player1_data = get_player_data(club_data[club1], player1_name) if player1_name else pd.DataFrame()
player2_data = get_player_data(club_data[club2], player2_name) if player2_name else pd.DataFrame()

if not player1_data.empty and not player2_data.empty:
    player1 = player1_data.iloc[0]
    player2 = player2_data.iloc[0]
    
    position = player1['position']
    if position in ['Forward', 'Midfielder', 'Defender']:
        attributes = ['match_played_keyStats', 'goals_goalkepping', 'assists_keyStats', 'min_per_goal', 'minutes_played']
    elif position == 'Goalkeeper':
        attributes = ['minutes_played', 'saved', 'conceded', 'match_played_keyStats']
    
    plot_player_comparison(player1, player2, attributes, player1_name, player2_name, attribute_labels)
else:
    st.write("Não foi possível encontrar os jogadores selecionados.")
