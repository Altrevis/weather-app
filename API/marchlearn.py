# Importation des bibliothèques nécessaires
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import joblib
import os

# === Chargement des données ===
print("Chargement des données...")
# Chemin vers le fichier CSV contenant les données météo
file_path = 'data/communes.csv'

# Charger les données depuis le fichier CSV
data = pd.read_csv(file_path)

# Afficher les colonnes pour vérifier leur format
print("Colonnes du fichier CSV après chargement :")
print(data.columns.tolist())

# Renommer les colonnes pour correspondre aux noms utilisés dans le modèle
data.columns = ['Forecast timestamp', 'Position', 'Forecast base',
                '2 metre temperature', '2 metre relative humidity',
                'Total precipitation', '10m wind speed',
                'Surface solar radiation downwards', 'Commune']

# === Prétraitement des données ===
# Liste des colonnes numériques à convertir
numerical_features = [
    '2 metre temperature',
    '2 metre relative humidity',
    'Total precipitation',
    '10m wind speed',
    'Surface solar radiation downwards'
]

# Conversion des colonnes en type numérique (gestion des erreurs)
for col in numerical_features:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Suppression des lignes contenant des valeurs manquantes dans les colonnes numériques
data = data.dropna(subset=numerical_features)

# Vérification si les données sont vides après nettoyage
if data.empty:
    raise ValueError("Les données sont vides après nettoyage.")

# Afficher un aperçu des données après nettoyage
print("\nDonnées après suppression des valeurs manquantes :")
print(data.head())

# Encodage de la colonne 'Commune' (catégorielle → numérique)
data['Commune'] = data['Commune'].astype('category').cat.codes

# === Séparation des caractéristiques et de la cible ===
# Sélection des colonnes d'entrée (features) et de la cible (target)
X = data[['2 metre relative humidity', 'Total precipitation', '10m wind speed', 'Surface solar radiation downwards', 'Commune']]
y = data['2 metre temperature']  # La cible est la température réelle

# === Normalisation des données ===
# Initialisation du scaler pour normaliser les données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === Division des données en ensembles d'entraînement et de test ===
# Division des données en 80% pour l'entraînement et 20% pour le test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# === Entraînement du modèle ===
print("\nEntraînement du modèle...")
# Initialisation du modèle Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
# Entraînement du modèle sur les données d'entraînement
model.fit(X_train, y_train)

# === Évaluation du modèle ===
# Prédiction sur l'ensemble de test
y_pred = model.predict(X_test)

# Calcul de l'erreur quadratique moyenne (MSE)
mse = mean_squared_error(y_test, y_pred)
print(f"\nErreur quadratique moyenne (MSE) : {mse:.4f}")

# === Sauvegarde du modèle et du scaler ===
# Sauvegarde du modèle entraîné dans un fichier
joblib.dump(model, 'weather_model.pkl')
# Sauvegarde du scaler utilisé pour la normalisation
joblib.dump(scaler, 'scaler.pkl')

print("\nModèle et scaler sauvegardés sous weather_model.pkl et scaler.pkl")

# === Fonction locale pour faire une prédiction ===
# Fonction pour prédire la température à partir de nouvelles données
def predict_weather(new_data):
    # Normalisation des nouvelles données
    new_data_scaled = scaler.transform(new_data)
    # Prédiction de la température
    predicted_temperature = model.predict(new_data_scaled)
    return predicted_temperature

# === Exemple de prédiction ===
# Exemple d'utilisation du modèle pour prédire la température d'une ville
example_city = X.iloc[[0]]  # Prend un exemple de ville dans les données
predicted_temp = predict_weather(example_city)
print(f"\nExemple de prédiction pour une ville: {predicted_temp[0]:.2f}°C")