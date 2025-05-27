import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

LEAGUE_FILES = {
    'nba': 'NBA_2024_25.csv',
    'nfl': 'NFL_2024.csv',
    'nhl': 'NHL_2024_25.csv',
    'mlb': 'MLB_2024.csv',
}

def load_data(file):
    df = pd.read_csv(file)
    return df

def create_matchups(df):
    teams = df['Team'].values
    X = []
    y = []
    for i in range(len(teams)):
        for j in range(len(teams)):
            if i == j:
                continue
            team_a = df.iloc[i]
            team_b = df.iloc[j]
            features = []
            for stat in ['Wins', 'Losses']:
                features.append(team_a[stat] - team_b[stat])
            X.append(features)
            y.append(1 if team_a['Wins'] > team_b['Wins'] else 0)
    return np.array(X), np.array(y)

def train_and_save_model(league):
    print(f"Training model for {league.upper()}...")
    df = load_data(LEAGUE_FILES[league])
    X, y = create_matchups(df)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    acc = model.score(X_test, y_test)
    print(f"{league.upper()} model accuracy: {acc:.2f}")

    joblib.dump(model, f"{league}_model.joblib")
    joblib.dump(scaler, f"{league}_scaler.joblib")
    print(f"Saved {league} model and scaler.\n")

if __name__ == "__main__":
    for league in LEAGUE_FILES:
        train_and_save_model(league)
