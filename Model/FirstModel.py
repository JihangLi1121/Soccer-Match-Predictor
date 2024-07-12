import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer

# Load the data
data_2021 = pd.read_csv('C:/Users/larry/OneDrive/桌面/Soccer-Match-Predictor-main/data/bundesliga_2021.csv')
data_2022 = pd.read_csv('C:/Users/larry/OneDrive/桌面/Soccer-Match-Predictor-main/data/bundesliga_2022.csv')
data_2023 = pd.read_csv('C:/Users/larry/OneDrive/桌面/Soccer-Match-Predictor-main/data/bundesliga_2023.csv')

# Combine the datasets
data = pd.concat([data_2021, data_2022, data_2023])

# Extract relevant features and the target variable
data['Outcome'] = data.apply(lambda row: 'HomeWin' if row['Home Goals'] > row['Away Goals'] else ('AwayWin' if row['Home Goals'] < row['Away Goals'] else 'Draw'), axis=1)
features = ['Home Team', 'Away Team', 'Home xG', 'Away xG']  # Removed 'Home Goals' and 'Away Goals'
X = data[features]
y = data['Outcome']

# Encode categorical variables
label_encoder = LabelEncoder()
X['Home Team'] = label_encoder.fit_transform(X['Home Team'])
X['Away Team'] = label_encoder.transform(X['Away Team'])
y = label_encoder.fit_transform(y)

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions and evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
classification_report_str = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:')
print(classification_report_str)


