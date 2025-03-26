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
const weatherData = document.getElementById('weatherData');

cityInput.addEventListener('input', function() {
const city = cityInput.value.trim();
if (city !== '') {
  fetch(`/weather/${city}`)
    .then(response => response.json())
    .then(data => {
      if (data.weather_data) {
        const weather = data.weather_data[0];
        weatherData.innerHTML = `
          <strong>🌍 Ville :</strong> ${weather.City} <br>
          <strong>📅 Date :</strong> ${weather.DateTime} <br>
          <strong>🏙️ Département :</strong> ${weather.Department} <br>
          <strong>🕒 Heure :</strong> ${weather.HourTime} <br>
          <strong>🌡️ Température :</strong> ${weather.Temperature}°C <br>
          <strong>💧 Humidité :</strong> ${weather.Humidity}% <br>
          <strong>🌞 Ensoleillement :</strong> ${weather.Sunshine} heures <br>
          <strong>🌬️ Vitesse du vent :</strong> ${weather.WindSpeed} km/h <br>
          <strong>📍 Latitude :</strong> ${weather.Latitude} <br>
          <strong>📍 Longitude :</strong> ${weather.Longitude} <br>
          <strong>🌤️ Condition :</strong> ${weather.WeatherCondition} <br>
        `;
      } else {
        weatherData.innerText = 'Aucune donnée disponible.';
      }
    })
    .catch(error => {
      console.error('Erreur:', error);
      weatherData.innerText = 'Erreur lors de la récupération des données.';
    });
} else {
  weatherData.innerText = '';
}
});
