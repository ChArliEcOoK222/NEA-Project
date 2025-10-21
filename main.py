# Required libraries for the expected goals mode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.linear_model import LogisticRegression
import joblib
import os
import json
import glob

# Loading the shots
folders = ['/Users/charlie/Documents/Training Data', '/Users/charlie/Downloads/drive-download-20251021T125250Z-1-001']
files = []

for folder in folders:
    files.extend(glob.glob(os.path.join(folder, '*.csv')))

# List to store individual DataFrames
dataframes = []

# Reading each individual file
for file in files:
    df = pd.read_csv(file)
    dataframes.append(df)

shots = pd.concat(dataframes, ignore_index=True)

# Calculating the distance from the goal and angle of the shot
shots['Angle'] = np.arctan(np.absolute(shots['x'] - 34) / np.absolute(shots['y'] - 105))
shots['Distance'] = np.sqrt((shots['x'] - 34)**2 + (shots['y'] - 105)**2)

# Encoding the shot types
shot_types = pd.get_dummies(shots['type'], prefix='shot_type')

# Creating a binary column
shots['Binary'] = 0
# Assigning a binary value for each shot
for index, row in shots.iterrows():
    if row['outcome'] == 'Goal':
        shots.at[index, 'Binary'] = 1

# Creating the Expected Gaols Model
xGmodel = LogisticRegression()
# Training data
X = pd.concat([shots[['Angle', 'Distance']], shot_types], axis=1)
y = shots['Binary']
# Fitting the model to this data
xGmodel.fit(X, y)
# Saving the model
joblib.dump(xGmodel, 'xG_model.pkl')

