import os  # Operating system functionalities

import pandas as pd  # Data manipulation and analysis
from sklearn.model_selection import train_test_split  # train_test_split for splitting data
from sklearn.ensemble import RandomForestRegressor  # Regression analysis
from sklearn.metrics import mean_squared_error  # Error calculation
from sklearn.model_selection import GridSearchCV  # Hyperparameter tuning
from sklearn.model_selection import cross_val_score  # Cross-validation
from sklearn.linear_model import LinearRegression  # Linear regression analysis
from sklearn.metrics import r2_score  # Calculating R-squared metric


file_path = '/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/data/cleaned_data/bundesliga_cleaned.csv'

# Load the data from the CSV file into a Pandas DataFrame
data = pd.read_csv(file_path)

encoding_dict = {
    'Arminia': 'St. Pauli',
    'Greuther Fürth': 'Holstein Kiel',
    'Schalke 04': 'St. Pauli',
    'Hertha BSC': 'Holstein Kiel',
    'Köln': 'St. Pauli',
    'Darmstadt 98': 'Holstein Kiel'
}

# Apply the encoding to the 'Home Team' and 'Away Team' columns
data['Home Team'] = data['Home Team'].replace(encoding_dict)
data['Away Team'] = data['Away Team'].replace(encoding_dict)

# Feature engineering
def feature_engineering(df, window=5):

    """
    Perform feature engineering on the given DataFrame by calculating rolling averages
    for goals scored, goals conceded, assists, and expected goals (xG) over a specified window.

    Args:
        df: The input DataFrame containing match data.
        window: The window size for calculating rolling averages.

    Returns:
        pd.DataFrame: The DataFrame with additional features for each match.
    """

    # Get unique team names from the DataFrame
    teams = pd.concat([df['Home Team'], df['Away Team']]).unique()

    # Dictionary for team stats
    team_stats = {team: {'goals_scored': [], 'goals_conceded': [], 'assists': [], 'xG': []} for team in teams}

    for idx, row in df.iterrows():
        home_team = row['Home Team']
        away_team = row['Away Team']
        home_goals = row['Home Goals']
        away_goals = row['Away Goals']
        home_ast = row['Home Ast']
        away_ast = row['Away Ast']
        home_xG = row['Home xG']
        away_xG = row['Away xG']

        if len(team_stats[home_team]['goals_scored']) >= window:
            team_stats[home_team]['goals_scored'].pop(0)
            team_stats[home_team]['goals_conceded'].pop(0)
            team_stats[home_team]['assists'].pop(0)
            team_stats[home_team]['xG'].pop(0)

        if len(team_stats[away_team]['goals_scored']) >= window:
            team_stats[away_team]['goals_scored'].pop(0)
            team_stats[away_team]['goals_conceded'].pop(0)
            team_stats[away_team]['assists'].pop(0)
            team_stats[away_team]['xG'].pop(0)

        # Update statistics for home team
        team_stats[home_team]['goals_scored'].append(home_goals)
        team_stats[home_team]['goals_conceded'].append(away_goals)
        team_stats[home_team]['assists'].append(home_ast)
        team_stats[home_team]['xG'].append(home_xG)

        # Update statistics for away team
        team_stats[away_team]['goals_scored'].append(away_goals)
        team_stats[away_team]['goals_conceded'].append(home_goals)
        team_stats[away_team]['assists'].append(away_ast)
        team_stats[away_team]['xG'].append(away_xG)

        # Calculate rolling averages for home team and assign to DataFrame
        df.at[idx, 'Home_avg_goals_scored'] = sum(team_stats[home_team]['goals_scored']) / len(team_stats[home_team]['goals_scored'])
        df.at[idx, 'Home_avg_goals_conceded'] = sum(team_stats[home_team]['goals_conceded']) / len(team_stats[home_team]['goals_conceded'])
        df.at[idx, 'Home_avg_assists'] = sum(team_stats[home_team]['assists']) / len(team_stats[home_team]['assists'])
        df.at[idx, 'Home_avg_xG'] = sum(team_stats[home_team]['xG']) / len(team_stats[home_team]['xG'])

        # Calculate rolling averages for away team and assign to DataFrame
        df.at[idx, 'Away_avg_goals_scored'] = sum(team_stats[away_team]['goals_scored']) / len(team_stats[away_team]['goals_scored'])
        df.at[idx, 'Away_avg_goals_conceded'] = sum(team_stats[away_team]['goals_conceded']) / len(team_stats[away_team]['goals_conceded'])
        df.at[idx, 'Away_avg_assists'] = sum(team_stats[away_team]['assists']) / len(team_stats[away_team]['assists'])
        df.at[idx, 'Away_avg_xG'] = sum(team_stats[away_team]['xG']) / len(team_stats[away_team]['xG'])

    return df

