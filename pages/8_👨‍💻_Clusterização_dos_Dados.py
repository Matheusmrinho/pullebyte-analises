import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import plotly.graph_objects as go

@st.cache_data
def load_data(file_path):
    return pd.read_parquet(file_path)

def main():
    st.title("👨‍💻 Clusterização dos Dados")
    st.write("Clusterização é o processo de organizar objetos de modo que itens semelhantes fiquem juntos em grupos, ou clusters.")
    st.write("Essa análise nos permite identificar padrões e semelhanças entre as partidas, contribuindo para uma melhor compreensão dos dados e tomada de decisões.")
    st.info(icon="ℹ️", body='**Dados utilizados na clusterização**\n\nUtilizamos a junção dos dados das partidas realizadas pelos clubes, junto com os eventos referentes a cada partida, como: gols, cartões, faltas, chutes a gol, entre outros.')
    st.divider()
    st.subheader("🎲 Dados Utilizados na Clusterização")
    st.write("Os dados brutos obtidos no dataset do keagle foram retirando dados nulos e com tipagem incorreta, além de terem sido selecionados pela liga(UCL - Champions League) e informações relevantes da partida como:")
    st.write("- club_name\n- club_formation\n- team_type\n- yellow_cards\n- red_cards\n- goals\n- assists")
    
    # Exibindo o conjunto de dados original filtrado
    cluster_data = load_data(r"DataSet Project/clustering/data/merge_filtred_default.parquet")
    st.write("Conjunto de dados utilizados na clusterização:")
    st.dataframe(cluster_data)
    
    st.write("Para a clusterização dos dados, utilizamos o algoritmo KMeans, que é um método de agrupamento que visa particionar n observações em k clusters.")
    st.write("Para esse algoritmo funcionar, é necessario realizar a dummyficação dos dados, ou seja, transformar as variáveis categóricas em variáveis numéricas.")
    st.write("Fizemos dois tipos de clusterização visando identificar qual obteve melhores resultados:")
    st.write("- CLusterização com dados estatíticos normalizados\n- Clusterização com dados estatíticos padronizados")

    st.header("🦾 Aplicando o método do cotovelo")
    st.write("O método do cotovelo é uma técnica utilizada para identificar o número ideal de clusters em um conjunto de dados.")
    dados_clusterizacao = st.selectbox("Selecione o tipo dado utilizado na clusterizacao", ["Selecione", "Normalizado", "Padronizado"])
    
    if dados_clusterizacao in ["Normalizado", "Padronizado"]:
        metodo_cotovelo(dados_clusterizacao)
    
        
    qtd_clusters = st.number_input("Após analise, quantos clusters você quer separar?", min_value=2, max_value=14, value=4)
    
    st.header("🫧 Clusterização")
    st.write("Após a identificação do número de clusters ideal, aplicamos o algoritmo KMeans para clusterizar os dados.")
    st.write("Abaixo, apresentamos os dados clusterizados: ")
    
    if dados_clusterizacao in ["Normalizado", "Padronizado"] and qtd_clusters != 0:
        cluster_data_clusterizado = get_cluster_data(dados_clusterizacao, qtd_clusters)
        st.dataframe(cluster_data_clusterizado)
        
    
@st.cache_data
def metodo_cotovelo(dados_clusterizacao):
    if dados_clusterizacao == "Normalizado":
        data = load_data(r"DataSet Project/clustering/data/merge_normalized_dummy.parquet")
    elif dados_clusterizacao == "Padronizado":
        data = load_data(r"DataSet Project/clustering/data/merge_standardized_dummy.parquet")
    
    distortions = []
    n_clusters = list(range(2, 15))
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
