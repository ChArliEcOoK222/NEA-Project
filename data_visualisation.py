# Required libraries for data visualisation
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

# Gathering the data required for the scatter plot
data = pd.read_csv("/Users/charlie/Documents/NEA Project II/expected_goals.csv")

# Creating the pitch background
pitch = plt.imread("/Users/charlie/Documents/NEA Project II/pitch_diagram.jpg")
# Creating the axes and figure with an aspect ratio of 10:7
fig, ax = plt.subplots(figsize=(10,7))
# Displaying the image as the background
ax.imshow(pitch, extent=[0, 68, 0, 105])
# Removing the axes labels
ax.axis('off')

# Colours for each plot
colours = {'Goal': 'green', 'Shot': 'red'}

# Plotting the shots
for _, shot in data.iterrows():
    ax.scatter(
        shot['x'], shot['y'], 
        s=shot['xG'] * 800,
        color=colours.get(shot['outcome'], 'blue')
    )

    ax.text(
        shot['x'] + 0.7,
        shot['y'] + 0.7,
        shot['position'], 
        fontsize=8, 
        color='black'
    )

# Sizes to use for the expected goals key
xg_sizes =[0.25, 0.5, 0.75, 1.00]
# Handles for shot outcomes and expected goals
outcome_handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markeredgecolor='black', markersize=10) for color in colours.values()]    
xg_handles = [    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markeredgecolor='black', markersize=size*800**0.5) for size in xg_sizes]
# Combining the handles
handles = outcome_handles + xg_handles
labels = list(colours.keys()) + [f"xG={x}" for x in xg_sizes]
# Adding the key to the axex
ax.legend(handles, labels, title="Shot Outcome & xG", loc='upper left', bbox_to_anchor=(-0.5, 1), frameon=True)
# Display the plot 
plt.show()