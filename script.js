// script.js

// Функция для получения данных о погоде
function getWeatherData() {
  fetch('/weather')
    .then(response => {
      if (!response.ok) {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      document.getElementById('weatherData').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => {
      console.error('Erreur:', error);
      document.getElementById('weatherData').innerText = 'Erreur lors de la récupération des données.';
    });
}

// Функция для создания нового пользователя (если используется)
function createUser() {
  fetch('/users', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
      document.getElementById('newUser').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error('Erreur:', error));
}

// Функция для получения списка пользователей (если используется)
function getUsers() {
  fetch('/users')
    .then(response => response.json())
    .then(data => {
      document.getElementById('userList').textContent = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error('Erreur:', error));
}

// Обработчик ввода города
const cityInput = document.getElementById('city');
const weatherData = document.getElementById('weatherData');

cityInput.addEventListener('input', function () {
  const city = cityInput.value.trim();
  if (city !== '') {
    fetch(`/weather/${city}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        if (data.weather_data && data.weather_data.length > 0) {
          const weather = data.weather_data[0];
          weatherData.innerHTML = `
            <div>
              <strong>🌍 Ville :</strong> ${weather.Commune || 'Non spécifié'} <br>
              <strong>📅 Date :</strong> ${new Date(weather['Forecast timestamp']).toLocaleDateString() || 'Non spécifié'} <br>
              <strong>🌡️ Température :</strong> ${weather['2 metre temperature'] || 'Non spécifié'}°C <br>
              <strong>💧 Humidité :</strong> ${weather['2 metre relative humidity'] || 'Non spécifié'}% <br>
              <strong>🌧️ Précipitations totales :</strong> ${weather['Total precipitation'] || 'Non spécifié'} mm <br>
              <strong>🌬️ Vitesse du vent :</strong> ${weather['10m wind speed'] || 'Non spécifié'} km/h <br>
              <strong>🌞 Rayonnement solaire :</strong> ${weather['Surface solar radiation downwards'] || 'Non spécifié'} W/m² <br>
              <strong>📍 Position :</strong> ${weather.Position || 'Non spécifié'} <br>
            </div>
          `;
        } else {
          weatherData.innerText = 'Aucune donnée disponible pour cette ville.';
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