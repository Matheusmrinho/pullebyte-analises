
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import plotly.express as px
competitions = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/parquet/competitions.parquet')
clubs = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/parquet/clubs.parquet')
games = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/parquet/games.parquet')
games['date'] = pd.to_datetime(games['date'])
players = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/parquet/players.parquet')
appearances = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/parquet/appearances.parquet')
appearances['date'] = pd.to_datetime(appearances['date'])
player_valuations = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/parquet/player_valuations.parquet')
player_valuations['date'] = pd.to_datetime(player_valuations['date'])
st.set_page_config(
    page_title = "Pullebyte - Análises",
    layout = "wide",
    menu_items = {
        'About': "Analise realizada da champions league com base nos datasets disponiveis no kaggle referente as temporadas <= 2022"
    }
)
def player_market_value_plot(player_name):
    pid = players[players.name == player_name].player_id.values[0]
    ax = player_valuations[player_valuations.player_id == pid].plot.line( x = 'date', y = 'market_value_in_eur', figsize = (10,4), title = player_name);


    club_ids = appearances[appearances.player_id == pid].player_club_id.value_counts().index.to_list()
    
    for cid, c in zip(club_ids, ['b','r','c','m','g','y']):
        date_min = appearances[(appearances.player_id == pid) & (appearances.player_club_id == cid)].date.min()
        date_max = appearances[(appearances.player_id == pid) & (appearances.player_club_id == cid)].date.max()
        if clubs[clubs.club_id == cid].shape[0] == 0:
            cname = 'unknown'
        else:
            cname = clubs[clubs.club_id == cid].name.values[0]
        player_valuations[(player_valuations.player_id == pid) & (player_valuations.date >= date_min) & (player_valuations.date <= date_max) ].plot.scatter( x = 'date', y = 'market_value_in_eur',  label = cname,  color = c, ax = ax);
        print(cname, ': from', date_min, ' to ', date_max)

    ax.set_xlabel(''); ax.set_ylabel('')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))

def list_of_club_names(local_games):
    club_names = set()
    for idx, row in local_games.iterrows():
        club_names.add(row['home_club_name'])
        club_names.add(row['away_club_name'])
    club_names.discard(np.nan)
    return list(club_names)
def list_of_club_ids(local_games):
    club_names = set()
    for idx, row in local_games.iterrows():
        club_names.add(row['home_club_id'])
        club_names.add(row['away_club_id'])
    club_names.discard(np.nan)
    return list(club_names)

    
def creating_domestic_dataset(country_name, verbose = False):
    '''
    return dataset contatining all games in all competitions for specific country
    '''
    c_ = competitions[competitions.country_name == country_name].competition_id.values
    g_ = games[games.competition_id.isin(c_)].dropna(subset = ['home_club_name', 'away_club_name'])  # dropping games with nonane clubs
 
    if verbose:
        s_ = pd.pivot_table(data = g_, values = 'game_id', index = 'season', columns = 'competition_id', aggfunc = 'count', margins = True)
        print('Matches by seasons:')
        print(s_)
        
    return g_
competitions[competitions.country_id != -1].groupby(by = 'country_name').name.count()
@st.cache_data
def clubs_valuation(country_name, verbose=False):
        cid_, cname_, s_, t_, prev_, postv_, g_, w_, d_, l_ = [],[],[],[],[],[],[],[],[],[]
        local_games = creating_domestic_dataset(country_name, verbose=verbose)

        # Verificar se as colunas necessárias estão presentes
        required_columns = ['home_club_id', 'away_club_id', 'season', 'home_club_goals', 'away_club_goals', 'game_id']
        for col in required_columns:
            if col not in local_games.columns:
                raise KeyError(f"A coluna '{col}' está ausente no DataFrame 'local_games'")

        club_idx = list_of_club_ids(local_games)
        seasons = sorted(local_games.season.value_counts().index.to_list())

        for season in seasons:
            if verbose:
                print(season)
            for club_id in club_idx:
                cid_.append(club_id)
                cname_.append(clubs[clubs.club_id == club_id].name.values[0])
                if verbose:
                    print(cname_[-1], end='; ')
                s_.append(season)
                gidx = local_games[((local_games.home_club_id == club_id) | (local_games.away_club_id == club_id)) & (local_games.season == season)].game_id.values
                g_.append(len(gidx))
                w_.append(local_games[(local_games.season == season) & 
                        ((local_games.home_club_id == club_id) & (local_games.home_club_goals > local_games.away_club_goals) | 
                        ((local_games.away_club_id == club_id) & (local_games.home_club_goals < local_games.away_club_goals)))].game_id.count())
                d_.append(local_games[(local_games.season == season) & 
                        ((local_games.home_club_id == club_id) & (local_games.home_club_goals == local_games.away_club_goals) | 
                        ((local_games.away_club_id == club_id) & (local_games.home_club_goals == local_games.away_club_goals)))].game_id.count())
                l_.append(local_games[(local_games.season == season) & 
                        ((local_games.home_club_id == club_id) & (local_games.home_club_goals < local_games.away_club_goals) | 
                        ((local_games.away_club_id == club_id) & (local_games.home_club_goals > local_games.away_club_goals)))].game_id.count())
                if appearances[(appearances.game_id.isin(gidx)) & (appearances.player_club_id == club_id)].shape[0] > 0:
                    squad_stats = get_squad_stats(local_games, club_id, season)
                    t_.append(squad_stats['post_market_value'].count())
                    prev_.append(squad_stats['pre_market_value'].sum())
                    postv_.append(squad_stats['post_market_value'].sum())
                else:
                    t_.append(np.nan)
                    prev_.append(np.nan)
                    postv_.append(np.nan)
            if verbose:
                print()
        print('Values calculation is finished')
        return pd.DataFrame({'club_id': cid_, 'club_name': cname_, 'season': s_, 'no_of_players': t_, 'games': g_, 'win': w_, 'draw': d_, 'loss': l_, 'pre_market_value': prev_, 'post_market_value': postv_})
