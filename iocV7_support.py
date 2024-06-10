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
    print(f"Current directory added: {current_directory}")
else:
    print("Current directory successfully loaded!")
    
extra_directory_1 = os.path.join(current_directory, "Final")
if not extra_directory_1 in sys.path:
    sys.path.append(extra_directory_1)
    print(f"New directory added: {extra_directory_1}")
else:
    print("Extra directory 1 successfully loaded!")
    
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

# Own imports:
from PyQt5.QtWidgets import QApplication, QFileDialog
import webbrowser
#from tkinter import filedialog, messagebox
import datetime

try:
    from dobbel import *
except Exception as e:
    print(f"An error occured: {e}")
    
try:
    from calibrator import *
except Exception as e:
    print(f"An error occured: {e}")
    
try:
    from analysis import *
except Exception as e:
    print(f"An error occured: {e}")
    
###

import iocV7

_debug = True  # False to eliminate debug printing from callback functions.


### GENERAL FUNCTIONS ###
# Helper function for directory selection
def select_directory():
    app = QApplication([])
    directory = QFileDialog.getExistingDirectory(None, "Select Directory")
    if directory:
        print("Selected directory:", directory)
        return directory
    
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
    file_path = os.path.join(directory, filename)
    try:
        df.to_csv(file_path, index=False)
        print(f"DataFrame successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving DataFrame to CSV: {e}")


### CONNECT FUNCTIONS ###
def connect_function():
    dob = dobbellogger()
    dob.connect()
    return dob

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




