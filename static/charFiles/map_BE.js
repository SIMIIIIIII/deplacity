// Initialisation de la carte
var map_BE = L.map('map').setView([50.6402809, 4.6667145], 9);

// Ajout de la couche de la carte
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map_BE);

// Récupération du dictionnaire coordonnee depuis le HTML et conversion en objet JavaScript
var coordonnee = JSON.parse(document.getElementById('coordonnee').textContent);
var cities = JSON.parse(document.getElementById('cities').textContent);

// Ajout d'un marqueur pour chaque coordonnée dans le dictionnaire
for (var key in coordonnee) {
    L.marker(coordonnee[key]).addTo(map_BE)
        .bindPopup('<b style="font-size: larger;">' + key + '</b><br>' +
        "Nombre de piétond observés : " + cities[key][0] + '<br>'+
        "Nombre de cyclistes observés : " + cities[key][1] + '<br>' +
        "Nombre de voitures observées : " + cities[key][2] + '<br>' +
        "Nombre de voitures lourdes observées : " + cities[key][3] + '<br>')
        .openPopup();
}
