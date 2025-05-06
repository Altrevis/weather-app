import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

# Chemin vers le fichier CSV contenant les données météo
file_path = 'data/meteo-0025.csv'

# Charger le fichier CSV dans un DataFrame avec le bon séparateur
data = pd.read_csv(file_path, sep=',')  # Changez sep=',' si nécessaire

# Afficher les colonnes pour vérifier leur format
print("Colonnes du fichier CSV après chargement :")
print(data.columns)

# Renommer les colonnes si elles ne correspondent pas aux attentes
data.columns = ['Position', '2 metre temperature', 'Minimum temperature at 2 metres',
                'Maximum temperature at 2 metres', 'Commune']

# Convertir les colonnes nécessaires en type numérique (ignorer '2 metre temperature')
numerical_features = ['Minimum temperature at 2 metres', 'Maximum temperature at 2 metres']
for col in numerical_features:
    data[col] = pd.to_numeric(data[col], errors='coerce')  # Convertir en numérique, remplacer les erreurs par NaN

# Supprimer les lignes avec des valeurs manquantes
data = data.dropna(subset=numerical_features)

# Vérifier les données après suppression des valeurs manquantes
if data.empty:
    raise ValueError("Les données sont vides après le filtrage. Vérifiez le fichier CSV ou les étapes de nettoyage.")

print("\nDonnées après suppression des valeurs manquantes :")
print(data)

# Réduire la taille des données pour l'entraînement
data = data.sample(n=10000, random_state=42)  # Échantillon de 10 000 lignes

# Séparer les données en Features (X) et Target (y)
X = data[['Minimum temperature at 2 metres', 'Maximum temperature at 2 metres']]
y = data['Maximum temperature at 2 metres']  # Utiliser 'Maximum temperature at 2 metres' comme cible

# Vérifier les données avant la normalisation
print("\nFeatures (X) avant normalisation :")
print(X)

# Normaliser les données
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Séparer les données en ensemble d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Créer et entraîner le modèle
model = RandomForestRegressor(n_estimators=20, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Prédire sur les données de test
y_pred = model.predict(X_test)

# Évaluer le modèle
mse = mean_squared_error(y_test, y_pred)
print(f'\nErreur quadratique moyenne (MSE) : {mse}')

# Afficher les premières prédictions
print("\nQuelques prédictions:")
print(y_pred[:5])

# Sauvegarder le modèle et le scaler pour réutilisation
joblib.dump(model, 'weather_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Fonction pour prédire la température avec le modèle enregistré
def predict_weather(new_data):
    # Charger le modèle et le scaler
    model = joblib.load('weather_model.pkl')
    scaler = joblib.load('scaler.pkl')

    # Normaliser les nouvelles données
    new_data_scaled = scaler.transform(new_data)

    # Faire la prédiction
    predicted_temperature = model.predict(new_data_scaled)
    return predicted_temperature

# Générer des prédictions pour les 3 prochains jours
start_date = datetime(2025, 4, 25)  # Date de départ (demain)
predictions = []
for i in range(3):
    date = start_date + timedelta(days=i)
    new_data = pd.DataFrame({
        'Minimum temperature at 2 metres': [10 + i],  # Exemple de données
        'Maximum temperature at 2 metres': [20 + i]  # Exemple de données
    })
    predicted_temperature = predict_weather(new_data)
    predictions.append((date.strftime('%Y-%m-%d'), predicted_temperature[0]))

# Afficher les prédictions avec les dates
print("\nPrédictions pour les 3 prochains jours :")
for date, temp in predictions:
    print(f"Date : {date}, Température prédite : {temp:.2f}°C")
