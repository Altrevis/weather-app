from flask import Flask, jsonify, request, send_from_directory
import mysql.connector
import os

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

if __name__ == '__main__':
    app.run(debug=True)