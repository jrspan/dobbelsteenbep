# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:28:17 2024

@author: zibbo
"""

### DIRECTORY TEST ###
import os
import pandas as pd

filename = "hahah.xlsx"

filepath = os.path.dirname((os.path.abspath(__file__)))
print(f"Current file directory: {filepath}")
print(f"Current working directory: {os.getcwd()}")

full_filepath = os.path.join(filepath, filename)
print(full_filepath)

try:
    open(full_filepath)
    print("Werkt goed!")
except:
    raise FileNotFoundError("Bestand niet goed gevonden")

###############################################################################
def get_filepath(filename: str):
    filepath = os.path.dirname((os.path.abspath(__file__)))
    return os.path.join(filepath, filename)
###############################################################################



### PANDAS READ CSV TEST ###
print(f"--- START OF READ CSV TEST ---")
filename = "acceleration_data.csv"
full_path = get_filepath(filename)
print(full_path)

try:
    file = pd.read_csv(full_path, header=None, skiprows=1)
except FileNotFoundError:
    raise FileNotFoundError("File does not exist in directory")
    
print(file)

try:
    time_1 = file[0][0]
    time_2 = file[0][1]
    dt = time_2 - time_1
except:
    raise IndexError("Er is maar 1 meting in het bestand! Potverdorie doe het opnieuw!")
    
acceleration_t = [value for value in file[0]]
acceleration_x = [value for value in file[1]]
acceleration_y = [value for value in file[2]]
acceleration_z = [value for value in file[3]]

acceleration_XYZ = [[acceleration_t[i], acceleration_x[i], acceleration_y[i], acceleration_z[i]] for i in range(len(acceleration_x))]
#===============================================================================
array_of_lists = [row.tolist() for _, row in file.iterrows()]
print(array_of_lists)
#===============================================================================