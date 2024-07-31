import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt# parte gráfica
import seaborn as sns # parte gráfica
import plotly.express as px

def header():
    st.title("Características da base de dados 🔍")
    text = ''' <p> Caracteristicas encontradas na base de dados.'''
    st.markdown(text,unsafe_allow_html=True)

def build_body():
    df = pd.read_parquet("DataSet Project\merge-data-by-clubs\merge-time-completo.parquet")
    n_rows , n_columns = df.shape
    text = f'''<h2> O dataset possui {n_rows} linhas e {n_columns} colunas </h2>'''
    st.markdown(text,unsafe_allow_html=True)
    data_types(df)
    summary(df)

def data_types(df):
    st.subheader("Tipos de dados das colunas do dataset:")
    elemento_1 , elemento_2 = st.tabs(['Gráfico',"Tabela"])
    dataset_tipos = df.dtypes.value_counts()

    with elemento_1:
        plt.figure(figsize=(12,4))
 
        dataset_tipos.plot(kind='bar',color='#66c3a4')
        # plt.
        plt.title("Distribuição dos tipos de dados")
        plt.xlabel("Tipos de dados")
        plt.ylabel("Ocorrência")
        st.pyplot(plt)# gráfico numero 1

    with elemento_2:
        total = dataset_tipos.sum()
        df_tipos = pd.DataFrame({
            'Numero de colunas com esse tipo' : dataset_tipos.values,
            'Porcentagem' : (dataset_tipos/total) * 100 
        })
        df_tipos['Porcentagem'] = df_tipos['Porcentagem'].map('{:.2f}'.format)# duas casas decimais para não ficar feio :))
        text = f'''<h4> Neste Dataset existem {dataset_tipos.count()} tipos de dados, que estão distribuidos desta maneira:</h4>'''
        st.markdown(text,unsafe_allow_html=True)
        st.table(df_tipos)

def summary(df):
    st.subheader("Resumo das colunas:")
    dataset_info = df.describe()
    col1 , col2 = st.columns([.3,.7])
    lista_info = [i for i in dataset_info.columns]
    escolha_status = col1.selectbox("\n",lista_info,label_visibility='collapsed',key="status")
    botao_placeholder = col2.empty()
    elemento_1 , elemento_2 = st.tabs(['Gráfico',"Tabela"])
    if botao_placeholder.button('Analisar'):
        with elemento_1:
            st.table(dataset_info[escolha_status])
            IQR = (dataset_info[escolha_status]['75%']) - (dataset_info[escolha_status]['25%'])
            print(IQR)
        with elemento_2:
            st.dataframe(df[escolha_status].head(10), width=1000)
    
    

def main():
    header()
    build_body()

main()
