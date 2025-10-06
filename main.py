# Required libraries for the expected goals mode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
import joblib
import os
import json

# Path the json events folder
path = "/Users/charlie/Documents/NEA Project II/open-data/data/events"
# List to store the events data
data = []

# Iterating over all files in the events path
for file in os.listdir(path):

    # Code can only run if the file is JSON
    if not file.endswith(".json"):
        continue

    # Creating the specific path name of the file
    file_path = os.path.join(path, file)
    # Reading the content of the json file
    with open(file_path, "r") as content:
        events = json.load(content)

    # Iterating over the content to locate the shots
    for event in events:
        try:
            # Locating the shots from within the file
            if event ["type"]["name"] == "Shot":
                # Attempts to access location 
                loc = event.get("location", [None, None])
                # Saving the relevant data to a new variable
                shot = {
                    "x": loc[0],
                    "y": loc[1],
                    "body_part": event["shot"]["body_part"]["name"],
                    "outcome": event["shot"]["outcome"]["name"],
                    "statsbomb_xg": event["shot"]["statsbomb_xg"]["name"]
                }
                # Appending the data to the list
                data.append(shot)
        # Ensuring the code does not crash
        except (TypeError, IndexError, KeyError):
            pass

# Loading the data into a pandas Dataframe
shots = pd.DataFrame(data)

# Calculating the distance from the goal and angle of the shot
shots['Angle'] = np.arctan(np.absolute(shots['x'] - 40) / np.absolute(shots['y'] - 120))
shots['Distance'] = np.sqrt((shots['x'] - 120)**2 + (shots['y'] - 40)**2)

# Encoding shot type as binary
encoder = OneHotEncoder(sparse=False)
shot_type_encoded = encoder.fit_transform(shots[['body_part']])
shot_types = pd.DataFrame(shot_type_encoded, columns=encoder.get_feature_names_out(['body_part']))

# Creating a binary column
shots["Binary"] = 0
# Assigning a binary value to each shot
for index, row in shots.iterrows():
    if row['outcome'] == 'Goal':
        shots.at[index, 'Binary'] = 1

# Training and saving the model
X = pd.concat([shots[['Distance', 'Angle']], shot_types], axis=1)
y = shots["Binary"]
xGmodel = LogisticRegression()
xGmodel.fit(X, y)
# Saving the model for future use
joblib.dump(xGmodel)



# Calculating expected goals
xG = xGmodel.predict_proba(shots[['Distance', 'Angle']])[:,1]
shots['xG'] = xG
shots.to_csv('expected goals.csv')


