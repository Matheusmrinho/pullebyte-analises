import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import plotly.express as px
from ydata_profiling import ProfileReport
import os
import streamlit.components.v1 as components


df = pd.read_parquet('DataSet Project/football-transfermarkt-dataset-01/parquet/club_games.parquet')

st.title("Características da base de dados  🔍")
st.write("""
         Caracteristicas encontradas na base de dados.
""")

st.write("""
         <h4>O dataset possui 10 arquivos com registros de jogos de futebol ao redor do mundo</h4>
<p>Esses arquivos incluem eventos das partidas, resultados, escalações e desempenho dos jogadores.</p>
""", unsafe_allow_html=True)
# Load the parquet file into a DataFrame

# Get the number of rows and columns in the DataFrame
num_rows = df.shape[0]
num_cols = df.shape[1]

# Create a table to display the number of rows and columns
table = pd.DataFrame({'Number of Rows': [num_rows], 'Number of Columns': [num_cols]})

# Display the table
st.write("> Quantidade de linhas e colunas do arquivo dos eventos das partidas - Principais arquivo utilizado na analise")
st.table(table)

st.divider()

@st.cache_data
def  lista_parquet():
    diretorio = "DataSet Project/football-transfermarkt-dataset-01/parquet/"
    return [i for i in os.listdir(diretorio) if i.endswith('.parquet')]

@st.cache_data
def leitura_parquet(arquivo):
    return pd.read_parquet(arquivo)

@st.cache_data
def building_profile(caminho, arquivo):
    nome_dataframe = arquivo.split('.')[0]
    if nome_dataframe in st.session_state:
        return
    df = leitura_parquet(caminho)
    profile = ProfileReport(df, title=f"{arquivo} Dataset")
    if not os.path.exists("reports"):
        os.makedirs("reports")
    profile.to_file(f"reports/{nome_dataframe}.html")
    st.session_state[nome_dataframe] = df

def build_body():
    st.subheader("Selecione o dataset:")
    col1, col2 = st.columns([.3, .7])
    caminho = "DataSet Project/football-transfermarkt-dataset-01/parquet/"
    arquivo = col1.selectbox("\n", lista_parquet(), label_visibility='collapsed', key='dataset')
    caminho += arquivo
    botao_placeholder = col2.empty()
    if botao_placeholder.button('Analisar'):
        botao_placeholder.button('Processando...', disabled=True)
        building_profile(caminho, arquivo)
        mostrar_profile()

def mostrar_profile():
    nome_dataframe = st.session_state.dataset.split('.')[0]
    if nome_dataframe not in st.session_state:
        return
    st.write(f'Dataset: <i>{nome_dataframe}</i>', unsafe_allow_html=True)
    report_file = open(f'reports/{nome_dataframe}.html', 'r', encoding='utf-8')
    source_code = report_file.read()
    components.html(source_code, height=600, scrolling=True)


build_body()