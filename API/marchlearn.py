import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Chemin vers le fichier CSV contenant les données météo
file_path = 'data/meteo-0025.csv'

# Charger le fichier CSV dans un DataFrame avec le bon séparateur
data = pd.read_csv(file_path, sep=',')

# Renommer les colonnes si nécessaire
data.columns = ['Position', '2 metre temperature', 'Minimum temperature at 2 metres',
                'Maximum temperature at 2 metres', 'Commune']

# Convertir les colonnes nécessaires en type numérique
numerical_features = ['Minimum temperature at 2 metres', 'Maximum temperature at 2 metres']
for col in numerical_features:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Supprimer les lignes avec des valeurs manquantes
data = data.dropna(subset=numerical_features)

if data.empty:
    raise ValueError("Les données sont vides après le filtrage.")

# Ajouter la commune comme variable catégorielle (si vous voulez que modèle sache d'où взяты данные)
data['Commune'] = data['Commune'].astype('category').cat.codes  # Encoder les villes

# Features et cible
X = data[['Minimum temperature at 2 metres', 'Maximum temperature at 2 metres', 'Commune']]
y = data['Maximum temperature at 2 metres']

# Normaliser les données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Diviser les données
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Entraîner le modèle
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Sauvegarder le modèle et le scaler
joblib.dump(model, 'weather_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Modèle entraîné et sauvegardé.")