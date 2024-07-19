import pandas as pd # Data manipulation and analysis

# Machine learning model selection and evaluation
from sklearn.model_selection import train_test_split  # Splitting data into training and testing sets
from sklearn.model_selection import GridSearchCV  # Hyperparameter tuning using grid search
from sklearn.model_selection import cross_val_score  # Evaluating model performance using cross-validation

# Regression models
from sklearn.ensemble import RandomForestRegressor  # Random Forest regression
from sklearn.linear_model import LinearRegression  # Linear regression
from sklearn.svm import SVR  # Support Vector Regression
from sklearn.neighbors import KNeighborsRegressor  # k-Nearest Neighbors regression
from sklearn.ensemble import GradientBoostingRegressor  # Gradient Boosting regression
from xgboost import XGBRegressor  # XGBoost regression
from sklearn.linear_model import Ridge, Lasso  # Ridge and Lasso regression

# Metrics for evaluating model performance
from sklearn.metrics import mean_squared_error  # Calculating Mean Squared Error
from sklearn.metrics import r2_score  # Calculating R-squared metric

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

# RandomForestRegressor

# Best parameters for RandomForestRegressor models
best_params_home = {'bootstrap': True, 'max_depth': 10, 'min_samples_leaf': 2, 'min_samples_split': 10, 'n_estimators': 200}
best_params_away = {'bootstrap': True, 'max_depth': None, 'min_samples_leaf': 4, 'min_samples_split': 10, 'n_estimators': 100}

# Define the final RandomForestRegressor models
model_home_final = RandomForestRegressor(**best_params_home, random_state=42)
model_away_final = RandomForestRegressor(**best_params_away, random_state=42)

# Train the model for home team expected goals
model_home_final.fit(X_train, y_train_home)

# Train the model for away team expected goals
model_away_final.fit(X_train, y_train_away)

# Perform cross-validation for the home team model
cv_scores_home = cross_val_score(model_home_final, X, y_home, cv=5, scoring='neg_mean_squared_error')

# Perform cross-validation for the away team model
cv_scores_away = cross_val_score(model_away_final, X, y_away, cv=5, scoring='neg_mean_squared_error')

# Calculate the mean and standard deviation of the cross-validation scores
mean_cv_score_home = -cv_scores_home.mean()
std_cv_score_home = cv_scores_home.std()

mean_cv_score_away = -cv_scores_away.mean()
std_cv_score_away = cv_scores_away.std()

print(f'Home Model (RandomForestRegressor) CV Mean MSE: {mean_cv_score_home:.4f} (± {std_cv_score_home:.4f})')
print(f'Away Model (RandomForestRegressor) CV Mean MSE: {mean_cv_score_away:.4f} (± {std_cv_score_away:.4f})')

# Make predictions on the test set for home team
y_pred_home_final = model_home_final.predict(X_test)

# Make predictions on the test set for away team
y_pred_away_final = model_away_final.predict(X_test)

# Calculate R-squared for the home team model
r2_home_final = r2_score(y_test_home, y_pred_home_final)
mse_home_final = mean_squared_error(y_test_home, y_pred_home_final)

# Calculate R-squared for the away team model
r2_away_final = r2_score(y_test_away, y_pred_away_final)
mse_away_final = mean_squared_error(y_test_away, y_pred_away_final)

print(f'Home Model (RandomForestRegressor) R-squared: {r2_home_final:.4f}')
print(f'Home Model (RandomForestRegressor) MSE: {mse_home_final:.4f}')
print(f'Away Model (RandomForestRegressor) R-squared: {r2_away_final:.4f}')
print(f'Away Model (RandomForestRegressor) MSE: {mse_away_final:.4f}')

# LinearRegression

model_home_lr = LinearRegression()
model_away_lr = LinearRegression()

# Perform cross-validation for the home team model
cv_scores_home_lr = cross_val_score(model_home_lr, X, y_home, cv=5, scoring='neg_mean_squared_error')

# Perform cross-validation for the away team model
cv_scores_away_lr = cross_val_score(model_away_lr, X, y_away, cv=5, scoring='neg_mean_squared_error')

# Calculate the mean and standard deviation of the cross-validation scores
mean_cv_score_home_lr = -cv_scores_home_lr.mean()
std_cv_score_home_lr = cv_scores_home_lr.std()

mean_cv_score_away_lr = -cv_scores_away_lr.mean()
std_cv_score_away_lr = cv_scores_away_lr.std()

print(f'Home Model (Linear Regression) CV Mean MSE: {mean_cv_score_home_lr:.4f} (± {std_cv_score_home_lr:.4f})')
print(f'Away Model (Linear Regression) CV Mean MSE: {mean_cv_score_away_lr:.4f} (± {std_cv_score_away_lr:.4f})')

