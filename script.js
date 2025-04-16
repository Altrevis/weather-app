// script.js

function getWeatherData() {
  fetch('/weather')
      .then(response => response.json())
      .then(data => {
          document.getElementById('weatherData').textContent = JSON.stringify(data, null, 2);
      })
      .catch(error => console.error('Erreur:', error));
}

function createUser() {
  fetch('/users', { method: 'POST' })
      .then(response => response.json())
      .then(data => {
          document.getElementById('newUser').textContent = JSON.stringify(data, null, 2);
      })
      .catch(error => console.error('Erreur:', error));
}

function getUsers() {
  fetch('/users')
      .then(response => response.json())
      .then(data => {
          document.getElementById('userList').textContent = JSON.stringify(data, null, 2);
      })
      .catch(error => console.error('Erreur:', error));
}

const cityInput = document.getElementById('city');
const weatherCards = document.getElementById('weatherCards');

cityInput.addEventListener('input', function () {
  const city = cityInput.value.trim();
  if (city !== '') {
    fetch(`/weather/${city}`)
      .then(response => response.json())
      .then(data => {
        if (data.weather_data) {
          weatherCards.innerHTML = ''; // Réinitialiser les cartes
          data.weather_data.forEach(weather => {
            const card = document.createElement('div');
            card.className = 'weather-card';
            card.innerHTML = `
              <strong>🌍 Ville :</strong> ${weather.City} <br>
              <strong>🌡️ Température :</strong> ${weather.Temperature}°C <br>
              <strong>💧 Humidité :</strong> ${weather.Humidity}% <br>
              <strong>🌬️ Vent :</strong> ${weather.WindSpeed} km/h <br>
              <strong>🕰️ Temps :</strong> ${weather.DateTime} <br>
              <strong>⬆️ Latitude :</strong> ${weather.Latitude} <br>
              <strong>➡️ Longitude :</strong> ${weather.Longitude} <br>
              <strong>☀️ Ensoleillement :</strong> ${weather.Sunshine} <br>
              <strong>🌈 Codition météo :</strong> ${weather.WeatherCondition} <br>
            `;
            weatherCards.appendChild(card);
          });
        } else {
          weatherCards.innerHTML = '<p>Aucune donnée disponible.</p>';
        }
      })
      .catch(error => {
        console.error('Erreur:', error);
        weatherCards.innerHTML = '<p>Erreur lors de la récupération des données.</p>';
      });
  } else {
    weatherCards.innerHTML = '';
  }
});
