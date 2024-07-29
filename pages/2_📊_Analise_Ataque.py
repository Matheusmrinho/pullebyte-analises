import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
import seaborn as sns

# Função para carregar dados
def load_data(file_path):
    return pd.read_parquet(file_path)

# Função para filtrar dados por clube
@st.cache_data
def filter_data(data_frame, filter_by, item_filtro):
    return data_frame[data_frame[filter_by] == item_filtro]

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
goals_df = load_data(r'DataSet Project/ucl-matches-dataset-02/parquet/goals.parquet')

# Dicionário de clubes
club_data_goals = {
    'Real Madrid': filter_data(goals_df, 'club', 'Real Madrid'),
    'Liverpool': filter_data(goals_df, 'club', 'Liverpool'),
    'Villarreal': filter_data(goals_df, 'club', 'Villarreal'),
    'Man. City': filter_data(goals_df, 'club', 'Man. City'),
    'Benfica': filter_data(goals_df, 'club','Benfica'),
    'Atlético Madrid': filter_data(goals_df, 'club', 'Atlético'),
    'Bayern Munich': filter_data(goals_df, 'club', 'Bayern'),
    'Chelsea': filter_data(goals_df, 'club', 'Chelsea'),
    'LOSC': filter_data(goals_df, 'club', 'LOSC'),
    'Inter': filter_data(goals_df, 'club', 'Inter'),
    'Salzburg': filter_data(goals_df, 'club', 'Salzburg'),
    'Ajax': filter_data(goals_df, 'club', 'Ajax'),
    'Paris Saint-Germain': filter_data(goals_df, 'club', 'Paris'),
    'Sporting CP': filter_data(goals_df, 'club', 'Sporting CP'),
    'Juventus': filter_data(goals_df, 'club', 'Juventus'),
    'Manchester United': filter_data(goals_df, 'club', 'Man. United'),
    'Barcelona': filter_data(goals_df, 'club', 'Barcelona'),
    'Club Brugge': filter_data(goals_df, 'club', 'Club Brugge'),
    'Sheriff': filter_data(goals_df, 'club', 'Sheriff'),
    'Wolfsburg': filter_data(goals_df, 'club', 'Wolfsburg'),
    'Dynamo Kyiv': filter_data(goals_df, 'club', 'Dynamo Kyiv'),
    'Sevilla': filter_data(goals_df, 'club', 'Sevilla'),
    'Shakhtar Donetsk': filter_data(goals_df, 'club', 'Shakhtar Donetsk'),
    'Zenit': filter_data(goals_df, 'club', 'Zenit'),
    'Porto': filter_data(goals_df, 'club', 'Porto'),
    'Milan': filter_data(goals_df, 'club', 'Milan'),
    'Dortmund': filter_data(goals_df, 'club', 'Dortmund'),
    'Young Boys': filter_data(goals_df, 'club', 'Young Boys'),
    'Malmo': filter_data(goals_df, 'club', 'Malmö'),
    'RB Leipzig': filter_data(goals_df, 'club', 'Leipzig'),
    'Besiktas': filter_data(goals_df, 'club', 'Beşiktaş'),
    'Atalanta': filter_data(goals_df, 'club', 'Atalanta'),
}

# Título e descrição
st.title("Chutes a Gol por Clube")
st.markdown("Selecione um clube para visualizar a distribuição de chutes nas diferentes áreas do campo.")

# Seleção do clube
selected_club = st.selectbox("Escolha um clube:", list(club_data_goals.keys()))

# Dados do clube selecionado
selected_data = club_data_goals[selected_club]
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

#==============================================================================#

# Carregar os dados
attempts_df = load_data(r'DataSet Project/ucl-matches-dataset-02/parquet/attempts.parquet')

