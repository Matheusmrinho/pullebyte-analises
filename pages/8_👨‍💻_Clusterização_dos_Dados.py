from sklearn.metrics import silhouette_samples, silhouette_score
import numpy as np
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import plotly.express as px

@st.cache_data
def load_data(file_path):
    return pd.read_parquet(file_path)

def categorize_formations(data):
    offensive_formations = [
    "4-3-3 attacking",
    "4-3-1-2",
    "3-4-3",
    "3-5-2 attacking",
    "3-1-4-2",
    "3-4-3 diamond",
    "4-4-2 diamond"
]

# Formações defensivas
    defensive_formations = [
        "4-3-3 defending",
        "5-4-1",
        "4-5-1 flat",
        "4-1-4-1",
        "3-3-3-1"
]

    # Formações equilibradas
    balanced_formations = [
        "4-4-2 double 6",
        "3-5-2 flat",
        "4-2-3-1",
        "4-4-2",
        "4-4-1-1",
        "3-4-2-1",
        "4-4-2 flat",
        "3-5-2"
]

    def categorize(formation):
        if any(off in formation for off in offensive_formations):
            return "Ofensiva"
        elif any(defn in formation for defn in defensive_formations):
            return "Defensiva"
        elif any(bal in formation for bal in balanced_formations):
            return "Equilibrada"
        else:
            return "Outras"

    data['club_formation'] = data['club_formation'].apply(categorize)
    return data

def main():
    st.title("👨‍💻 Clusterização dos Dados")
    st.write("Organizamos objetos semelhantes em grupos para identificar padrões e melhorar a tomada de decisões.")
    st.divider()

    st.subheader("🎲 Dados Selecionados")
        # Dados para a tabela
        # Dados para a tabela
    data = {
            "Campo": [
                "club_name", 
                "club_formation", 
                "team_type", 
                "yellow_cards", 
                "red_cards", 
                "goals", 
                "suffered_goals", 
                "assists", 
                "is_win"
            ],
            "Descrição": [
                "Nome do clube", 
                "Formação tática", 
                "Tipo de equipe", 
                "Cartões amarelos", 
                "Cartões vermelhos", 
                "Gols marcados", 
                "Gols sofridos", 
                "Assistências", 
                "Vitória (1), Empate (0), Derrota (-1)"
            ]
        }

        # Criar DataFrame sem índice
    df = pd.DataFrame(data)
        
    st.write(df.to_html(index=False, escape=False), unsafe_allow_html=True)

    st.header("🦾 Método do Cotovelo")
    st.write("Utilizamos o método do cotovelo para determinar o número ideal de clusters.")
    st.write("Aplicamos o algoritmo KMeans para agrupar as observações em clusters, com as variáveis categóricas dummyficadas.")
    dados_clusterizacao = st.selectbox("Selecione o tipo dado utilizado na clusterizacao", ["Selecione", "Normalizado", "Padronizado"])
    
    qtd_clusters = st.slider("Após analise, quantos clusters você quer separar?", value=3, min_value=2, max_value=8)
    
    df = None
    
    if dados_clusterizacao in ["Normalizado", "Padronizado"]:
        if dados_clusterizacao == "Normalizado":
            df = load_data(r"DataSet Project/clustering/data/merge_normalized_dummy.parquet")
        elif dados_clusterizacao == "Padronizado":
            df = load_data(r"DataSet Project/clustering/data/merge_standardized_dummy.parquet")
        
        metodo_cotovelo(df)

        grafico_silhueta(df, qtd_clusters)
        
        st.header("🫧 Clusterização")
        st.write("Após a identificação do número de clusters ideal, aplicamos o algoritmo KMeans para clusterizar os dados.")
        st.write("Abaixo, apresentamos os dados clusterizados: ")
        
        if dados_clusterizacao:
            cluster_data_clusterizado = get_cluster_data(df, qtd_clusters)
            cluster_data_clusterizado = categorize_formations(cluster_data_clusterizado)
            st.dataframe(cluster_data_clusterizado)
            
            st.subheader("📊 Distribuição dos Jogos dos Times entre Clusters")
            selected_teams = st.multiselect("Selecione os times para visualização", cluster_data_clusterizado['club_name'].unique(),default=['real madrid','bayern munich'])
            
            if selected_teams:
                team_data = cluster_data_clusterizado[cluster_data_clusterizado['club_name'].isin(selected_teams)]
                distribution_by_cluster(team_data, selected_teams)
            
            st.subheader("📊 Comparativo | Gols Marcados X Sofridos")
            
            gols_marcados_levados(cluster_data_clusterizado)
            
            st.subheader("📊 Distribuição | Vitórias, Derrotas e Empates")
            
            cols = st.columns(qtd_clusters)
            
            with cols[0]:
                treemap(cluster_data_clusterizado, 0, "Cluster 0")
            with cols[1]:
                treemap(cluster_data_clusterizado, 1, "Cluster 1")
            with cols[2]:
                treemap(cluster_data_clusterizado, 2, "Cluster 2")
            
            st.subheader("📊 Distribuição de Assistências por Cluster")

            plot_assists_boxplot(cluster_data_clusterizado)
            
            st.subheader("📊 Cartões Amarelos e Vermelhos")
            cards_grafic(cluster_data_clusterizado, 'cluster', ['yellow_cards', 'red_cards'])
            
            st.subheader("📊 Distribuição de formações por Cluster")
            formacoes_taticas(cluster_data_clusterizado, qtd_clusters)
        
