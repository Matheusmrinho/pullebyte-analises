import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from imblearn.under_sampling import RandomUnderSampler
import pickle


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


definir_resultado = lambda home_goals, away_goals: 1 if home_goals > away_goals else (-1 if home_goals < away_goals else 0)
df['target'] = df.apply(lambda x: definir_resultado(x['home_club_goals'], x['away_club_goals']), axis=1)


features = ['media_gols_minuto', 'media_faltas_jogo', 'assists', 'home_club_formation', 'away_club_formation']
X = df[features]
y = df['target']



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


numeric_features = X_train.select_dtypes(include=['number']).columns.tolist()
non_numeric_features = X_train.select_dtypes(exclude=['number']).columns.tolist()


numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, non_numeric_features)
    ])

preprocessing_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor)
])


X_train_preprocessed = preprocessing_pipeline.fit_transform(X_train)
X_test_preprocessed = preprocessing_pipeline.transform(X_test)


undersampler = RandomUnderSampler(random_state=42)
X_train_resampled, y_train_resampled = undersampler.fit_resample(X_train_preprocessed, y_train)


models = {
    'Gradient Boosting': GradientBoostingClassifier(),
    'Random Forest': RandomForestClassifier(),
    'Support Vector Machine': SVC(probability=True)
}

results = {}
for model_name, model in models.items():
    model.fit(X_train_resampled, y_train_resampled)
    
    
    y_train_pred = model.predict(X_train_resampled)
    train_report = classification_report(y_train_resampled, y_train_pred, output_dict=True)
    
    
    y_test_pred = model.predict(X_test_preprocessed)
    test_report = classification_report(y_test, y_test_pred, output_dict=True)
    
    
    conf_matrix = confusion_matrix(y_test, y_test_pred)
    
    
    results[model_name] = {
    'model': model,  # Certifique-se de que o modelo está sendo armazenado
    'Train Report': train_report,
    'Test Report': test_report,
    'Confusion Matrix': conf_matrix
}

# Salvando os resultados para uso posterior no Streamlit
with open('model_results.pkl', 'wb') as f:
    pickle.dump(results, f)

print("Model training complete. Results saved in 'model_results.pkl'.")
print(results[model_name]['Test Report'].keys())