club_data_attempts = {
    'Real Madrid': filter_data(attempts_df, 'club', 'Real Madrid'),
    'Liverpool': filter_data(attempts_df, 'club', 'Liverpool'),
    'Villarreal': filter_data(attempts_df, 'club', 'Villarreal'),
    'Man. City': filter_data(attempts_df, 'club', 'Man. City'),
    'Benfica': filter_data(attempts_df, 'club','Benfica'),
    'Atlético Madrid': filter_data(attempts_df, 'club', 'Atlético'),
    'Bayern Munich': filter_data(attempts_df, 'club', 'Bayern'),
    'Chelsea': filter_data(attempts_df, 'club', 'Chelsea'),
    'LOSC': filter_data(attempts_df, 'club', 'LOSC'),
    'Inter': filter_data(attempts_df, 'club', 'Inter'),
    'Salzburg': filter_data(attempts_df, 'club', 'Salzburg'),
    'Ajax': filter_data(attempts_df, 'club', 'Ajax'),
    'Paris Saint-Germain': filter_data(attempts_df, 'club', 'Paris'),
    'Sporting CP': filter_data(attempts_df, 'club', 'Sporting CP'),
    'Juventus': filter_data(attempts_df, 'club', 'Juventus'),
    'Manchester United': filter_data(attempts_df, 'club', 'Man. United'),
    'Barcelona': filter_data(attempts_df, 'club', 'Barcelona'),
    'Club Brugge': filter_data(attempts_df, 'club', 'Club Brugge'),
    'Sheriff': filter_data(attempts_df, 'club', 'Sheriff'),
    'Wolfsburg': filter_data(attempts_df, 'club', 'Wolfsburg'),
    'Dynamo Kyiv': filter_data(attempts_df, 'club', 'Dynamo Kyiv'),
    'Sevilla': filter_data(attempts_df, 'club', 'Sevilla'),
    'Shakhtar Donetsk': filter_data(attempts_df, 'club', 'Shakhtar Donetsk'),
    'Zenit': filter_data(attempts_df, 'club', 'Zenit'),
    'Porto': filter_data(attempts_df, 'club', 'Porto'),
    'Milan': filter_data(attempts_df, 'club', 'Milan'),
    'Dortmund': filter_data(attempts_df, 'club', 'Dortmund'),
    'Young Boys': filter_data(attempts_df, 'club', 'Young Boys'),
    'Malmo': filter_data(attempts_df, 'club', 'Malmö'),
    'RB Leipzig': filter_data(attempts_df, 'club', 'Leipzig'),
    'Besiktas': filter_data(attempts_df, 'club', 'Beşiktaş'),
    'Atalanta': filter_data(attempts_df, 'club', 'Atalanta'),
}

posicoes = {
    'Atacante':'Forward',
    'Meio-campista':'Midfielder',
    'Zagueiro':'Defender'
}

st.divider()
st.title("Comparativo de Chutes a Gol")
st.markdown("Escolha os clubes para comparar a distribuição de chutes a gol de jogadores em diferentes posições.")

# Seleção dos clubes
variancia_club_selecionados= st.multiselect("Escolha dois clubes:", list(club_data_attempts.keys()), default=['Real Madrid', 'Liverpool'])
variancia_posicoes = st.selectbox("Escolha uma posição de campo:", list(posicoes.keys()))


# Filtrando os dados para os clubes e posição selecionados
clubs_filtrados_posicao = pd.concat(
    [filter_data(club_data_attempts[club], 'position', posicoes[variancia_posicoes]) 
     for club in variancia_club_selecionados]
)
# Plotando o gráfico de barras agrupadas
st.markdown("## ")
fig, ax = plt.subplots(figsize=(10, 6))
    
clubs_barplot_df = clubs_filtrados_posicao.melt(
    id_vars=['club'], 
    value_vars=['total_attempts', 'on_target', 'off_target'], 
    var_name='Tipo de Chute', 
    value_name='Quantidade'
)
# Mapeamento dos rótulos do eixo x
tipo_chute_labels = {
    'total_attempts': 'Total de Chutes',
    'on_target': 'Chutes no Gol',
    'off_target': 'Chutes para Fora'
}
clubs_barplot_df['Tipo de Chute'] = clubs_barplot_df['Tipo de Chute'].map(tipo_chute_labels)

sns.barplot(data=clubs_barplot_df, x='Tipo de Chute', y='Quantidade', hue='club', ax=ax, palette='Set2')
ax.set_title('Comparação de Chutes a Gol')
ax.set_ylabel('Quantidade')
ax.set_xlabel('Tipo de Chute')
sns.despine(trim=True)

st.pyplot(fig)