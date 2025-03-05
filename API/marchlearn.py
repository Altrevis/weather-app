import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Chemin vers ton fichier CSV
file_path = 'data/Longitude_Latitude_Ville.csv'

# Charger le fichier CSV dans un DataFrame
data = pd.read_csv(file_path)

# Afficher un aperçu des données
print("Aperçu des données :")
print(data.head())

# Convertir la colonne DateTime en format datetime
data['DateTime'] = pd.to_datetime(data['DateTime'])

# Gérer les valeurs manquantes (imputation par la moyenne ou suppression)
data.fillna(data.mean(), inplace=True)

# Exemple de normalisation (scaling) des données numériques
scaler = StandardScaler()
data[['Temperature', 'Humidity', 'WindSpeed', 'Sunshine']] = scaler.fit_transform(data[['Temperature', 'Humidity', 'WindSpeed', 'Sunshine']])

# Vérifier si des colonnes catégorielles existent (ex. City) et les encoder
data = pd.get_dummies(data, columns=['City'], drop_first=True)

print("Données après prétraitement :")
print(data.head())

# Séparer les données en Features (X) et Target (y)
X = data[['Latitude', 'Longitude', 'Humidity', 'WindSpeed', 'Sunshine'] + [col for col in data.columns if 'City' in col]]
y = data['Temperature']

# Séparer les données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Créer et entraîner le modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prédire sur les données de test
y_pred = model.predict(X_test)

# Évaluer le modèle
mse = mean_squared_error(y_test, y_pred)
print(f'\nErreur quadratique moyenne (MSE) : {mse}')

# Afficher les premières prédictions
print("\nQuelques prédictions:")
print(y_pred[:5])

# Sauvegarder le modèle pour réutilisation
joblib.dump(model, 'weather_model.pkl')

# Sauvegarder le scaler pour réutilisation
joblib.dump(scaler, 'scaler.pkl')

# Fonction pour prédire la température avec le modèle enregistré
def predict_weather(new_data):
    # Charger le modèle et le scaler
    model = joblib.load('weather_model.pkl')
    scaler = joblib.load('scaler.pkl')

    # Normaliser les nouvelles données
    new_data_scaled = scaler.transform(new_data[['Humidity', 'WindSpeed', 'Sunshine']])

    # Faire la prédiction
    predicted_temperature = model.predict(new_data_scaled)
    return predicted_temperature[0]

# Exemple d'utilisation pour prédire avec de nouvelles données
new_data = pd.DataFrame({
    'Latitude': [48.8566],
    'Longitude': [2.3522],
    'Humidity': [55],
    'WindSpeed': [12],
    'Sunshine': [80],
    'City_Lyon': [0],
    'City_Marseille': [1]  # Adapte en fonction de ton dataset
})

predicted_temperature = predict_weather(new_data)
print(f"\nTempérature prédite pour la nouvelle donnée : {predicted_temperature}°C")
