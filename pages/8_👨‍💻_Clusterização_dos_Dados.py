import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import plotly.express as px

@st.cache_data
def load_data(file_path):
    return pd.read_parquet(file_path)

def main():
    st.title("👨‍💻 Clusterização dos Dados")
    st.write("Organizamos objetos semelhantes em grupos para identificar padrões e melhorar a tomada de decisões.")
    st.divider()

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

    cluster_data = load_data(r"DataSet Project/clustering/data/merge_filtred_default.parquet")
    st.write("### Conjunto de Dados Utilizado:")
    st.dataframe(cluster_data)

    st.write("### Algoritmo Utilizado")
    st.write("Aplicamos o algoritmo KMeans para agrupar as observações em clusters, com as variáveis categóricas dummyficadas.")
    st.write("Testamos dois tipos de clusterização:")
    st.markdown("""
    - **Normalização:** Clusterização com dados normalizados
    - **Padronização:** Clusterização com dados padronizados
    """)

    st.header("🦾 Método do Cotovelo")
    st.write("Utilizamos o método do cotovelo para determinar o número ideal de clusters.")
    dados_clusterizacao = st.selectbox("Selecione o tipo dado utilizado na clusterizacao", ["Selecione", "Normalizado", "Padronizado"])
    
    df = None
    
    if dados_clusterizacao in ["Normalizado", "Padronizado"]:
        if dados_clusterizacao == "Normalizado":
            df = load_data(r"DataSet Project/clustering/data/merge_normalized_dummy.parquet")
        elif dados_clusterizacao == "Padronizado":
            df = load_data(r"DataSet Project/clustering/data/merge_standardized_dummy.parquet")
        metodo_cotovelo(df)
    
    qtd_clusters = st.number_input("Após analise, quantos clusters você quer separar?", min_value=2, max_value=14, value=3)
    
    st.header("🫧 Clusterização")
    st.write("Após a identificação do número de clusters ideal, aplicamos o algoritmo KMeans para clusterizar os dados.")
    st.write("Abaixo, apresentamos os dados clusterizados: ")
    
    if dados_clusterizacao:
        cluster_data_clusterizado = get_cluster_data(df, qtd_clusters)
        st.dataframe(cluster_data_clusterizado)


        selected_teams = st.multiselect("Selecione os times para visualização", cluster_data_clusterizado['club_name'].unique(),default=['real madrid','bayern munich'],max_selections=7,)
        
        if selected_teams:
            team_data = cluster_data_clusterizado[cluster_data_clusterizado['club_name'].isin(selected_teams)]
            distribution_by_cluster(team_data, selected_teams)
        
        cards_grafic(cluster_data_clusterizado, 'cluster', ['yellow_cards', 'red_cards'])
        
        select_formations = st.multiselect("Selecione as formações táticas para visualizar a quantidade de formações táticas por cluster", cluster_data['club_formation'].unique(),default=['4-4-2 double 6','3-5-2 flat','4-2-3-1'],max_selections=7)
        formacoes_taticas(cluster_data_clusterizado, select_formations, qtd_clusters)


custom_palette = [
        '#F05A28',  # Laranja Escuro
        '#F46D25',  # Laranja Vibrante
        '#F7931E',  # Laranja Brilhante
        '#F6A623',  # Laranja Claro
        '#F7B500',  # Amarelo Dourado
        '#F8D25C',  # Amarelo Claro
        '#FFF0BC',  # Amarelo Suave
    ]


# GRÁFICO DE DISTRIBUIÇÃO DOS TIMES
def distribution_by_cluster(data, team_names):
    st.header(f"Distribuição de Times por cluster:")
    
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
            ticktext=[f'Cluster {i}' for i in data['cluster'].unique()]
        ),
        yaxis=dict(
            title='Número de Ocorrências',
            tickformat='d'  
        )
    )
    
    st.plotly_chart(fig)


# GRÁFICO DE FORMAÇÃO TATICA
@st.cache_data
def formacoes_taticas(data, formations, qtd_clusters):
    if 'club_formation' not in data.columns:
        st.error("A coluna 'club_formation' não existe no DataFrame.")
        return

    filtered_data = data[data['club_formation'].isin(formations)]

    if filtered_data.empty:
        st.warning("Não há dados para as formações táticas selecionadas.")
        return

    formation_counts = filtered_data.groupby(['cluster', 'club_formation']).size().reset_index(name='count')

    all_clusters = pd.DataFrame({'cluster': range(qtd_clusters)})
    all_formations = pd.DataFrame({'club_formation': formations})
    all_combinations = all_clusters.merge(all_formations, how='cross')  
    formation_counts = pd.merge(all_combinations, formation_counts, on=['cluster', 'club_formation'], how='left').fillna(0)

    formation_counts['cluster_label'] = 'Cluster ' + formation_counts['cluster'].astype(str)
    
    fig = px.bar(formation_counts, x='cluster_label', y='count', color='club_formation',
                 labels={'cluster_label': '', 'count': 'Count', 'club_formation': 'Club Formation'},
                 title="Quantidade de Formações Táticas por Cluster",
                 barmode='group',
                 color_discrete_sequence=custom_palette)

    st.plotly_chart(fig)

   

# GRÁFICO DE BARRA EMPILHADA PARA CARTÕES
@st.cache_data
def cards_grafic(data, cluster_column, columns_to_plot):
    if cluster_column not in data.columns:
        st.error(f"A coluna '{cluster_column}' não existe no DataFrame.")
        return
    fig = go.Figure()

    color_map = {
        'yellow_cards': '#ffde4d',  
        'red_cards': '#D9534F'      
    }

    for column in columns_to_plot:
        if column not in data.columns:
            st.warning(f"A coluna '{column}' não existe no DataFrame.")
            continue
        cluster_means = data.groupby(cluster_column)[column].mean().reset_index()

        fig.add_trace(go.Bar(
            x=cluster_means[cluster_column].astype(str), 
            y=cluster_means[column],
            name=column,
            marker_color=color_map.get(column, 'blue')  
        ))

    fig.update_layout(
        yaxis_title='Count',
        title='Cartões amarelhos e vermelhos',
        barmode='stack',  
        xaxis=dict(
            tickmode='array',
            tickvals=[str(i) for i in range(len(cluster_means[cluster_column].unique()))],  
            ticktext=[f'Cluster {i}' for i in range(len(cluster_means[cluster_column].unique()))]  
        )
    )

    st.plotly_chart(fig)

    
@st.cache_data
def metodo_cotovelo(dados_clusterizacao):
    distortions = []
    n_clusters = list(range(2, 10))
    for n_clus in n_clusters:
        distortions.append(KMeans(n_clusters=n_clus, max_iter=10_000, n_init=100, random_state=61658).fit(dados_clusterizacao).inertia_)

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
    
    km = KMeans(n_clusters=qtd_clusters, max_iter=10_000, n_init=100, random_state=42)
    merged_default = km.fit_predict(dados_clusterizacao)
    df_default['cluster'] = merged_default
    
    return df_default

if __name__ == "__main__":
    main()
