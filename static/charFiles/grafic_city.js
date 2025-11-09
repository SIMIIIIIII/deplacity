document.addEventListener('DOMContentLoaded', (event) => {
    var ctx = document.getElementById('requete_city').getContext('2d');
    var proportionsData = JSON.parse(document.getElementById('proportions').textContent);
    //var proportionsJSON = JSON.stringify(proportionsData)
    // création du graphique
    var myChart = new Chart(ctx, {
        type: 'pie',   // le type du graphique
        data: {        // les données
            labels: ['Pieton', 'Vélo', 'voiture', 'Voiture lourde'],
            datasets: [{
                label: 'Moyens de transport utilisés',
                data: proportionsData,
                backgroundColor: [
                    'rgb(255, 0, 0)',
                    'rgb(255, 255, 0)',
                    'rgb(0, 128, 0)',
                    'rgb(0, 0, 255)'
                ],
                borderColor: [
                    'rgba(255, 0, 1)',
                    'rgba(255, 255, 1)',
                    'rgba(0, 128, 1)',
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
