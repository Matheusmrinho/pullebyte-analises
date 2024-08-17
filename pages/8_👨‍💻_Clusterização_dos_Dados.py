import streamlit as st
import pandas as pd

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
    st.write("Conjunto de dados utilizados na clusterização:")
    st.dataframe(cluster_data)
    st.dataframe(apereence)
    
cluster_data = load_data(r"DataSet Project/transfermarkrt-dados-clean/merged_data/merge_club_games_events_dummy.parquet")
        
apereence = load_data(r"DataSet Project/transfermarkrt-dados-clean/appearances.parquet")
if __name__ == "__main__":
    main()