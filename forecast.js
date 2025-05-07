// forecast.js

document.addEventListener('DOMContentLoaded', function () {
  const urlParams = new URLSearchParams(window.location.search);
  const city = urlParams.get('city');
  const cityNameElement = document.getElementById('cityName');
  const forecastCards = document.getElementById('forecastCards');

  if (cityNameElement) {
      cityNameElement.textContent = city;
  }

  if (!city) {
      if (forecastCards) {
          forecastCards.innerHTML = '<p>Ville non spécifiée.</p>';
      }
      return;
  }

  fetch(`/forecast/${city}`)
      .then(response => {
          console.log('Réponse brute:', response);
          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
      })
      .then(data => {
          console.log('Données reçues:', data);

          if (!forecastCards) return;

          forecastCards.innerHTML = '';

          if (data.predictions && Array.isArray(data.predictions)) {
              data.predictions.forEach(prediction => {
                  const card = document.createElement('div');
                  card.className = 'weather-card';
                  card.innerHTML = `
                      <strong>📅 Date :</strong> ${prediction.date} <br>
                      <strong>🌡 Température prévue :</strong> ${prediction.temperature}°C
                  `;
                  forecastCards.appendChild(card);
              });
          } else {
              forecastCards.innerHTML = '<p>Aucune prévision disponible.</p>';
          }
      })
      .catch(error => {
          console.error('Erreur lors de la récupération des données:', error);
          if (forecastCards) {
              forecastCards.innerHTML = `<p>Erreur: ${error.message}</p>`;
          }
      });
});
