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

# Loading the datasets
training_dataset = "/Users/charlie/Documents/NEA Project II/Football-Shots-Dataset-for-xG-models/data/Shots.csv"
# Saving the dataset as a DataFrame
training_shots = pd.read_csv(training_dataset)

# Variables to be used when calculating the distance from the goal and angle of the shot
goal_x = 1.0
goal_y = 0.5
goal_width = 0.073
goal_top_y = goal_y + goal_width / 2
goal_bottom_y = goal_y - goal_width / 2
goal_span = goal_top_y - goal_bottom_y

# Calculating angle and distance
training_shots['Angle'] = np.arctan2(goal_span, goal_x - training_shots[' X'])
training_shots['Distance'] = np.sqrt((goal_x - training_shots[' X'])**2 + (goal_y - training_shots[' Y'])**2)

# Encoding the shot types 
type_encoder = OneHotEncoder(sparse_output=False)
encoded_shots = type_encoder.fit_transform(training_shots[[' shotType']])
encoded_shot_types = pd.DataFrame(encoded_shots, columns=type_encoder.get_feature_names_out([' shotType']))

# Creating a binary column for the shot outcome
training_shots['Binary'] = training_shots.apply(
    lambda row: 1 if (row[' h_a'] == 1 and row[' h_goals'] == 1) or 
                    (row[' h_a'] == 0 and row[' a_goals'] == 1) else 0,
    axis=1
)

# Training and saving the model
X = pd.concat([training_shots[['Distance', 'Angle']], encoded_shot_types], axis=1)
y = training_shots['Binary']
xGmodel = LogisticRegression()
xGmodel.fit(X, y)
# Saving the model for future use
joblib.dump(xGmodel, 'xG_model.pkl')
