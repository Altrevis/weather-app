from flask import Flask, jsonify, request, send_from_directory
import mysql.connector
import os

app = Flask(__name__)

# === Configuration de la base de données ===
db_config = {
    'host': '10.37.4.104',
    'user': 'ynov_user',
    'password': 'ynov2024',
    'database': 'meteo'
}

# === Connexion à la base de données ===
def get_db_connection():
    return mysql.connector.connect(**db_config)

# === Routes Frontend ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/styles.css')
def serve_css():
    return send_from_directory(BASE_DIR, 'styles.css')

@app.route('/script.js')
def serve_js():
    return send_from_directory(BASE_DIR, 'script.js')

# === Routes API ===

@app.route('/weather', methods=['GET'])
def get_weather_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT c.Temperature, c.Sunshine, c.Humidity, c.WindSpeed, c.WeatherCondition,
           l.City, l.Department, l.Latitude, l.Longitude,
           t.HourTime, t.DateTime
    FROM Climate c
    JOIN Location l ON c.LocationID = l.ID
    JOIN Time t ON c.TimeID = t.ID
    ORDER BY t.DateTime DESC, t.HourTime DESC
    LIMIT 10;
    """

    cursor.execute(query)
    weather_data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)
