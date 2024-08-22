import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
@st.cache_data
def load_data():
    players = pd.read_parquet('DataSet Project/transfermarkrt-dados-clean/players.parquet')
    appearances = pd.read_parquet('DataSet Project/transfermarkrt-dados-clean/appearances.parquet')
    clubs = pd.read_parquet('DataSet Project/transfermarkrt-dados-clean/clubs.parquet')
    games = pd.read_parquet('DataSet Project/transfermarkrt-dados-clean/games.parquet')
    events = pd.read_parquet('DataSet Project/transfermarkrt-dados-clean/game_events.parquet')
    return players, appearances, clubs, games, events
# Carregar os dados
players, appearances, clubs, games, events = load_data()
# Remover valores NaN
appearances.dropna()
games.dropna()
events.dropna()
def rename_column(df, old_name, new_name):
    df = df.rename(columns={old_name: new_name})
    return df
players2 = rename_column(players, 'name', 'player_name')
def determine_result(row):
    if row['home_club_goals'] > row['away_club_goals']:
        return 'win'
    elif row['home_club_goals'] < row['away_club_goals']:
        return 'lose'
    else:
        return 'draw'
# Criar a coluna 'result' no DataFrame 'games'
games['result'] = games.apply(determine_result, axis=1)
# Merge dos DataFrames appearances e games
combined_df = pd.merge(appearances, games, on='game_id')
combined_df2 = pd.merge(combined_df, events, on='game_id')
# Pré-processamento dos dados
features = ['yellow_cards', 'red_cards', 'goals', 'assists', 'minutes_played', 'type', 'description']
X = combined_df2[features]
y = combined_df2['result']  # Variável alvo
# Converter colunas para valores numéricos
X = X.apply(pd.to_numeric, errors='coerce')
# Preencher valores NaN com zero
X = X.fillna(0)
# Balanceamento das classes
df = pd.concat([X, y], axis=1)
draw = df[df.result == 'draw'].sample(n=333, random_state=42)
lose = df[df.result == 'lose'].sample(n=333, random_state=42)
win = df[df.result == 'win'].sample(n=333, random_state=42)
# Combine as amostras selecionadas
df_balanced = pd.concat([win, draw, lose])
X = df_balanced[features]
y = df_balanced['result']
# Normalização dos dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
# Definir os modelos e parâmetros para GridSearchCV
models = {
    'Gradient Boosting': GradientBoostingClassifier(),
    'Random Forest': RandomForestClassifier(),
    'Support Vector Machine': SVC()
}
param_grids = {
    'Gradient Boosting': {
        'n_estimators': [100, 333],
        'learning_rate': [0.1, 0.05],
        'max_depth': [3, 5]
    },
    'Random Forest': {
        'n_estimators': [100, 333],
        'max_depth': [27],
        'min_samples_split': [2, 5]
    },
    'Support Vector Machine': {
        'C': [1, 10],
        'kernel': ['linear', 'rbf']
    }
}
# Treinar e avaliar os modelos
results = {}
for model_name, model in models.items():
    # Criar pipeline de pré-processamento e modelo
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', model)
    ])
    
    # Definir GridSearchCV com pipeline
    grid_search = GridSearchCV(estimator=pipeline, param_grid={'model__' + k: v for k, v in param_grids[model_name].items()}, cv=5, scoring='recall_macro', n_jobs=1)
    
    # Treinar o modelo
    grid_search.fit(X_train, y_train)
    
    # Melhor modelo
    best_model = grid_search.best_estimator_
    
    # Avaliação com cross-validation
    cv_scores = cross_val_score(best_model, X_train, y_train, cv=5, scoring='recall_macro')
    
    # Previsões no conjunto de teste
    y_pred = best_model.predict(X_test)
    
    # Armazenar resultados
    results[model_name] = {
        'Cross-Validation Recall Mean': cv_scores.mean(),
        'Accuracy': accuracy_score(y_test, y_pred),
        'Classification Report': classification_report(y_test, y_pred, output_dict=True)
    }

st.title("👨‍💻 Classificação dos Dados")
st.subheader("Resultados dos Modelos de Classificação")
for model_name, result in results.items():
    col1, col2 = st.columns([4, 4])

    with col1:
        st.subheader(model_name)
        st.metric(label="Recall Médio (Validação Cruzada)", value=f"{result['Cross-Validation Recall Mean']:.2f}")
        st.metric(label="Acurácia", value=f"{result['Accuracy']:.2f}")

    with col2:
        st.subheader('Relatório de Classificação')
        report_df = pd.DataFrame(result['Classification Report']).transpose()
        st.table(report_df)

# Preparar dados para o gráfico de barras horizontais
recalls = [result['Cross-Validation Recall Mean'] for result in results.values()]
accuracies = [result['Accuracy'] for result in results.values()]
model_names = list(results.keys())

# Criar DataFrame para o gráfico
df_chart = pd.DataFrame({
    'Modelo': model_names,
    'Recall Médio': recalls,
    'Acurácia': accuracies
})

# Gráfico de barras horizontais para Recall Médio
fig_recall = px.bar(df_chart, x='Recall Médio', y='Modelo', orientation='h', title='Comparação de Recall Médio', color='Modelo')
fig_recall.update_layout(
    xaxis_title='Recall Médio',
    yaxis_title='Modelo',
    title_font=dict(size=20, family='Arial, sans-serif', color='white'),
    xaxis=dict(title_font=dict(size=16, family='Arial, sans-serif', color='white')),
    yaxis=dict(title_font=dict(size=16, family='Arial, sans-serif', color='white')),
    legend_title=dict(font=dict(size=14, family='Arial, sans-serif', color='white'))
)

# Gráfico de barras horizontais para Acurácia
fig_accuracy = px.bar(df_chart, x='Acurácia', y='Modelo', orientation='h', title='Comparação de Acurácia', color='Modelo')
fig_accuracy.update_layout(
    xaxis_title='Acurácia',
    yaxis_title='Modelo',
    title_font=dict(size=20, family='Arial, sans-serif', color='white'),
    xaxis=dict(title_font=dict(size=16, family='Arial, sans-serif', color='white')),
    yaxis=dict(title_font=dict(size=16, family='Arial, sans-serif', color='white')),
    legend_title=dict(font=dict(size=14, family='Arial, sans-serif', color='white'))
)

# Exibir gráficos no Streamlit
st.subheader('Comparação de Métricas')
st.plotly_chart(fig_recall, use_container_width=True)
st.plotly_chart(fig_accuracy, use_container_width=True)