model_home_lr = LinearRegression()
model_away_lr = LinearRegression()

model_home_lr.fit(X_train, y_train_home)
model_away_lr.fit(X_train, y_train_away)

y_pred_home_lr = model_home_lr.predict(X_test)
mse_home_lr = mean_squared_error(y_test_home, y_pred_home_lr)

y_pred_away_lr = model_away_lr.predict(X_test)
mse_away_lr = mean_squared_error(y_test_away, y_pred_away_lr)

print(f'(Linear Regression) Test Set Mean Squared Error for Home Model: {mse_home_lr:.4f}')
print(f'(Linear Regression) Test Set Mean Squared Error for Away Model: {mse_away_lr:.4f}')

# Calculate R-squared for the home team model
r2_home_lr = r2_score(y_test_home, y_pred_home_lr)
mse_home_lr = mean_squared_error(y_test_home, y_pred_home_lr)

# Calculate R-squared for the away team model
r2_away_lr = r2_score(y_test_away, y_pred_away_lr)
mse_away_lr = mean_squared_error(y_test_away, y_pred_away_lr)

print(f'Home Model (Linear Regression) R-squared: {r2_home_lr:.4f}')
print(f'Away Model (Linear Regression) R-squared: {r2_away_lr:.4f}')

# SVR

# Define the model
model_home_svr = SVR()
model_away_svr = SVR()

# Perform cross-validation for the home team model
cv_scores_home_svr = cross_val_score(model_home_svr, X, y_home, cv=5, scoring='neg_mean_squared_error')

# Perform cross-validation for the away team model
cv_scores_away_svr = cross_val_score(model_away_svr, X, y_away, cv=5, scoring='neg_mean_squared_error')

# Calculate the mean and standard deviation of the cross-validation scores
mean_cv_score_home_svr = -cv_scores_home_svr.mean()
std_cv_score_home_svr = cv_scores_home_svr.std()

mean_cv_score_away_svr = -cv_scores_away_svr.mean()
std_cv_score_away_svr = cv_scores_away_svr.std()

print(f'Home Model (SVR) CV Mean MSE: {mean_cv_score_home_svr:.4f} (± {std_cv_score_home_svr:.4f})')
print(f'Away Model (SVR) CV Mean MSE: {mean_cv_score_away_svr:.4f} (± {std_cv_score_away_svr:.4f})')

# KNN

# Define the model
model_home_knn = KNeighborsRegressor()
model_away_knn = KNeighborsRegressor()

# Perform cross-validation for the home team model
cv_scores_home_knn = cross_val_score(model_home_knn, X, y_home, cv=5, scoring='neg_mean_squared_error')

# Perform cross-validation for the away team model
cv_scores_away_knn = cross_val_score(model_away_knn, X, y_away, cv=5, scoring='neg_mean_squared_error')

# Calculate the mean and standard deviation of the cross-validation scores
mean_cv_score_home_knn = -cv_scores_home_knn.mean()
std_cv_score_home_knn = cv_scores_home_knn.std()

mean_cv_score_away_knn = -cv_scores_away_knn.mean()
std_cv_score_away_knn = cv_scores_away_knn.std()

print(f'Home Model (KNN) CV Mean MSE: {mean_cv_score_home_knn:.4f} (± {std_cv_score_home_knn:.4f})')
print(f'Away Model (KNN) CV Mean MSE: {mean_cv_score_away_knn:.4f} (± {std_cv_score_away_knn:.4f})')

# GradientBoostingRegressor

# Define the Gradient Boosting Regressor model
gbr = GradientBoostingRegressor(random_state=42)

# Define the hyperparameter grid
param_grid = {
    'n_estimators': [100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 4, 5]
}