# Apply feature engineering
data = feature_engineering(data)

# Select features and target variables
features = [
    'Home_avg_goals_scored', 'Home_avg_goals_conceded', 'Home_avg_assists', 'Home_avg_xG',
    'Away_avg_goals_scored', 'Away_avg_goals_conceded', 'Away_avg_assists', 'Away_avg_xG'
]

target_home = 'Home xG'
target_away = 'Away xG'

X = data[features]
y_home = data[target_home]
y_away = data[target_away]

# Split the data into training and testing sets for home/away team predictions
X_train, X_test, y_train_home, y_test_home = train_test_split(X, y_home, test_size=0.2, random_state=42)
_, _, y_train_away, y_test_away = train_test_split(X, y_away, test_size=0.2, random_state=42)

model_home_lr = LinearRegression()
model_away_lr = LinearRegression()

# Train the linear regression model for the home/away team
model_home_lr.fit(X_train, y_train_home)
model_away_lr.fit(X_train, y_train_away)

y_pred_home_lr = model_home_lr.predict(X_test)
mse_home_lr = mean_squared_error(y_test_home, y_pred_home_lr)

y_pred_away_lr = model_away_lr.predict(X_test)
mse_away_lr = mean_squared_error(y_test_away, y_pred_away_lr)

print(f'Test Set Mean Squared Error for Home Model: {mse_home_lr:.4f}')
print(f'Test Set Mean Squared Error for Away Model: {mse_away_lr:.4f}')

# Calculate R-squared for the home team model
r2_home_lr = r2_score(y_test_home, y_pred_home_lr)

# Calculate R-squared for the away team model
r2_away_lr = r2_score(y_test_away, y_pred_away_lr)

print(f'Home Model (Linear Regression) R-squared: {r2_home_lr:.4f}')
print(f'Away Model (Linear Regression) R-squared: {r2_away_lr:.4f}')


# Creating a team_stats dictionary for prediction
teams = pd.concat([data['Home Team'], data['Away Team']]).unique()
team_stats = {team: {'goals_scored': [], 'goals_conceded': [], 'assists': [], 'xG': []} for team in teams}

for idx, row in data.iterrows():
    home_team = row['Home Team']
    away_team = row['Away Team']
    home_goals = row['Home Goals']
    away_goals = row['Away Goals']
    home_ast = row['Home Ast']
    away_ast = row['Away Ast']
    home_xG = row['Home xG']
    away_xG = row['Away xG']
    
    # Update statistics for home team
    team_stats[home_team]['goals_scored'].append(home_goals)
    team_stats[home_team]['goals_conceded'].append(away_goals)
    team_stats[home_team]['assists'].append(home_ast)
    team_stats[home_team]['xG'].append(home_xG)
    
    # Update statistics for away team
    team_stats[away_team]['goals_scored'].append(away_goals)
    team_stats[away_team]['goals_conceded'].append(home_goals)
    team_stats[away_team]['assists'].append(away_ast)
    team_stats[away_team]['xG'].append(away_xG)


team_calendar_dir = '/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/2425_Calendars/Team_Calendars'

csv_files = [f for f in os.listdir(team_calendar_dir) if f.endswith('.csv')]

