import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import os


file_path = '/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/data/cleaned_data/bundesliga_cleaned.csv'
data = pd.read_csv(file_path)

encoding_dict = {
    'Arminia': 'St. Pauli',
    'Greuther Fürth': 'Holstein Kiel',
    'Schalke 04': 'St. Pauli',
    'Hertha BSC': 'Holstein Kiel',
    # 'Köln': 'St. Pauli',
    # 'Darmstadt 98': 'Holstein Kiel'
}

# Apply the encoding to the 'Home Team' and 'Away Team' columns
data['Home Team'] = data['Home Team'].replace(encoding_dict)
data['Away Team'] = data['Away Team'].replace(encoding_dict)

# Feature engineering
def feature_engineering(df, window=5):

    teams = pd.concat([df['Home Team'], df['Away Team']]).unique()
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

        team_stats[home_team]['goals_scored'].append(home_goals)
        team_stats[home_team]['goals_conceded'].append(away_goals)
        team_stats[home_team]['assists'].append(home_ast)
        team_stats[home_team]['xG'].append(home_xG)

        team_stats[away_team]['goals_scored'].append(away_goals)
        team_stats[away_team]['goals_conceded'].append(home_goals)
        team_stats[away_team]['assists'].append(away_ast)
        team_stats[away_team]['xG'].append(away_xG)

        df.at[idx, 'Home_avg_goals_scored'] = sum(team_stats[home_team]['goals_scored']) / len(team_stats[home_team]['goals_scored'])
        df.at[idx, 'Home_avg_goals_conceded'] = sum(team_stats[home_team]['goals_conceded']) / len(team_stats[home_team]['goals_conceded'])
        df.at[idx, 'Home_avg_assists'] = sum(team_stats[home_team]['assists']) / len(team_stats[home_team]['assists'])
        df.at[idx, 'Home_avg_xG'] = sum(team_stats[home_team]['xG']) / len(team_stats[home_team]['xG'])

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

X_train, X_test, y_train_home, y_test_home = train_test_split(X, y_home, test_size=0.2, random_state=42)
_, _, y_train_away, y_test_away = train_test_split(X, y_away, test_size=0.2, random_state=42)

# # Train model for home team expected goals
# model_home = RandomForestRegressor(random_state=42)
# model_home.fit(X_train, y_train_home)

# # Train model for away team expected goals
# model_away = RandomForestRegressor(random_state=42)
# model_away.fit(X_train, y_train_away)

# # Predictions
# y_pred_home = model_home.predict(X_test)
# y_pred_away = model_away.predict(X_test)

