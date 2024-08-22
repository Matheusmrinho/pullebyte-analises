import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import LabelEncoder

@st.cache_data
def load_data(file_path):
    return pd.read_parquet(file_path)

def main():
   # Título e descrição principal
    st.title("👨‍💻 Clusterização dos Dados")
    st.write("Organizamos objetos semelhantes em grupos para identificar padrões e melhorar a tomada de decisões.")
    st.divider()

    # Subtítulo e lista dos dados selecionados
    st.subheader("🎲 Dados Selecionados")
    st.write("""
    - **club_name:** Nome do clube
    - **club_formation:** Formação tática do clube
    - **team_type:** Tipo de equipe (titular/reserva)
    - **yellow_cards:** Cartões amarelos
    - **red_cards:** Cartões vermelhos
    - **goals:** Gols marcados
    - **assists:** Assistências
    """)

    # Exibindo o conjunto de dados
    cluster_data = load_data(r"DataSet Project/clustering/data/merge_filtred_default.parquet")
    st.write("### Conjunto de Dados Utilizado:")
    st.dataframe(cluster_data.head())

    # Algoritmo utilizado e tipos de clusterização
    st.write("### Algoritmo Utilizado")
    st.write("Aplicamos o algoritmo KMeans para agrupar as observações em clusters, com as variáveis categóricas dummyficadas.")
    st.write("Testamos dois tipos de clusterização:")
    st.markdown("""
    - **Normalização:** Clusterização com dados normalizados
    - **Padronização:** Clusterização com dados padronizados
    """)

    # Método do Cotovelo
    st.header("🦾 Método do Cotovelo")
    st.write("Utilizamos o método do cotovelo para determinar o número ideal de clusters.")
    dados_clusterizacao = st.selectbox("Selecione o tipo dado utilizado na clusterizacao", ["Selecione", "Normalizado", "Padronizado"])
    
    if dados_clusterizacao in ["Normalizado", "Padronizado"]:
        metodo_cotovelo(dados_clusterizacao)
    
        
    qtd_clusters = st.number_input("Após analise, quantos clusters você quer separar?", min_value=2, max_value=14, value=3)
    
    st.header("🫧 Clusterização")
    st.write("Após a identificação do número de clusters ideal, aplicamos o algoritmo KMeans para clusterizar os dados.")
    st.write("Abaixo, apresentamos os dados clusterizados: ")
    
    if dados_clusterizacao in ["Normalizado", "Padronizado"] and qtd_clusters != 0:
        cluster_data_clusterizado = get_cluster_data(dados_clusterizacao, qtd_clusters)
        st.dataframe(cluster_data_clusterizado.head())
        plot_bar_charts(cluster_data_clusterizado, 'cluster', ['yellow_cards', 'red_cards', 'goals', 'suffered_goals', 'assists'])
        
        select_formations = st.multiselect("Selecione as formações táticas para visualizar a quantidade de formações táticas por cluster", cluster_data['club_formation'].unique())
        formacoes_taticas(cluster_data_clusterizado, select_formations, qtd_clusters)
        
        select_treemp = st.selectbox("Selecione a visualização dos clubes por cluster", cluster_data_clusterizado.columns, index=0)
        treemap(cluster_data_clusterizado, select_treemp, 'Agrupamento de dados por cluster')

def treemap(df, column, title):
    for cluster in sorted(df['cluster'].unique()):
        filtered_df = df[df['cluster'] == cluster]
        fig = px.treemap(filtered_df, path=[column], title=f"Agrupamento - Cluster {cluster}", width=700, height=500)
        fig.update_layout(margin = dict(t=50, l=25, r=35, b=25))
        fig.update_traces(marker=dict(cornerradius=3))
        st.plotly_chart(fig)

