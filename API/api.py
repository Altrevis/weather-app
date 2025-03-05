from flask import Flask, jsonify, request, send_from_directory
import mysql.connector
import os

app = Flask(__name__)

# === Configuration de la base de données ===
db_config = {
    'host': '10.37.2.104',
    'user': 'ynov_user',
    'password': 'ynov2025',
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
@app.route('/weather/<city>', methods=['GET'])
@app.route('/weather/<city>/<day>', methods=['GET'])
@app.route('/weather/<city>/<day>/<month>', methods=['GET'])
@app.route('/weather/<city>/<day>/<month>/<year>', methods=['GET'])
def get_weather_data(city=None, day=None, month=None, year=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT c.Temperature, c.Sunshine, c.Humidity, c.WindSpeed, c.WeatherCondition,
           l.City, l.Department, l.Latitude, l.Longitude,
           t.HourTime, t.DateTime
    FROM Climate c
    JOIN Location l ON c.LocationID = l.ID
    JOIN Time t ON c.TimeID = t.ID
    """

    if city:
        query += " WHERE l.City LIKE %s OR l.Department LIKE %s"

    query += " ORDER BY t.DateTime DESC, t.HourTime DESC LIMIT 10;"

    if city:
        cursor.execute(query, (f'%{city}%', f'%{city}%'))
    else:
        cursor.execute(query)

    weather_data = cursor.fetchall()

    # Convertir les objets timedelta en chaînes de caractères
    for entry in weather_data:
        if isinstance(entry.get("HourTime"), (str, bytes)):  # Vérifier si c'est déjà une chaîne
            continue
        elif entry.get("HourTime") is not None:
            entry["HourTime"] = str(entry["HourTime"])  # Convertir timedelta en string
        

    cursor.close()
    conn.close()

    if city:
        route_message = city
        if day:
            route_message += f" : {day}"
            if month:
                route_message += f"/{month}"
                if year:
                    route_message += f"/{year}"
    else:
        route_message = "Route is empty"

    response = {
        "weather_data": weather_data,
        "route_message": route_message
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)