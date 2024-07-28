import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch

# Função para carregar dados
def load_data(file_path):
    return pd.read_parquet(file_path)

# Função para filtrar dados por clube
def filter_data(time_completo_df, club_id):
    return time_completo_df[time_completo_df['club_id'] == club_id]

# Função para plotar o campo de futebol com dados de chutes
def plot_shots(chutes_penalty_area, chutes_penalty_box, chutes_pitch_box):
    # Configurações do campo com estilo específico
    fig, ax = plt.subplots(figsize=(13, 9))
    fig.set_facecolor('#0F1821')
    ax.patch.set_facecolor('#0F1821')

    # Criando o campo
    pitch = Pitch(pitch_type='statsbomb', half=True, 
                  pitch_color='#0F1821', line_color='#c7d5cc')
    pitch.draw(ax=ax)

    # Dimensões e posicionamento das áreas
    penalty_box = plt.Rectangle((102, 18), 18, 44, color='blue', alpha=0.3)
    pitch_box = plt.Rectangle((60, 0), 60, 80, color='green', alpha=0.1)
    penalty_area = plt.Rectangle((102, 30), 6, 20, color='red', alpha=0.5)

    # Adicionando as áreas ao campo
    ax.add_patch(penalty_box)
    ax.add_patch(pitch_box)
    ax.add_patch(penalty_area)

    # Adicionando labels para cada área
    ax.text(114, 40, int(chutes_penalty_box), color='white', fontsize=15, ha='center')
    ax.text(90, 40, int(chutes_pitch_box), color='white', fontsize=15, ha='center')
    ax.text(105, 40, int(chutes_penalty_area), color='white', fontsize=15, ha='center')

    # Ajustes finais
    plt.gca().invert_yaxis()
    return fig

# Carregar os dados
time_completo_df = load_data(r'DataSet Project/merge-data-by-clubs/merge-time-completo.parquet')

# Dicionário de clubes
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

# Título e descrição
st.title("Chutes a Gol por Clube")
st.markdown("Selecione um clube para visualizar a distribuição de chutes nas diferentes áreas do campo.")

# Seleção do clube
selected_club = st.selectbox("Escolha um clube:", list(club_data.keys()))

# Dados do clube selecionado
selected_data = club_data[selected_club]
chutes_penalty_area = selected_data['penalties'].sum()
chutes_penalty_box  = selected_data['inside_area'].sum()
chutes_pitch_box    = selected_data['outside_areas'].sum()

# Exibir estatísticas em uma tabela
st.markdown(f"> #### Estatísticas de chutes a gol do **{selected_club}**:")

stats_data = {
    "Área": ["Fora da Grande Área", "Dentro da Grande Área", "Cobranças de Pênalti"],
    "Gols": [int(chutes_pitch_box), int(chutes_penalty_box), int(chutes_penalty_area)]
}
stats_df = pd.DataFrame(stats_data)
st.table(stats_df)

# Exibir gráfico
fig = plot_shots(chutes_penalty_area, chutes_penalty_box, chutes_pitch_box)
st.pyplot(fig)
