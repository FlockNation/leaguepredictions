import joblib
import numpy as np
import random

def predict_game(team_a_stats, team_b_stats, league):
    model = joblib.load(f"{league}_model.joblib")
    scaler = joblib.load(f"{league}_scaler.joblib")

    if league == 'nhl' and 'OTL' in team_a_stats and 'OTL' in team_b_stats:
        features = np.array([
            team_a_stats['Wins'] - team_b_stats['Wins'],
            team_a_stats['Losses'] - team_b_stats['Losses'],
            team_a_stats['OTL'] - team_b_stats['OTL']
        ]).reshape(1, -1)
    else:
        features = np.array([
            team_a_stats['Wins'] - team_b_stats['Wins'],
            team_a_stats['Losses'] - team_b_stats['Losses']
        ]).reshape(1, -1)

    features_scaled = scaler.transform(features)
    win_prob = model.predict_proba(features_scaled)[0][1]

    adjusted_prob = np.clip(win_prob + random.uniform(-0.15, 0.15), 0, 1)

    return random.random() < adjusted_prob