@st.cache_data
def get_squad_stats(local_games, club_id, season):
        player_stat_cols = ['yellow_cards', 'red_cards', 'goals', 'assists', 'minutes_played']
        season_start_date  = min(local_games[(local_games.away_club_id == club_id) & (local_games.season == season)].date.min(), local_games[(local_games.home_club_id == club_id) & (local_games.season == season)].date.min())
        season_finish_date = max(local_games[(local_games.home_club_id == club_id) & (local_games.season == season)].date.max(), local_games[(local_games.away_club_id == club_id) & (local_games.season == season)].date.max())
        
        club_games_ = np.concatenate((local_games[(local_games.home_club_id == club_id) & (local_games.season == season)].game_id.values, local_games[(local_games.away_club_id == club_id) & (local_games.season == season)].game_id.values))
        player_stats_ = pd.pivot_table(data = appearances[ (appearances.game_id.isin(club_games_)) & (appearances.player_club_id == club_id)], values = player_stat_cols, index = ['player_id','player_name'], columns = 'game_id', aggfunc = 'sum', margins = True).loc[:,pd.IndexSlice[:, ['All'] ]].droplevel(1, axis = 1)[:-1]
        
        player_stats_['season'] = season
        player_stats_['club_id'] = club_id
        player_stats_['club_name'] = clubs[clubs.club_id == club_id].name.values[0]
        player_stats_['season_start_date'] = season_start_date
        player_stats_['season_finish_date'] = season_finish_date
        player_stats_ = player_stats_.reset_index().set_index('player_id')
        player_stats_['games'] = pd.pivot_table(data = appearances[ (appearances.game_id.isin(club_games_)) & (appearances.player_club_id == club_id)], values = 'minutes_played', index = 'player_id', columns = 'game_id', aggfunc = 'count', margins = True)['All'][:-1]
        
        player_idx = player_stats_.index
        pre_value, post_value = [],[]
        for player_id in player_idx:
            if player_valuations[(player_valuations.player_id == player_id) & (player_valuations.date >= season_start_date)].shape[0] > 0:
                pre_value.append(player_valuations[(player_valuations.player_id == player_id) & (player_valuations.date >= season_start_date)].market_value_in_eur.values[0])
            else:
                pre_value.append(np.nan)
            if player_valuations[(player_valuations.player_id == player_id) & (player_valuations.date >= season_finish_date)].shape[0] > 0:
                post_value.append(player_valuations[(player_valuations.player_id == player_id) & (player_valuations.date >= season_finish_date)].market_value_in_eur.values[0])
            else:
                post_value.append(np.nan)
            
        col_order = ['club_id', 'club_name',  'season', 'season_start_date', 'season_finish_date', 'player_id', 'player_name', 'games', 'minutes_played', 'yellow_cards', 'red_cards', 'goals', 'assists', 'pre_market_value', 'post_market_value']
        return pd.concat([player_stats_, pd.DataFrame({'player_id' : player_idx, 'pre_market_value' : pre_value, 'post_market_value' : post_value}).set_index('player_id')], axis = 1).reset_index()[col_order]
club_values = st.selectbox('Select a country', [x for x in competitions.country_name.unique()])
club_values_ES = clubs_valuation(club_values, verbose=False)

# Verificar se a coluna 'club_id' está presente
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