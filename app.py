from flask import Flask, request, jsonify
import pandas as pd
import joblib
import random

app = Flask(__name__)

def predict_game(team_a_stats, team_b_stats, league):
    model = joblib.load(f"{league}_model.joblib")
    scaler = joblib.load(f"{league}_scaler.joblib")
    features = [[team_a_stats['Wins'] - team_b_stats['Wins'], team_a_stats['Losses'] - team_b_stats['Losses']]]
    features_scaled = scaler.transform(features)
    win_prob = model.predict_proba(features_scaled)[0][1]
    upset_chance = 0.1
    adjusted_prob = win_prob * (1 - upset_chance) + (random.random() * upset_chance)
    return adjusted_prob > 0.5

def simulate_season(league):
    csv_file = f"{league.upper()}_2024_25.csv" if league in ['nba', 'nhl'] else f"{league.upper()}_2024.csv"
    df = pd.read_csv(csv_file)
    teams = df['Team'].tolist()
    standings = {team: 0 for team in teams}
    team_stats = {}
    for _, row in df.iterrows():
        team_stats[row['Team']] = {'Wins': row['Wins'], 'Losses': row['Losses']}
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            team_a = teams[i]
            team_b = teams[j]
            team_a_stats = team_stats[team_a]
            team_b_stats = team_stats[team_b]
            winner_is_a = predict_game(team_a_stats, team_b_stats, league)
            if winner_is_a:
                standings[team_a] += 1
            else:
                standings[team_b] += 1
    sorted_standings = sorted(standings.items(), key=lambda x: x[1], reverse=True)
    return sorted_standings

@app.route('/simulate_season', methods=['GET'])
def api_simulate_season():
    league = request.args.get('league')
    if league not in ['nba', 'nfl', 'nhl', 'mlb']:
        return jsonify({"error": "Invalid league"}), 400
    standings = simulate_season(league)
    return jsonify({"standings": standings})

if __name__ == "__main__":
    app.run(debug=True)
