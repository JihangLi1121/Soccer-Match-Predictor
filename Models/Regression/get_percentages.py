import os  # Operating system functionalities
import numpy as np  # Numerical operations
import pandas as pd  # Data manipulation and analysis


def simulate_match_outcomes(predicted_home_xG, predicted_away_xG, num_simulations=10000):

    """
    Simulate match outcomes based on predicted expected goals (xG) for home and away teams.

    Args:
        predicted_home_xG: The predicted expected goals for the home team.
        predicted_away_xG: The predicted expected goals for the away team.
        num_simulations: The number of simulations to run.

    Returns:
        tuple: Probabilities of home win, tie, and away win (in percentage).
    """

    home_wins = 0
    away_wins = 0
    ties = 0
    
    for _ in range(num_simulations):
        # Simulate the number of goals scored by each team using Poisson distribution
        home_goals = np.random.poisson(predicted_home_xG)
        away_goals = np.random.poisson(predicted_away_xG)
        
        # Determine the outcome of the match
        if home_goals > away_goals:
            home_wins += 1
        elif home_goals < away_goals:
            away_wins += 1
        else:
            ties += 1
    
    total_simulations = home_wins + away_wins + ties

    # Calculate the probabilities of each outcome
    home_win_probability = (home_wins / total_simulations) * 100
    away_win_probability = (away_wins / total_simulations) * 100
    tie_probability = (ties / total_simulations) * 100
    
    return home_win_probability, tie_probability, away_win_probability


team_prediction_dir = '/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/Model_Jihang/predicted_teams_regression'


json_files = [f for f in os.listdir(team_prediction_dir) if f.endswith('.csv')]

for json_file in json_files:
    # Construct the full file path
    file_path = os.path.join(team_prediction_dir, json_file)

    # Read the JSON file into a DataFrame
    df = pd.read_json(file_path)

    # Initialize probability columns
    df['Home_Win_Probability'] = 0.0
    df['Tie_Probability'] = 0.0
    df['Away_Win_Probability'] = 0.0

    for index, row in df.iterrows():

         # Simulate match outcomes and get probabilities
        home_win_prob, tie_prob, away_win_prob = simulate_match_outcomes(row['Predicted_Home_xG'], row['Predicted_Away_xG'])
        
        # Update the DataFrame with the calculated probabilities
        df.at[index, 'Home_Win_Probability'] = round(home_win_prob, ndigits=4)
        df.at[index, 'Tie_Probability'] = round(tie_prob, ndigits=4)
        df.at[index, 'Away_Win_Probability'] = round(away_win_prob, ndigits=4)
    
    df.to_json(file_path)