from sklearn.metrics import silhouette_samples, silhouette_score
import numpy as np
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import plotly.express as px

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

    defensive_formations = [
        "4-3-3 defending",
        "5-4-1",
        "4-5-1 flat",
        "4-1-4-1",
        "3-3-3-1"
    ]

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

    df = pd.DataFrame(data)
    st.write(df.to_html(index=False, escape=False), unsafe_allow_html=True)

    st.divider()

    st.header("🪐 Seleção de Dados para Análise")
    st.write("Após análises, foi identificado que os dados padronizados são mais adequados para a clusterização, considerando isso abaixo você pode selecionar os dados que deseja analisar:")
    
    dados_clusterizacao = st.selectbox("Selecione o tipo dado utilizado na clusterização", ["Selecione", "Normalizado", "Padronizado"])
    
    tipo_time_selection = st.selectbox("Selecione se os dados utilizados devem ser dos times que jogaram em casa, fora de casa ou ambos", ["Todos", "Time da casa", "Time fora de casa"])

    if tipo_time_selection == "Time da casa":
        team_type_selection = "home"
    elif tipo_time_selection == "Time fora de casa":
        team_type_selection = "away"
    else:
        team_type_selection = "Todos"
    
    qtd_clusters = 3
    
    df = None
    
    if dados_clusterizacao in ["Normalizado", "Padronizado"]:
        if dados_clusterizacao == "Normalizado":
            df = load_data(r"DataSet Project/clustering/clustered-data/clustered_data_normalized.parquet")
        elif dados_clusterizacao == "Padronizado":
            df = load_data(r"DataSet Project/clustering/clustered-data/clustered_data_standardized.parquet")
        
          
        if team_type_selection != "Todos":
            df = df[df['team_type'] == team_type_selection]
        
        st.dataframe(df)

        st.subheader("🔍 Seleção de Gráficos")
        selected_charts = st.multiselect(
            "Escolha quais gráficos deseja exibir:",
            ["Distribuição dos Jogos dos Times entre Clusters",
             "Comparativo | Gols Marcados X Sofridos",
             "Distribuição | Vitórias, Derrotas e Empates",
             "Distribuição de Assistências por Cluster",
             "Cartões Amarelos e Vermelhos",
             "Distribuição de Formações por Cluster"]
        )
        
        if "Distribuição dos Jogos dos Times entre Clusters" in selected_charts:
            st.subheader("📊 Distribuição dos Jogos dos Times entre Clusters")
            selected_teams = st.multiselect("Selecione os times para visualização", df['club_name'].unique(),default=['real madrid','bayern munich'])
            if selected_teams:
                team_data = df[df['club_name'].isin(selected_teams)]
                distribution_by_cluster(team_data, selected_teams)
        
        if "Comparativo | Gols Marcados X Sofridos" in selected_charts:
            st.subheader("📊 Comparativo | Gols Marcados X Sofridos")
            gols_marcados_levados(df)
        
        if "Distribuição | Vitórias, Derrotas e Empates" in selected_charts:
            st.subheader("📊 Distribuição | Vitórias, Derrotas e Empates")
            cols = st.columns(qtd_clusters)
            for i in range(qtd_clusters):
                with cols[i]:
                    treemap(df, i, f"Cluster {i}")
        
        if "Distribuição de Assistências por Cluster" in selected_charts:
            st.subheader("📊 Distribuição de Assistências por Cluster")
            plot_assists_boxplot(df)
        
        if "Cartões Amarelos e Vermelhos" in selected_charts:
            st.subheader("📊 Cartões Amarelos e Vermelhos")
            cards_grafic(df, 'cluster', ['yellow_cards', 'red_cards'])
        
        if "Distribuição de Formações por Cluster" in selected_charts:
            st.subheader("📊 Distribuição de Formações por Cluster")
            formacoes_taticas(df, qtd_clusters)

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
            marker_color=custom_palette[i % len(custom_palette)]  
        ))
    
    fig.update_layout(
        yaxis_title='Número de Ocorrências',
        barmode='group',  
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(len(data['cluster'].unique()))),
            ticktext=[f'Cluster {i}' for i in sorted(data['cluster'].unique())] 
        ),
        legend=dict(
            orientation='h',  
            yanchor='top',  
            y=-0.2,  
            xanchor='center',  
            x=0.5  
        ),
        margin=dict(
            l=40,
            r=30,
            b=150,  
            t=50  
        ),
        yaxis=dict(
            title='Número de Ocorrências',
            tickformat='d'  
        )
    )
    
    st.plotly_chart(fig)


