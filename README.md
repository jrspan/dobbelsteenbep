
# Die Measurement Tool Guide

## Table of Contents
- Software requirements
- User interface overview
- Usage of logging tool
- Usage of results tool

## Software requirements
The only requirements that are needed for the device are a (stable) bluetooth connection and the ability to execute Python codes.

Within Python, the following modules are needed:
- MetaWear
- NumPy
- Pandas
- Matplotlib
- PyQt5
- tkinter
- webbrowser
- datetime

Most of these modules are already installed by default.
If any of these modules are not present or found, the software will fail to start.

## User interface overview
The user interface enables using and visualizing the Python code without the need for any prior knowledge of Python. 

### GUI main window
When the software is first openeed, there are 4 main windows which the user will make use of: storage, calibrator, logging tool, and results.

### File types and storage
The die measurement tool mainly uses 2 file formats: CSV and NPZ. The CSV format is used to store all measured data, and is used for every calculation. The NPZ file is used to store the calibration data. When a file is created and saved through the software, the filename will always contain the date and time at which it was created (format: YYYY-MM-DD-HH-MM-SS).

## Usage of logging tool
The die logging tool will provide two files which can be used to obtain results: the raw data of the logged die, and the calibration values. Both of these files are needed to accurately calculate the results. 

Below are the steps to use the die logging tool:
1. In the storage window, browse to a directory. This directory will be used to store both the calibration file and the raw data file.
2. Connect the die with the software. Make sure that your bluetooth is enabled both on the die and on your device. When the die is connected, a pop-will appear and the connection status will change to "Connected".
3. In the calibrator window, fill in all the calibration parameters. Then, click "Calibrate". Follow all the steps throughout the process. When the calibration process is finished, a .npz file will be stored in the browse location.
4. In the die logging window, fill in the logging parameters. These can be copied directly from the calibrator, but other values may be used as well. Following the the logging instructions. After the logging process, a .csv file will be stored in the previously selected directory.

With these two files, result can be compiled with the built-in results tool.

## Usage of results tool
Results can be obtained from the raw data file and the corresponding calibration file. Adding to this, the results can also be directly compiled from a results file, which is also formatted in .csv. In the latter case, no calibration file is needed.

Here are the steps to obtain results:
1. In the storage window, browse to the directory in which your .csv file (either raw data or results) is located. All eligible files will be loaded in the listbox.
2. In the listbox, click on the file you want to load and select "Apply". The selected file will now appear in the results window.
3. Click on "Show Results". If a raw data file was selected, a pop-up will appear asking for the calibration (.npz) file.
4. The results window will now load. Note: if the data is deemed "uncertain", a notification will appear and some results will be missing.

There is also an option to save the calculated results file. When the "Save Results" button is pressed, a pop up will appear in which you can select the storage directory. Once selected, the file will be saved in there.
