from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import joblib
import random
import os

app = Flask(__name__, static_folder='.', static_url_path='')

LEAGUE_GAMES = {
    'nba': 82,
    'nfl': 17,
    'nhl': 82,
    'mlb': 162
}

def predict_game(team_a_stats, team_b_stats, league):
    model = joblib.load(f"{league}_model.joblib")
    scaler = joblib.load(f"{league}_scaler.joblib")
    features = [[team_a_stats['Wins'] - team_b_stats['Wins'],
                 team_a_stats['Losses'] - team_b_stats['Losses']]]
    features_scaled = scaler.transform(features)
    win_prob = model.predict_proba(features_scaled)[0][1]
    upset_factor = random.uniform(-0.15, 0.15)
    adjusted_prob = min(max(win_prob + upset_factor, 0), 1)
    return random.random() < adjusted_prob

def simulate_season(league):
    if league not in LEAGUE_GAMES:
        raise ValueError("Unsupported league.")
    csv_file = f"{league.upper()}_2024_25.csv" if league in ['nba', 'nhl'] else f"{league.upper()}_2024.csv"
    df = pd.read_csv(csv_file)
    teams = df['Team'].tolist()
    team_stats = {row['Team']: {'Wins': row['Wins'], 'Losses': row['Losses']} for _, row in df.iterrows()}
    standings = {team: 0 for team in teams}
    games_per_team = LEAGUE_GAMES[league]
    matchups = []
    total_games = (games_per_team * len(teams)) // 2
    while len(matchups) < total_games:
        team_a, team_b = random.sample(teams, 2)
        if (team_a, team_b) not in matchups and (team_b, team_a) not in matchups:
            matchups.append((team_a, team_b))
    for team_a, team_b in matchups:
        team_a_stats = team_stats[team_a]
        team_b_stats = team_stats[team_b]
        if predict_game(team_a_stats, team_b_stats, league):
            standings[team_a] += 1
        else:
            standings[team_b] += 1
    sorted_standings = sorted(standings.items(), key=lambda x: x[1], reverse=True)
    return sorted_standings

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/simulate_season', methods=['GET'])
def api_simulate_season():
    league = request.args.get('league')
    if league not in LEAGUE_GAMES:
        return jsonify({"error": "Invalid league"}), 400
    try:
        standings = simulate_season(league)
        return jsonify({"standings": standings})
    except Exception as e:
        print(f"Error simulating season for {league}: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
