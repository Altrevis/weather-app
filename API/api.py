# Importation des bibliothèques nécessaires
from flask import Flask, jsonify, request, send_from_directory
import mysql.connector
import os
import pandas as pd
import joblib
from datetime import datetime, timedelta

# Initialisation de l'application Flask
app = Flask(__name__)

# === Configuration de la base de données ===
# Informations de connexion à la base de données MySQL
db_config = {
    'host': 'localhost',
    'user': 'xxx',  # Remplacer par l'utilisateur de la base de données
    'port': 3306,   # Port MySQL
    'password': 'xxx',  # Remplacer par le mot de passe de la base de données
    'database': 'meteo'  # Nom de la base de données
}

# === Connexion à la base de données ===
# Fonction pour établir une connexion à la base de données
def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        raise

# Chargement du modèle de prédiction et du scaler pour la normalisation des données
model = joblib.load('weather_model.pkl')  # Modèle de prédiction
scaler = joblib.load('scaler.pkl')        # Scaler pour normaliser les données

# === Fonction de prédiction météo ===
# Fonction pour prédire la température en utilisant le modèle
def predict_weather(new_data):
    # Normaliser les nouvelles données
    new_data_scaled = scaler.transform(new_data)
    # Faire la prédiction
    predicted_temperature = model.predict(new_data_scaled)
    return predicted_temperature

# === Routes pour le frontend ===
# Définition du répertoire de base pour servir les fichiers statiques
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Route pour servir la page d'accueil
@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

# Route pour servir la page des prévisions météo
@app.route('/forecast.html')
def serve_forecast():
    return send_from_directory(BASE_DIR, 'forecast.html')

# Route pour servir le fichier CSS
@app.route('/styles.css')
def serve_css():
    return send_from_directory(BASE_DIR, 'styles.css')

# Route pour servir le fichier JavaScript principal
@app.route('/script.js')
def serve_js():
    return send_from_directory(BASE_DIR, 'script.js')

# Route pour servir le fichier JavaScript des prévisions
@app.route('/forecast.js')
def serve_forecast_script():
    return send_from_directory(BASE_DIR, 'forecast.js')

# === Routes pour l'API ===

# Route pour récupérer les données météo avec des filtres optionnels (ville, date)
@app.route('/weather', methods=['GET'])
@app.route('/weather/<city>', methods=['GET'])
@app.route('/weather/<city>/<day>', methods=['GET'])
@app.route('/weather/<city>/<day>/<month>', methods=['GET'])
@app.route('/weather/<city>/<day>/<month>/<year>', methods=['GET'])
def get_weather_data(city=None, day=None, month=None, year=None):
    try:
        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Requête SQL de base
        query = """
        SELECT `Forecast timestamp`, Position, `Forecast base`,
               `2 metre temperature`, `2 metre relative humidity`,
               `Total precipitation`, `10m wind speed`,
               `Surface solar radiation downwards`, Commune
        FROM WeatherData
        """

        # Ajout de filtres dynamiques en fonction des paramètres
        filters = []
        params = []
        if city:
            filters.append("Commune LIKE %s")
            params.append(f'%{city}%')

        if day and month and year:
            filters.append("DATE(`Forecast timestamp`) = %s")
            params.append(f"{year}-{month.zfill(2)}-{day.zfill(2)}")
        elif day and month:
            filters.append("DATE_FORMAT(`Forecast timestamp`, '%Y-%m') = %s")
            params.append(f"{year or '2024'}-{month.zfill(2)}")
        elif day:
            filters.append("DAY(`Forecast timestamp`) = %s")
            params.append(day)

        # Ajout des filtres à la requête SQL
        if filters:
            query += " WHERE " + " AND ".join(filters)

        # Ajout d'un tri et d'une limite
        query += " ORDER BY `Forecast timestamp` DESC LIMIT 10;"

        # Exécution de la requête
        cursor.execute(query, params)
        weather_data = cursor.fetchall()

        # Conversion des timestamps en chaînes de caractères
        for entry in weather_data:
            if entry.get("Forecast timestamp"):
                entry["Forecast timestamp"] = str(entry["Forecast timestamp"])

        # Création d'un message décrivant la route utilisée
        route_message = city or "Route is empty"
        if day:
            route_message += f" : {day}"
            if month:
                route_message += f"/{month}"
                if year:
                    route_message += f"/{year}"

        # Construction de la réponse JSON
        response = {
            "weather_data": weather_data,
            "route_message": route_message
        }

        return jsonify(response)

    except Exception as e:
        # Gestion des erreurs
        return jsonify({"error": f"Une erreur est survenue: {str(e)}"}), 500

    finally:
        # Fermeture de la connexion à la base de données
        cursor.close()
        conn.close()

# Route pour obtenir les prévisions météo pour les 3 prochains jours
@app.route('/forecast/<city>', methods=['GET'])
def get_forecast(city):
    try:
        print(f"Requête reçue pour la ville : {city}")
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Requête SQL pour récupérer les données les plus récentes pour une ville
        query = """
            SELECT 
                `2 metre relative humidity`,
                `Total precipitation`,
                `10m wind speed`,
                `Surface solar radiation downwards`,
                Commune
            FROM WeatherData
            WHERE Commune LIKE %s
            ORDER BY `Forecast timestamp` DESC
            LIMIT 1
        """
        cursor.execute(query, (f"%{city}%",))
        result = cursor.fetchone()

        if not result:
            # Si aucune donnée n'est trouvée pour la ville
            return jsonify({"error": "Aucune donnée disponible pour cette ville"}), 404

        # Préparation des données d'entrée pour le modèle
        new_data = pd.DataFrame({
            '2 metre relative humidity': [float(result['2 metre relative humidity'])],
            'Total precipitation': [float(result['Total precipitation'])],
            '10m wind speed': [float(result['10m wind speed'])],
            'Surface solar radiation downwards': [float(result['Surface solar radiation downwards'])],
            'Commune': [hash(result['Commune']) % 100000]  # Encodage simple
        })

        # Date de début pour les prévisions
        start_date = datetime.now() + timedelta(days=1)
        predictions = []

        # Génération des prévisions pour les 3 prochains jours
        for i in range(3):
            date = start_date + timedelta(days=i)

            # Modification des données pour chaque jour
            daily_data = new_data.copy()
            daily_data['2 metre relative humidity'] *= (1 + i * 0.01)
            daily_data['Total precipitation'] += i * 0.1
            daily_data['10m wind speed'] += i * 0.5
            daily_data['Surface solar radiation downwards'] -= i * 500

            # Prédiction de la température
            predicted_temperature = predict_weather(daily_data)
            predictions.append({
                "date": date.strftime('%Y-%m-%d'),
                "temperature": round(predicted_temperature[0], 2)
            })

        # Retour des prévisions sous forme de réponse JSON
        return jsonify({
            "city": city,
            "predictions": predictions
        })

    except Exception as e:
        # Gestion des erreurs
        print(f"Erreur lors de la génération des prédictions : {e}")
        return jsonify({"error": str(e)}), 500

# Point d'entrée principal de l'application
if __name__ == '__main__':
    app.run(debug=True)