# Required libraries for the expected goals mode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.linear_model import LogisticRegression
import joblib

# Loading the data into a pandas dataframe
shots = pd.read_csv("/Users/charlie/Downloads/shots_exports.csv")

# Calculating the distance from the goal and angle of the shot
shots['Angle'] = np.arctan(np.absolute(shots['x'] - 34) / np.absolute(shots['y'] - 105))
shots['Distance'] = np.sqrt((shots['x'] - 34)**2 + (shots['y'] - 105)**2)

# Creating the Expected Goals Model
xGmodel = joblib.load('xGmodel')       

# Calculating expected goals
xG = xGmodel.predict_proba(shots[['Distance', 'Angle']])[:,1]
shots['xG'] = xG
shots.to_csv('expected goals.csv')



