import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Define the absolute paths to CSV files
base_path = "/Users/sergioelizaldecasarrubiasjr./Documents/GitHub/Soccer-Match-Predictor/data/cleaned_data/"
data_2021_path = os.path.join(base_path, "bundesliga_2021_cleaned.csv")
data_2022_path = os.path.join(base_path, "bundesliga_2022_cleaned.csv")
data_2023_path = os.path.join(base_path, "bundesliga_2023_cleaned.csv")

# Load data
data_2021 = pd.read_csv(data_2021_path)
data_2022 = pd.read_csv(data_2022_path)
data_2023 = pd.read_csv(data_2023_path)

# Adding weights to dataframes
data_2021["weight"] = 1
data_2022["weight"] = 2
data_2023["weight"] = 3

# Concatenate data
data = pd.concat([data_2021, data_2022, data_2023], ignore_index=True)


# Calculate weighted average goals scored in the last n matches
def weighted_average_goals_last_n_matches(data, n=5):
    # Calculate weighted average goals scored in the last n matches for Home Team
    data["weighted_home_goals"] = data["Home Goals"] * data["weight"]
    data["avg_home_goals_scored"] = data.groupby("Home Team")[
        "weighted_home_goals"
    ].rolling(n, min_periods=1).mean().reset_index(level=0, drop=True) / data.groupby(
        "Home Team"
    )[
        "weight"
    ].rolling(
        n, min_periods=1
    ).sum().reset_index(
        level=0, drop=True
    )

    # Calculate weighted average goals scored in the last n matches for Away Team
    data["weighted_away_goals"] = data["Away Goals"] * data["weight"]
    data["avg_away_goals_scored"] = data.groupby("Away Team")[
        "weighted_away_goals"
    ].rolling(n, min_periods=1).mean().reset_index(level=0, drop=True) / data.groupby(
        "Away Team"
    )[
        "weight"
    ].rolling(
        n, min_periods=1
    ).sum().reset_index(
        level=0, drop=True
    )

    return data


data = weighted_average_goals_last_n_matches(data)


# Encode the outcome (win, draw, loss)
def encode_outcome(row):
    if row["Home Goals"] > row["Away Goals"]:
        return "win"
    elif row["Home Goals"] == row["Away Goals"]:
        return "draw"
    else:
        return "loss"


data["outcome"] = data.apply(encode_outcome, axis=1)

# Preprocess the data
X = data[
    ["avg_home_goals_scored", "avg_away_goals_scored"]
]  # Using both avg_home_goals_scored and avg_away_goals_scored as features
y = data["outcome"]

# Encode the categorical target variable
le = LabelEncoder()
y = le.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train the random forest classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train, sample_weight=data.loc[X_train.index, "weight"])

# Predict and evaluate
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
