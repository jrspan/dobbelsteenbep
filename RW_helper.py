import os
import sys
current_directory = os.path.dirname(__file__)
if not os.path.dirname(__file__) in sys.path:
    sys.path.append(os.path.dirname(__file__))
    print(f"Current directory added: {current_directory}")
else:
    print("Current directory successfully loaded!")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### INITIAL VALUES - DELETE THIS WHEN CODE IS DONE ###
filename = "DATAFRAME.csv"
dataframe = pd.read_csv(filename)
print(dataframe.columns)
### END OF INITIAL VALUES ###





def RW_TotalTime(df):
    # Returns the total time (in seconds)
    endtime = df.loc[df.index[-1], 'timestamp']
    starttime = df.loc[df.index[0], 'timestamp']
    return (endtime - starttime) / 1000

def RW_PlotAccXYZ(df):
    """Function to create a figure and axes for plotting accelerometer data."""
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)  # Make the figure background transparent
    ax.plot(df['timestamp'] / 1000, df['x_acc'], label='X Acceleration', color='r')
    ax.plot(df['timestamp'] / 1000, df['y_acc'], label='Y Acceleration', color='g')
    ax.plot(df['timestamp'] / 1000, df['z_acc'], label='Z Acceleration', color='b')

    # Add labels inside the plot
    ax.text(0.5, -0.05, 'Timestamp (sec)', ha='center', va='center', transform=ax.transAxes)
    ax.text(-0.05, 0.5, 'Acceleration (g = N/m^2)', ha='center', va='center', transform=ax.transAxes, rotation='vertical')

    ax.set_title('Accelerometer Raw Data')
    ax.legend(loc='upper left')  # Move the legend to the upper left corner
    ax.grid(True)
    
    ax.tick_params(axis="y", direction="in", pad=-22)
    ax.tick_params(axis="x", direction="in", pad=-15)
    # Hide the border
    ax.set_frame_on(False)

    # Set axis labels
    ax.set_xlabel('Timestamp (sec)')
    ax.set_ylabel('Acceleration (g = N/m^2)')

    # Set subplot margins to zero
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    return fig, ax

# Example usage:
# Call the function to get the figure and axes objects
acc_fig, acc_ax = RW_PlotAccXYZ(dataframe)
