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
        weatherData.innerText = JSON.stringify(data, null, 2);
      });
  } else {
    weatherData.innerText = '';
  }
});