def feature_engineering_new_matches(df, team_stats, window=5):

    """
    Perform feature engineering on new match data by calculating rolling averages
    for goals scored, goals conceded, assists, and expected goals (xG) over a specified window.

    Args:
        df: The input DataFrame containing new match data.
        team_stats: A dictionary containing historical team statistics.
        window: The window size for calculating rolling averages. Default is 5.

    Returns:
        pd.DataFrame: The DataFrame with additional features for each match.
    """

    for idx, row in df.iterrows():
        home_team = row['Home Team']
        away_team = row['Away Team']

        # Calculate rolling averages for the home team
        home_avg_goals_scored = sum(team_stats[home_team]['goals_scored'][-window:]) / len(team_stats[home_team]['goals_scored'][-window:])
        home_avg_goals_conceded = sum(team_stats[home_team]['goals_conceded'][-window:]) / len(team_stats[home_team]['goals_conceded'][-window:])
        home_avg_assists = sum(team_stats[home_team]['assists'][-window:]) / len(team_stats[home_team]['assists'][-window:])
        home_avg_xG = sum(team_stats[home_team]['xG'][-window:]) / len(team_stats[home_team]['xG'][-window:])
        
        # Calculate rolling averages for the away team
        away_avg_goals_scored = sum(team_stats[away_team]['goals_scored'][-window:]) / len(team_stats[away_team]['goals_scored'][-window:])
        away_avg_goals_conceded = sum(team_stats[away_team]['goals_conceded'][-window:]) / len(team_stats[away_team]['goals_conceded'][-window:])
        away_avg_assists = sum(team_stats[away_team]['assists'][-window:]) / len(team_stats[away_team]['assists'][-window:])
        away_avg_xG = sum(team_stats[away_team]['xG'][-window:]) / len(team_stats[away_team]['xG'][-window:])

         # Assign the calculated averages to the DataFrame
        df.at[idx, 'Home_avg_goals_scored'] = home_avg_goals_scored
        df.at[idx, 'Home_avg_goals_conceded'] = home_avg_goals_conceded
        df.at[idx, 'Home_avg_assists'] = home_avg_assists
        df.at[idx, 'Home_avg_xG'] = home_avg_xG

        df.at[idx, 'Away_avg_goals_scored'] = away_avg_goals_scored
        df.at[idx, 'Away_avg_goals_conceded'] = away_avg_goals_conceded
        df.at[idx, 'Away_avg_assists'] = away_avg_assists
        df.at[idx, 'Away_avg_xG'] = away_avg_xG

    return df

features = [
    'Home_avg_goals_scored', 'Home_avg_goals_conceded', 'Home_avg_assists', 'Home_avg_xG',
    'Away_avg_goals_scored', 'Away_avg_goals_conceded', 'Away_avg_assists', 'Away_avg_xG'
]

team_name_mapping = {
    '1. FC Heidenheim 1846': 'Heidenheim',
    '1. FC Union Berlin': 'Union Berlin',
    '1. FSV Mainz 05': 'Mainz 05',
    'Bayer 04 Leverkusen': 'Bayer Leverkusen',
    'Borussia Dortmund': 'Dortmund',
    'Borussia Mönchengladbach': 'Mönchengladbach',
    'Eintracht Frankfurt': 'Eintracht Frankfurt',
    'FC Augsburg': 'Augsburg',
    'FC Bayern München': 'Bayern Munich',
    'FC St. Pauli': 'St. Pauli',
    'Holstein Kiel': 'Holstein Kiel',
    'RB Leipzig': 'RB Leipzig',
    'Sport-Club Freiburg': 'Freiburg',
    'SV Werder Bremen': 'Werder Bremen',
    'TSG Hoffenheim': 'Hoffenheim',
    'VfB Stuttgart': 'Stuttgart',
    'VfL Bochum 1848': 'Bochum',
    'VfL Wolfsburg': 'Wolfsburg'
}

for csv_file in csv_files:
    # Construct the full file path
    file_path = os.path.join(team_calendar_dir, csv_file)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Map team names to their shorter versions
    df['Home Team'] = df['Home Team'].map(team_name_mapping)
    df['Away Team'] = df['Away Team'].map(team_name_mapping)

    
    df.dropna(subset=['Home Team', 'Away Team'], inplace=True)

    # Drop unnecessary columns
    df = df.drop(columns=['Date', 'Matchday'])
    
    # Apply feature engineering to the DataFrame
    df = feature_engineering_new_matches(df, team_stats)
    
    new_matches_features = df[features]
    
    # Predict expected goals (xG) for home and away teams
    predicted_home_xG_new = model_home_lr.predict(new_matches_features)
    predicted_away_xG_new = model_away_lr.predict(new_matches_features)
    
    # Add predictions to the DataFrame
    df['Predicted_Home_xG'] = predicted_home_xG_new.round(4)
    df['Predicted_Away_xG'] = predicted_away_xG_new.round(4)
    
    output_file_path = os.path.join('/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/Model_Jihang/predicted_teams_regression', 
                                    'predicted_' + csv_file.replace('.csv', '.json'))
    
    # Drop feature columns to prepare the DataFrame for saving
    df = df.drop(columns=['Home_avg_goals_scored', 'Home_avg_goals_conceded', 'Home_avg_assists', 'Home_avg_xG', 
                          'Away_avg_goals_scored', 'Away_avg_goals_conceded', 'Away_avg_assists', 'Away_avg_xG'])
    
    df.to_json(output_file_path)

