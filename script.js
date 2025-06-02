function callPrediction(league) {
  fetch(`/simulate_season?league=${league.toLowerCase()}`)
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert(`Failed to simulate ${league}: ${data.error}`);
        return;
      }

      const standings = data.standings;
      let output = `<h2>${league.toUpperCase()} Season Simulation</h2><ol>`;
      standings.forEach(([team, wins, losses]) => {
        output += `<li><strong>${team}</strong>: ${wins}-${losses}</li>`;
      });
      output += '</ol>';

      document.getElementById('simulation-results').innerHTML = output;
    })
    .catch(error => {
      console.error(`Error simulating ${league}:`, error);
      alert(`Failed to simulate ${league}`);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const buttons = {
    "nba-btn": "NBA",
    "nfl-btn": "NFL",
    "nhl-btn": "NHL",
    "mlb-btn": "MLB"
  };

  for (const [btnId, league] of Object.entries(buttons)) {
    const btn = document.getElementById(btnId);
    if (btn) {
      btn.addEventListener("click", () => callPrediction(league));
    }
  }
});
