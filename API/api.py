from flask import Flask, jsonify, request, send_from_directory
import os
import random

app = Flask(__name__)

# === Configuration des fichiers statiques ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# === Classes ===

class WeatherData:
    def __init__(self):
        self.temperature = random.randint(10, 30)
        self.humidity = random.randint(40, 80)
        self.wind_speed = random.randint(5, 20)

    def to_dict(self):
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'wind_speed': self.wind_speed
        }

# === Routes Frontend ===

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
    weather_data = WeatherData()
    return jsonify(weather_data.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
