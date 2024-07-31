import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import os
import streamlit.components.v1 as components

def build_header():
    text ='''<h1>Análise Exploratória</h1>
    <p>Este streamlit tem como objetivo realizar a análise exploratória dos dados contidos nos datasets de futebol.
    Foram utilizados as seguintes bases de dados:</p>
    <ol>
        <li><a href="https://www.kaggle.com/datasets/davidcariboo/player-scores?select=game_lineups.csv">Football Data from Transfermarkt</a></li>
        <li><a href="https://www.kaggle.com/datasets/azminetoushikwasi/ucl-202122-uefa-champions-league">UCL | Matches & Players Data</a></li>
    </ol>
    '''
    st.markdown(text, unsafe_allow_html=True)

# def load_data():
#     data = pd.read_parquet("DataSet Project\DataSets Parquet\merge_keyStates_clubs.parquet.parquet")
#     return data

def  lista_parquet():
    diretorio = "DataSet Project/ucl-matches-dataset-02/parquet/"
    return [i for i in os.listdir(diretorio) if i.endswith('.parquet')]

def leitura_parquet(arquivo):
    return pd.read_parquet(arquivo)

def building_profile(caminho,arquivo):
    nome_dataframe = st.session_state.dataset
    if nome_dataframe in st.session_state:
        return
    df = leitura_parquet(caminho)
    profile = ProfileReport(df,title=f"{arquivo} Dataset")
    profile.to_file(f"reports/{nome_dataframe}.html")
    st.session_state[arquivo] = df
    # st.write(profile.to_file)
    # st.write(st.session_state[arquivo])

def build_body():
    # data = load_data()
    st.subheader("Selecione o dataset:")
    col1, col2 = st.columns([.3,.7])
    caminho = "DataSet Project/ucl-matches-dataset-02/parquet/"
    arquivo = col1.selectbox("\n",lista_parquet(),label_visibility='collapsed',key='dataset')
    caminho += arquivo
    botao_placeholder = col2.empty()
    if botao_placeholder.button('Analisar'):
        botao_placeholder.button('Processando...',disabled=True)
        building_profile(caminho,arquivo)
        mostrar_profile()
        st.experimental_rerun()


def mostrar_profile():
    nome_dataframe = st.session_state.dataset
    if nome_dataframe not in st.session_state:
        return
    st.write(f'Dataset: <i>{nome_dataframe}</i>', unsafe_allow_html=True)
    report_file = open(f'reports/{nome_dataframe}.html', 'r', encoding='utf-8')
    source_code = report_file.read() 
    components.html(source_code, height=400, scrolling=True)



def main():
    build_header()
    build_body()
    mostrar_profile()
    #if st.checkbox("Dados a partir do merge"):
    #    st.subheader("Dados brutos")
    #    st.write(data)
if __name__ == "__main__":
    main()