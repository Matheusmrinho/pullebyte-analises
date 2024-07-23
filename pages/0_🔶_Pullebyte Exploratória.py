import streamlit as st
import pandas as pd

def build_header():
    text ='''<h1>Análise Exploratória</h1>
    <p>Este streamlit tem como objetivo realizar a análise exploratória dos dados contidos nos datasets de futebol.
    Foram utilizados as seguintes bases de dados:</p>
    <ol>
        <li><a href="https://www.kaggle.com/datasets/davidcariboo/player-scores?select=game_lineups.csv">Football Data from Transfermarkt</a></li>
        <li><a href="https://www.kaggle.com/datasets/azminetoushikwasi/ucl-202122-uefa-champions-league">UCL | Matches & Players Data</a></li>
    </ol>
    <br>
    '''
    st.markdown(text, unsafe_allow_html=True)

def load_data():
    data = pd.read_parquet("DataSet Project\DataSets Parquet\merge_keyStates_clubs.parquet.parquet")
    return data

def build_body():
    data = load_data()
    st.write(data)

def main():
    build_header()
    build_body()

if __name__ == "__main__":
    main()