@st.cache_data
def formacoes_taticas(data, formations, qtd_clusters):
    # Verifica se a coluna 'club_formation' existe no DataFrame
    if 'club_formation' not in data.columns:
        st.error("A coluna 'club_formation' não existe no DataFrame.")
        return

    # Filtra os dados para as formações táticas selecionadas
    filtered_data = data[data['club_formation'].isin(formations)]

    # Verifica se há dados filtrados
    if filtered_data.empty:
        st.warning("Não há dados para as formações táticas selecionadas.")
        return

    # Conta a quantidade de formações táticas em cada cluster
    formation_counts = filtered_data.groupby(['cluster', 'club_formation']).size().reset_index(name='count')

    # Garante que todos os clusters estejam representados, mesmo os que não têm formações
    all_clusters = pd.DataFrame({'cluster': range(qtd_clusters)})
    all_formations = pd.DataFrame({'club_formation': formations})
    all_combinations = all_clusters.merge(all_formations, how='cross')  # Combinação cruzada de clusters e formações
    formation_counts = pd.merge(all_combinations, formation_counts, on=['cluster', 'club_formation'], how='left').fillna(0)

    # Plota o gráfico de barras para todas as formações táticas, agrupadas por cluster
    fig = px.bar(formation_counts, x='cluster', y='count', color='club_formation',
                 labels={'cluster': 'Cluster', 'count': 'Count', 'club_formation': 'Club Formation'},
                 title="Quantidade de Formações Táticas por Cluster",
                 barmode='group',
                 color_discrete_sequence=px.colors.qualitative.Pastel)  # Paleta de tons pastéis

    st.plotly_chart(fig)
    
@st.cache_data
def plot_bar_charts(data, cluster_column, columns_to_plot):
    # Verifica se a coluna de clusters existe
    if cluster_column not in data.columns:
        st.error(f"A coluna '{cluster_column}' não existe no DataFrame.")
        return

    # Cria uma lista de cores baseada no número de clusters
    unique_clusters = data[cluster_column].unique()
    color_map = px.colors.qualitative.Pastel

    for column in columns_to_plot:
        if column not in data.columns:
            st.warning(f"A coluna '{column}' não existe no DataFrame.")
            continue

        # Agrupa os dados por cluster e calcula a média da coluna
        cluster_means = data.groupby(cluster_column)[column].mean().reset_index()

        # Cria o gráfico de barras com cores diferentes para cada cluster
        fig = go.Figure()

        for i, cluster in enumerate(unique_clusters):
            cluster_data = cluster_means[cluster_means[cluster_column] == cluster]
            fig.add_trace(go.Bar(
                x=cluster_data[cluster_column],
                y=cluster_data[column],
                name=f'Cluster {cluster}',
                marker_color=color_map[i % len(color_map)]  # Aplica cores cíclicas da paleta
            ))

        fig.update_layout(
            xaxis_title='Cluster',
            yaxis_title=column,
            title=f'Média de {column} por Cluster',
            barmode='group'  # Exibe as barras lado a lado
        )

        st.plotly_chart(fig)
    
@st.cache_data
def metodo_cotovelo(dados_clusterizacao):
    if dados_clusterizacao == "Normalizado":
        data = load_data(r"DataSet Project/clustering/data/merge_normalized_dummy.parquet")
    elif dados_clusterizacao == "Padronizado":
        data = load_data(r"DataSet Project/clustering/data/merge_standardized_dummy.parquet")
    
    distortions = []
    n_clusters = list(range(2, 10))
    for n_clus in n_clusters:
        distortions.append(KMeans(n_clusters=n_clus, max_iter=10_000, n_init=100, random_state=61658).fit(data).inertia_)

    fig = go.Figure(data=go.Scatter(x=n_clusters, y=distortions))
    fig.update_layout(
        xaxis_title='Number of clusters',
        yaxis_title='Inertia',
        title='Elbow Curve'
    )
    st.plotly_chart(fig)
        
@st.cache_data
def get_cluster_data(dados_clusterizacao, qtd_clusters):
    df_default = load_data(r"DataSet Project/clustering/data/merge_filtred_default.parquet")
    df = None
    if dados_clusterizacao == "Normalizado":
        df = load_data(r"DataSet Project/clustering/data/merge_normalized_dummy.parquet")
    elif dados_clusterizacao == "Padronizado":
        df = load_data(r"DataSet Project/clustering/data/merge_standardized_dummy.parquet")
    
    km = KMeans(n_clusters=qtd_clusters, max_iter=10_000, n_init=100, random_state=42)
    merged_default = km.fit_predict(df)
    df_default['cluster'] = merged_default
    
    return df_default

if __name__ == "__main__":
    main()