custom_palette = [
        '#F05A28',  # Laranja Escuro
        '#40A578',  # Amarelo Dourado
        '#E4003A',  # Amarelo Claro
        '#F46D25',  # Laranja Vibrante
        '#F7931E',  # Laranja Brilhante
        '#FFF0BC',  # Amarelo Suave
        '#F6A623',  # Laranja Claro
    ]


# GRÁFICO DE DISTRIBUIÇÃO DOS TIMES
def distribution_by_cluster(data, team_names):
    fig = go.Figure()
      
    for i, team_name in enumerate(team_names):
        team_data = data[data['club_name'] == team_name]
        cluster_counts = team_data['cluster'].value_counts().sort_index()
        
        fig.add_trace(go.Bar(
            x=cluster_counts.index,
            y=cluster_counts.values,
            name=team_name,
            hovertemplate=f'Time: {team_name}<br>Cluster: %{{x}}<br>Número de Ocorrências: %{{y:.0f}}<extra></extra>',
            marker_color=custom_palette[i % len(custom_palette)]  # Aplica uma cor customizada
        ))
    
    fig.update_layout(
        yaxis_title='Número de Ocorrências',
        barmode='group',  
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(data['cluster'].unique()))),
            ticktext=[f'Cluster {i}' for i in sorted(data['cluster'].unique())]  # Ordena os clusters de forma ascendente
        ),
        legend=dict(
            orientation='h',  # Define a orientação da legenda para horizontal
            yanchor='top',  # Alinha a parte superior da legenda com o topo do gráfico
            y=-0.2,  # Ajusta a posição vertical da legenda para fora do gráfico
            xanchor='center',  # Alinha a legenda no centro horizontalmente
            x=0.5  # Posiciona a legenda no centro horizontalmente
        ),
        margin=dict(
            l=40,
            r=30,
            b=150,  # Aumenta o espaço inferior para acomodar a legenda
            t=50  # Ajusta o espaço superior para o título
        ),
        yaxis=dict(
            title='Número de Ocorrências',
            tickformat='d'  
        )
    )
    
    st.plotly_chart(fig)


# GRÁFICO DE FORMAÇÃO TATICA
@st.cache_data
def formacoes_taticas(data, qtd_clusters):
    if 'club_formation' not in data.columns:
        st.error("A coluna 'club_formation' não existe no DataFrame.")
        return

    color_map = {
        'yellow_cards': '#ffde4d',
        'red_cards': '#D9534F'
    }

    # Contar a quantidade de cada categoria de formação por cluster
    formation_counts = data.groupby(['cluster', 'club_formation']).size().reset_index(name='count')

    # Criar DataFrame com todas as combinações possíveis de clusters e categorias de formação
    all_clusters = pd.DataFrame({'cluster': range(qtd_clusters)})
    all_categories = pd.DataFrame({'club_formation': ['Ofensiva', 'Defensiva', 'Equilibrada', 'Outras']})
    all_combinations = all_clusters.merge(all_categories, how='cross')

    # Garantir que todas as combinações estão presentes no DataFrame final
    formation_counts = pd.merge(all_combinations, formation_counts, on=['cluster', 'club_formation'], how='left').fillna(0)

    # Adicionar rótulos aos clusters
    formation_counts['cluster_label'] = 'Cluster ' + formation_counts['cluster'].astype(str)
    
    # Criar o gráfico
    fig = px.bar(formation_counts, x='cluster_label', y='count', color='club_formation',
                 labels={'cluster_label': '', 'count': 'Count', 'club_formation': 'Categoria de Formação'},
                 barmode='group',
                 color_discrete_sequence=custom_palette)

    fig.update_layout(
        legend=dict(
            title=None,
            orientation='h',  # Define a orientação da legenda para horizontal
            yanchor='top',  # Alinha a parte superior da legenda com o topo do gráfico
            y=-0.2,  # Ajusta a posição vertical da legenda para fora do gráfico
            xanchor='center',  # Alinha a legenda no centro horizontalmente
            x=0.5 
    ))

    st.plotly_chart(fig)

