import os  # File operations

import pandas as pd  # Data manipulation


# Define the path where the matchday CSV files are stored
matchday_path = '/Users/joathcarrera/Desktop/CSE115A/Soccer-Match-Predictor/2425_Calendars/Matchday_Calendars'

# Define the path where the team-specific CSV files will be saved
output_path = '/Users/joathcarrera/Desktop/CSE115A/Soccer-Match-Predictor/2425_Calendars/Team_Calendars'


# Listing all the CSV files in the matchday directory
matchday_files = [f for f in os.listdir(matchday_path) if f.endswith('.csv')]

# Sorting the list of CSV files in alphabetical order
matchday_files.sort()

# Reading each CSV file into a DataFrame
matchdays = [pd.read_csv(os.path.join(matchday_path, file)) for file in matchday_files]

# Creating a set of unique teams from the matchday DataFrames
teams = set()
for df in matchdays:
    teams.update(df['Home Team'].unique())
    teams.update(df['Away Team'].unique())

# Creating a dictionary to store matches for each team
team_matches = {team: [] for team in teams}

# Loop through matchday DataFrames and add each row to the corresponding team's list.
# Matches are added to both home and away team's lists for complete match history.

for df in matchdays:

    # Loop over each row in the current matchday DataFrame
    for index, row in df.iterrows():

        # Get the names of the teams from the current row
        home_team = row['Home Team']
        away_team = row['Away Team']
        
        # Add the current row to the list for the home team and the away team
        team_matches[home_team].append(row)
        team_matches[away_team].append(row)

# Create a DataFrame for each team and save it to a separate CSV file
for team, matches in team_matches.items():
    
    team_df = pd.DataFrame(matches)
    
    # Save the DataFrame to a CSV file without an index column
    team_df.to_csv(os.path.join(output_path, f'{team}.csv'), index=False)

