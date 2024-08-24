import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay, confusion_matrix
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from imblearn.under_sampling import RandomUnderSampler
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

players = pd.read_parquet('DataSet Project/transfermarkrt-dados-clean/players.parquet')
appearances = pd.read_parquet('DataSet Project/transfermarkrt-dados-clean/appearances.parquet')
clubs = pd.read_parquet('DataSet Project/transfermarkrt-dados-clean/clubs.parquet')
games = pd.read_parquet('DataSet Project/transfermarkrt-dados-clean/games.parquet')
events = pd.read_parquet('DataSet Project/transfermarkrt-dados-clean/game_events.parquet')
df1 = pd.merge(games, appearances, on='game_id', how='left')

df_gol_minuto = appearances.groupby('player_id')[['goals', 'minutes_played']].sum().reset_index()
df_gol_minuto['media_gols_minuto'] = df_gol_minuto['goals'] / df_gol_minuto['minutes_played']
df = pd.merge(df1, df_gol_minuto, on='player_id', how='left')

appearances['faltas'] = appearances['yellow_cards'] + appearances['red_cards']
df_faltas_jogo = appearances.groupby(['player_id', 'game_id'])[['faltas', 'minutes_played']].sum().reset_index()
df_faltas_jogo['media_faltas_jogo'] = df_faltas_jogo['faltas'] / df_faltas_jogo['minutes_played']
df = pd.merge(df, df_faltas_jogo, on=['player_id', 'game_id'], how='left')
print(df.columns)

# Cálculo da target (substitua 'home_team_goals' e 'away_team_goals' pelas colunas corretas)
def definir_resultado(home_goals, away_goals):
    if home_goals > away_goals:
        return 1  # Vitória
    elif home_goals < away_goals:
        return -1  # Derrota
    else:
        return 0  # Empate

# Correcting column names to match the merged DataFrame
# Check the column names in your 'df' DataFrame and replace
# 'home_team_goals_correct' and 'away_team_goals_correct' with the actual names
df['target'] = df.apply(lambda x: definir_resultado(x['home_club_goals'], x['away_club_goals']), axis=1)

# Selecionando as features (ajuste conforme suas necessidades)
features = ['media_gols_minuto', 'media_faltas_jogo','assists','home_club_formation','away_club_formation']

# Dividindo os dados em treino e teste
X = df[features]
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Identify numeric and non-numeric features
numeric_features = X_train.select_dtypes(include=['number']).columns.tolist()
non_numeric_features = X_train.select_dtypes(exclude=['number']).columns.tolist()

# Create transformers for numeric and non-numeric features
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')), # Use most frequent for categorical
    ('onehot', OneHotEncoder(handle_unknown='ignore')) # Handle unknown categories
])

# Combine transformers using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, non_numeric_features)
    ])
preprocessing_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor)
])
X_train_preprocessed = preprocessing_pipeline.fit_transform(X_train)
undersampler = RandomUnderSampler(random_state=42)
X_train_resampled, y_train_resampled = undersampler.fit_resample(X_train_preprocessed, y_train)

models = {
    'Gradient Boosting': GradientBoostingClassifier(),
    'Random Forest': RandomForestClassifier(),
    'Support Vector Machine': SVC()
}
for model_name, model in models.items():
    print(f"Evaluating {model_name}...")
    model.fit(X_train_resampled, y_train_resampled)

    # Evaluate on Training Data (Resampled)
    y_train_pred = model.predict(X_train_resampled)
    print("Training Results (Resampled Data):\n")
    print(classification_report(y_train_resampled, y_train_pred))

    # Preprocess the test data
    X_test_preprocessed = preprocessing_pipeline.transform(X_test)

    # Make predictions on the test data
    y_pred = model.predict(X_test_preprocessed)
    print("\nTest Results:\n")
    print(classification_report(y_test, y_pred))
    print("-" * 40)