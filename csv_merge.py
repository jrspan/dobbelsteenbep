# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 11:51:25 2024

@author: zibbo
"""
import os
import pandas as pd
import numpy as np

directory_path = os.path.dirname((os.path.abspath(__file__)))

filename_1 = "acceleration_data.csv"
filename_2 = "gyroscope_data.csv"


file_1 = pd.read_csv(os.path.join(directory_path, filename_1))
file_2 = pd.read_csv(os.path.join(directory_path, filename_2))

first_non_zero_index = (file_1.iloc[:, 1:] != 0).any(axis=1).idxmax()

# Shift values in columns B, C, and D upwards to match the first non-zero value in the time column
for col in file_1.columns[1:]:
    file_1[col] = file_1[col].shift(-first_non_zero_index)

# Drop rows after shifting
file_1_v1 = file_1.iloc[:first_non_zero_index]
###############################################################################
def remove_zero_rows(df):
    first_non_zero_index = (df.iloc[:, 1:] != 0).any(axis=1).idxmax()
    for col in df.columns[1:]:
        df.loc[first_non_zero_index:, col] = df[col].shift(-first_non_zero_index)

    # Drop rows with NaN values in columns B, C, or D
    df = df.dropna(subset=df.columns[1:])
    return(df)
###############################################################################

file_1_v1 = remove_zero_rows(file_1)
file_2_v1 = remove_zero_rows(file_2)

file_3 = pd.merge(file_1_v1, file_2_v1, on='time', how='outer')
file_3.interpolate(inplace=True)
last_nan_index = file_3.dropna().index[-1]
print(last_nan_index)

file_3.ffill(inplace=True)
file_3.drop_duplicates(subset='time', keep='first', inplace=True)
###############################################################################
def merge_datafiles(df1, df2, col='time'):
    df3 = pd.merge(file_1_v1, file_2_v1, on=col, how='outer')
    df3.interpolate(inplace=True)
    df3.ffill(inplace=True)
    df3.drop_duplicates(subset=col, keep='first', inplace=True)
    return df3
###############################################################################
print(merge_datafiles(file_1_v1, file_2_v1))

###############################################################################
def export_to_csv(df, filename: str):
    directory_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(directory_path, filename)
    df.to_csv(filepath, index=False)
    print(f"Succesfully saved file as '{filename}'!")
    print(f"Directory location: {directory_path}")
    return None
###############################################################################

file_4 = merge_datafiles(file_1_v1, file_2_v1)
export_to_csv(file_4, 'merged_data_file_testv1.csv')