# Required libraries for the expected goals mode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.linear_model import LogisticRegression
import joblib
import os
import json

# Path the json events folder
path = "/Users/charlie/Documents/NEA Project II/open-data/data/events"
# List to store the events data
data = []

# Iterating over all files in the events path
for file in os.listdir(path):
    # Creating the specific path name of the file
    path = os.path.join(path, file)
    # Reading the content of the json file
    content = open(path, "r")
    # Saving the content to a variable
    events = json.load(content)

    # Iterating over the content to locate the shots
    for event in events:
        # Locating the shots from within the file
        if event ["type"]["name"] == "Shot":
            # Saving the relevant data to a new variable
            shot = {
                "x": event["location"][0],
                "y": event["location"][1],
                "body_part": event["shot"]["body_part"]["name"],
                "outcome": event["shot"]["outcome"]["name"],
                "statsbomb_xg": event["shot"]["statsbomb_xg"]["name"]
            }
            # Appending the data to the list
            data.append(shot)



# Loading the data into a pandas Dataframe
shots = pd.DataFrame(data)

# Calculating the distance from the goal and angle of the shot
shots['Angle'] = np.arctan(np.absolute(shots['x'] - 40) / np.absolute(shots['y'] - 120))
shots['Distance'] = np.sqrt((shots['x'] - 120)**2 + (shots['y'] - 40)**2)

# Creating a binary column
shots["Binary"] = 0
# Assigning a binary value to each shot
for index, row in shots.iterrows():
    if row['outcome'] == 'Goal':
        shots.at[index, 'Binary'] = 1

# Creating the Expected Goals Model
xGmodel = joblib.load('xGmodel.pkl')       

# Calculating expected goals
xG = xGmodel.predict_proba(shots[['Distance', 'Angle']])[:,1]
shots['xG'] = xG
shots.to_csv('expected goals.csv')