# GRÁFICO DE FORMAÇÃO TATICA
def formacoes_taticas(data, qtd_clusters):
    if 'club_formation' not in data.columns:
        st.error("A coluna 'club_formation' não existe no DataFrame.")
        return

    categorize_checkbox = st.checkbox("Categorizar Formaçōes", value=True)

    if categorize_checkbox:
        formation_counts = categorize_formations(data).groupby(['cluster', 'club_formation']).size().reset_index(name='count')
        fig = px.bar(formation_counts, x='cluster', y='count', color='club_formation',
                    labels={'cluster': 'Cluster', 'count': 'Count', 'club_formation': 'Categoria de Formação'},
                    color_discrete_sequence=custom_palette)
    else:
        formation_options = data['club_formation'].unique()  

        default_selections = list(formation_options[:3])

        selected_formations = st.multiselect("Selecione as formações para exibir:", formation_options, default=default_selections)
        
        if selected_formations:
            filtered_data = data[data['club_formation'].isin(selected_formations)]
            formation_counts = filtered_data.groupby(['cluster', 'club_formation']).size().reset_index(name='count')
            fig = px.bar(formation_counts, x='cluster', y='count', color='club_formation',
                        labels={'cluster': 'Cluster', 'count': 'Count', 'club_formation': 'Formação'},
                        color_discrete_sequence=custom_palette)
        else:
            st.warning("Nenhuma formação selecionada.")
            return

    fig.update_layout(
        barmode='group',
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
            marker_color=color_map.get(column, '#1f77b4'), 
            text=cluster_means[column].round(2),  
            textposition='outside'  
        ))
    
    fig.update_layout(
        barmode='group',  
        yaxis_title='Quantidade Média de Gols',
        xaxis=dict(
            tickmode='array',
            tickvals=[str(i) for i in data[cluster_column].unique()],
            ticktext=[f'Cluster {i}' for i in data[cluster_column].unique()]
        ),
        legend=dict(
            orientation='h',  
            yanchor='top',  
            y=-0.2,  
            xanchor='center',  
            x=0.5 
        ),
        template='simple_white', 
        margin=dict(
            l=40,
            r=30,
            b=80,
            t=30 
        ),
        plot_bgcolor='rgba(0,0,0,0)',  
        paper_bgcolor='rgba(0,0,0,0)'  
    )
    
    st.plotly_chart(fig)
                  
def treemap(df, cluster, title):
    df['result'] = df['is_win'].map({1: 'Vitórias', 0: 'Empates', -1: 'Derrotas'})
    
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
        color='result', 
        color_discrete_map=color_map  
    )
    
    fig.update_layout(margin=dict(t=10, l=0, r=0, b=0))
    fig.update_traces(marker=dict(cornerradius=3))
    
    fig.data[0].insidetextfont = dict(size=12, color='white')
    fig.data[0].branchvalues = 'total'
    fig.data[0].textinfo = 'label+percent entry'
    fig.data[0].hovertemplate = '<b>%{label}</b><br>%{value}<br>%{percentParent}'
    
    st.plotly_chart(fig)
    
    st.markdown(f"<h6 style='text-align: center; margin-top:-18px,'>{title}</h6>", unsafe_allow_html=True)
    

def plot_assists_boxplot(df):
    color_map = {
        0: '#1f77b4',  # Azul padrão
        1: '#ff7f0e',  # Laranja padrão
        2: '#d62728'   # Vermelho padrão
    }
    
    orientation = st.selectbox("Escolha a orientação do boxplot", ["Vertical", "Horizontal"])

    if orientation == "Vertical":
        fig = px.box(df, x="cluster", y="assists", color="cluster",
                     color_discrete_map=color_map,
                     labels={"assists": "Assistências"},
                     template="plotly_white")  
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
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    cluster_labels = kmeans.fit_predict(df)


    silhouette_avg = silhouette_score(df, cluster_labels)

    sample_silhouette_values = silhouette_samples(df, cluster_labels)

    y_lower = 10
    silhouette_data = []

    for i in range(n_clusters):
        ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]

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

    silhouette_data.append(go.Scatter(
        x=[silhouette_avg, silhouette_avg],
        y=[0, y_lower],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Média Silhouette'
    ))

    layout = go.Layout(
        title=None,
        xaxis=dict(title="Valores de Silhouette", range=[-0.1, 1.0]),
        yaxis=dict(title="Cluster", showticklabels=False),
        showlegend=True
    )

    fig = go.Figure(data=silhouette_data, layout=layout)

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
