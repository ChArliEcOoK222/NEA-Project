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

# Encoding the shot types 
type_encoder = OneHotEncoder(sparse_output=False)
encoded_shots = type_encoder.fit_transform(shots[['type']])
encoded_shot_types = pd.DataFrame(encoded_shots, columns=type_encoder.get_feature_names_out(['type']))

# Renaming encoded columns
new_names = {'type_Left_Footed': ' shotType_1.0', 'type_Right_Footed': ' shotType_2.0', 'type_Headed': ' shotType_3.0', 'type_Other': ' shotType_4.0'}

encoded_shot_types.rename(columns=new_names, inplace=True)

# Ensure all expected columns exist, even if missing in current data
for col in [' shotType_1.0', ' shotType_2.0', ' shotType_3.0', ' shotType_4.0']:
    if col not in encoded_shot_types.columns:
        encoded_shot_types[col] = 0  # fill with zeros

encoded_shot_types = encoded_shot_types[[' shotType_1.0', ' shotType_2.0', ' shotType_3.0', ' shotType_4.0']]

# Loading the trained expected goals model
xGmodel = joblib.load('xG_model.pkl')

# Combining the Angle and Distance with the encoded shot types as input
features = pd.concat([shots[['Distance', 'Angle']].reset_index(drop=True), encoded_shot_types.reset_index(drop=True)], axis=1)
# Calculating expected goals
xG = xGmodel.predict_proba(features)[:, 1]

# Saving the data to a CSV file
shots['xG'] = xG
shots.to_csv('expected_goals.csv', index=False)

