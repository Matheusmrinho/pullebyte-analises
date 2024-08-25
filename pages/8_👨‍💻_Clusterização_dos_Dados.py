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

    # Método do Cotovelo
    st.header("🦾 Método do Cotovelo")
    st.write("Utilizamos o método do cotovelo para determinar o número ideal de clusters.")
    st.write("Aplicamos o algoritmo KMeans para agrupar as observações em clusters, com as variáveis categóricas dummyficadas.")
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
        legend_title='Tipo de Gol',
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
    st.markdown(f"<h6 style='text-align: center; margin-top:-15px'>{title}</h6>", unsafe_allow_html=True)
    
def plot_assists_boxplot(df):
    # Mapeamento das cores para cada cluster com cores sólidas e padrão
    color_map = {
        0: '#1f77b4',  # Azul padrão
        1: '#ff7f0e',  # Laranja padrão
        2: '#d62728'   # Vermelho padrão
    }
    
    # Criando o box plot com Plotly
    fig = px.box(df, x="cluster", y="assists", color="cluster",
                 color_discrete_map=color_map,
                 labels={"assists": "Assistências"},
                 template="plotly_white")  # Tema claro

    # Customizando o layout do gráfico
    fig.update_layout(
        xaxis_title="Cluster",
        yaxis_title="Quantidade de Assist.",
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
