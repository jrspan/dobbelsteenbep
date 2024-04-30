import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Define location of data file (CSV)
def get_filepath(filename: str):
    # Returns full filepath of input filename
    # Used in combination with "load_datafile" function
    directory_path = os.path.dirname((os.path.abspath(__file__)))
    return os.path.join(directory_path, filename)

# Retrieve pandas dataframe from filename
def load_datafile(filename: str):
    # Returns pd.dataFrame
    # Retrieve relative directory path
    filepath = get_filepath(filename)
    # Attempt to load data
    try:
        data = pd.read_csv(filepath, header=None, skiprows=1)
        steps = data.values.tolist()
        columns = [data[col].tolist() for col in data.columns]
        return data, steps, columns
    except FileNotFoundError:
        raise FileNotFoundError(f"Data file not found in directory {filepath}")
        
def integrate_acceleration(velocity, acceleration, dt):
    return velocity + acceleration * dt
        

filename = "merged_testfile.csv"
dataframe, steps, columns = load_datafile(filename)


'''
How to roll dice:
    
To calculate velocity for specific time[i]:
    - Get measured acceleration on time[i - 1]
    - Multiply this value by "dt" (= time[i] - time[i-1])
    - Transform rotation XYZ-axis with help of quaternions
    - Add previously calculated velocity from time[i-1] to this value
    
To calculate position for specific time[i]:
    - Get previously calculated velocity (from time[i-1])
    - Multiply this value by "dt" (= time[i] - time[i-1])
    - Transform rotation XYZ-axis help of quaternions
    - Add previously calculated position from time[i-1] to this value
    
To get rotation of XYZ-axis relative to real world:
    - ???????????????????????



'''