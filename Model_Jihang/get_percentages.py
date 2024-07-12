import numpy as np
import pandas as pd
import os

def simulate_match_outcomes(predicted_home_xG, predicted_away_xG, num_simulations=10000):
    home_wins = 0
    away_wins = 0
    ties = 0
    
    for _ in range(num_simulations):
        home_goals = np.random.poisson(predicted_home_xG)
        away_goals = np.random.poisson(predicted_away_xG)
        
        if home_goals > away_goals:
            home_wins += 1
        elif home_goals < away_goals:
            away_wins += 1
        else:
            ties += 1
    
    total_simulations = home_wins + away_wins + ties
    home_win_probability = (home_wins / total_simulations) * 100
    away_win_probability = (away_wins / total_simulations) * 100
    tie_probability = (ties / total_simulations) * 100
    
    return home_win_probability, tie_probability, away_win_probability

team_prediction_dir = '/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/Model_Jihang/predicted_teams_regression'

csv_files = [f for f in os.listdir(team_prediction_dir) if f.endswith('.csv')]

for csv_file in csv_files:
    file_path = os.path.join(team_prediction_dir, csv_file)
    df = pd.read_csv(file_path)

    df['Home_Win_Probability'] = 0.0
    df['Tie_Probability'] = 0.0
    df['Away_Win_Probability'] = 0.0

    for index, row in df.iterrows():
        home_win_prob, tie_prob, away_win_prob = simulate_match_outcomes(row['Predicted_Home_xG'], row['Predicted_Away_xG'])
        df.at[index, 'Home_Win_Probability'] = round(home_win_prob, ndigits=4)
        df.at[index, 'Tie_Probability'] = round(tie_prob, ndigits=4)
        df.at[index, 'Away_Win_Probability'] = round(away_win_prob, ndigits=4)
    
    df.to_csv(file_path, index=False)