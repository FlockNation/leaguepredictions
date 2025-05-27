function callPrediction(league) {
  fetch(`/simulate_season?league=${league.toLowerCase()}`, {
    method: 'GET'
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      alert(`Failed to simulate ${league}: ${data.error}`);
      return;
    }
    let standings = data.standings;
    let output = `<h3>${league} Season Simulation Complete</h3><ol>`;
    standings.forEach(([team, wins]) => {
      output += `<li>${team}: ${wins} wins</li>`;
    });
    output += '</ol>';
    document.getElementById('simulation-results').innerHTML = output;
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
