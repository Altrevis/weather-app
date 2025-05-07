import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import joblib
import os

print("Chargement des données...")
# Chemin vers le fichier CSV

file_path = 'data/output_unique_communes.csv'
# Charger les données
data = pd.read_csv(file_path)

# Afficher les colonnes pour vérifier leur format
print("Colonnes du fichier CSV après chargement :")
print(data.columns.tolist())

# Renommer les colonnes si nécessaire (pour correspondre à votre modèle)
data.columns = ['Forecast timestamp', 'Position', 'Forecast base',
                '2 metre temperature', '2 metre relative humidity',
                'Total precipitation', '10m wind speed',
                'Surface solar radiation downwards', 'Commune']

# Convertir en type numérique les colonnes nécessaires
numerical_features = [
    '2 metre temperature',
    '2 metre relative humidity',
    'Total precipitation',
    '10m wind speed',
    'Surface solar radiation downwards'
]

for col in numerical_features:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Supprimer les lignes avec des valeurs manquantes
data = data.dropna(subset=numerical_features)

if data.empty:
    raise ValueError("Les données sont vides après nettoyage.")

print("\nDonnées après suppression des valeurs manquantes :")
print(data.head())

# Encoder la commune (catégorielle → numérique)
data['Commune'] = data['Commune'].astype('category').cat.codes

# Features et cible
X = data[['2 metre relative humidity', 'Total precipitation', '10m wind speed', 'Surface solar radiation downwards', 'Commune']]
y = data['2 metre temperature']  # On veut prédire la température réelle

# Normaliser les données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Diviser les données
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Entraîner le modèle
print("\nEntraînement du modèle...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prédiction sur le jeu de test
y_pred = model.predict(X_test)

# Évaluation
mse = mean_squared_error(y_test, y_pred)
print(f"\nErreur quadratique moyenne (MSE) : {mse:.4f}")

# Sauvegarder le modèle et le scaler

joblib.dump(model, 'weather_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("\nModèle et scaler sauvegardés sous weather_model.pkl et scaler.pkl")

# Fonction locale pour faire une prédiction
def predict_weather(new_data):
    new_data_scaled = scaler.transform(new_data)
    predicted_temperature = model.predict(new_data_scaled)
    return predicted_temperature

# Exemple de prédiction
example_city = X.iloc[[0]]  # Prend un exemple de ville
predicted_temp = predict_weather(example_city)
print(f"\nExemple de prédiction pour une ville: {predicted_temp[0]:.2f}°C")