// === Script pour afficher les prévisions météo ===

// Exécuter le script une fois que le DOM est complètement chargé
document.addEventListener('DOMContentLoaded', function () {
    // Récupération des paramètres de l'URL (par exemple, ?city=Paris)
    const urlParams = new URLSearchParams(window.location.search);
    const city = urlParams.get('city'); // Récupère la valeur du paramètre 'city'

    // Sélection des éléments HTML où afficher les données
    const cityNameElement = document.getElementById('cityName'); // Élément pour afficher le nom de la ville
    const forecastCards = document.getElementById('forecastCards'); // Conteneur pour les cartes de prévisions

    // Afficher le nom de la ville dans l'élément correspondant
    if (cityNameElement) {
        cityNameElement.textContent = city;
    }

    // Si aucune ville n'est spécifiée, afficher un message d'erreur
    if (!city) {
        if (forecastCards) {
            forecastCards.innerHTML = '<p>Ville non spécifiée.</p>';
        }
        return; // Arrêter l'exécution du script
    }

    // Effectuer une requête pour récupérer les prévisions météo pour la ville spécifiée
    fetch(`/forecast/${city}`)
        .then(response => {
            console.log('Réponse brute:', response); // Afficher la réponse brute dans la console pour débogage
            if (!response.ok) {
                // Si la réponse HTTP n'est pas correcte, lever une erreur
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json(); // Convertir la réponse en JSON
        })
        .then(data => {
            console.log('Données reçues:', data); // Afficher les données reçues dans la console

            if (!forecastCards) return; // Si le conteneur des cartes n'existe pas, arrêter ici

            // Réinitialiser le contenu du conteneur des cartes
            forecastCards.innerHTML = '';

            // Vérifier si des prévisions sont disponibles et si elles sont sous forme de tableau
            if (data.predictions && Array.isArray(data.predictions)) {
                // Parcourir chaque prévision et créer une carte pour l'afficher
                data.predictions.forEach(prediction => {
                    const card = document.createElement('div'); // Créer un élément div pour la carte
                    card.className = 'weather-card'; // Ajouter une classe CSS pour le style
                    card.innerHTML = `
                        <strong>📅 Date :</strong> ${prediction.date} <br>
                        <strong>🌡 Température prévue :</strong> ${prediction.temperature}°C
                    `;
                    forecastCards.appendChild(card); // Ajouter la carte au conteneur
                });
            } else {
                // Si aucune prévision n'est disponible, afficher un message
                forecastCards.innerHTML = '<p>Aucune prévision disponible.</p>';
            }
        })
        .catch(error => {
            // Gestion des erreurs lors de la récupération des données
            console.error('Erreur lors de la récupération des données:', error); // Afficher l'erreur dans la console
            if (forecastCards) {
                // Afficher un message d'erreur dans le conteneur
                forecastCards.innerHTML = `<p>Erreur: ${error.message}</p>`;
            }
        });
});
