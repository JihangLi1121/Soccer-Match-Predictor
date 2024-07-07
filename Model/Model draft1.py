import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error
from sklearn.impute import SimpleImputer

# Load the data
data_2021 = pd.read_csv('C:/Users/larry/OneDrive/桌面/Soccer-Match-Predictor-main/data/bundesliga_2021.csv')
data_2022 = pd.read_csv('C:/Users/larry/OneDrive/桌面/Soccer-Match-Predictor-main/data/bundesliga_2022.csv')
data_2023 = pd.read_csv('C:/Users/larry/OneDrive/桌面/Soccer-Match-Predictor-main/data/bundesliga_2023.csv')

data = pd.concat([data_2021, data_2022, data_2023])

for index, value in data['Away Goals'].items():
    if pd.isna(value):  # Check if value is NaN
        data = data.drop(index)  # Remove row with NaN value



# Extract relevant features without xG
features = ['Home Team', 'Away Team']
X = data[features]

# Targets
y_outcome = data.apply(lambda row: 'HomeWin' if row['Home Goals'] > row['Away Goals'] else ('AwayWin' if row['Home Goals'] < row['Away Goals'] else 'Draw'), axis=1)
y_home_goals = data['Home Goals']
y_away_goals = data['Away Goals']


# Encode categorical variables
label_encoder = LabelEncoder()
X['Home Team'] = label_encoder.fit_transform(X['Home Team'])
X['Away Team'] = label_encoder.transform(X['Away Team'])
y_outcome = label_encoder.fit_transform(y_outcome)

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

# Split the data for outcome prediction
X_train_outcome, X_test_outcome, y_train_outcome, y_test_outcome = train_test_split(X, y_outcome, test_size=0.2, random_state=42)

# Split the data for home and away score predictions
X_train_home, X_test_home, y_train_home, y_test_home = train_test_split(X, y_home_goals, test_size=0.2, random_state=42)
X_train_away, X_test_away, y_train_away, y_test_away = train_test_split(X, y_away_goals, test_size=0.2, random_state=42)


# Initialize and train the models
model_outcome = RandomForestClassifier(n_estimators=100, random_state=42)
model_home_goals = RandomForestRegressor(n_estimators=100, random_state=42)
model_away_goals = RandomForestRegressor(n_estimators=100, random_state=42)


model_outcome.fit(X_train_outcome, y_train_outcome)
model_home_goals.fit(X_train_home, y_train_home)
model_away_goals.fit(X_train_away, y_train_away)

# Evaluate the models
y_pred_outcome = model_outcome.predict(X_test_outcome)
y_pred_home = model_home_goals.predict(X_test_home)
y_pred_away = model_away_goals.predict(X_test_away)

accuracy = accuracy_score(y_test_outcome, y_pred_outcome)
classification_report_str = classification_report(y_test_outcome, y_pred_outcome, target_names=label_encoder.classes_)
mse_home = mean_squared_error(y_test_home, y_pred_home)
mse_away = mean_squared_error(y_test_away, y_pred_away)

print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:')
print(classification_report_str)
print(f'Home Goals Prediction MSE: {mse_home:.2f}')
print(f'Away Goals Prediction MSE: {mse_away:.2f}')