@st.cache_data
def cards_grafic(data, cluster_column, columns_to_plot):
    if cluster_column not in data.columns:
        st.error(f"A coluna '{cluster_column}' não existe no DataFrame.")
        return
    
    fig = go.Figure()

    color_map = {
        'yellow_cards': '#FFB200',  
        'red_cards': '#E4003A'      
    }

    for column in columns_to_plot:
        if column not in data.columns:
            st.warning(f"A coluna '{column}' não existe no DataFrame.")
            continue
        
        cluster_means = data.groupby(cluster_column)[column].mean().reset_index()

        fig.add_trace(go.Bar(
            x=cluster_means[cluster_column].astype(str), 
            y=cluster_means[column],
            name='Cartões amarelos' if column == 'yellow_cards' else 'Cartões vermelhos',
            marker_color=color_map.get(column, 'blue')  
        ))

    fig.update_layout(
        yaxis_title='Count',
        barmode='stack',  
        xaxis=dict(
            tickmode='array',
            tickvals=[str(i) for i in range(len(cluster_means[cluster_column].unique()))],  
            ticktext=[f'Cluster {i}' for i in range(len(cluster_means[cluster_column].unique()))]  
        ),
        legend=dict(
            title=None,
            orientation='h',
            yanchor='top',
            y=-0.2,
            xanchor='center',
            x=0.5 
        )
    )

    st.plotly_chart(fig)


@st.cache_data
def gols_marcados_levados(data, cluster_column='cluster', columns_to_plot=['goals', 'suffered_goals']):
    if cluster_column not in data.columns:
        st.error(f"A coluna '{cluster_column}' não existe no DataFrame.")
        return

    fig = go.Figure()

    color_map = {
        'suffered_goals': '#E4003A',
        'goals': '#40A578'
    }
    
    # Adicionar uma barra para cada coluna em columns_to_plot
    for column in columns_to_plot:
        if column not in data.columns:
            st.warning(f"A coluna '{column}' não existe no DataFrame.")
            continue
        cluster_means = data.groupby(cluster_column)[column].mean().reset_index()
    
        if column == 'suffered_goals':
            column_label = 'Gols Sofridos'
        elif column == 'goals':
            column_label = 'Gols Marcados'
        else:
            column_label = column
    
        fig.add_trace(go.Bar(
            x=cluster_means[cluster_column].astype(str),
            y=cluster_means[column],
            name=column_label,
            marker_color=color_map.get(column, '#1f77b4'),  # Altera para a cor azul escura
            text=cluster_means[column].round(2),  # Adiciona o texto com a média
            textposition='outside'  # Posiciona o texto fora das barras
        ))
    
    fig.update_layout(
        barmode='group',  # Muda o modo para barras agrupadas
        yaxis_title='Quantidade Média de Gols',
        xaxis=dict(
            tickmode='array',
            tickvals=[str(i) for i in data[cluster_column].unique()],
            ticktext=[f'Cluster {i}' for i in data[cluster_column].unique()]
        ),
        legend=dict(
            orientation='h',  # Define a orientação da legenda para horizontal
            yanchor='top',  # Alinha a parte superior da legenda com o topo do gráfico
            y=-0.2,  # Ajusta a posição vertical da legenda para fora do gráfico
            xanchor='center',  # Alinha a legenda no centro horizontalmente
            x=0.5  # Posiciona a legenda no centro horizontalmente
        ),
        template='simple_white',  # Opção de template para um visual limpo
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=30  # Modifiquei o valor do topo para reduzir o espaço reservado para o título
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Remove a borda branca do fundo do gráfico
        paper_bgcolor='rgba(0,0,0,0)'  # Remove a borda branca do fundo do papel
    )
    
    st.plotly_chart(fig)
                  
def treemap(df, cluster, title):
    # Cria uma coluna categorizada para as vitórias, empates e derrotas
    df['result'] = df['is_win'].map({1: 'Vitórias', 0: 'Empates', -1: 'Derrotas'})
    
    # Define as cores para cada categoria
    color_map = {
        'Vitórias': '#40A578',
        'Empates': 'orange',
        'Derrotas': '#E4003A'
    }
    
    filtered_df = df[df['cluster'] == cluster]
    fig = px.treemap(
        filtered_df, 
        path=['result'],
        width=220, 
        height=400,
        labels={'value': 'Quantidade'},
        color='result',  # Usa a coluna 'result' para definir as cores
        color_discrete_map=color_map  # Aplica o mapa de cores definido
    )
    
    fig.update_layout(margin=dict(t=10, l=0, r=0, b=0))
    fig.update_traces(marker=dict(cornerradius=3))
    
    fig.data[0].insidetextfont = dict(size=12, color='white')
    fig.data[0].branchvalues = 'total'
    fig.data[0].textinfo = 'label+percent entry'
    fig.data[0].hovertemplate = '<b>%{label}</b><br>%{value}<br>%{percentParent}'
    
    # Renderiza o gráfico
    st.plotly_chart(fig)
    
    # Adiciona o título abaixo do gráfico
    st.markdown(f"<h6 style='text-align: center; margin-top:-18px,'>{title}</h6>", unsafe_allow_html=True)
    

