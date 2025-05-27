import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from joblib import dump

def create_matchup_data(df):
    matchups = []
    teams = df['Team'].values
    for i in range(len(teams)):
        for j in range(len(teams)):
            if i != j:
                team_a = df.iloc[i]
                team_b = df.iloc[j]
                diff = team_a.drop('Team') - team_b.drop('Team')
                matchups.append({
                    **diff.to_dict(),
                    'Winner': 1
                })
    return pd.DataFrame(matchups)

def train_model(league_name, csv_path):
    df = pd.read_csv(csv_path)
    df.fillna(0, inplace=True)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
    matchups = create_matchup_data(df)
    X = matchups.drop(columns=['Winner'])
    y = matchups['Winner']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    accuracy = model.score(X_test, y_test)
    print(f"{league_name} model accuracy: {accuracy:.2f}")
    dump(model, f"{league_name.lower()}_model.joblib")

train_model("NBA", "nba_2024.csv")
train_model("NFL", "nfl_2024.csv")
train_model("NHL", "nhl_2024.csv")
train_model("MLB", "mlb_2024.csv")