# Use GridSearchCV to find the best hyperparameters
grid_search_home = GridSearchCV(estimator=gbr, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_away = GridSearchCV(estimator=gbr, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)

# Perform Grid Search
grid_search_home.fit(X_train, y_train_home)
grid_search_away.fit(X_train, y_train_away)

# Get the best parameters
best_params_home = grid_search_home.best_params_
best_params_away = grid_search_away.best_params_

# Train the best Gradient Boosting model on the training data
best_gbr_home = GradientBoostingRegressor(**best_params_home, random_state=42)
best_gbr_home.fit(X_train, y_train_home)
best_gbr_away = GradientBoostingRegressor(**best_params_away, random_state=42)
best_gbr_away.fit(X_train, y_train_away)

# Make predictions on the test set for home team
y_pred_gbr_home = best_gbr_home.predict(X_test)

# Make predictions on the test set for away team
y_pred_gbr_away = best_gbr_away.predict(X_test)

# Calculate R-squared and MSE for the home team model
r2_gbr_home = r2_score(y_test_home, y_pred_gbr_home)
mse_gbr_home = mean_squared_error(y_test_home, y_pred_gbr_home)

# Calculate R-squared and MSE for the away team model
r2_gbr_away = r2_score(y_test_away, y_pred_gbr_away)
mse_gbr_away = mean_squared_error(y_test_away, y_pred_gbr_away)

print(f'Home Model (Gradient Boosting) R-squared: {r2_gbr_home:.4f}')
print(f'Home Model (Gradient Boosting) MSE: {mse_gbr_home:.4f}')
print(f'Away Model (Gradient Boosting) R-squared: {r2_gbr_away:.4f}')
print(f'Away Model (Gradient Boosting) MSE: {mse_gbr_away:.4f}')

# XGBRegressor

# Define the model
model_home_xgb = XGBRegressor(random_state=42)
model_away_xgb = XGBRegressor(random_state=42)

# Perform cross-validation for the home team model
cv_scores_home_xgb = cross_val_score(model_home_xgb, X, y_home, cv=5, scoring='neg_mean_squared_error')

# Perform cross-validation for the away team model
cv_scores_away_xgb = cross_val_score(model_away_xgb, X, y_away, cv=5, scoring='neg_mean_squared_error')

# Calculate the mean and standard deviation of the cross-validation scores
mean_cv_score_home_xgb = -cv_scores_home_xgb.mean()
std_cv_score_home_xgb = cv_scores_home_xgb.std()

mean_cv_score_away_xgb = -cv_scores_away_xgb.mean()
std_cv_score_away_xgb = cv_scores_away_xgb.std()

print(f'Home Model (XGBoost) CV Mean MSE: {mean_cv_score_home_xgb:.4f} (± {std_cv_score_home_xgb:.4f})')
print(f'Away Model (XGBoost) CV Mean MSE: {mean_cv_score_away_xgb:.4f} (± {std_cv_score_away_xgb:.4f})')

# Define the Ridge and Lasso regression models
ridge = Ridge()
lasso = Lasso()

# Define the hyperparameter grid for Ridge and Lasso
param_grid = {
    'alpha': [0.01, 0.1, 1, 10, 100]
}

# Use GridSearchCV to find the best hyperparameters for Ridge
grid_search_ridge_home = GridSearchCV(estimator=ridge, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_ridge_away = GridSearchCV(estimator=ridge, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)

# Use GridSearchCV to find the best hyperparameters for Lasso
grid_search_lasso_home = GridSearchCV(estimator=lasso, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
grid_search_lasso_away = GridSearchCV(estimator=lasso, param_grid=param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)

# Perform Grid Search for Ridge Regression
grid_search_ridge_home.fit(X_train, y_train_home)
grid_search_ridge_away.fit(X_train, y_train_away)

# Perform Grid Search for Lasso Regression
grid_search_lasso_home.fit(X_train, y_train_home)
grid_search_lasso_away.fit(X_train, y_train_away)

# Get the best parameters
best_params_ridge_home = grid_search_ridge_home.best_params_
best_params_ridge_away = grid_search_ridge_away.best_params_
best_params_lasso_home = grid_search_lasso_home.best_params_
best_params_lasso_away = grid_search_lasso_away.best_params_

# Train the best Ridge model on the training data
best_ridge_home = Ridge(**best_params_ridge_home)
best_ridge_home.fit(X_train, y_train_home)
best_ridge_away = Ridge(**best_params_ridge_away)
best_ridge_away.fit(X_train, y_train_away)

# Train the best Lasso model on the training data
best_lasso_home = Lasso(**best_params_lasso_home)
best_lasso_home.fit(X_train, y_train_home)
best_lasso_away = Lasso(**best_params_lasso_away)
best_lasso_away.fit(X_train, y_train_away)

# Evaluate the best Ridge model on the test data
y_pred_ridge_home = best_ridge_home.predict(X_test)
mse_ridge_home = mean_squared_error(y_test_home, y_pred_ridge_home)

y_pred_ridge_away = best_ridge_away.predict(X_test)
mse_ridge_away = mean_squared_error(y_test_away, y_pred_ridge_away)

# Evaluate the best Lasso model on the test data
y_pred_lasso_home = best_lasso_home.predict(X_test)
mse_lasso_home = mean_squared_error(y_test_home, y_pred_lasso_home)

y_pred_lasso_away = best_lasso_away.predict(X_test)
mse_lasso_away = mean_squared_error(y_test_away, y_pred_lasso_away)

print(f'Ridge Test Set Mean Squared Error for Home Model: {mse_ridge_home:.4f}')
print(f'Ridge Test Set Mean Squared Error for Away Model: {mse_ridge_away:.4f}')
print(f'Lasso Test Set Mean Squared Error for Home Model: {mse_lasso_home:.4f}')
print(f'Lasso Test Set Mean Squared Error for Away Model: {mse_lasso_away:.4f}')