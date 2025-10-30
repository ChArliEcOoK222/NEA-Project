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
import glob

# Loading shot types
shots = pd.read_csv("/Users/charlie/Downloads/shots_exports.csv")

# Calculating the distance from the goal and angle of the shot
shots['Angle'] = np.arctan(np.absolute(shots['x'] - 34) / np.absolute(shots['y'] - 105))
shots['Distance'] = np.sqrt((shots['x'] - 34)**2 + (shots['y'] - 105)**2)

# Encode shot types using OneHotEncoder
shot_encoder = joblib.load('shot_encoder.pkl')
shot_types_encoded = shot_encoder.transform(shots[['type']])
shot_types_df = pd.DataFrame(shot_types_encoded, columns=["shot_type_Left Footed", "shot_type_Right Footed", "shot_type_Headed", "shot_type_Other"], index=shots.index)

# Loading the Expected Gaols Model
xGmodel = joblib.load('xG_model.pkl')
# Model features
features = pd.concat([shots[['Angle', 'Distance']], shot_types_df], axis=1)
# Calculating and saving the results
shots['xG'] = xGmodel.predict_proba(features)[:, 1]
shots.to_csv('expected_goals.csv', index=False)

