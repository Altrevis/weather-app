from flask import Flask, jsonify, request, send_from_directory
import mysql.connector
import os
import pandas as pd
import joblib
from datetime import datetime, timedelta

app = Flask(__name__)

# === Configuration de la base de données ===
db_config = {
    'host': 'localhost',
    'user': 'leo',
    'port': 3307,
    'password': 'leo',
    'database': 'meteo'
}

# === Connexion à la base de données ===
def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        raise

# Charger le modèle et le scaler
model = joblib.load('weather_model.pkl')
scaler = joblib.load('scaler.pkl')

# Fonction pour prédire la température
def predict_weather(new_data):
    # Normaliser les nouvelles données
    new_data_scaled = scaler.transform(new_data)
    # Faire la prédiction
    predicted_temperature = model.predict(new_data_scaled)
    return predicted_temperature

# === Routes Frontend ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/forecast.html')
def serve_forecast():
    return send_from_directory(BASE_DIR, 'forecast.html')

@app.route('/styles.css')
def serve_css():
    return send_from_directory(BASE_DIR, 'styles.css')

@app.route('/script.js')
def serve_script():
    return send_from_directory(BASE_DIR, 'script.js')

@app.route('/forecast.js')
def serve_forecast_script():
    return send_from_directory(BASE_DIR, 'forecast.js')

# === Routes API ===
@app.route('/weather', methods=['GET'])
@app.route('/weather/<city>', methods=['GET'])
@app.route('/weather/<city>/<day>', methods=['GET'])
@app.route('/weather/<city>/<day>/<month>', methods=['GET'])
@app.route('/weather/<city>/<day>/<month>/<year>', methods=['GET'])
def get_weather_data(city=None, day=None, month=None, year=None):
    try:
        # Подключение к базе данных
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Базовый SQL-запрос
        query = """
        SELECT `Forecast timestamp`, Position, `Forecast base`,
               `2 metre temperature`, `2 metre relative humidity`,
               `Total precipitation`, `10m wind speed`,
               `Surface solar radiation downwards`, Commune
        FROM WeatherData
        """

        # Фильтрация по городу
        filters = []
        params = []
        if city:
            filters.append("Commune LIKE %s")
            params.append(f'%{city}%')

        # Фильтрация по дате
        if day and month and year:
            filters.append("DATE(`Forecast timestamp`) = %s")
            params.append(f"{year}-{month.zfill(2)}-{day.zfill(2)}")
        elif day and month:
            filters.append("DATE_FORMAT(`Forecast timestamp`, '%Y-%m') = %s")
            params.append(f"{year or '2024'}-{month.zfill(2)}")
        elif day:
            filters.append("DAY(`Forecast timestamp`) = %s")
            params.append(day)

        # Добавление фильтров к запросу
        if filters:
            query += " WHERE " + " AND ".join(filters)

        # Сортировка и ограничение
        query += " ORDER BY `Forecast timestamp` DESC LIMIT 10;"

        # Выполнение запроса
        cursor.execute(query, params)
        weather_data = cursor.fetchall()

        # Преобразование datetime в строку (если необходимо)
        for entry in weather_data:
            if entry.get("Forecast timestamp"):
                entry["Forecast timestamp"] = str(entry["Forecast timestamp"])

        # Формирование сообщения о маршруте
        route_message = city or "Route is empty"
        if day:
            route_message += f" : {day}"
            if month:
                route_message += f"/{month}"
                if year:
                    route_message += f"/{year}"

        response = {
            "weather_data": weather_data,
            "route_message": route_message
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Une erreur est survenue: {str(e)}"}), 500

    finally:
        # Закрытие соединения
        cursor.close()
        conn.close()

# Route pour obtenir les prévisions météo pour les 3 prochains jours
@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    try:
        print(f"Requête reçue pour la ville : {city}")
        
        # Exemple de données d'entrée pour la prédiction
        start_date = datetime.now() + timedelta(days=1)  # Commence à partir de demain
        predictions = []
        for i in range(3):
            date = start_date + timedelta(days=i)
            # Exemple de données fictives pour la ville
            new_data = pd.DataFrame({
                'Minimum temperature at 2 metres': [10 + i],  # Exemple de données
                'Maximum temperature at 2 metres': [20 + i]  # Exemple de données
            })
            print(f"Préparation des données pour le jour {i + 1}: {new_data}")
            predicted_temperature = predict_weather(new_data)
            print(f"Prédiction pour le jour {i + 1}: {predicted_temperature[0]}")
            predictions.append({
                "date": date.strftime('%Y-%m-%d'),
                "temperature": round(predicted_temperature[0], 2)
            })

        # Retourner les prédictions sous forme de JSON
        print(f"Prédictions générées : {predictions}")
        return jsonify({
            "city": city,
            "predictions": predictions
        })

    except Exception as e:
        print(f"Erreur lors de la génération des prédictions : {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)