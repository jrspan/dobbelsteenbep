import os
import sys
current_directory = os.path.dirname(__file__)
os.chdir(current_directory)
if not os.path.dirname(__file__) in sys.path:
    sys.path.append(os.path.dirname(__file__))
    print(f"[RW_helper] Current directory added: {current_directory}")
else:
    print("[RW_helper] Current directory successfully loaded!")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### INITIAL VALUES - DELETE THIS WHEN CODE IS DONE ###
#filename = "DATAFRAME.csv"
#filename2 = "2024-06-12_11-28-53_RawDieData.csv"
#filename3 = "2024-06-12_12-09-43_Results.csv"
# filename4 = "2024-06-12_12-40-31_Results.csv"
# dataframe = pd.read_csv(filename4)
# print(dataframe.columns)
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

# Helper function
def RW_gfe(df, key):
    # Getting first entry of keys.
    # If KeyError: Returns the string "undefined".
    try:
        return str(df.loc[df.index[0], key])
    except KeyError:
        print(f"KeyError: {key} not a valid column of dataframe.")
        return None

# Time functions
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
    return round(float(RW_gfe(df, 'Lucht tijd'))/1000, 2)

def RW_StartToRelease(df):
    return RW_gfe(df, 'Start tot los')

def RW_StartToGround(df):
    # Eerste stuiter
    return round(float(RW_gfe(df, 'Start tot grond')) / 1000, 2)

# Tijd in hand
def RW_TimeInHand(df):
    try:
        return str((float(RW_StartToRelease(df)) - float(RW_TimestampGrab(df))) / 1000)
    except:
        return str('<Undefined>')

# Die end
def RW_DieEndValue(df):
    return str(int(round(float(RW_gfe(df, 'Laatste zijde')), 0)))


# Acceleration functions
def RW_MeanAccHand(df):
    return round(float(RW_gfe(df, 'Mean acc hand')), 3)

def RW_MaxAccHand(df):
    return round(float(RW_gfe(df, 'Max acc hand')), 3)

def RW_MeanAccRoll(df):
    return round(float(RW_gfe(df, 'Mean acc roll')), 3)

def RW_MaxAccRoll(df):
    return round(float(RW_gfe(df, 'Max acc roll')), 3)

def RW_MeanAccWholeThrow(df):
    return round(float(RW_gfe(df, 'Mean acc whole throw')), 3)

def RW_MaxAccWholeThrow(df):
    return round(float(RW_gfe(df, 'Max acc whole throw')), 3)


# Acceleration w. Gravity
def RW_MeanAccHandG(df):
    return round(float(RW_gfe(df, 'Mean acc hand with gravity')), 3)

def RW_MaxAccHandG(df):
    return round(float(RW_gfe(df, 'Max acc hand with gravity')), 3)

def RW_MeanAccRollG(df):
    return round(float(RW_gfe(df, 'Mean acc roll with gravity')), 3)

def RW_MaxAccRollG(df):
    return round(float(RW_gfe(df, 'Max acc roll with gravity')), 3)

def RW_MeanAccWholeThrowG(df):
    return round(float(RW_gfe(df, 'Mean acc whole throw with gravity')), 3)

def RW_MaxAccWholeThrowG(df):
    return round(float(RW_gfe(df, 'Max acc whole throw with gravity')), 3)


# NIET IN RESULTS!
def RW_DeltaTheta(df):
    return RW_gfe(df, 'Delta theta')


# Rotations
def RW_TotalRotHand(df):
    return round(float(RW_gfe(df, 'Total rotation hand'))/ 360, 2)

def RW_TotalRotFlight(df):
    return round(float(RW_gfe(df, 'Total rotation flight')) / 360, 2)

def RW_TotalRotRoll(df):
    return round(float(RW_gfe(df, 'Total rotation roll')) / 360, 2)

def RW_TotalRotWholeThrow(df):
    return round(float(RW_gfe(df, 'Total rotation whole throw')) / 360, 2)

# Angular velocity
def RW_MeanAngVelHand(df):
    return round(float(RW_gfe(df, 'Mean ang. vel. hand')), 2)

def RW_MaxAngVelHand(df):
    return round(float(RW_gfe(df, 'Max ang. vel. hand')), 2)

def RW_MeanAngVelFlight(df):
    return round(float(RW_gfe(df, 'Mean ang. vel. flight')), 2)

def RW_MaxAngVelFlight(df):
    return round(float(RW_gfe(df, 'Max ang. vel. flight')), 2)

def RW_MeanAngVelRoll(df):
    return round(float(RW_gfe(df, 'Mean ang. vel. roll')), 2)

def RW_MaxAngVelRoll(df):
    return round(float(RW_gfe(df, 'Max ang. vel. roll')), 2)

