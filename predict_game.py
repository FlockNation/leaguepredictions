import numpy as np
from joblib import load

def predict_game(team_a_stats, team_b_stats, model_path):
    model = load(model_path)
    diff = np.array(team_a_stats) - np.array(team_b_stats)
    win_prob = model.predict_proba([diff])[0][1]

    upset_factor = 0.05
    adjusted_prob = win_prob * (1 - upset_factor) + (1 - win_prob) * upset_factor

    return np.random.rand() < adjusted_prob
