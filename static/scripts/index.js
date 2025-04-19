async function fetchPlayerStats() {
  const playerName = document.getElementById("playerInput").value.trim();
  const infoDiv = document.getElementById("playerInfo");

  // Clear previous content
  infoDiv.innerHTML = "";

  if (!playerName) {
    infoDiv.innerHTML = "<p>Please enter a player name.</p>";
    return;
  }

  const url = `http://localhost:8000/get_player_stats?name=${encodeURIComponent(playerName)}`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (data.error) {
      infoDiv.innerHTML = `<p>${data.error}</p>`;
      return;
    }

    // Show the GET request
    const requestEl = document.createElement("div");
    requestEl.style.marginBottom = "1rem";
    requestEl.innerHTML = `<code><strong>GET:</strong> ${url}</code>`;
    infoDiv.appendChild(requestEl);

    // Render each game stat entry
    data.stats.forEach(stat => {
      const statCard = document.createElement("div");
      statCard.className = "stat-card";
      statCard.innerHTML = `
        <h3>${stat.person_name} – ${stat.season_year}</h3>
        <p><strong>Date:</strong> ${stat.game_date}</p>
        <p><strong>Matchup:</strong> ${stat.matchup}</p>
        <p><strong>Team:</strong> ${stat.team_name} (${stat.team_tricode})</p>
        <p><strong>Position:</strong> ${stat.position} | <strong>Jersey #:</strong> ${stat.jersey_num}</p>
        <p><strong>Minutes:</strong> ${stat.minutes}</p>
        <p><strong>FG:</strong> ${stat.field_goals_made}/${stat.field_goals_attempted} (${stat.field_goals_percentage}%)</p>
        <p><strong>3P:</strong> ${stat.three_pointers_made}/${stat.three_pointers_attempted} (${stat.three_pointers_percentage}%)</p>
        <p><strong>FT:</strong> ${stat.free_throws_made}/${stat.free_throws_attempted} (${stat.free_throws_percentage}%)</p>
        <p><strong>REB:</strong> ${stat.rebounds_total} (Off: ${stat.rebounds_offensive}, Def: ${stat.rebounds_defensive})</p>
        <p><strong>AST:</strong> ${stat.assists} | <strong>STL:</strong> ${stat.steals} | <strong>BLK:</strong> ${stat.blocks}</p>
        <p><strong>TO:</strong> ${stat.turnovers} | <strong>PF:</strong> ${stat.fouls_personal}</p>
        <p><strong>PTS:</strong> ${stat.points} | <strong>+/-:</strong> ${stat.plus_minus_points}</p>
      `;
      infoDiv.appendChild(statCard);
    });
  } catch (err) {
    infoDiv.innerHTML = `<p>Error fetching player stats.</p>`;
    console.error("Fetch error:", err);
  }
}