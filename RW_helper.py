import os
import sys
current_directory = os.path.dirname(__file__)
os.chdir(current_directory)
if not os.path.dirname(__file__) in sys.path:
    sys.path.append(os.path.dirname(__file__))
    print(f"Current directory added: {current_directory}")
else:
    print("Current directory successfully loaded!")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### INITIAL VALUES - DELETE THIS WHEN CODE IS DONE ###
#filename = "DATAFRAME.csv"
#filename2 = "2024-06-12_11-28-53_RawDieData.csv"
#filename3 = "2024-06-12_12-09-43_Results.csv"
#filename4 = "2024-06-12_12-40-31_Results.csv"
#dataframe = pd.read_csv(filename4)
#print(dataframe.columns)
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

def RW_gfe(df, key):
    # Getting first entry of keys.
    # If KeyError: Returns the string "undefined".
    try:
        return str(df.loc[df.index[0], key])
    except KeyError:
        print(f"KeyError: {key} not a valid column of dataframe.")
        return str('<Undefined>')

def RW_TotalTime(df):
    # Returns the total time (in seconds) 
    endtime = df.loc[df.index[-1], 'timestamp']
    starttime = df.loc[df.index[0], 'timestamp']
    return (endtime - starttime) / 1000

def RW_TimestampGrab(df):
    # Returns the time it takes before die is grabbed.
    # If KeyError: "onzekere meting"
    return RW_gfe(df, 'Raap tijd')

def RW_ReleaseTimestamp(df):
    return RW_gfe(df, 'Gooi tijd')

def RW_AirborneTime(df):
    return RW_gfe(df, 'Lucht tijd')

def RW_StartToRelease(df):
    return RW_gfe(df, 'Start tot los')

def RW_StartToGround(df):
    return RW_gfe(df, 'Start tot grond')

def RW_DieEndValue(df):
    return RW_gfe(df, 'Laatste zijde')

def RW_MeanAccHand(df):
    return RW_gfe(df, 'Mean acc hand')

def RW_MaxAccHand(df):
    return RW_gfe(df, 'Max acc hand')

def RW_MeanAccRoll(df):
    return RW_gfe(df, 'Mean acc roll')

def RW_MaxAccRoll(df):
    return RW_gfe(df, 'Max acc roll')

def RW_MeanAccWholeThrow(df):
    return RW_gfe(df, 'Mean acc whole throw')

def RW_MaxAccWholeThrow(df):
    return RW_gfe(df, 'Max acc whole throw')

def RW_MeanAccHandG(df):
    return RW_gfe(df, 'Mean acc hand with gravity')

def RW_MaxAccHandG(df):
    return RW_gfe(df, 'Max acc hand with gravity')

def RW_MeanAccRollG(df):
    return RW_gfe(df, 'Mean acc roll with gravity')

def RW_MaxAccRollG(df):
    return RW_gfe(df, 'Max acc roll with gravity')

def RW_MeanAccWholeThrowG(df):
    return RW_gfe(df, 'Mean acc whole throw with gravity')

def RW_MaxAccWholeThrowG(df):
    return RW_gfe(df, 'Max acc whole throw with gravity')

def RW_DeltaTheta(df):
    return RW_gfe(df, 'Delta theta')

def RW_TotalRotHand(df):
    return RW_gfe(df, 'Total rotation hand')

def RW_TotalRotFlight(df):
    return RW_gfe(df, 'Total rotation flight')

def RW_TotalRotRoll(df):
    return RW_gfe(df, 'Total rotation roll')

def RW_TotalRotWholeThrow(df):
    return RW_gfe(df, 'Total rotation whole throw')

def RW_MeanAngVelHand(df):
    return RW_gfe(df, 'Mean ang. vel. hand')

def RW_MaxAngVelHand(df):
    return RW_gfe(df, 'Max ang. vel. hand')

def RW_MeanAngVelFlight(df):
    return RW_gfe(df, 'Mean ang. vel. flight')

def RW_MaxAngVelFlight(df):
    return RW_gfe(df, 'Max ang. vel. flight')

def RW_MeanAngVelRoll(df):
    return RW_gfe(df, 'Mean ang. vel. roll')

def RW_MaxAngVelRoll(df):
    return RW_gfe(df, 'Max ang. vel. roll')


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

