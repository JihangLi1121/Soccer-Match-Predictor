import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np
import os

file_path = '/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/data/cleaned_data/bundesliga_cleaned.csv'
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

teams = pd.concat([data['Home Team'], data['Away Team']]).unique()
team_stats = {team: {'goals_scored': [], 'goals_conceded': [], 'assists': [], 'xG': []} for team in teams}

# Feature engineering
def feature_engineering(df, team_stats, window=5):

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

    return df, team_stats

# Apply feature engineering
data, team_stats = feature_engineering(data, team_stats)

# Select features and target variables
features = [
    'Home_avg_goals_scored', 'Home_avg_goals_conceded', 'Home_avg_assists', 'Home_avg_xG',
    'Away_avg_goals_scored', 'Away_avg_goals_conceded', 'Away_avg_assists', 'Away_avg_xG'
]

# Convert the regression targets into classification targets
def get_class(home_goals, away_goals):
    if home_goals > away_goals:
        return 'win'
    elif home_goals < away_goals:
        return 'loss'
    else:
        return 'draw'

data['Result_Home'] = data.apply(lambda row: get_class(row['Home Goals'], row['Away Goals']), axis=1)
data['Result_Away'] = data.apply(lambda row: get_class(row['Away Goals'], row['Home Goals']), axis=1)

# Define the features and target variables for classification
X = data[features]
y_home = data['Result_Home']
y_away = data['Result_Away']

# Split the data into training and test sets
X_train, X_test, y_train_home, y_test_home = train_test_split(X, y_home, test_size=0.2, random_state=42)
_, _, y_train_away, y_test_away = train_test_split(X, y_away, test_size=0.2, random_state=42)

# Define the RandomForestClassifier model
model_home_rf = RandomForestClassifier(random_state=42)
model_away_rf = RandomForestClassifier(random_state=42)

# Train the model for home team results
model_home_rf.fit(X_train, y_train_home)

# Train the model for away team results
model_away_rf.fit(X_train, y_train_away)

# Perform cross-validation for the home team model
cv_scores_home = cross_val_score(model_home_rf, X, y_home, cv=5, scoring='accuracy')

# Perform cross-validation for the away team model
cv_scores_away = cross_val_score(model_away_rf, X, y_away, cv=5, scoring='accuracy')

# Calculate the mean and standard deviation of the cross-validation scores
mean_cv_score_home = cv_scores_home.mean()
std_cv_score_home = cv_scores_home.std()

mean_cv_score_away = cv_scores_away.mean()
std_cv_score_away = cv_scores_away.std()

print(f'Home Model (RandomForestClassifier) CV Mean Accuracy: {mean_cv_score_home:.4f} (± {std_cv_score_home:.4f})')
print(f'Away Model (RandomForestClassifier) CV Mean Accuracy: {mean_cv_score_away:.4f} (± {std_cv_score_away:.4f})')

# Make predictions on the test set for home team
y_pred_home_rf = model_home_rf.predict(X_test)

# Make predictions on the test set for away team
y_pred_away_rf = model_away_rf.predict(X_test)

# Evaluate the home team model
accuracy_home_rf = accuracy_score(y_test_home, y_pred_home_rf)
conf_matrix_home_rf = confusion_matrix(y_test_home, y_pred_home_rf)
class_report_home_rf = classification_report(y_test_home, y_pred_home_rf)

# Evaluate the away team model
accuracy_away_rf = accuracy_score(y_test_away, y_pred_away_rf)
conf_matrix_away_rf = confusion_matrix(y_test_away, y_pred_away_rf)
class_report_away_rf = classification_report(y_test_away, y_pred_away_rf)

print(f'Home Model (RandomForestClassifier) Test Accuracy: {accuracy_home_rf:.4f}')
print(f'Classification Report (Home Model):\n{class_report_home_rf}')

print(f'Away Model (RandomForestClassifier) Test Accuracy: {accuracy_away_rf:.4f}')
print(f'Classification Report (Away Model):\n{class_report_away_rf}')

team_calendar_dir = '/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/2425_Calendars/Team_Calendars'

csv_files = [f for f in os.listdir(team_calendar_dir) if f.endswith('.csv')]

def feature_engineering_for_new_match(home_team, away_team, team_stats, window=5):
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
    
    # Create a feature vector as a DataFrame with feature names
    features = pd.DataFrame({
        'Home_avg_goals_scored': [home_avg_goals_scored],
        'Home_avg_goals_conceded': [home_avg_goals_conceded],
        'Home_avg_assists': [home_avg_assists],
        'Home_avg_xG': [home_avg_xG],
        'Away_avg_goals_scored': [away_avg_goals_scored],
        'Away_avg_goals_conceded': [away_avg_goals_conceded],
        'Away_avg_assists': [away_avg_assists],
        'Away_avg_xG': [away_avg_xG]
    })
    return features

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

    predictions = []
    
    for index, row in df.iterrows():
        home_team = row['Home Team']
        away_team = row['Away Team']
        
        # Prepare the feature vector for the match
        features_for_match = feature_engineering_for_new_match(home_team, away_team, team_stats)
        
        # Predict the probabilities using the trained model for home team
        predicted_probabilities_home = model_home_rf.predict_proba(features_for_match)
        predicted_probabilities_away = model_away_rf.predict_proba(features_for_match)
        
        # Get the class labels
        class_labels = model_home_rf.classes_
        
        # Create a dictionary to map class labels to probabilities
        home_prob_dict = {class_labels[i]: predicted_probabilities_home[0][i] for i in range(len(class_labels))}
        away_prob_dict = {class_labels[i]: predicted_probabilities_away[0][i] for i in range(len(class_labels))}
    
        # Append the results to the predictions list
        predictions.append({
            'Home Team': home_team,
            'Away Team': away_team,
            'Home Win Probability': home_prob_dict['win'],
            'Draw Probability': home_prob_dict['draw'],
            'Away Win Probability': away_prob_dict['win'],
        })
    
    predictions_df = pd.DataFrame(predictions)
    
    output_file_path = os.path.join('/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/Model_Jihang/predicted_teams_classify', 
                                    'predicted_' + csv_file.replace('.csv', '.json'))
    
    predictions_df.to_json(output_file_path)