#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 8.0
#  in conjunction with Tcl version 8.6
#    Jun 04, 2024 10:26:20 AM CEST  platform: Windows NT

import os
import sys
current_directory = os.path.dirname(__file__)
if not os.path.dirname(__file__) in sys.path:
    sys.path.append(os.path.dirname(__file__))
    print(f"[ioc_SUPPORT] Current directory added: {current_directory}")
else:
    print("[ioc_SUPPORT] Current directory successfully loaded!")
    
#extra_directory_1 = os.path.join(current_directory, "Final")
#if not extra_directory_1 in sys.path:
#    sys.path.append(extra_directory_1)
#    print(f"New directory added: {extra_directory_1}")
#else:
#    print("Extra directory 1 successfully loaded!")

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter.constants import *
    # Own imports
    from PyQt5.QtWidgets import QApplication, QFileDialog
    import webbrowser
    import datetime
    import pandas as pd
    import numpy as np
except Exception as e:
    print(f"[ioc_SUPPORT Imports] An error occured: {e}")

try:
    from dobbel import *
except Exception as e:
    print(f"[ioc_SUPPORT Imports] An error occured: {e}. (Error with importing dobbel.py)")
    
try:
    from calibrator import *
except Exception as e:
    print(f"[ioc_SUPPORT Imports] An error occured: {e}. (Error with importing calibrator.py)")
    
try:
    from analysis import *
except Exception as e:
    print(f"[ioc_SUPPORT Imports] An error occured: {e}. (Error with importing analysis.py)")
    
###
try:
    import iocV7
except Exception as e:
    print(f"[ioc_SUPPORT Imports] An error occured: {e}. (Error while importing iocV7.py)")
    
_debug = True  # False to eliminate debug printing from callback functions.
# June 12, 11:22

def select_directory():
    app = QApplication([])
    directory = QFileDialog.getExistingDirectory(None, "Select Directory")
    app.quit()
    if directory:
        print("[ioc_SUPPORT] Selected directory:", directory)
        return directory
    print("[ioc_SUPPORT] No directory selected")
    return None
    
def select_npz_file():
    print("[ioc_SUPPORT] Selecting NPZ file...")
    try:
        app = QApplication([])
        file_path, _ = QFileDialog.getOpenFileName(None, "Select Calibration File", "", "NPZ Files (*.npz)")
        app.quit()  # Quit the application to avoid blocking the script
        if file_path:
            print("[ioc_SUPPORT] Selected calibration file:", file_path)
            return file_path
        print("[ioc_SUPPORT] No NPZ file selected")
        return None
    except Exception as e:
        print(f"[ioc_SUPPORT] An error occued: {e}")
        return None
    
# Used to create filename for data
def create_filename_date():
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{date_string}"
    return filename

# Helper function to convert dataframe to csv and save in specified directory
def save_dataframe_to_csv(df, filename, directory):
    """
    Parameters:
    df (pandas.DataFrame): The DataFrame to be saved.
    filename (str): The name of the CSV file (without directory path).
    directory (str): The path to the directory where the file will be saved.
    """
    file_path = f"{os.path.join(directory, filename)}.csv"
    try:
        df.to_csv(file_path, index=False)
        print(f"[ioc_SUPPORT] DataFrame successfully saved to {file_path}")
    except Exception as e:
        print(f"[ioc_SUPPORT] Error saving DataFrame to CSV: {e}")
        
### FILE SAVING FUNCTIONS ###
# Function to save dictionaries to an .npz file
def save_dicts_as_npz(file_path, **dicts):
    combined_data = {}
    for dict_name, d in dicts.items():
        for key, value in d.items():
            combined_data[f'{dict_name}_{key}'] = value
    np.savez(file_path, **combined_data)
    print(f"[ioc_SUPPORT] Data has been saved to {file_path}")
    
# Function to load .npz file and reconstruct dictionaries
def load_npz_as_dicts(file_path):
    loaded_data = np.load(file_path)
    dicts = {}
    for key in loaded_data:
        dict_name, array_key = key.split('_', 1)
        if dict_name not in dicts:
            dicts[dict_name] = {}
        dicts[dict_name][array_key] = loaded_data[key]
    return dicts

def verify_CSV_columns(df):
    required_columns = ['timestamp', 'x_acc', 'y_acc', 'z_acc', 'x_gyro', 'y_gyro', 'z_gyro']
    if set(required_columns).issubset(df.columns):
        return True
    else:
        return False

### CONNECT FUNCTIONS ###
def connect_function():
    dob = dobbellogger()
    dob.connect()
    return dob

### CALIBRATE FUNCTION ###
def calibrate_function_list(css_value, dob, list1, list2, list3, list4, mt, freq, ar, gr, lowi=1):
    column, sign, side = css_value
    try:
        list1, list2, list3, list4 = cali_loop(column, sign, side, dob, mt, lowi, freq, ar, gr, list1, list2, list3, list4)
    except Exception as e:
        print(f"[ioc_SUPPORT] Error encountered: {e}")
        return None
    return list1, list2, list3, list4

def calibrate_cali_stdcali(dob, list1, list2, list3, list4, mt, freq, gr):
    cali = calibrate_rot_bias(list1, list2, list3, list4)
    std_cali = cali_std(dob, mt, freq, gr)
    return cali, std_cali

def save_cali_values(cali, std_cali, directory):
    if not os.path.isdir(directory):
        print("[ioc_SUPPORT] Minor error: Directory not specified. Allowing user to select directory.")
        tk.messagebox.showinfo(title="Saving Calibration Data",
                               message="Please select the directory in which you want to save your data.")
        directory = select_directory()  # Assuming select_directory function is defined elsewhere
        if not directory:
            return  # User cancelled directory selection
    cali_filedate = create_filename_date()  # Assuming create_filename_date function is defined elsewhere
    cali_filename = f"{cali_filedate}_CalibrationValues.npz"
    cali_filepath = os.path.join(directory, cali_filename)
    save_dicts_as_npz(cali_filepath, dict1=cali, dict2=std_cali)  # Assuming save_dicts_as_npz function is defined elsewhere

def load_cali_values():
    app = QApplication([])
    cali_file = QFileDialog.getOpenFileName(None, "Select .npz Calibration File", "", "NPZ Files (*.npz)")[0]
    app.quit()
    if cali_file:
        loaded_dicts = load_npz_as_dicts(cali_file)  # Assuming load_npz_as_dicts function is defined elsewhere
        cali = loaded_dicts.get('dict1')
        std_cali = loaded_dicts.get('dict2')
        return cali, std_cali
    return None, None  # Return None if no file is selected or user cancels

### LOGGING FUNCTIONS ###
def logging_function(dob, mt, freq, ar, gr):
    dob.connect()
    dob.log(mt, freq, ar, gr)
    dob.download()
    out_data = dob.datadf
    return out_data

        
### TKINTER FUNCTIONS ###
def on_destroy():
    root.destroy()
    sys.exit()
    
def open_website():
    webbrowser.open("https://github.com/jrspan/dobbelsteenbep")

def open_second_window(window_title, RW_csv, cali, std_cali):
    global _top2, _w2
    _top2 = tk.Toplevel(root)
    _w2 = iocV7.TW_Result(_top2, RW_csv, cali, std_cali)
    _top2.title(f"Results for: {window_title}")
    
def close_second_window():
    if _top2:
        _top2.destroy()

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', on_destroy)
    
    # Create the first window
    global _top1, _w1
    _top1 = root
    _w1 = iocV7.Toplevel1(_top1)
    
    root.mainloop()

if __name__ == '__main__':
    iocV7.start_up()