def RW_MeanAngVelWholeThrow(df):
    try:
        return round(float(RW_gfe(df, 'Mean ang. vel. whole throw')), 2)
    except Exception as e:
        print(f"An error occurd: {e} (Executed during Mean ang. vel. whole throw")
        return
    
def RW_MaxAngVelWholeThrow(df):
    try:
        return round(float(RW_gfe(df, 'Max ang. vel. whole throw')), 2)
    except Exception as e:
        print(f"An error occured: {e} (Executed during Max Ang. Vel. Whole Throw)")
        return


### PLOTS ###
def RW_PlotAccXYZ(df, vline=False):
    """Function to create a figure and axes for plotting accelerometer data."""
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'] / 1000, df['x_acc'], label='X Acceleration', color='r') #df.loc[(df['timestamp'] > 1000) & (df['timestamp'] < 4000), 'timestamp'] / 1000, df.loc[(df['timestamp'] > 1000) & (df['timestamp'] < 4000),
    ax.plot(df['timestamp'] / 1000, df['y_acc'], label='Y Acceleration', color='g')
    ax.plot(df['timestamp'] / 1000, df['z_acc'], label='Z Acceleration', color='b')

    if vline:
        ax.axvline(x=df.loc[0, 'Raap tijd'] / 1000, label='Events', color='black', linestyle='dashed')
        ax.axvline(x=df.loc[0, 'Start tot los'] / 1000, color='black', linestyle='dashed')
        ax.axvline(x=df.loc[0, 'Start tot grond'] / 1000, color='black', linestyle='dashed')

    # Add labels inside the plot
    ax.text(0.5, -0.05, 'Timestamp (s)', ha='center', va='center', transform=ax.transAxes)
    ax.text(-0.05, 0.5, 'Acceleration (g)', ha='center', va='center', transform=ax.transAxes, rotation='vertical')

    ax.set_title('Accelerometer Raw Data')
    ax.legend(loc='upper left')  # Move the legend to the upper left corner
    ax.grid(True)
    
    ax.tick_params(axis="y", direction="in", pad=-22)
    ax.tick_params(axis="x", direction="in", pad=-15)

    # Set subplot margins to zero
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    return fig, ax


def RW_PlotGyrXYZ(df, vline=False):
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'] / 1000, df['x_gyro'], label='Angular Velocity X', color='r')
    ax.plot(df['timestamp'] / 1000, df['y_gyro'], label='Angular Velocity Y', color='g')
    ax.plot(df['timestamp'] / 1000, df['z_gyro'], label='Angular Velocity Z', color='b')

    if vline:
        ax.axvline(x=df.loc[0, 'Raap tijd'] / 1000, label='Events', color='black', linestyle='dashed')
        ax.axvline(x=df.loc[0, 'Start tot los'] / 1000, color='black', linestyle='dashed')
        ax.axvline(x=df.loc[0, 'Start tot grond'] / 1000, color='black', linestyle='dashed')
    
    ax.text(0.5, -0.05, 'Timestamp (s)', ha='center', va='center', transform=ax.transAxes)
    ax.text(-0.05, 0.5, 'Angular Velocity (deg/s)', ha='center', va='center', transform=ax.transAxes, rotation='vertical')
    
    ax.set_title('Gyroscope Raw Data')
    ax.legend(loc='upper left')  # Move the legend to the upper left corner
    ax.grid(True)
    
    ax.tick_params(axis="y", direction="in", pad=-22)
    ax.tick_params(axis="x", direction="in", pad=-15)

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    return fig, ax


def RW_PlotEuler(df, vline=False):
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'] / 1000, df['psi']*(180/np.pi), label='Psi', color='r')
    ax.plot(df['timestamp'] / 1000, df['theta']*(180/np.pi), label='Theta', color='g')
    ax.plot(df['timestamp'] / 1000, df['phi']*(180/np.pi), label='Phi', color='b')

    if vline:
        ax.axvline(x=df.loc[0, 'Raap tijd'] / 1000, label='Events', color='black', linestyle='dashed')
        ax.axvline(x=df.loc[0, 'Start tot los'] / 1000, color='black', linestyle='dashed')
        ax.axvline(x=df.loc[0, 'Start tot grond'] / 1000, color='black', linestyle='dashed')
    
    ax.text(0.5, -0.05, 'Timestamp (s)', ha='center', va='center', transform=ax.transAxes)
    ax.text(-0.05, 0.5, 'Euler angles (deg)', ha='center', va='center', transform=ax.transAxes, rotation='vertical')
    
    ax.set_title('Gyroscope Raw Data')
    ax.legend(loc='upper left')  # Move the legend to the upper left corner
    ax.grid(True)
    
    ax.tick_params(axis="y", direction="in", pad=-22)
    ax.tick_params(axis="x", direction="in", pad=-15)

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    return fig, ax

