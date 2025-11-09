document.addEventListener('DOMContentLoaded', (event) => {
    var ctx = document.getElementById('moon_city').getContext('2d');
    var proportionsData = JSON.parse(document.getElementById('moons').textContent);
    //var proportionsJSON = JSON.stringify(proportionsData)
    // création du graphique
    var myChart = new Chart(ctx, {
        type: 'pie',   // le type du graphique
        data: {        // les données
            labels: ['Pleine Lune', 'Autres jours'],
            datasets: [{
                label: 'Moyens de transport utilisés',
                data: proportionsData,
                backgroundColor: [
                    'rgb(255, 0, 0)',
                    'rgb(0, 0, 255)'
                ],
                borderColor: [
                    'rgba(255, 0, 1)',
                    'rgba(0, 0, 255)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',  // ajuster l'emplacement des labels à droite
                }
            }
        }
    });
});