def train_and_evaluate(X_train, X_test, y_train, y_test, params):
    model = RandomForestRegressor(**params, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return mse

# param_grid = {
#     'n_estimators': [50, 100, 200],
#     'max_depth': [None, 10, 20, 30],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4],
#     'bootstrap': [True, False]
# }

# grid_search_home = GridSearchCV(estimator=RandomForestRegressor(random_state=42), param_grid=param_grid, 
#                                 cv=3, n_jobs=-1, verbose=2)

# grid_search_away = GridSearchCV(estimator=RandomForestRegressor(random_state=42), param_grid=param_grid, 
#                                 cv=3, n_jobs=-1, verbose=2)

# # Fit the grid search to the data
# grid_search_home.fit(X_train, y_train_home)
# grid_search_away.fit(X_train, y_train_away)

# # Get the best parameters
# best_params_home = grid_search_home.best_params_
# best_params_away = grid_search_away.best_params_

best_params_home = {'bootstrap': True, 'max_depth': 10, 'min_samples_leaf': 2, 'min_samples_split': 10, 'n_estimators': 200}
best_params_away = {'bootstrap': True, 'max_depth': None, 'min_samples_leaf': 4, 'min_samples_split': 10, 'n_estimators': 100}

# Train the final model for home team expected goals
model_home_final = RandomForestRegressor(**best_params_home, random_state=42)
model_home_final.fit(X_train, y_train_home)

# Train the final model for away team expected goals
model_away_final = RandomForestRegressor(**best_params_away, random_state=42)
model_away_final.fit(X_train, y_train_away)

# Predictions
y_pred_home_final = model_home_final.predict(X_test)
y_pred_away_final = model_away_final.predict(X_test)

# Evaluation
mse_home_final = mean_squared_error(y_test_home, y_pred_home_final)
mse_away_final = mean_squared_error(y_test_away, y_pred_away_final)

print(mse_home_final, mse_away_final)

# Function to predict fixture outcome
def predict_fixture(home_team, away_team, model_home, model_away, team_stats, window=5):
    # Calculate the feature values for the home team
    home_avg_goals_scored = sum(team_stats[home_team]['goals_scored'][-window:]) / len(team_stats[home_team]['goals_scored'][-window:])
    home_avg_goals_conceded = sum(team_stats[home_team]['goals_conceded'][-window:]) / len(team_stats[home_team]['goals_conceded'][-window:])
    home_avg_assists = sum(team_stats[home_team]['assists'][-window:]) / len(team_stats[home_team]['assists'][-window:])
    home_avg_xG = sum(team_stats[home_team]['xG'][-window:]) / len(team_stats[home_team]['xG'][-window:])
    
    # Calculate the feature values for the away team
    away_avg_goals_scored = sum(team_stats[away_team]['goals_scored'][-window:]) / len(team_stats[away_team]['goals_scored'][-window:])
    away_avg_goals_conceded = sum(team_stats[away_team]['goals_conceded'][-window:]) / len(team_stats[away_team]['goals_conceded'][-window:])
    away_avg_assists = sum(team_stats[away_team]['assists'][-window:]) / len(team_stats[away_team]['assists'][-window:])
    away_avg_xG = sum(team_stats[away_team]['xG'][-window:]) / len(team_stats[away_team]['xG'][-window:])
    
    # Prepare the feature vector
    features = [
        home_avg_goals_scored, home_avg_goals_conceded, home_avg_assists, home_avg_xG,
        away_avg_goals_scored, away_avg_goals_conceded, away_avg_assists, away_avg_xG
    ]
    
    # Predict expected goals for home and away teams
    predicted_home_xG = model_home.predict([features])[0]
    predicted_away_xG = model_away.predict([features])[0]
    
    return predicted_home_xG, predicted_away_xG

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
    
    team_stats[home_team]['goals_scored'].append(home_goals)
    team_stats[home_team]['goals_conceded'].append(away_goals)
    team_stats[home_team]['assists'].append(home_ast)
    team_stats[home_team]['xG'].append(home_xG)
    
    team_stats[away_team]['goals_scored'].append(away_goals)
    team_stats[away_team]['goals_conceded'].append(home_goals)
    team_stats[away_team]['assists'].append(away_ast)
    team_stats[away_team]['xG'].append(away_xG)


team_calendar_dir = '/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/2425_Calendars/Team_Calendars'

csv_files = [f for f in os.listdir(team_calendar_dir) if f.endswith('.csv')]

def feature_engineering_new_matches(df, team_stats, window=5):
    for idx, row in df.iterrows():
        home_team = row['Home Team']
        away_team = row['Away Team']

        home_avg_goals_scored = sum(team_stats[home_team]['goals_scored'][-window:]) / len(team_stats[home_team]['goals_scored'][-window:])
        home_avg_goals_conceded = sum(team_stats[home_team]['goals_conceded'][-window:]) / len(team_stats[home_team]['goals_conceded'][-window:])
        home_avg_assists = sum(team_stats[home_team]['assists'][-window:]) / len(team_stats[home_team]['assists'][-window:])
        home_avg_xG = sum(team_stats[home_team]['xG'][-window:]) / len(team_stats[home_team]['xG'][-window:])
        
        away_avg_goals_scored = sum(team_stats[away_team]['goals_scored'][-window:]) / len(team_stats[away_team]['goals_scored'][-window:])
        away_avg_goals_conceded = sum(team_stats[away_team]['goals_conceded'][-window:]) / len(team_stats[away_team]['goals_conceded'][-window:])
        away_avg_assists = sum(team_stats[away_team]['assists'][-window:]) / len(team_stats[away_team]['assists'][-window:])
        away_avg_xG = sum(team_stats[away_team]['xG'][-window:]) / len(team_stats[away_team]['xG'][-window:])

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
    file_path = os.path.join(team_calendar_dir, csv_file)
    df = pd.read_csv(file_path)
    
    df['Home Team'] = df['Home Team'].map(team_name_mapping)
    df['Away Team'] = df['Away Team'].map(team_name_mapping)

    df.dropna(subset=['Home Team', 'Away Team'], inplace=True)

    df = df.drop(columns=['Date', 'Matchday'])
    
    df = feature_engineering_new_matches(df, team_stats)
    
    new_matches_features = df[features]
    
    predicted_home_xG_new = model_home_final.predict(new_matches_features)
    predicted_away_xG_new = model_away_final.predict(new_matches_features)
    
    df['Predicted_Home_xG'] = predicted_home_xG_new.round(4)
    df['Predicted_Away_xG'] = predicted_away_xG_new.round(4)
    
    output_file_path = os.path.join('/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/Model_Jihang/predicted_teams', 
                                    'predicted_' + csv_file)
    
    df = df.drop(columns=['Home_avg_goals_scored', 'Home_avg_goals_conceded', 'Home_avg_assists', 'Home_avg_xG', 
                          'Away_avg_goals_scored', 'Away_avg_goals_conceded', 'Away_avg_assists', 'Away_avg_xG'])
    
    df.to_csv(output_file_path, index=False)

