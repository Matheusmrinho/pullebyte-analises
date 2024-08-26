import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Carregar os resultados do arquivo pickle
with open('model_results.pkl', 'rb') as f:
    results = pickle.load(f)

# Título e subtítulo
st.title("👨‍💻 Classificação dos Dados")
st.subheader("Resultados dos Modelos de Classificação")

# Iterar sobre os resultados para exibir as métricas, o relatório de classificação, e a matriz de confusão
for model_name, result in results.items():
    col1, col2 = st.columns([4, 4])

    with col1:
        st.subheader(model_name)
        report_df = pd.DataFrame(result['Test Report']).transpose()
        
        # Fazer o recall_value e precision_value com valores reais, sem N/A
        recall_value = report_df.loc['weighted avg', 'recall'] * 100
        precision_value = report_df.loc['weighted avg', 'precision'] * 100
        
        st.metric(label="Recall Médio (Validação Cruzada)", value=f"{recall_value:.1f}%")
        st.metric(label="Precisão", value=f"{precision_value:.1f}%", delta=True)

    with col2:
        st.subheader('Relatório de Classificação')
        st.table(report_df)

# Preparar dados para o gráfico de barras horizontais
recalls = [result['Test Report'].get('weighted avg', {}).get('recall', 0) * 100 for result in results.values()]
precisions = [result['Test Report'].get('weighted avg', {}).get('precision', 0) * 100 for result in results.values()]
model_names = list(results.keys())

# Criar DataFrame para o gráfico
df_chart = pd.DataFrame({
    'Modelo': model_names,
    'Recall Médio (%)': recalls,
    'Precisão (%)': precisions
})

# Gráfico de barras horizontais para Recall Médio
fig_recall = px.bar(df_chart, x='Recall Médio (%)', y='Modelo', orientation='h', title='Comparação de Recall Médio', color='Modelo')
fig_recall.update_layout(
    xaxis_title='Recall Médio (%)',
    yaxis_title='Modelo',
    title_font=dict(size=20, family='Arial, sans-serif', color='white'),
    xaxis=dict(title_font=dict(size=16, family='Arial, sans-serif', color='white')),
    yaxis=dict(title_font=dict(size=16, family='Arial, sans-serif', color='white')),
    legend_title=dict(font=dict(size=14, family='Arial, sans-serif', color='white'))
)

# Gráfico de barras horizontais para Precisão
fig_precision = px.bar(df_chart, x='Precisão (%)', y='Modelo', orientation='h', title='Comparação de Precisão', color='Modelo')
fig_precision.update_layout(
    xaxis_title='Precisão (%)',
    yaxis_title='Modelo',
    title_font=dict(size=20, family='Arial, sans-serif', color='white'),
    xaxis=dict(title_font=dict(size=16, family='Arial, sans-serif', color='white')),
    yaxis=dict(title_font=dict(size=16, family='Arial, sans-serif', color='white')),
    legend_title=dict(font=dict(size=14, family='Arial, sans-serif', color='white'))
)

# Exibir gráficos no Streamlit
st.subheader('Comparação de Métricas')
st.plotly_chart(fig_recall, use_container_width=True)
st.plotly_chart(fig_precision, use_container_width=True)

if 'Confusion Matrix' in result:
    st.subheader(f"Matriz de Confusão - {model_name}")
    cm = result['Confusion Matrix']
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    fig, ax = plt.subplots(figsize=(8, 6))
    disp.plot(ax=ax, cmap='Blues', values_format='d')
    plt.title(f'Matriz de Confusão - {model_name}')
    st.pyplot(fig)

