import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt# parte gráfica
import seaborn as sns # parte gráfica
# from ydata_profiling import ProfileReport
# # import streamlit.components.v1 as components

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

def build_body():
    df = pd.read_parquet("DataSet Project\merge-data-by-clubs\merge-time-completo.parquet")
    caracteristicas(df)
    # função()
    pass



def caracteristicas(df):
    show = lambda x: st.write(x)
    show(df.head())
    st.write(df.shape)
    st.write(df.describe())
    st.write(df.dtypes)
    

def main():
    build_header()
    build_body()
    # mostrar_profile()
    #if st.checkbox("Dados a partir do merge"):
    #    st.subheader("Dados brutos")
    #    st.write(data)
if __name__ == "__main__":
    main()