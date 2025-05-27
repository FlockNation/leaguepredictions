function callPrediction(league) {
    fetch(`/predict/${league.toLowerCase()}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        alert(`${league} Simulation Complete:\n${data.message}`);
    })
    .catch(error => {
        console.error('Error:', error);
        alert(`Failed to simulate ${league}`);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("nba-btn").addEventListener("click", function () {
        callPrediction("NBA");
    });

    document.getElementById("nfl-btn").addEventListener("click", function () {
        callPrediction("NFL");
    });

    document.getElementById("nhl-btn").addEventListener("click", function () {
        callPrediction("NHL");
    });

    document.getElementById("mlb-btn").addEventListener("click", function () {
        callPrediction("MLB");
    });
});
