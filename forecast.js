// forecast.js

// Récupérer les paramètres de l'URL
const urlParams = new URLSearchParams(window.location.search);
const city = urlParams.get('city');

// Afficher le nom de la ville
document.getElementById('cityName').textContent = city;

// Récupérer les prévisions météo pour les 3 prochains jours
fetch(`/weather/${city}`)
  .then(response => {
    console.log('Réponse brute :', response);
    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('Données reçues :', data); // Ajoutez ce log
    const forecastCards = document.getElementById('forecastCards');
    forecastCards.innerHTML = ''; // Réinitialiser les cartes

    // Afficher les prédictions retournées par l'API
    data.predictions.forEach(prediction => {
      const card = document.createElement('div');
      card.className = 'weather-card';
      card.innerHTML = `
        <strong>📅 Date :</strong> ${prediction.date} <br>
        <strong>🌡️ Température :</strong> ${prediction.temperature}°C <br>
      `;
      forecastCards.appendChild(card);
    });
  })
  .catch(error => {
    console.error('Erreur lors de la récupération des données :', error);
    document.getElementById('forecastCards').innerHTML = '<p>Erreur lors de la récupération des données.</p>';
  });