# Data manipulation and visualization
import pandas as pd  # Data manipulation and analysis
import matplotlib.pyplot as plt  # Plotting library

# Machine learning preprocessing, model selection, and evaluation
from sklearn.preprocessing import LabelEncoder  # Encoding categorical data
from sklearn.model_selection import train_test_split, GridSearchCV  # Splitting data and hyperparameter tuning
from sklearn.ensemble import RandomForestRegressor  # Random Forest regression model
from sklearn.metrics import mean_absolute_error  # Error metric for regression


data = pd.read_csv('/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/data/cleaned_data/bundesliga_cleaned.csv')

missing_values = data.isnull().sum()

# Encode categorical features
label_encoder = LabelEncoder()
data['Home Team'] = label_encoder.fit_transform(data['Home Team'])
data['Away Team'] = label_encoder.fit_transform(data['Away Team'])

# Calculate aggregated statistics for home teams
team_stats = data.groupby('Home Team').agg({
    'Home Goals': 'mean',
    'Away Goals': 'mean',
    'Home Ast': 'mean',
    'Away Ast': 'mean',
    'Home xG': 'mean',
    'Away xG': 'mean'
}).rename(columns={
    'Home Goals': 'Avg Home Goals Scored',
    'Away Goals': 'Avg Home Goals Conceded',
    'Home Ast': 'Avg Home Assists',
    'Away Ast': 'Avg Home Assists Conceded',
    'Home xG': 'Avg Home xG',
    'Away xG': 'Avg Home xG Conceded'
})

# Calculate aggregated statistics for away teams
away_team_stats = data.groupby('Away Team').agg({
    'Home Goals': 'mean',
    'Away Goals': 'mean',
    'Home Ast': 'mean',
    'Away Ast': 'mean',
    'Home xG': 'mean',
    'Away xG': 'mean'
}).rename(columns={
    'Home Goals': 'Avg Away Goals Conceded',
    'Away Goals': 'Avg Away Goals Scored',
    'Home Ast': 'Avg Away Assists Conceded',
    'Away Ast': 'Avg Away Assists',
    'Home xG': 'Avg Away xG Conceded',
    'Away xG': 'Avg Away xG'
})

# Merge home and away team statistics
team_stats = team_stats.merge(away_team_stats, left_index=True, right_index=True, suffixes=('_Home', '_Away'))

# Merge statistics with the main dataset for home and away teams
data = data.merge(team_stats, left_on='Home Team', right_index=True)
data = data.merge(team_stats, left_on='Away Team', right_index=True, suffixes=('_HomeTeam', '_AwayTeam'))

# Define features and target variables
features = data.drop(columns=['Home Goals', 'Away Goals'])
target_home_goals = data['Home Goals']
target_away_goals = data['Away Goals']

# Split the data into training and testing sets
X_train, X_test, y_train_home, y_test_home, y_train_away, y_test_away = train_test_split(
    features, target_home_goals, target_away_goals, test_size=0.2, random_state=42
)

# Initialize and train Random Forest models for home and away goals
model_home_goals = RandomForestRegressor(random_state=42)
model_away_goals = RandomForestRegressor(random_state=42)

model_home_goals.fit(X_train, y_train_home)
model_away_goals.fit(X_train, y_train_away)

# Make predictions
pred_home_goals = model_home_goals.predict(X_test)
pred_away_goals = model_away_goals.predict(X_test)

# Calculate mean absolute error for the predictions
mae_home_goals = mean_absolute_error(y_test_home, pred_home_goals)
mae_away_goals = mean_absolute_error(y_test_away, pred_away_goals)

# use grid search to finetune hyper-parameters 

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# GridSearchCV for home goals
grid_search_home = GridSearchCV(estimator=RandomForestRegressor(random_state=42),
                                param_grid=param_grid,
                                cv=3,
                                n_jobs=-1,
                                scoring='neg_mean_absolute_error')

# GridSearchCV for away goals
grid_search_away = GridSearchCV(estimator=RandomForestRegressor(random_state=42),
                                param_grid=param_grid,
                                cv=3,
                                n_jobs=-1,
                                scoring='neg_mean_absolute_error')

# Fit GridSearchCV for home and away goals
grid_search_home.fit(X_train, y_train_home)
grid_search_away.fit(X_train, y_train_away)

# Extract best parameters and best scores from GridSearchCV
best_params_home = grid_search_home.best_params_
best_score_home = -grid_search_home.best_score_ 

best_params_away = grid_search_away.best_params_
best_score_away = -grid_search_away.best_score_

# Train the best Random Forest model on the training data
model_home_goals_best = RandomForestRegressor(**best_params_home, random_state=42)
model_away_goals_best = RandomForestRegressor(**best_params_away, random_state=42)

model_home_goals_best.fit(X_train, y_train_home)
model_away_goals_best.fit(X_train, y_train_away)

# Make predictions
pred_home_goals_best = model_home_goals_best.predict(X_test)
pred_away_goals_best = model_away_goals_best.predict(X_test)

# Calculate mean absolute error for the predictions
mae_home_goals_best = mean_absolute_error(y_test_home, pred_home_goals_best)
mae_away_goals_best = mean_absolute_error(y_test_away, pred_away_goals_best)

# Feature Importance Analysis

# Get feature importances from the model
importance_home = model_home_goals_best.feature_importances_
importance_away = model_away_goals_best.feature_importances_

# Get feature names
feature_names = X_train.columns

# Create a DataFrame for easy plotting
feature_importance_home = pd.DataFrame({'Feature': feature_names, 'Importance': importance_home})
feature_importance_away = pd.DataFrame({'Feature': feature_names, 'Importance': importance_away})

