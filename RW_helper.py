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

### DATA INFO ###
'''
Raaptijd = Tijdsmoment van oppakken
Gooitijd = Moment van loslaten
Luchttijd (duration) = Tijd tussen release en bounce
Start tot los = Tijdsinterval (start measuring - release time)
Start tot grond = (start measuring - first bounce)
Laatste zijde = welke kant bovenop ligt
Mean acc hand = gemiddelde acceleratie in hand
Max acc hand = maximum acceleratie in hand
Mean acc roll = gemiddelde acc van rol, na de 1e stuiter
Max acc roll = Maximum acceleratie van rol, na 1e stuiter
Mean acc whole throw
Max acc whole throw
Mean acc hand with gravityh
Max acc hand with gravity
Mean acc roll with gravity
Max acc roll with gravity
Mean cc whole thtow with gravit
Max acc whole row with gravity
Delta theta
Total rotation hand
Total rotation flight
Total rotation roll
Total rotation whole throw
Mean ang vel hand
Max ang vel hand
Mean ang vel flight
Max ang vel flight Mean ang vel roll
Max ang vel roll
'''
def RW_TotalTime(df):
    # Returns the total time (in seconds)
    endtime = df.loc[df.index[-1], 'timestamp']
    starttime = df.loc[df.index[0], 'timestamp']
    return (endtime - starttime) / 1000

def RW_TimestampGrab(df):
    pass





### PLOTS ###
def RW_PlotAccXYZ(df):
    """Function to create a figure and axes for plotting accelerometer data."""
    fig, ax = plt.subplots()
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

    # Set axis labels
    ax.set_ylabel('Acceleration (g = N/m^2)')
    ax.set_xlabel('Timestamp (sec)')
    # Set subplot margins to zero
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    return fig, ax


def RW_PlotGyrXYZ(df):
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'] / 1000, df['x_gyro'], label='Angular Velocity X', color='r')
    ax.plot(df['timestamp'] / 1000, df['y_gyro'], label='Angular Velocity Y', color='g')
    ax.plot(df['timestamp'] / 1000, df['z_gyro'], label='Angular Velocity Z', color='b')
    
    ax.text(0.5, -0.05, 'Timestamp (sec)', ha='center', va='center', transform=ax.transAxes)
    ax.text(-0.05, 0.5, 'Angular Velocity (deg/sec)', ha='center', va='center', transform=ax.transAxes, rotation='vertical')
    
    ax.set_title('Gyroscope Raw Data')
    ax.legend(loc='upper left')  # Move the legend to the upper left corner
    ax.grid(True)
    
    ax.tick_params(axis="y", direction="in", pad=-22)
    ax.tick_params(axis="x", direction="in", pad=-15)
    
    ax.set_ylabel('Angular Velocity (deg / sec)')
    ax.set_xlabel('Timestamp (sec)')

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    return fig, ax


def RW_PlotEuler(df):
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'] / 1000, df['psi']*(180/np.pi), label='Roll', color='r')
    ax.plot(df['timestamp'] / 1000, df['theta']*(180/np.pi), label='Pitch', color='g')
    ax.plot(df['timestamp'] / 1000, df['phi']*(180/np.pi), label='Yaw', color='b')
    
    ax.text(0.5, -0.05, 'Timestamp (sec)', ha='center', va='center', transform=ax.transAxes)
    ax.text(-0.05, 0.5, 'Euler angles (deg)', ha='center', va='center', transform=ax.transAxes, rotation='vertical')
    
    ax.set_title('Gyroscope Raw Data')
    ax.legend(loc='upper left')  # Move the legend to the upper left corner
    ax.grid(True)
    
    ax.tick_params(axis="y", direction="in", pad=-22)
    ax.tick_params(axis="x", direction="in", pad=-15)
    
    ax.set_ylabel('Euler angles (deg)')
    ax.set_xlabel('Timestamp (sec)')

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    return fig, ax

