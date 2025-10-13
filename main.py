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

# Loading the shots
shots = pd.read_csv("/Users/charlie/Downloads/shots_exports.csv")

# Calculating angle and distance
shots['Angle'] = np.arctan(np.absolute(shots['x'] - 34) / np.absolute(shots['y'] - 105))
shots['Distance'] = np.sqrt((shots['x'] - 34)**2 + (shots['y'] - 105)**2)

# Map text shot types to the numeric codes used during training
mapping = {
    'Left Footed': 1.0,
    'Right Footed': 2.0,
    'Headed': 3.0,
    'Other': 4.0
}

shots[' shotType'] = shots['type'].map(mapping)

# Encoding the shot types 
type_encoder = joblib.load('type_encoder.pkl')
encoded_shots = type_encoder.transform(shots[[' shotType']])
encoded_shot_types = pd.DataFrame(encoded_shots, columns=type_encoder.get_feature_names_out([' shotType']))

# Loading the trained expected goals model
xGmodel = joblib.load('xG_model.pkl')

# Combining the Angle and Distance with the encoded shot types as input
features = pd.concat([shots[['Distance', 'Angle']].reset_index(drop=True), encoded_shot_types.reset_index(drop=True)], axis=1)
# Calculating expected goals
xG = xGmodel.predict_proba(features)[:, 1]

# Saving the data to a CSV file
shots['xG'] = xG
shots.to_csv('expected_goals.csv', index=False)