def plot_assists_boxplot(df):
    # Mapeamento das cores para cada cluster com cores sólidas e padrão
    color_map = {
        0: '#1f77b4',  # Azul padrão
        1: '#ff7f0e',  # Laranja padrão
        2: '#d62728'   # Vermelho padrão
    }
    
    # Selecionar a orientação do boxplot
    orientation = st.selectbox("Escolha a orientação do boxplot", ["Vertical", "Horizontal"])

    # Criando o box plot com Plotly
    if orientation == "Vertical":
        fig = px.box(df, x="cluster", y="assists", color="cluster",
                     color_discrete_map=color_map,
                     labels={"assists": "Assistências"},
                     template="plotly_white")  # Tema claro
        fig.update_layout(
            xaxis_title="Cluster",
            yaxis_title="Quantidade de Assist.",
            xaxis_title_font_size=16,
            yaxis_title_font_size=16,
            showlegend=True
        )
    elif orientation == "Horizontal":
        fig = px.box(df, x="assists", y="cluster", color="cluster",
                     color_discrete_map=color_map,
                     labels={"assists": "Assistências"},
                     template="plotly_white",
                     orientation = "h"
                     )
                    
        fig.update_layout(
            xaxis_title="Quantidade de Assist.",
            yaxis_title="Cluster",
            xaxis_title_font_size=16,
            yaxis_title_font_size=16,
            showlegend=True
        )
    
    # Exibindo o gráfico no Streamlit
    st.plotly_chart(fig)

    
@st.cache_data
def metodo_cotovelo(dados_clusterizacao):
    distortions = []
    n_clusters = list(range(2, 10))
    for n_clus in n_clusters:
        distortions.append(KMeans(n_clusters=n_clus, max_iter=10_000, n_init=100, random_state=61658).fit(dados_clusterizacao).inertia_)

    fig = go.Figure(data=go.Scatter(x=n_clusters, y=distortions, line=dict(color='#F46D25')))
    fig.update_layout(
        
        xaxis_title='Number of clusters',
        yaxis_title='Inertia',
        title='Elbow Curve',
    )
    st.plotly_chart(fig)
    
def grafico_silhueta(df, n_clusters=3):
    # Ajustar o KMeans ao DataFrame df
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    cluster_labels = kmeans.fit_predict(df)

    # Calcular a pontuação média de Silhouette
    silhouette_avg = silhouette_score(df, cluster_labels)

    # Calcular as pontuações de Silhouette para cada ponto
    sample_silhouette_values = silhouette_samples(df, cluster_labels)

    y_lower = 10
    silhouette_data = []

    for i in range(n_clusters):
        # Agregar as pontuações de silhouette para o cluster i e ordenar
        ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]

        # Adicionar dados ao gráfico
        silhouette_data.append(go.Scatter(
            x=ith_cluster_silhouette_values,
            y=np.arange(y_lower, y_upper),
            mode='lines',
            fill='tozerox',
            fillcolor=color,
            line=dict(color=color),
            name=f'Cluster {i}'
        ))

        y_lower = y_upper + 10

    # Linha vertical para a pontuação média de silhouette de todos os valores
    silhouette_data.append(go.Scatter(
        x=[silhouette_avg, silhouette_avg],
        y=[0, y_lower],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Média Silhouette'
    ))

    # Layout do gráfico
    layout = go.Layout(
        title=None,
        xaxis=dict(title="Valores de Silhouette", range=[-0.1, 1.0]),
        yaxis=dict(title="Cluster", showticklabels=False),
        showlegend=True
    )

    fig = go.Figure(data=silhouette_data, layout=layout)

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)
    st.write(f"Pontuação Média de Silhouette: {silhouette_avg:.4f}")
        

@st.cache_data
def get_cluster_data(dados_clusterizacao, qtd_clusters):
    df_default = load_data(r"DataSet Project/clustering/data/merge_filtred_default.parquet")
    
    km = KMeans(n_clusters=qtd_clusters, max_iter=10_000, n_init=100, random_state=42)
    merged_default = km.fit_predict(dados_clusterizacao)
    df_default['cluster'] = merged_default
    
    return df_default

if __name__ == "__main__":
    main()
