from flask import Flask, jsonify, request
import json
import uuid
import random

app = Flask(__name__)

# Classe pour générer des données météorologiques
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

# Classe pour générer un identifiant utilisateur
class UserID:
    def __init__(self):
        self.user_id = str(uuid.uuid4())

    def to_dict(self):
        return {
            'user_id': self.user_id
        }

# API pour générer des données météorologiques et un identifiant utilisateur
@app.route('/weather', methods=['GET'])
def get_weather_data():
    weather_data = WeatherData()
    user_id = UserID()
    data = {**weather_data.to_dict(), **user_id.to_dict()}
    return jsonify(data)

# API pour générer des données météorologiques par identifiant utilisateur
@app.route('/weather/<user_id>', methods=['GET'])
def get_weather_data_by_user_id(user_id):
    weather_data = WeatherData()
    data = {**weather_data.to_dict(), 'user_id': user_id}
    return jsonify(data)

# API pour mettre à jour des données météorologiques par identifiant utilisateur
@app.route('/weather/<user_id>', methods=['PUT'])
def update_weather_data(user_id):
    weather_data = WeatherData()
    data = {**weather_data.to_dict(), 'user_id': user_id}
    return jsonify(data)

# API pour supprimer des données météorologiques par identifiant utilisateur
@app.route('/weather/<user_id>', methods=['DELETE'])
def delete_weather_data(user_id):
    return jsonify({'message': 'Données météorologiques supprimées'})

# API pour créer un nouvel utilisateur
@app.route('/users', methods=['POST'])
def create_user():
    user_id = UserID()
    data = user_id.to_dict()
    return jsonify(data)

# API pour obtenir la liste des utilisateurs
@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for _ in range(10):
        user_id = UserID()
        users.append(user_id.to_dict())
    return jsonify(users)

# API pour obtenir les informations d'un utilisateur
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user_id = UserID()
    data = user_id.to_dict()
    return jsonify(data)

# API pour mettre à jour les informations d'un utilisateur
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_id = UserID()
    data = user_id.to_dict()
    return jsonify(data)

# API pour supprimer un utilisateur
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    return jsonify({'message': 'Utilisateur supprimé'})

if __name__ == '__main__':
    app.run(debug=True)