# Sort by importance
feature_importance_home = feature_importance_home.sort_values(by='Importance', ascending=False)
feature_importance_away = feature_importance_away.sort_values(by='Importance', ascending=False)

# Plot the feature importances
# plt.figure(figsize=(12, 6))

# plt.subplot(1, 2, 1)
# plt.title("Home Goals - Feature Importance")
# plt.barh(feature_importance_home['Feature'], feature_importance_home['Importance'])
# plt.gca().invert_yaxis()

# plt.subplot(1, 2, 2)
# plt.title("Away Goals - Feature Importance")
# plt.barh(feature_importance_away['Feature'], feature_importance_away['Importance'])
# plt.gca().invert_yaxis()

# Set a threshold for feature importance
importance_threshold = 0.01

important_features_home = feature_importance_home[feature_importance_home['Importance'] >= importance_threshold]['Feature']
important_features_away = feature_importance_away[feature_importance_away['Importance'] >= importance_threshold]['Feature']

important_features_combined = list(set(important_features_home).union(set(important_features_away)))

X_train_important = X_train[important_features_combined]
X_test_important = X_test[important_features_combined]

model_home_goals_refined = RandomForestRegressor(**best_params_home, random_state=42)
model_away_goals_refined = RandomForestRegressor(**best_params_away, random_state=42)

# Train the model on the training data with important features
model_home_goals_refined.fit(X_train_important, y_train_home)
model_away_goals_refined.fit(X_train_important, y_train_away)

# Predict on the test data
pred_home_goals_refined = model_home_goals_refined.predict(X_test_important)
pred_away_goals_refined = model_away_goals_refined.predict(X_test_important)

# Evaluate the model's performance
mae_home_goals_refined = mean_absolute_error(y_test_home, pred_home_goals_refined)
mae_away_goals_refined = mean_absolute_error(y_test_away, pred_away_goals_refined)

print(f'Refined Model MAE for Home Goals: {mae_home_goals_refined}')
print(f'Refined Model MAE for Away Goals: {mae_away_goals_refined}')

# upcoming_matches_path = '/Users/jihangli/ucsc_cse_course/CSE115A/Soccer-Match-Predictor/2425_Calendars/Team_Calendars/FC Augsburg.csv'
# upcoming_matches = pd.read_csv(upcoming_matches_path)

# team_name_mapping = {
#     '1. FC Heidenheim 1846': 'Heidenheim',
#     '1. FC Union Berlin': 'Union Berlin',
#     '1. FSV Mainz 05': 'Mainz 05',
#     'Bayer 04 Leverkusen': 'Bayer Leverkusen',
#     'Borussia Dortmund': 'Dortmund',
#     'Borussia Mönchengladbach': 'Mönchengladbach',
#     'Eintracht Frankfurt': 'Eintracht Frankfurt',
#     'FC Augsburg': 'Augsburg',
#     'FC Bayern München': 'Bayern Munich',
#     'FC St. Pauli': 'St. Pauli',
#     'Holstein Kiel': 'Holstein Kiel',
#     'RB Leipzig': 'RB Leipzig',
#     'Sport-Club Freiburg': 'Freiburg',
#     'SV Werder Bremen': 'Werder Bremen',
#     'TSG Hoffenheim': 'Hoffenheim',
#     'VfB Stuttgart': 'Stuttgart',
#     'VfL Bochum 1848': 'Bochum',
#     'VfL Wolfsburg': 'Wolfsburg'
# }

# # Apply the mapping to Home Team and Away Team columns
# upcoming_matches['Home Team'] = upcoming_matches['Home Team'].map(team_name_mapping)
# upcoming_matches['Away Team'] = upcoming_matches['Away Team'].map(team_name_mapping)

# # Handle any missing values if the mapping failed
# upcoming_matches.dropna(subset=['Home Team', 'Away Team'], inplace=True)

# upcoming_matches = upcoming_matches.drop(columns=['Date', 'Matchday'])

# # Encode the team names using the label encoder from the training data
# label_encoder = LabelEncoder()
# label_encoder.fit(list(team_name_mapping.values()))

# upcoming_matches['Home Team'] = label_encoder.transform(upcoming_matches['Home Team'])
# upcoming_matches['Away Team'] = label_encoder.transform(upcoming_matches['Away Team'])

# # Merge with team statistics to get all necessary features
# upcoming_matches = upcoming_matches.merge(data[['Home xG', 'Home Ast']], left_on='Home Team', right_index=True, suffixes=('', '_HomeTeam'))
# upcoming_matches = upcoming_matches.merge(data[['Away xG', 'Away Ast']], left_on='Away Team', right_index=True, suffixes=('_HomeTeam', '_AwayTeam'))

# # Select the columns relevant for the model
# upcoming_matches = upcoming_matches[['Home Ast', 'Away Ast', 'Home xG', 'Away xG']]

# # print(upcoming_matches.head())

# # Function to simulate a single match multiple times
# def simulate_match(model, match_data, n_simulations=1):
#     simulations = []
#     for _ in range(n_simulations):
#         prediction = model.predict(match_data)
#         simulations.append(prediction[0])
#     return simulations

# first_match = upcoming_matches.iloc[0].values.reshape(1, -1)

# home_goals_simulations = simulate_match(model_home_goals_refined, first_match, n_simulations=1)
# away_goals_simulations = simulate_match(model_away_goals_refined, first_match, n_simulations=1)

# # Store results in a DataFrame
# simulation_results = pd.DataFrame({
#     'Home Goals Simulations': home_goals_simulations,
#     'Away Goals Simulations': away_goals_simulations
# })

# # write the simulation result
# with open('result.csv', 'a') as f:
#     simulation_results.to_csv(f, header=f.tell()==0, index=False)





