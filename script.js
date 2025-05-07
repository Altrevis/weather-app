// script.js

// === Script principal pour gérer les interactions avec l'API météo ===

// Fonction pour récupérer les données météo générales
function getWeatherData() {
  // Effectuer une requête GET vers l'API météo
  fetch('/weather')
    .then(response => {
      if (!response.ok) {
        // Si la réponse HTTP n'est pas correcte, lever une erreur
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      return response.json(); // Convertir la réponse en JSON
    })
    .then(data => {
      // Afficher les données météo dans l'élément HTML avec l'ID 'weatherData'
      document.getElementById('weatherData').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
      // Gestion des erreurs lors de la récupération des données
      console.error('Erreur:', error);
      document.getElementById('weatherData').innerText = 'Erreur lors de la récupération des données.';
    });
}

// Fonction pour créer un nouvel utilisateur (si nécessaire)
function createUser() {
  // Effectuer une requête POST vers l'API pour créer un utilisateur
  fetch('/users', { method: 'POST' })
    .then(response => response.json()) // Convertir la réponse en JSON
    .then(data => {
      // Afficher les informations du nouvel utilisateur dans l'élément HTML avec l'ID 'newUser'
      document.getElementById('newUser').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error('Erreur:', error)); // Gestion des erreurs
}

// Fonction pour récupérer la liste des utilisateurs (si nécessaire)
function getUsers() {
  // Effectuer une requête GET vers l'API pour récupérer les utilisateurs
  fetch('/users')
    .then(response => response.json()) // Convertir la réponse en JSON
    .then(data => {
      // Afficher la liste des utilisateurs dans l'élément HTML avec l'ID 'userList'
      document.getElementById('userList').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error('Erreur:', error)); // Gestion des erreurs
}

// Gestionnaire pour l'entrée de la ville
const cityInput = document.getElementById('city'); // Champ d'entrée pour la ville
const weatherData = document.getElementById('weatherData'); // Élément pour afficher les données météo

// Ajouter un écouteur d'événement pour détecter les changements dans le champ d'entrée
cityInput.addEventListener('input', function () {
  const city = cityInput.value.trim(); // Récupérer la valeur entrée et supprimer les espaces inutiles
  if (city !== '') {
    // Si une ville est spécifiée, effectuer une requête pour récupérer ses données météo
    fetch(`/weather/${city}`)
      .then(response => {
        if (!response.ok) {
          // Si la réponse HTTP n'est pas correcte, lever une erreur
          throw new Error(`Erreur HTTP: ${response.status}`);
        }
        return response.json(); // Convertir la réponse en JSON
      })
      .then(data => {
        const weatherCards = document.getElementById('weatherCards'); // Conteneur pour les cartes météo
        weatherCards.innerHTML = ''; // Réinitialiser le contenu des cartes

        // Vérifier si des données météo sont disponibles
        if (data.weather_data && data.weather_data.length > 0) {
          // Parcourir les données météo et créer une carte pour chaque entrée
          data.weather_data.forEach(weather => {
            const card = document.createElement('div'); // Créer un élément div pour la carte
            card.className = 'weather-card'; // Ajouter une classe CSS pour le style
            card.innerHTML = `
              <a href="forecast.html?city=${encodeURIComponent(weather.Commune)}" class="weather-link">
                <strong>🌍 Ville :</strong> ${weather.Commune || 'Non spécifié'} <br>
                <strong>📅 Date :</strong> ${new Date(weather['Forecast timestamp']).toLocaleDateString() || 'Non spécifié'} <br>
                <strong>🌡️ Température :</strong> ${weather['2 metre temperature'] || 'Non spécifié'}°C <br>
                <strong>💧 Humidité :</strong> ${weather['2 metre relative humidity'] || 'Non spécifié'}% <br>
                <strong>🌧️ Précipitations totales :</strong> ${weather['Total precipitation'] || 'Non spécifié'} mm <br>
                <strong>🌬️ Vitesse du vent :</strong> ${weather['10m wind speed'] || 'Non spécifié'} km/h <br>
                <strong>🌞 Rayonnement solaire :</strong> ${weather['Surface solar radiation downwards'] || 'Non spécifié'} W/m² <br>
                <strong>📍 Position :</strong> ${weather.Position || 'Non spécifié'} <br>
              </a>
            `;
            weatherCards.appendChild(card); // Ajouter la carte au conteneur
          });
        } else {
          // Si aucune donnée n'est disponible, afficher un message
          weatherCards.innerHTML = '<p>Aucune donnée disponible pour cette ville.</p>';
        }
      })
      .catch(error => {
        // Gestion des erreurs lors de la récupération des données
        console.error('Erreur:', error);
        document.getElementById('weatherCards').innerHTML = '<p>Erreur lors de la récupération des données.</p>';
      });
  } else {
    // Si le champ est vide, réinitialiser le contenu des cartes
    document.getElementById('weatherCards').innerHTML = '';
  }
});