# Edited 12 June 11:22

import os
import sys

current_directory = os.path.dirname(__file__)
if not os.path.dirname(__file__) in sys.path:
    sys.path.append(os.path.dirname(__file__))
    print(f"Current directory added: {current_directory}")
else:
    print("Current directory successfully loaded!")
    
#extra_directory_1 = os.path.join(current_directory, "Final")
#if not extra_directory_1 in sys.path:
#    sys.path.append(extra_directory_1)
#    print(f"New directory added: {extra_directory_1}")
#else:
#    print("Extra directory 1 successfully loaded!")

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import messagebox
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

_location = os.path.dirname(__file__)

import iocV7_support
from RW_helper import *

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 

_style_code_ran = 0
def _style_code():
    global _style_code_ran
    if _style_code_ran: return        
    try: iocV7_support.root.tk.call('source',
                os.path.join(_location, 'themes', 'default.tcl'))
    except: pass
    style = ttk.Style()
    style.theme_use('default')
    style.configure('.', font = "TkDefaultFont")
    if sys.platform == "win32":
       style.theme_use('winnative')    
    _style_code_ran = 1

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("1450x720+1+2")
        top.minsize(120, 0)
        top.maxsize(3004, 1901)
        top.resizable(1,  1)
        top.title("Illusion of Control - Modelling a Die")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")
        
        #
        self.selected_directory = None # Directory
        
        # Class Variables
        self.c_lowi = "2"
        self.c_mt = ""
        self.c_freq = ""
        self.c_accrange = ""
        self.c_gyrrange = ""
        
        self.l_mt = ""
        self.l_freq = ""
        self.l_accrange = ""
        self.l_gyrrange = ""
        
        self.gyrrange_options = ["125", "250", "500", "1000", "2000"]
        self.accrange_options = ["1", "2", "4", "8", "16"]
        self.freq_options = ["25", "50", "100", "200", "400", "800"]
        
        ### Variables for DATASET OVERALL
        self.dob = None
        
        ### Variables for CALIBRATOR
        self.css_list = [(2, 1, 1), (0, 1, 2), (1, 1, 3), (1, -1, 4), (0, -1, 5), (2, -1, 6)]
        self.cali = None
        self.std_cali = None
        
        
        ### Variables for RESULT WINDOW (All start with "RW_")
        self.RW_title = None
        self.RW_csv = None # Wordt waarschijnlijk een filepath: "C:\Users\(...)\data.csv"
        

        self.top = top

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Frame2 = tk.Frame(self.top)
        self.Frame2.place(relx=0.014, rely=0.188, relheight=0.739
                , relwidth=0.386)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background="#d9d9d9")
        self.Frame2.configure(highlightbackground="#d9d9d9")
        self.Frame2.configure(highlightcolor="#000000")

        _style_code()
        self.Scrolledlistbox1 = ScrolledListBox(self.Frame2)
        self.Scrolledlistbox1.place(relx=0.054, rely=0.195, relheight=0.705
                , relwidth=0.882)
        self.Scrolledlistbox1.configure(background="white")
        self.Scrolledlistbox1.configure(cursor="xterm")
        self.Scrolledlistbox1.configure(disabledforeground="#a3a3a3")
        self.Scrolledlistbox1.configure(font="TkFixedFont")
        self.Scrolledlistbox1.configure(foreground="black")
        self.Scrolledlistbox1.configure(highlightbackground="#d9d9d9")
        self.Scrolledlistbox1.configure(highlightcolor="#d9d9d9")
        self.Scrolledlistbox1.configure(selectbackground="#d9d9d9")
        self.Scrolledlistbox1.configure(selectforeground="black")
        self.Scrolledlistbox1.bind('<<ScrolledlistboxSelect>>', self.on_select_listbox)

        self.s_StoreDataLabel = tk.Label(self.Frame2)
        self.s_StoreDataLabel.place(relx=0.054, rely=0.132, height=20, width=411)

        self.s_StoreDataLabel.configure(activebackground="#d9d9d9")
        self.s_StoreDataLabel.configure(activeforeground="black")
        self.s_StoreDataLabel.configure(anchor='w')
        self.s_StoreDataLabel.configure(background="#d9d9d9")
        self.s_StoreDataLabel.configure(compound='left')
        self.s_StoreDataLabel.configure(disabledforeground="#a3a3a3")
        self.s_StoreDataLabel.configure(font="-family {Segoe UI} -size 9")
        self.s_StoreDataLabel.configure(foreground="#000000")
        self.s_StoreDataLabel.configure(highlightbackground="#d9d9d9")
        self.s_StoreDataLabel.configure(highlightcolor="#000000")
        self.s_StoreDataLabel.configure(text='''This location will also be used to store logged data.''')

        self.s_DataFolderLabel = tk.Label(self.Frame2)
        self.s_DataFolderLabel.place(relx=0.054, rely=0.088, height=20, width=76)

        self.s_DataFolderLabel.configure(activebackground="#d9d9d9")
        self.s_DataFolderLabel.configure(activeforeground="black")
        self.s_DataFolderLabel.configure(anchor='w')
        self.s_DataFolderLabel.configure(background="#d9d9d9")
        self.s_DataFolderLabel.configure(compound='left')
        self.s_DataFolderLabel.configure(disabledforeground="#a3a3a3")
        self.s_DataFolderLabel.configure(font="-family {Segoe UI} -size 9")
        self.s_DataFolderLabel.configure(foreground="#000000")
        self.s_DataFolderLabel.configure(highlightbackground="#d9d9d9")
        self.s_DataFolderLabel.configure(highlightcolor="#000000")
        self.s_DataFolderLabel.configure(text='''Data folder:''')

        self.s_ApplyButton = tk.Button(self.Frame2)
        self.s_ApplyButton.place(relx=0.753, rely=0.934, height=26, width=97)
        self.s_ApplyButton.configure(activebackground="#d9d9d9")
        self.s_ApplyButton.configure(activeforeground="black")
        self.s_ApplyButton.configure(background="#d9d9d9")
        self.s_ApplyButton.configure(disabledforeground="#a3a3a3")
        self.s_ApplyButton.configure(font="-family {Segoe UI} -size 9")
        self.s_ApplyButton.configure(foreground="#000000")
        self.s_ApplyButton.configure(highlightbackground="#d9d9d9")
        self.s_ApplyButton.configure(highlightcolor="#000000")
        self.s_ApplyButton.configure(text='''Apply''')
        self.s_ApplyButton.configure(command=self.apply_selection)

        self.s_BrowseButton = tk.Button(self.Frame2)
        self.s_BrowseButton.place(relx=0.753, rely=0.135, height=26, width=97)
        self.s_BrowseButton.configure(activebackground="#d9d9d9")
        self.s_BrowseButton.configure(activeforeground="black")
        self.s_BrowseButton.configure(background="#d9d9d9")
        self.s_BrowseButton.configure(disabledforeground="#a3a3a3")
        self.s_BrowseButton.configure(font="-family {Segoe UI} -size 9")
        self.s_BrowseButton.configure(foreground="#000000")
        self.s_BrowseButton.configure(highlightbackground="#d9d9d9")
        self.s_BrowseButton.configure(highlightcolor="#000000")
        self.s_BrowseButton.configure(text='''Browse''')
        self.s_BrowseButton.configure(command=self.browse_directory)

        self.s_StorageHeader = tk.Label(self.Frame2)
        self.s_StorageHeader.place(relx=0.036, rely=0.011, height=29, width=531)
        self.s_StorageHeader.configure(activebackground="#d9d9d9")
        self.s_StorageHeader.configure(activeforeground="black")
        self.s_StorageHeader.configure(background="#d9d9d9")
        self.s_StorageHeader.configure(compound='left')
        self.s_StorageHeader.configure(disabledforeground="#a3a3a3")
        self.s_StorageHeader.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.s_StorageHeader.configure(foreground="#000000")
        self.s_StorageHeader.configure(highlightbackground="#d9d9d9")
        self.s_StorageHeader.configure(highlightcolor="#000000")
        self.s_StorageHeader.configure(text='''Storage''')

        self.s_Dirname = tk.Label(self.Frame2)
        self.s_Dirname.place(relx=0.215, rely=0.075, height=20, width=408)
        self.s_Dirname.configure(activebackground="#d9d9d9")
        self.s_Dirname.configure(activeforeground="black")
        self.s_Dirname.configure(anchor='w')
        self.s_Dirname.configure(background="#ffffff")
        self.s_Dirname.configure(compound='left')
        self.s_Dirname.configure(disabledforeground="#a3a3a3")
        self.s_Dirname.configure(font="-family {Segoe UI} -size 9")
        self.s_Dirname.configure(foreground="#000000")
        self.s_Dirname.configure(highlightbackground="#d9d9d9")
        self.s_Dirname.configure(highlightcolor="#000000")
        self.s_Dirname.configure(text="No directory selected.")

        self.Frame3 = tk.Frame(self.top)
        self.Frame3.place(relx=0.403, rely=0.188, relheight=0.297, relwidth=0.58)

        self.Frame3.configure(relief='groove')
        self.Frame3.configure(borderwidth="2")
        self.Frame3.configure(relief="groove")
        self.Frame3.configure(background="#d9d9d9")
        self.Frame3.configure(highlightbackground="#d9d9d9")
        self.Frame3.configure(highlightcolor="#000000")

        self.q_FullGuideButton = tk.Button(self.Frame3)
        self.q_FullGuideButton.place(relx=0.864, rely=0.86, height=26, width=97)
        self.q_FullGuideButton.configure(activebackground="#d9d9d9")
        self.q_FullGuideButton.configure(activeforeground="black")
        self.q_FullGuideButton.configure(background="#d9d9d9")
        self.q_FullGuideButton.configure(disabledforeground="#a3a3a3")
        self.q_FullGuideButton.configure(font="-family {Segoe UI} -size 9")
        self.q_FullGuideButton.configure(foreground="#000000")
        self.q_FullGuideButton.configure(highlightbackground="#d9d9d9")
        self.q_FullGuideButton.configure(highlightcolor="#000000")
        self.q_FullGuideButton.configure(text='''View full guide''')
        self.q_FullGuideButton.configure(command=iocV7_support.open_website)

        self.Message2 = tk.Message(self.Frame3)
        self.Message2.place(relx=0.012, rely=0.234, relheight=0.659
                , relwidth=0.482)
        self.Message2.configure(anchor='nw')
        self.Message2.configure(background="#d9d9d9")
        self.Message2.configure(font="-family {Segoe UI} -size 9")
        self.Message2.configure(foreground="#000000")
        self.Message2.configure(highlightbackground="#d9d9d9")
        self.Message2.configure(highlightcolor="#000000")
        self.Message2.configure(padx="1")
        self.Message2.configure(pady="1")
        self.Message2.configure(text='''How to use the data logger:
1. Select a file directory. This location will be used to save the logged data.
2. Connect the die, fill in all the calibration parameters, and start the calibrator.
3. After completing the calibration process, fill in the logging parameters and start the data logger.

The die will now start the logging process and store the logged data in the selected directory.''')
        self.Message2.configure(width=395)

        self.q_QuickGuideLabel = tk.Label(self.Frame3)
        self.q_QuickGuideLabel.place(relx=0.012, rely=0.042, height=29
                , width=818)
        self.q_QuickGuideLabel.configure(activebackground="#d9d9d9")
        self.q_QuickGuideLabel.configure(activeforeground="black")
        self.q_QuickGuideLabel.configure(background="#d9d9d9")
        self.q_QuickGuideLabel.configure(compound='left')
        self.q_QuickGuideLabel.configure(disabledforeground="#a3a3a3")
        self.q_QuickGuideLabel.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.q_QuickGuideLabel.configure(foreground="#000000")
        self.q_QuickGuideLabel.configure(highlightbackground="#d9d9d9")
        self.q_QuickGuideLabel.configure(highlightcolor="#000000")
        self.q_QuickGuideLabel.configure(text='''Quick guide''')

        self.Message3 = tk.Message(self.Frame3)
        self.Message3.place(relx=0.535, rely=0.234, relheight=0.355
                , relwidth=0.421)
        self.Message3.configure(anchor='nw')
        self.Message3.configure(background="#d9d9d9")
        self.Message3.configure(font="-family {Segoe UI} -size 9")
        self.Message3.configure(foreground="#000000")
        self.Message3.configure(highlightbackground="#d9d9d9")
        self.Message3.configure(highlightcolor="#000000")
        self.Message3.configure(padx="1")
        self.Message3.configure(pady="1")
        self.Message3.configure(text='''How to analyze data:
1. Select the directory in which the file is located.
2. In the scroll box, select the file to be analyzed, and hit apply.
3. Click on Show Results. A new window will pop up with the results from the selected file.''')
        self.Message3.configure(width=346)

        self.Frame5 = tk.Frame(self.top)
        self.Frame5.place(relx=0.7, rely=0.489, relheight=0.326, relwidth=0.283)
        self.Frame5.configure(relief='groove')
        self.Frame5.configure(borderwidth="2")
        self.Frame5.configure(relief="groove")
        self.Frame5.configure(background="#d9d9d9")
        self.Frame5.configure(highlightbackground="#d9d9d9")
        self.Frame5.configure(highlightcolor="#000000")

        self.l_CopyButton = tk.Button(self.Frame5)
        self.l_CopyButton.place(relx=0.071, rely=0.328, height=26, width=167)
        self.l_CopyButton.configure(activebackground="#d9d9d9")
        self.l_CopyButton.configure(activeforeground="black")
        self.l_CopyButton.configure(background="#d9d9d9")
        self.l_CopyButton.configure(disabledforeground="#a3a3a3")
        self.l_CopyButton.configure(font="-family {Segoe UI} -size 9")
        self.l_CopyButton.configure(foreground="#000000")
        self.l_CopyButton.configure(highlightbackground="#d9d9d9")
        self.l_CopyButton.configure(highlightcolor="#000000")
        self.l_CopyButton.configure(text='''Copy values from calibrator''')
        self.l_CopyButton.configure(command = self.copy_values)

        self.l_MeasurementTimeLabel = tk.Label(self.Frame5)
        self.l_MeasurementTimeLabel.place(relx=0.071, rely=0.489, height=20
                , width=120)
        self.l_MeasurementTimeLabel.configure(activebackground="#d9d9d9")
        self.l_MeasurementTimeLabel.configure(activeforeground="black")
        self.l_MeasurementTimeLabel.configure(anchor='w')
        self.l_MeasurementTimeLabel.configure(background="#d9d9d9")
        self.l_MeasurementTimeLabel.configure(compound='left')
        self.l_MeasurementTimeLabel.configure(disabledforeground="#a3a3a3")
        self.l_MeasurementTimeLabel.configure(font="-family {Segoe UI} -size 9")
        self.l_MeasurementTimeLabel.configure(foreground="#000000")
        self.l_MeasurementTimeLabel.configure(highlightbackground="#d9d9d9")
        self.l_MeasurementTimeLabel.configure(highlightcolor="#000000")
        self.l_MeasurementTimeLabel.configure(text='''Measurement time''')

        self.l_MeasurementTimeEntry = tk.Entry(self.Frame5)
        self.l_MeasurementTimeEntry.place(relx=0.508, rely=0.489, height=20
                , relwidth=0.205)
        self.l_MeasurementTimeEntry.configure(background="white")
        self.l_MeasurementTimeEntry.configure(disabledforeground="#a3a3a3")
        self.l_MeasurementTimeEntry.configure(font="-family {Courier New} -size 10")
        self.l_MeasurementTimeEntry.configure(foreground="#000000")
        self.l_MeasurementTimeEntry.configure(highlightbackground="#d9d9d9")
        self.l_MeasurementTimeEntry.configure(highlightcolor="#000000")
        self.l_MeasurementTimeEntry.configure(insertbackground="#000000")
        self.l_MeasurementTimeEntry.configure(selectbackground="#d9d9d9")
        self.l_MeasurementTimeEntry.configure(selectforeground="black")

        self.l_Sec = tk.Label(self.Frame5)
        self.l_Sec.place(relx=0.745, rely=0.489, height=20, width=32)
        self.l_Sec.configure(activebackground="#d9d9d9")
        self.l_Sec.configure(activeforeground="black")
        self.l_Sec.configure(anchor='w')
        self.l_Sec.configure(background="#d9d9d9")
        self.l_Sec.configure(compound='left')
        self.l_Sec.configure(disabledforeground="#a3a3a3")
        self.l_Sec.configure(font="-family {Segoe UI} -size 9")
        self.l_Sec.configure(foreground="#000000")
        self.l_Sec.configure(highlightbackground="#d9d9d9")
        self.l_Sec.configure(highlightcolor="#000000")
        self.l_Sec.configure(text='''Sec''')

        self.l_FreqLabel = tk.Label(self.Frame5)
        self.l_FreqLabel.place(relx=0.071, rely=0.57, height=20, width=71)
        self.l_FreqLabel.configure(activebackground="#d9d9d9")
        self.l_FreqLabel.configure(activeforeground="black")
        self.l_FreqLabel.configure(anchor='w')
        self.l_FreqLabel.configure(background="#d9d9d9")
        self.l_FreqLabel.configure(compound='left')
        self.l_FreqLabel.configure(disabledforeground="#a3a3a3")
        self.l_FreqLabel.configure(font="-family {Segoe UI} -size 9")
        self.l_FreqLabel.configure(foreground="#000000")
        self.l_FreqLabel.configure(highlightbackground="#d9d9d9")
        self.l_FreqLabel.configure(highlightcolor="#000000")
        self.l_FreqLabel.configure(text='''Frequency''')

        self.l_FreqEntry = ttk.Combobox(self.Frame5)
        self.l_FreqEntry.place(relx=0.508, rely=0.57, height=20, relwidth=0.205)
        self.l_FreqEntry.configure(background="white")
        self.l_FreqEntry.configure(font="-family {Courier New} -size 10")
        self.l_FreqEntry.configure(foreground="#000000")
        self.l_FreqEntry.configure(state='readonly')
        self.l_FreqEntry.configure(values=self.freq_options)
        self.l_FreqEntry.set(self.freq_options[2])

        self.l_Hz = tk.Label(self.Frame5)
        self.l_Hz.place(relx=0.745, rely=0.57, height=20, width=32)
        self.l_Hz.configure(activebackground="#d9d9d9")
        self.l_Hz.configure(activeforeground="black")
        self.l_Hz.configure(anchor='w')
        self.l_Hz.configure(background="#d9d9d9")
        self.l_Hz.configure(compound='left')
        self.l_Hz.configure(disabledforeground="#a3a3a3")
        self.l_Hz.configure(font="-family {Segoe UI} -size 9")
        self.l_Hz.configure(foreground="#000000")
        self.l_Hz.configure(highlightbackground="#d9d9d9")
        self.l_Hz.configure(highlightcolor="#000000")
        self.l_Hz.configure(text='''Hz''')

        self.l_AccRangeLabel = tk.Label(self.Frame5)
        self.l_AccRangeLabel.place(relx=0.071, rely=0.651, height=21, width=110)
        self.l_AccRangeLabel.configure(activebackground="#d9d9d9")
        self.l_AccRangeLabel.configure(activeforeground="black")
        self.l_AccRangeLabel.configure(anchor='w')
        self.l_AccRangeLabel.configure(background="#d9d9d9")
        self.l_AccRangeLabel.configure(compound='left')
        self.l_AccRangeLabel.configure(disabledforeground="#a3a3a3")
        self.l_AccRangeLabel.configure(font="-family {Segoe UI} -size 9")
        self.l_AccRangeLabel.configure(foreground="#000000")
        self.l_AccRangeLabel.configure(highlightbackground="#d9d9d9")
        self.l_AccRangeLabel.configure(highlightcolor="#000000")
        self.l_AccRangeLabel.configure(text='''Acceleration range''')

        self.l_AccRangeEntry = ttk.Combobox(self.Frame5)
        self.l_AccRangeEntry.place(relx=0.508, rely=0.651, height=20
                , relwidth=0.205)
        self.l_AccRangeEntry.configure(background="white")
        self.l_AccRangeEntry.configure(font="-family {Courier New} -size 10")
        self.l_AccRangeEntry.configure(foreground="#000000")
        self.l_AccRangeEntry.configure(values=self.accrange_options)
        self.l_AccRangeEntry.configure(state='readonly')
        self.l_AccRangeEntry.set(self.accrange_options[-2])

        self.l_g = tk.Label(self.Frame5)
        self.l_g.place(relx=0.745, rely=0.651, height=21, width=71)
        self.l_g.configure(activebackground="#d9d9d9")
        self.l_g.configure(activeforeground="black")
        self.l_g.configure(anchor='w')
        self.l_g.configure(background="#d9d9d9")
        self.l_g.configure(compound='left')
        self.l_g.configure(disabledforeground="#a3a3a3")
        self.l_g.configure(font="-family {Segoe UI} -size 9")
        self.l_g.configure(foreground="#000000")
        self.l_g.configure(highlightbackground="#d9d9d9")
        self.l_g.configure(highlightcolor="#000000")
        self.l_g.configure(text='''g (N/m^2)''')

        self.l_GyrRangeLabel = tk.Label(self.Frame5)
        self.l_GyrRangeLabel.place(relx=0.071, rely=0.736, height=20, width=100)
        self.l_GyrRangeLabel.configure(activebackground="#d9d9d9")
        self.l_GyrRangeLabel.configure(activeforeground="black")
        self.l_GyrRangeLabel.configure(anchor='w')
        self.l_GyrRangeLabel.configure(background="#d9d9d9")
        self.l_GyrRangeLabel.configure(compound='left')
        self.l_GyrRangeLabel.configure(disabledforeground="#a3a3a3")
        self.l_GyrRangeLabel.configure(font="-family {Segoe UI} -size 9")
        self.l_GyrRangeLabel.configure(foreground="#000000")
        self.l_GyrRangeLabel.configure(highlightbackground="#d9d9d9")
        self.l_GyrRangeLabel.configure(highlightcolor="#000000")
        self.l_GyrRangeLabel.configure(text='''Gyroscope range''')

        self.l_GyrRangeEntry = ttk.Combobox(self.Frame5)
        self.l_GyrRangeEntry.place(relx=0.508, rely=0.736, height=20
                , relwidth=0.205)
        self.l_GyrRangeEntry.configure(background="white")
        self.l_GyrRangeEntry.configure(font="-family {Courier New} -size 10")
        self.l_GyrRangeEntry.configure(foreground="#000000")
        self.l_GyrRangeEntry.configure(values=self.gyrrange_options)
        self.l_GyrRangeEntry.configure(state='readonly')
        self.l_GyrRangeEntry.set(self.gyrrange_options[-1])

        self.l_DegSec = tk.Label(self.Frame5)
        self.l_DegSec.place(relx=0.745, rely=0.736, height=20, width=61)
        self.l_DegSec.configure(activebackground="#d9d9d9")
        self.l_DegSec.configure(activeforeground="black")
        self.l_DegSec.configure(anchor='w')
        self.l_DegSec.configure(background="#d9d9d9")
        self.l_DegSec.configure(compound='left')
        self.l_DegSec.configure(disabledforeground="#a3a3a3")
        self.l_DegSec.configure(font="-family {Segoe UI} -size 9")
        self.l_DegSec.configure(foreground="#000000")
        self.l_DegSec.configure(highlightbackground="#d9d9d9")
        self.l_DegSec.configure(highlightcolor="#000000")
        self.l_DegSec.configure(text='''Deg / Sec''')

        self.l_LogSetTitle = tk.Label(self.Frame5)
        self.l_LogSetTitle.place(relx=0.027, rely=0.038, height=20, width=378)
        self.l_LogSetTitle.configure(activebackground="#d9d9d9")
        self.l_LogSetTitle.configure(activeforeground="black")
        self.l_LogSetTitle.configure(background="#d9d9d9")
        self.l_LogSetTitle.configure(compound='left')
        self.l_LogSetTitle.configure(disabledforeground="#a3a3a3")
        self.l_LogSetTitle.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.l_LogSetTitle.configure(foreground="#000000")
        self.l_LogSetTitle.configure(highlightbackground="#d9d9d9")
        self.l_LogSetTitle.configure(highlightcolor="#000000")
        self.l_LogSetTitle.configure(text='''Logging Settings''')

        self.l_StartLoggingButton = tk.Button(self.Frame5)
        self.l_StartLoggingButton.place(relx=0.732, rely=0.851, height=26
                , width=97)
        self.l_StartLoggingButton.configure(activebackground="#d9d9d9")
        self.l_StartLoggingButton.configure(activeforeground="black")
        self.l_StartLoggingButton.configure(background="#d9d9d9")
        self.l_StartLoggingButton.configure(disabledforeground="#a3a3a3")
        self.l_StartLoggingButton.configure(font="-family {Segoe UI} -size 9")
        self.l_StartLoggingButton.configure(foreground="#000000")
        self.l_StartLoggingButton.configure(highlightbackground="#d9d9d9")
        self.l_StartLoggingButton.configure(highlightcolor="#000000")
        self.l_StartLoggingButton.configure(text='''Start logging''')
        self.l_StartLoggingButton.configure(command=self.on_click_logging)
        
        self.l_StatusLoggingLabel = tk.Label(self.Frame5)
        self.l_StatusLoggingLabel.place(relx=0.049, rely=0.851, height=21
                , width=104)
        self.l_StatusLoggingLabel.configure(activebackground="#d9d9d9")
        self.l_StatusLoggingLabel.configure(activeforeground="black")
        self.l_StatusLoggingLabel.configure(anchor='w')
        self.l_StatusLoggingLabel.configure(background="#d9d9d9")
        self.l_StatusLoggingLabel.configure(compound='left')
        self.l_StatusLoggingLabel.configure(cursor="fleur")
        self.l_StatusLoggingLabel.configure(disabledforeground="#a3a3a3")
        self.l_StatusLoggingLabel.configure(foreground="#000000")
        self.l_StatusLoggingLabel.configure(highlightbackground="#d9d9d9")
        self.l_StatusLoggingLabel.configure(highlightcolor="#000000")
        self.l_StatusLoggingLabel.configure(text='''Status Logging:''')

        self.l_StatusLogIndicator = tk.Label(self.Frame5)
        self.l_StatusLogIndicator.place(relx=0.309, rely=0.851, height=21
                , width=150)
        self.l_StatusLogIndicator.configure(activebackground="#d9d9d9")
        self.l_StatusLogIndicator.configure(activeforeground="black")
        self.l_StatusLogIndicator.configure(anchor='w')
        self.l_StatusLogIndicator.configure(background="#d9d9d9")
        self.l_StatusLogIndicator.configure(compound='left')
        self.l_StatusLogIndicator.configure(disabledforeground="#a3a3a3")
        self.l_StatusLogIndicator.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.l_StatusLogIndicator.configure(foreground="#ff0000")
        self.l_StatusLogIndicator.configure(highlightbackground="#d9d9d9")
        self.l_StatusLogIndicator.configure(highlightcolor="#000000")
        self.l_StatusLogIndicator.configure(text='''Not Logging''')

        self.Frame4 = tk.Frame(self.top)
        self.Frame4.place(relx=0.403, rely=0.489, relheight=0.326
                , relwidth=0.297)
        self.Frame4.configure(relief='groove')
        self.Frame4.configure(borderwidth="2")
        self.Frame4.configure(relief="groove")
        self.Frame4.configure(background="#d9d9d9")
        self.Frame4.configure(highlightbackground="#d9d9d9")
        self.Frame4.configure(highlightcolor="#000000")

        self.c_ConnectButton = tk.Button(self.Frame4)
        self.c_ConnectButton.place(relx=0.726, rely=0.204, height=26, width=107)
        self.c_ConnectButton.configure(activebackground="#d9d9d9")
        self.c_ConnectButton.configure(activeforeground="black")
        self.c_ConnectButton.configure(background="#d9d9d9")
        self.c_ConnectButton.configure(disabledforeground="#a3a3a3")
        self.c_ConnectButton.configure(font="-family {Segoe UI} -size 9")
        self.c_ConnectButton.configure(foreground="#000000")
        self.c_ConnectButton.configure(highlightbackground="#d9d9d9")
        self.c_ConnectButton.configure(highlightcolor="#000000")
        self.c_ConnectButton.configure(text='''Connect''')
        self.c_ConnectButton.configure(command=self.on_click_connect)

        self.c_ConnectIndicatorLabel = tk.Label(self.Frame4)
        self.c_ConnectIndicatorLabel.place(relx=0.307, rely=0.204, height=20
                , width=89)
        self.c_ConnectIndicatorLabel.configure(activebackground="#d9d9d9")
        self.c_ConnectIndicatorLabel.configure(activeforeground="black")
        self.c_ConnectIndicatorLabel.configure(anchor='w')
        self.c_ConnectIndicatorLabel.configure(background="#d9d9d9")
        self.c_ConnectIndicatorLabel.configure(compound='left')
        self.c_ConnectIndicatorLabel.configure(disabledforeground="#a3a3a3")
        self.c_ConnectIndicatorLabel.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.c_ConnectIndicatorLabel.configure(foreground="#ff0000")
        self.c_ConnectIndicatorLabel.configure(highlightbackground="#d9d9d9")
        self.c_ConnectIndicatorLabel.configure(highlightcolor="#000000")
        self.c_ConnectIndicatorLabel.configure(text='''Not Connected''')

        self.c_StatusCalibrationLabel = tk.Label(self.Frame4)
        self.c_StatusCalibrationLabel.place(relx=0.044, rely=0.855, height=21
                , width=98)
        self.c_StatusCalibrationLabel.configure(activebackground="#d9d9d9")
        self.c_StatusCalibrationLabel.configure(activeforeground="black")
        self.c_StatusCalibrationLabel.configure(anchor='w')
        self.c_StatusCalibrationLabel.configure(background="#d9d9d9")
        self.c_StatusCalibrationLabel.configure(compound='left')
        self.c_StatusCalibrationLabel.configure(disabledforeground="#a3a3a3")
        self.c_StatusCalibrationLabel.configure(font="-family {Segoe UI} -size 9")
        self.c_StatusCalibrationLabel.configure(foreground="#000000")
        self.c_StatusCalibrationLabel.configure(highlightbackground="#d9d9d9")
        self.c_StatusCalibrationLabel.configure(highlightcolor="#000000")
        self.c_StatusCalibrationLabel.configure(text='''Status Calibration:''')

        self.c_CalibrationIndicatorLabel = tk.Label(self.Frame4)
        self.c_CalibrationIndicatorLabel.place(relx=0.307, rely=0.855, height=21
                , width=89)
        self.c_CalibrationIndicatorLabel.configure(activebackground="#d9d9d9")
        self.c_CalibrationIndicatorLabel.configure(activeforeground="black")
        self.c_CalibrationIndicatorLabel.configure(anchor='w')
        self.c_CalibrationIndicatorLabel.configure(background="#d9d9d9")
        self.c_CalibrationIndicatorLabel.configure(compound='left')
        self.c_CalibrationIndicatorLabel.configure(disabledforeground="#a3a3a3")
        self.c_CalibrationIndicatorLabel.configure(font="-family {Segoe UI} -size 9 -weight bold")
        self.c_CalibrationIndicatorLabel.configure(foreground="#ff0000")
        self.c_CalibrationIndicatorLabel.configure(highlightbackground="#d9d9d9")
        self.c_CalibrationIndicatorLabel.configure(highlightcolor="#000000")
        self.c_CalibrationIndicatorLabel.configure(text='''Not Calibrated''')

        self.c_StatusConnectionLabel = tk.Label(self.Frame4)
        self.c_StatusConnectionLabel.place(relx=0.044, rely=0.204, height=20
                , width=108)
        self.c_StatusConnectionLabel.configure(activebackground="#d9d9d9")
        self.c_StatusConnectionLabel.configure(activeforeground="black")
        self.c_StatusConnectionLabel.configure(anchor='w')
        self.c_StatusConnectionLabel.configure(background="#d9d9d9")
        self.c_StatusConnectionLabel.configure(compound='left')
        self.c_StatusConnectionLabel.configure(disabledforeground="#a3a3a3")
        self.c_StatusConnectionLabel.configure(font="-family {Segoe UI} -size 9")
        self.c_StatusConnectionLabel.configure(foreground="#000000")
        self.c_StatusConnectionLabel.configure(highlightbackground="#d9d9d9")
        self.c_StatusConnectionLabel.configure(highlightcolor="#000000")
        self.c_StatusConnectionLabel.configure(text='''Status Connection:''')

        self.c_CalibratorButton = tk.Button(self.Frame4)
        self.c_CalibratorButton.place(relx=0.726, rely=0.855, height=26
                , width=107)
        self.c_CalibratorButton.configure(activebackground="#d9d9d9")
        self.c_CalibratorButton.configure(activeforeground="black")
        self.c_CalibratorButton.configure(background="#d9d9d9")
        self.c_CalibratorButton.configure(disabledforeground="#a3a3a3")
        self.c_CalibratorButton.configure(font="-family {Segoe UI} -size 9")
        self.c_CalibratorButton.configure(foreground="#000000")
        self.c_CalibratorButton.configure(highlightbackground="#d9d9d9")
        self.c_CalibratorButton.configure(highlightcolor="#000000")
        self.c_CalibratorButton.configure(text='''Start Calibrator''')
        self.c_CalibratorButton.configure(command=self.on_click_calibrate)

        #self.c_WaitLengthLabel = tk.Label(self.Frame4)
        #self.c_WaitLengthLabel.place(relx=0.044, rely=0.409, height=20
        #        , width=145)
        #self.c_WaitLengthLabel.configure(activebackground="#d9d9d9")
        #self.c_WaitLengthLabel.configure(activeforeground="black")
        #self.c_WaitLengthLabel.configure(anchor='w')
        #self.c_WaitLengthLabel.configure(background="#d9d9d9")
        #self.c_WaitLengthLabel.configure(compound='left')
        #self.c_WaitLengthLabel.configure(disabledforeground="#a3a3a3")
        #self.c_WaitLengthLabel.configure(font="-family {Segoe UI} -size 9")
        #self.c_WaitLengthLabel.configure(foreground="#000000")
        #self.c_WaitLengthLabel.configure(highlightbackground="#d9d9d9")
        #self.c_WaitLengthLabel.configure(highlightcolor="#000000")
        #self.c_WaitLengthLabel.configure(text='''Length of waiting interval''')

        self.c_MeasurementTimeLabel = tk.Label(self.Frame4)
        self.c_MeasurementTimeLabel.place(relx=0.044, rely=0.489, height=20
                , width=145)
        self.c_MeasurementTimeLabel.configure(activebackground="#d9d9d9")
        self.c_MeasurementTimeLabel.configure(activeforeground="black")
        self.c_MeasurementTimeLabel.configure(anchor='w')
        self.c_MeasurementTimeLabel.configure(background="#d9d9d9")
        self.c_MeasurementTimeLabel.configure(compound='left')
        self.c_MeasurementTimeLabel.configure(disabledforeground="#a3a3a3")
        self.c_MeasurementTimeLabel.configure(font="-family {Segoe UI} -size 9")
        self.c_MeasurementTimeLabel.configure(foreground="#000000")
        self.c_MeasurementTimeLabel.configure(highlightbackground="#d9d9d9")
        self.c_MeasurementTimeLabel.configure(highlightcolor="#000000")
        self.c_MeasurementTimeLabel.configure(text='''Measurement time''')

        #self.c_WaitLengthUnit = tk.Label(self.Frame4)
        #self.c_WaitLengthUnit.place(relx=0.726, rely=0.409, height=20, width=70)
        #self.c_WaitLengthUnit.configure(activebackground="#d9d9d9")
        #self.c_WaitLengthUnit.configure(activeforeground="black")
        #self.c_WaitLengthUnit.configure(anchor='w')
        #self.c_WaitLengthUnit.configure(background="#d9d9d9")
        #self.c_WaitLengthUnit.configure(compound='left')
        #self.c_WaitLengthUnit.configure(disabledforeground="#a3a3a3")
        #self.c_WaitLengthUnit.configure(font="-family {Segoe UI} -size 9")
        #self.c_WaitLengthUnit.configure(foreground="#000000")
        #self.c_WaitLengthUnit.configure(highlightbackground="#d9d9d9")
        #self.c_WaitLengthUnit.configure(highlightcolor="#000000")
        #self.c_WaitLengthUnit.configure(text='''Sec''')

        self.c_MeasurementTimeUnit = tk.Label(self.Frame4)
        self.c_MeasurementTimeUnit.place(relx=0.726, rely=0.489, height=20
                , width=51)
        self.c_MeasurementTimeUnit.configure(activebackground="#d9d9d9")
        self.c_MeasurementTimeUnit.configure(activeforeground="black")
        self.c_MeasurementTimeUnit.configure(anchor='w')
        self.c_MeasurementTimeUnit.configure(background="#d9d9d9")
        self.c_MeasurementTimeUnit.configure(compound='left')
        self.c_MeasurementTimeUnit.configure(disabledforeground="#a3a3a3")
        self.c_MeasurementTimeUnit.configure(font="-family {Segoe UI} -size 9")
        self.c_MeasurementTimeUnit.configure(foreground="#000000")
        self.c_MeasurementTimeUnit.configure(highlightbackground="#d9d9d9")
        self.c_MeasurementTimeUnit.configure(highlightcolor="#000000")
        self.c_MeasurementTimeUnit.configure(text='''Sec''')

        self.c_FrequencyLabel = tk.Label(self.Frame4)
        self.c_FrequencyLabel.place(relx=0.044, rely=0.57, height=20, width=164)
        self.c_FrequencyLabel.configure(activebackground="#d9d9d9")
        self.c_FrequencyLabel.configure(activeforeground="black")
        self.c_FrequencyLabel.configure(anchor='w')
        self.c_FrequencyLabel.configure(background="#d9d9d9")
        self.c_FrequencyLabel.configure(compound='left')
        self.c_FrequencyLabel.configure(disabledforeground="#a3a3a3")
        self.c_FrequencyLabel.configure(font="-family {Segoe UI} -size 9")
        self.c_FrequencyLabel.configure(foreground="#000000")
        self.c_FrequencyLabel.configure(highlightbackground="#d9d9d9")
        self.c_FrequencyLabel.configure(highlightcolor="#000000")
        self.c_FrequencyLabel.configure(text='''Frequency''')

        self.c_AccRangeLabel = tk.Label(self.Frame4)
        self.c_AccRangeLabel.place(relx=0.044, rely=0.651, height=21, width=127)
        self.c_AccRangeLabel.configure(activebackground="#d9d9d9")
        self.c_AccRangeLabel.configure(activeforeground="black")
        self.c_AccRangeLabel.configure(anchor='w')
        self.c_AccRangeLabel.configure(background="#d9d9d9")
        self.c_AccRangeLabel.configure(compound='left')
        self.c_AccRangeLabel.configure(disabledforeground="#a3a3a3")
        self.c_AccRangeLabel.configure(font="-family {Segoe UI} -size 9")
        self.c_AccRangeLabel.configure(foreground="#000000")
        self.c_AccRangeLabel.configure(highlightbackground="#d9d9d9")
        self.c_AccRangeLabel.configure(highlightcolor="#000000")
        self.c_AccRangeLabel.configure(text='''Acceleration range''')

        self.c_Hertz = tk.Label(self.Frame4)
        self.c_Hertz.place(relx=0.726, rely=0.57, height=20, width=41)
        self.c_Hertz.configure(activebackground="#d9d9d9")
        self.c_Hertz.configure(activeforeground="black")
        self.c_Hertz.configure(anchor='w')
        self.c_Hertz.configure(background="#d9d9d9")
        self.c_Hertz.configure(compound='left')
        self.c_Hertz.configure(disabledforeground="#a3a3a3")
        self.c_Hertz.configure(font="-family {Segoe UI} -size 9")
        self.c_Hertz.configure(foreground="#000000")
        self.c_Hertz.configure(highlightbackground="#d9d9d9")
        self.c_Hertz.configure(highlightcolor="#000000")
        self.c_Hertz.configure(text='''Hz''')

        self.c_g = tk.Label(self.Frame4)
        self.c_g.place(relx=0.726, rely=0.651, height=21, width=70)
        self.c_g.configure(activebackground="#d9d9d9")
        self.c_g.configure(activeforeground="black")
        self.c_g.configure(anchor='w')
        self.c_g.configure(background="#d9d9d9")
        self.c_g.configure(compound='left')
        self.c_g.configure(disabledforeground="#a3a3a3")
        self.c_g.configure(font="-family {Segoe UI} -size 9")
        self.c_g.configure(foreground="#000000")
        self.c_g.configure(highlightbackground="#d9d9d9")
        self.c_g.configure(highlightcolor="#000000")
        self.c_g.configure(text='''g (N/m^2)''')

        self.c_GyrRangeLabel = tk.Label(self.Frame4)
        self.c_GyrRangeLabel.place(relx=0.044, rely=0.736, height=20, width=127)
        self.c_GyrRangeLabel.configure(activebackground="#d9d9d9")
        self.c_GyrRangeLabel.configure(activeforeground="black")
        self.c_GyrRangeLabel.configure(anchor='w')
        self.c_GyrRangeLabel.configure(background="#d9d9d9")
        self.c_GyrRangeLabel.configure(compound='left')
        self.c_GyrRangeLabel.configure(disabledforeground="#a3a3a3")
        self.c_GyrRangeLabel.configure(font="-family {Segoe UI} -size 9")
        self.c_GyrRangeLabel.configure(foreground="#000000")
        self.c_GyrRangeLabel.configure(highlightbackground="#d9d9d9")
        self.c_GyrRangeLabel.configure(highlightcolor="#000000")
        self.c_GyrRangeLabel.configure(text='''Gyroscope range''')

        self.c_DegSec = tk.Label(self.Frame4)
        self.c_DegSec.place(relx=0.726, rely=0.736, height=20, width=60)
        self.c_DegSec.configure(activebackground="#d9d9d9")
        self.c_DegSec.configure(activeforeground="black")
        self.c_DegSec.configure(anchor='w')
        self.c_DegSec.configure(background="#d9d9d9")
        self.c_DegSec.configure(compound='left')
        self.c_DegSec.configure(disabledforeground="#a3a3a3")
        self.c_DegSec.configure(font="-family {Segoe UI} -size 9")
        self.c_DegSec.configure(foreground="#000000")
        self.c_DegSec.configure(highlightbackground="#d9d9d9")
        self.c_DegSec.configure(highlightcolor="#000000")
        self.c_DegSec.configure(text='''Deg / Sec''')

        self.Label7 = tk.Label(self.Frame4)
        self.Label7.place(relx=0.023, rely=0.038, height=19, width=410)
        self.Label7.configure(activebackground="#d9d9d9")
        self.Label7.configure(activeforeground="black")
        self.Label7.configure(background="#d9d9d9")
        self.Label7.configure(compound='left')
        self.Label7.configure(disabledforeground="#a3a3a3")
        self.Label7.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(highlightbackground="#d9d9d9")
        self.Label7.configure(highlightcolor="#000000")
        self.Label7.configure(text='''Die Connector & Calibrator''')

        #self.c_WaitLengthEntry = tk.Entry(self.Frame4)
        #self.c_WaitLengthEntry.place(relx=0.505, rely=0.409, height=20
        #        , relwidth=0.195)
        #self.c_WaitLengthEntry.configure(background="white")
        #self.c_WaitLengthEntry.configure(disabledforeground="#a3a3a3")
        #self.c_WaitLengthEntry.configure(font="-family {Courier New} -size 10")
        #self.c_WaitLengthEntry.configure(foreground="#000000")
        #self.c_WaitLengthEntry.configure(highlightbackground="#d9d9d9")
        #self.c_WaitLengthEntry.configure(highlightcolor="#000000")
        #self.c_WaitLengthEntry.configure(insertbackground="#000000")
        #self.c_WaitLengthEntry.configure(selectbackground="#d9d9d9")
        #self.c_WaitLengthEntry.configure(selectforeground="black")

        self.c_MeasurementTimeEntry = tk.Entry(self.Frame4)
        self.c_MeasurementTimeEntry.place(relx=0.505, rely=0.489, height=20
                , relwidth=0.195)
        self.c_MeasurementTimeEntry.configure(background="white")
        self.c_MeasurementTimeEntry.configure(disabledforeground="#a3a3a3")
        self.c_MeasurementTimeEntry.configure(font="-family {Courier New} -size 10")
        self.c_MeasurementTimeEntry.configure(foreground="#000000")
        self.c_MeasurementTimeEntry.configure(highlightbackground="#d9d9d9")
        self.c_MeasurementTimeEntry.configure(highlightcolor="#000000")
        self.c_MeasurementTimeEntry.configure(insertbackground="#000000")
        self.c_MeasurementTimeEntry.configure(selectbackground="#d9d9d9")
        self.c_MeasurementTimeEntry.configure(selectforeground="black")

        self.c_FrequencyEntry = ttk.Combobox(self.Frame4)
        self.c_FrequencyEntry.place(relx=0.505, rely=0.57, height=20
                , relwidth=0.195)
        self.c_FrequencyEntry.configure(background="white")
        self.c_FrequencyEntry.configure(font="-family {Courier New} -size 10")
        self.c_FrequencyEntry.configure(foreground="#000000")
        self.c_FrequencyEntry.configure(state='readonly')
        self.c_FrequencyEntry.configure(values=self.freq_options)
        self.c_FrequencyEntry.set(self.freq_options[2])


        self.c_AccRangeEntry = ttk.Combobox(self.Frame4)
        self.c_AccRangeEntry.place(relx=0.505, rely=0.651, height=20
                , relwidth=0.195)
        self.c_AccRangeEntry.configure(background="white")
        self.c_AccRangeEntry.configure(font="-family {Courier New} -size 10")
        self.c_AccRangeEntry.configure(foreground="#000000")
        self.c_AccRangeEntry.configure(values=self.accrange_options)
        self.c_AccRangeEntry.configure(state="readonly")
        self.c_AccRangeEntry.set(self.accrange_options[-2])
        
        self.c_GyrRangeEntry = ttk.Combobox(self.Frame4)
        self.c_GyrRangeEntry.place(relx=0.505, rely=0.736, height=20
                , relwidth=0.195)
        self.c_GyrRangeEntry.configure(background="white")
        self.c_GyrRangeEntry.configure(font="-family {Courier New} -size 10")
        self.c_GyrRangeEntry.configure(foreground="#000000")
        self.c_GyrRangeEntry.configure(values=self.gyrrange_options)
        self.c_GyrRangeEntry.configure(state="readonly")
        self.c_GyrRangeEntry.set(self.gyrrange_options[-1])

        self.Frame6 = tk.Frame(self.top)
        self.Frame6.place(relx=0.403, rely=0.821, relheight=0.106, relwidth=0.58)

        self.Frame6.configure(relief='groove')
        self.Frame6.configure(borderwidth="2")
        self.Frame6.configure(relief="groove")
        self.Frame6.configure(background="#d9d9d9")
        self.Frame6.configure(highlightbackground="#d9d9d9")
        self.Frame6.configure(highlightcolor="#000000")

        self.r_CurrentlyLoadedFileLabel = tk.Label(self.Frame6)
        self.r_CurrentlyLoadedFileLabel.place(relx=0.018, rely=0.303, height=25
                , width=116)
        self.r_CurrentlyLoadedFileLabel.configure(activebackground="#d9d9d9")
        self.r_CurrentlyLoadedFileLabel.configure(activeforeground="black")
        self.r_CurrentlyLoadedFileLabel.configure(anchor='w')
        self.r_CurrentlyLoadedFileLabel.configure(background="#d9d9d9")
        self.r_CurrentlyLoadedFileLabel.configure(compound='left')
        self.r_CurrentlyLoadedFileLabel.configure(disabledforeground="#a3a3a3")
        self.r_CurrentlyLoadedFileLabel.configure(font="-family {Segoe UI} -size 9")
        self.r_CurrentlyLoadedFileLabel.configure(foreground="#000000")
        self.r_CurrentlyLoadedFileLabel.configure(highlightbackground="#d9d9d9")
        self.r_CurrentlyLoadedFileLabel.configure(highlightcolor="#000000")
        self.r_CurrentlyLoadedFileLabel.configure(text='''Currently loaded file:''')

        self.r_LoadedFile = tk.Label(self.Frame6)
        self.r_LoadedFile.place(relx=0.171, rely=0.303, height=24, width=569)
        self.r_LoadedFile.configure(activebackground="#d9d9d9")
        self.r_LoadedFile.configure(activeforeground="black")
        self.r_LoadedFile.configure(anchor='w')
        self.r_LoadedFile.configure(background="#ffffff")
        self.r_LoadedFile.configure(compound='left')
        self.r_LoadedFile.configure(disabledforeground="#a3a3a3")
        self.r_LoadedFile.configure(font="-family {Segoe UI} -size 9")
        self.r_LoadedFile.configure(foreground="#000000")
        self.r_LoadedFile.configure(highlightbackground="#d9d9d9")
        self.r_LoadedFile.configure(highlightcolor="#000000")
        self.r_LoadedFile.configure(text='''No file loaded''')

        self.r_Results = tk.Button(self.Frame6)
        self.r_Results.place(relx=0.868, rely=0.263, height=26, width=97)
        self.r_Results.configure(activebackground="#d9d9d9")
        self.r_Results.configure(activeforeground="black")
        self.r_Results.configure(background="#d9d9d9")
        self.r_Results.configure(disabledforeground="#a3a3a3")
        self.r_Results.configure(font="-family {Segoe UI} -size 9")
        self.r_Results.configure(foreground="#000000")
        self.r_Results.configure(highlightbackground="#d9d9d9")
        self.r_Results.configure(highlightcolor="#000000")
        self.r_Results.configure(text='''Show Results''')
        self.r_Results.configure(command=self.on_click_results)

        self.QuitProgramButton = tk.Button(self.top)
        self.QuitProgramButton.place(relx=0.021, rely=0.944, height=26
                , width=127)
        self.QuitProgramButton.configure(activebackground="#d9d9d9")
        self.QuitProgramButton.configure(activeforeground="black")
        self.QuitProgramButton.configure(background="#d9d9d9")
        self.QuitProgramButton.configure(disabledforeground="#a3a3a3")
        self.QuitProgramButton.configure(font="-family {Segoe UI} -size 9")
        self.QuitProgramButton.configure(foreground="#000000")
        self.QuitProgramButton.configure(highlightbackground="#d9d9d9")
        self.QuitProgramButton.configure(highlightcolor="#000000")
        self.QuitProgramButton.configure(text='''Quit Program''')
        self.QuitProgramButton.configure(command=iocV7_support.on_destroy)

        self.Frame1 = tk.Frame(self.top)
        self.Frame1.place(relx=0.014, rely=0.014, relheight=0.165
                , relwidth=0.968)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="#000000")

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.place(relx=0.419, rely=0.059, height=22, width=290)
        self.Label1.configure(activebackground="#d9d9d9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(compound='left')
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font="-family {Segoe UI Black} -size 16 -weight bold -underline 1")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="#000000")
        self.Label1.configure(text='''Die Measurement Tool''')

        self.Message1 = tk.Message(self.Frame1)
        self.Message1.place(relx=0.128, rely=0.261, relheight=0.529
                , relwidth=0.783)
        self.Message1.configure(background="#d9d9d9")
        self.Message1.configure(font="-family {Segoe UI} -size 9")
        self.Message1.configure(foreground="#000000")
        self.Message1.configure(highlightbackground="#d9d9d9")
        self.Message1.configure(highlightcolor="#000000")
        self.Message1.configure(padx="1")
        self.Message1.configure(pady="1")
        self.Message1.configure(text='''This software has been created and developed by Bram Hament, Zibbo Huang, Niels van der Rijst, Jelte-Roel Span, and Thimo Speelman. This is performed as part of the Bachelor's End Project for Mechanical Engineering students at the Technical University of Delft.''')
        self.Message1.configure(width=1107)
    
    def browse_directory(self):
        #self.selected_directory = filedialog.askdirectory()
        print("Initializing browse directory...")
        self.selected_directory = iocV7_support.select_directory()
        if self.selected_directory:
            print(f"Directory selected: {self.selected_directory}")
            self.s_Dirname.configure(text=self.selected_directory)
            self.Scrolledlistbox1.delete(0, tk.END)
            for filename in os.listdir(self.selected_directory):
                if filename.endswith('.csv'):
                    self.Scrolledlistbox1.insert(tk.END, filename)
        else:
            self.selected_directory = None
            self.s_Dirname.configure(text="Please select a directory....")
        return self.selected_directory
                    
    def on_select_listbox(self, event):
        selected_item = self.Scrolledlistbox1.curselection()
        if selected_item:
            self.s_ApplyButton.configure(state=tk.NORMAL)
            
    def apply_selection(self):
        selected_item = self.Scrolledlistbox1.curselection()
        if selected_item:
            selected_file_name = self.Scrolledlistbox1.get(selected_item)
            self.RW_csv = os.path.join(self.selected_directory, selected_file_name)
            self.r_LoadedFile.configure(text=selected_file_name)
    
    def copy_values(self):
        # Retrieve the value from the Entry widget
        self.l_FreqEntry.set(self.c_FrequencyEntry.get())
        self.l_mt = self.c_MeasurementTimeEntry.get()
        self.l_MeasurementTimeEntry.delete(0, tk.END)
        self.l_MeasurementTimeEntry.insert(0, self.l_mt)
        self.l_AccRangeEntry.set(self.c_AccRangeEntry.get())
        self.l_GyrRangeEntry.set(self.c_GyrRangeEntry.get())

    def on_click_connect(self):
        self.disable_connect_cal_log()
        self.c_ConnectIndicatorLabel.configure(foreground="#ff8000")
        self.c_ConnectIndicatorLabel.configure(text="Connecting...")
        print("[LOG] Verbinding wordt geprobeerd....")
        try:
            #from dobbel import dobbellogger
            self.dob = iocV7_support.connect_function()
        except:
            print("[LOG] Foutmelding verbinding")
            tk.messagebox.showerror(title="Connection Error", message="Please check your bluetooth connection and try again.")
            self.c_ConnectIndicatorLabel.configure(foreground="#ff0000")
            self.c_ConnectIndicatorLabel.configure(text="Not Connected")
            self.enable_connect_cal_log()
            self.dob = None
            return
        print("[LOG] Verbinding vastgelegd, self.dob is defined.")
        tk.messagebox.showinfo(title="Connection", message="Connection successful")
        self.c_ConnectIndicatorLabel.configure(foreground="#008000")
        self.c_ConnectIndicatorLabel.configure(text="Connected")
        self.enable_connect_cal_log()
    
    def on_click_calibrate(self):
        if not self.selected_directory:
            tk.messagebox.showerror(title="Directory error",
                                   message="Please select a directory")
            self.selected_directory = self.browse_directory()
            if not self.selected_directory:
                tk.messagebox.showerror(title="Directory error",
                                       message="No directory selected. Exiting calibrator...")
                return
        self.disable_connect_cal_log()
        self.c_CalibrationIndicatorLabel.configure(foreground="#ff8000")
        self.c_CalibrationIndicatorLabel.configure(text="Calibrating...")
        self.list1 = []
        self.list2 = []
        self.list3 = []
        self.list4 = []
        if not self.dob:
            tk.messagebox.showerror(title="Error: Connection error",
                                   message = "Please connect the die to the software first.")
            self.c_CalibrationIndicatorLabel.configure(foreground="#ff0000")
            self.c_CalibrationIndicatorLabel.configure(text="Not Calibrated")
            self.enable_connect_cal_log()
            return
        try:
            self.c_lowi = 1
            self.c_mt = int(self.c_MeasurementTimeEntry.get())
            self.c_freq = int(self.c_FrequencyEntry.get())
            self.c_accrange = int(self.c_AccRangeEntry.get())
            self.c_gyrrange = int(self.c_GyrRangeEntry.get())
        except Exception as e:
            print(f"Error: {e}")
            tk.messagebox.showerror(title="Error: Calibration parameters",
                                   message = "One or multiple parameters are not integers!")
            self.c_CalibrationIndicatorLabel.configure(foreground="#ff0000")
            self.c_CalibrationIndicatorLabel.configure(text="Not Calibrated")
            self.enable_connect_cal_log()
            return
        for value in self.css_list:
            tk.messagebox.showinfo(title="Calibrator",
                                   message=f"Put the die with the number {value[2]} facing upwards. Then, press Ok. Do not touch the die after continuing.")
            try:
                self.list1, self.list2, self.list3, self.list4 = iocV7_support.calibrate_function_list(value, self.dob, self.list1, self.list2, self.list3, self.list4, self.c_mt, self.c_freq, self.c_accrange, self.c_gyrrange)
            except Exception as e:
                print(f"Error during calibration: {e}")
                return
        if not len(self.list1) == 6:
            tk.messagebox.showerror(title="Error: Calibration error",
                                   message = "Something went wrong during calibration.")
            self.c_CalibrationIndicatorLabel.configure(foreground="#ff0000")
            self.c_CalibrationIndicatorLabel.configure(text="Not Calibrated")
            self.enable_connect_cal_log()
            return
        try:
            self.cali, self.std_cali = iocV7_support.calibrate_cali_stdcali(self.dob, self.list1, self.list2, self.list3, self.list4, self.c_mt, self.c_freq, self.c_gyrrange)
        except AttributeError:
            tk.messagebox.showerror(title="Error: Connection Failure",
                                   message = "The die is disconnected.")
            self.c_CalibrationIndicatorLabel.configure(foreground="#ff0000")
            self.c_CalibrationIndicatorLabel.configure(text="Not Calibrated")
            self.enable_connect_cal_log()
            return
        except Exception as e:
            # Error detectie - Indien er iets misgaat. In theorie zou deze nooit voorkomen.
            print(f"An unexpected error occured: {e}")
            return
        ### SAVING CALIBRATION VLAUES ###
        if not self.selected_directory:
            self.selected_directory = iocV7_support.select_directory()
        iocV7_support.save_cali_values(self.cali, self.std_cali, self.selected_directory)
        ### END OF SAVE CODE ###
        self.c_CalibrationIndicatorLabel.configure(foreground="#008000")
        self.c_CalibrationIndicatorLabel.configure(text="Calibrated!")
        tk.messagebox.showinfo(title="Calibrator",
                               message = "The die has been calibrated and succesfully saved!")
        print("Calibration success!. Closing calibrator....")
        self.enable_connect_cal_log()
        
    def on_click_logging(self):
        self.disable_connect_cal_log()
        if not self.selected_directory:
            tk.messagebox.showerror(title="Directory error",
                                   message="Please select a directory to store logging results.")
            self.selected_directory = self.browse_directory()
            if not self.selected_directory:
                tk.messagebox.showerror(title="Directory error",
                                       message="No directory selected. Exiting logging tool...")
                self.enable_connect_cal_log()
                return
        try:
            self.l_mt = int(self.l_MeasurementTimeEntry.get())
            self.l_freq = int(self.l_FreqEntry.get())
            self.l_accrange = int(self.l_AccRangeEntry.get())
            self.l_gyrrange = int(self.l_GyrRangeEntry.get())
        except ValueError:
            tk.messagebox.showerror(title="Error: Logging parameters",
                                   message = "One or multiple logging parameters are not integers!")
            self.l_StatusLogIndicator.configure(foreground="#ff0000")
            self.l_StatusLogIndicator.configure(text="Not Logging")
            self.enable_connect_cal_log()
            return
        self.disable_connect_cal_log()
        self.l_StatusLogIndicator.configure(text="Preparing Logging Tool...")
        self.l_StatusLogIndicator.configure(foreground="#ffff00")
        if not self.dob:
            tk.messagebox.showerror(title="Error: Die connection error",
                                   message = "The die is not properly connected.")
            self.l_StatusLogIndicator.configure(foreground="#ff0000")
            self.l_StatusLogIndicator.configure(text="Not Logging")
            self.enable_connect_cal_log()
            return
        if not self.std_cali or not self.cali:
            tk.messagebox.showerror(title="Error: Die calibration error",
                                   message = "The die is not properly calibrated.")
            self.l_StatusLogIndicator.configure(foreground="#ff0000")
            self.l_StatusLogIndicator.configure(text="Not Logging")
            self.enable_connect_cal_log()
            return
        self.l_StatusLogIndicator.configure(text="Logging...")
        self.l_StatusLogIndicator.configure(foreground="#ff8000")
        tk.messagebox.showinfo(title="Die Logging Tool", 
                               message="Press Ok when you are ready to log. The logger will start after continuing.")
        
        #tk.messagebox.showinfo(title="Die Logging Tool", 
        #                       message="The logger has stopped logging. Downloading data now...")
        #self.l_StatusLogIndicator.configure(text="Downloading data...")
        #self.l_StatusLogIndicator.configure(foreground="#ff8000")
        #dob.download()
        self.output_data = iocV7_support.logging_function(self.dob, self.l_mt, self.l_freq, self.l_accrange, self.l_gyrrange)
        self.l_StatusLogIndicator.configure(text="Downloading...")
        self.l_StatusLogIndicator.configure(foreground="#008000")
        tk.messagebox.showinfo(title="Die Logging Tool", 
                               message="Logging Complete! Downloading data...")
        ############################
        ### NOG TE DOEN HIERTUSSEN:
        ### (- Data smoothing d.m.v. Kalman filter enz., tenzij dit pas wordt gedaan bij results)
        ############################
        self.date = iocV7_support.create_filename_date()
        self.filename = f"{self.date}_RawDieData"
        iocV7_support.save_dataframe_to_csv(self.output_data, self.filename, self.selected_directory)
        self.l_StatusLogIndicator.configure(text="Logging complete")
        self.l_StatusLogIndicator.configure(foreground="#008000")
        # Updating scrolled listbox with new entry
        if self.selected_directory:
            print(f"Reloading directory after logging: {self.selected_directory}")
            self.s_Dirname.configure(text=self.selected_directory)
            self.Scrolledlistbox1.delete(0, tk.END)
            for filename in os.listdir(self.selected_directory):
                if filename.endswith('.csv'):
                    self.Scrolledlistbox1.insert(tk.END, filename)
        # Select file instantly for review
        self.RW_csv = os.path.join(self.selected_directory, selected_file_name)
        
        tk.messagebox.showinfo(title="Die Logging Tool", message=f"Logging Complete. File is now saved in selected directory as {self.filename}")
        self.enable_connect_cal_log()
        
    def disable_connect_cal_log(self):
        self.c_CalibratorButton.configure(state=tk.DISABLED)
        self.l_StartLoggingButton.configure(state=tk.DISABLED)
        self.c_ConnectButton.configure(state=tk.DISABLED)
        
    def enable_connect_cal_log(self):
        self.c_CalibratorButton.configure(state=tk.NORMAL)
        self.l_StartLoggingButton.configure(state=tk.NORMAL)
        self.c_ConnectButton.configure(state=tk.NORMAL)
        
    def on_click_results(self):
        self.r_Results.configure(state=tk.DISABLED)
        if not self.RW_csv:
            tk.messagebox.showerror(title="CSV File Error",
                                    message="Please select a CSV file first.")
            self.r_Results.configure(state=tk.NORMAL)
            return
        print(f"[LOG] No calibration values specified yet.")
        tk.messagebox.showinfo(title="Calibration file",
                               message="Please select your calibration file (.npz)")
        self.cali, self.std_cali = iocV7_support.load_cali_values()
        if not self.cali or not self.std_cali:
            tk.messagebox.showerror(title="Results Error",
                                    message="No valid calibration values found and/or selected. Aborting process...")
            self.cali = None
            self.std_cali = None
            self.r_Results.configure(state=tk.NORMAL)
            return
        ## TODO: Variables defining for opening.
        self.RW_title = self.r_LoadedFile.cget("text")
        #self.cali = calibratie rot angles
        #self.std_cali = standard deviation
        #self.RW_csv = CSV bestand
        self.r_Results.configure(state=tk.NORMAL)
        iocV7_support.open_second_window(self.RW_title, self.RW_csv, self.cali, self.std_cali)
        
        
############## RESULTS WINDOW CLASS ##########################################        
class TW_Result:
    def __init__(self, top=None, RW_csv=None, cali=None, std_cali=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("1400x650+266+191")
        top.minsize(1400, 650)
        top.maxsize(1924, 1061)
        top.resizable(1,  1)
        #top.title("Results (Title of top window)")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")

        ### Initializing result variables
        self.top = top
        self.RW_csv = RW_csv        # Dit is het CSV bestand waar naar gekeken word.
        self.cali = cali
        self.std_cali = std_cali
        
        print(f"Bestand RW_csv: {self.RW_csv}")
        print(f"Type bestand van self.RW_csv: {type(self.RW_csv)}")
        ### Performing calculation
        try:
            self.df = pd.read_csv(self.RW_csv)
            print(f"[LOG] CSV geconverteerd naar pandas dataframe: {self.df}")
            self.results = iocV7_support.run_analysis(self.df, self.cali, self.std_cali, N=10, gamma=0.001, N_zv=5, gamma_zv=0.05, csv=False)
        except Exception as e:
            print(f"An unexpected error occured: {e}")
            tk.messagebox.showerror(title="Error: Results",
                                   message = "Results error! Please recheck your selected CSV file and try again.")
            iocV7_support.close_second_window()         

        self.Frame7 = tk.Frame(self.top)
        self.Frame7.place(relx=0.014, rely=0.015, relheight=0.94, relwidth=0.256)

        self.Frame7.configure(relief='groove')
        self.Frame7.configure(borderwidth="2")
        self.Frame7.configure(relief="groove")
        self.Frame7.configure(background="#d9d9d9")
        self.Frame7.configure(cursor="fleur")
        self.Frame7.configure(highlightbackground="#d9d9d9")
        self.Frame7.configure(highlightcolor="#000000")

        self.NR_PeakAcc = tk.Label(self.Frame7)
        self.NR_PeakAcc.place(relx=0.056, rely=0.458, height=27, width=145)
        self.NR_PeakAcc.configure(activebackground="#d9d9d9")
        self.NR_PeakAcc.configure(activeforeground="black")
        self.NR_PeakAcc.configure(anchor='w')
        self.NR_PeakAcc.configure(background="#d9d9d9")
        self.NR_PeakAcc.configure(compound='left')
        self.NR_PeakAcc.configure(disabledforeground="#a3a3a3")
        self.NR_PeakAcc.configure(font="-family {Segoe UI} -size 9")
        self.NR_PeakAcc.configure(foreground="#000000")
        self.NR_PeakAcc.configure(highlightbackground="#d9d9d9")
        self.NR_PeakAcc.configure(highlightcolor="#000000")
        self.NR_PeakAcc.configure(text='''Peak acceleration''')

        self.NR_PeakVel = tk.Label(self.Frame7)
        self.NR_PeakVel.place(relx=0.056, rely=0.409, height=28, width=131)
        self.NR_PeakVel.configure(activebackground="#d9d9d9")
        self.NR_PeakVel.configure(activeforeground="black")
        self.NR_PeakVel.configure(anchor='w')
        self.NR_PeakVel.configure(background="#d9d9d9")
        self.NR_PeakVel.configure(compound='left')
        self.NR_PeakVel.configure(disabledforeground="#a3a3a3")
        self.NR_PeakVel.configure(font="-family {Segoe UI} -size 9")
        self.NR_PeakVel.configure(foreground="#000000")
        self.NR_PeakVel.configure(highlightbackground="#d9d9d9")
        self.NR_PeakVel.configure(highlightcolor="#000000")
        self.NR_PeakVel.configure(text='''Peak velocity''')

        self.NR_AvgVelMidThrow = tk.Label(self.Frame7)
        self.NR_AvgVelMidThrow.place(relx=0.056, rely=0.36, height=27, width=214)

        self.NR_AvgVelMidThrow.configure(activebackground="#d9d9d9")
        self.NR_AvgVelMidThrow.configure(activeforeground="black")
        self.NR_AvgVelMidThrow.configure(anchor='w')
        self.NR_AvgVelMidThrow.configure(background="#d9d9d9")
        self.NR_AvgVelMidThrow.configure(compound='left')
        self.NR_AvgVelMidThrow.configure(disabledforeground="#a3a3a3")
        self.NR_AvgVelMidThrow.configure(font="-family {Segoe UI} -size 9")
        self.NR_AvgVelMidThrow.configure(foreground="#000000")
        self.NR_AvgVelMidThrow.configure(highlightbackground="#d9d9d9")
        self.NR_AvgVelMidThrow.configure(highlightcolor="#000000")
        self.NR_AvgVelMidThrow.configure(text='''Average velocity mid-throw''')

        self.NR_AvgVelOverall = tk.Label(self.Frame7)
        self.NR_AvgVelOverall.place(relx=0.056, rely=0.311, height=27, width=194)

        self.NR_AvgVelOverall.configure(activebackground="#d9d9d9")
        self.NR_AvgVelOverall.configure(activeforeground="black")
        self.NR_AvgVelOverall.configure(anchor='w')
        self.NR_AvgVelOverall.configure(background="#d9d9d9")
        self.NR_AvgVelOverall.configure(compound='left')
        self.NR_AvgVelOverall.configure(disabledforeground="#a3a3a3")
        self.NR_AvgVelOverall.configure(font="-family {Segoe UI} -size 9")
        self.NR_AvgVelOverall.configure(foreground="#000000")
        self.NR_AvgVelOverall.configure(highlightbackground="#d9d9d9")
        self.NR_AvgVelOverall.configure(highlightcolor="#000000")
        self.NR_AvgVelOverall.configure(text='''Average velocity overall''')

        self.NR_Rotations = tk.Label(self.Frame7)
        self.NR_Rotations.place(relx=0.056, rely=0.622, height=27, width=159)
        self.NR_Rotations.configure(activebackground="#d9d9d9")
        self.NR_Rotations.configure(activeforeground="black")
        self.NR_Rotations.configure(anchor='w')
        self.NR_Rotations.configure(background="#d9d9d9")
        self.NR_Rotations.configure(compound='left')
        self.NR_Rotations.configure(disabledforeground="#a3a3a3")
        self.NR_Rotations.configure(font="-family {Segoe UI} -size 9")
        self.NR_Rotations.configure(foreground="#000000")
        self.NR_Rotations.configure(highlightbackground="#d9d9d9")
        self.NR_Rotations.configure(highlightcolor="#000000")
        self.NR_Rotations.configure(text='''Amount of rotations''')

        self.NR_AvgAngVel = tk.Label(self.Frame7)
        self.NR_AvgAngVel.place(relx=0.056, rely=0.573, height=27, width=187)
        self.NR_AvgAngVel.configure(activebackground="#d9d9d9")
        self.NR_AvgAngVel.configure(activeforeground="black")
        self.NR_AvgAngVel.configure(anchor='w')
        self.NR_AvgAngVel.configure(background="#d9d9d9")
        self.NR_AvgAngVel.configure(compound='left')
        self.NR_AvgAngVel.configure(disabledforeground="#a3a3a3")
        self.NR_AvgAngVel.configure(font="-family {Segoe UI} -size 9")
        self.NR_AvgAngVel.configure(foreground="#000000")
        self.NR_AvgAngVel.configure(highlightbackground="#d9d9d9")
        self.NR_AvgAngVel.configure(highlightcolor="#000000")
        self.NR_AvgAngVel.configure(text='''Average angular velocity''')

        self.NR_StartTopValue = tk.Label(self.Frame7)
        self.NR_StartTopValue.place(relx=0.056, rely=0.72, height=27, width=131)
        self.NR_StartTopValue.configure(activebackground="#d9d9d9")
        self.NR_StartTopValue.configure(activeforeground="black")
        self.NR_StartTopValue.configure(anchor='w')
        self.NR_StartTopValue.configure(background="#d9d9d9")
        self.NR_StartTopValue.configure(compound='left')
        self.NR_StartTopValue.configure(disabledforeground="#a3a3a3")
        self.NR_StartTopValue.configure(font="-family {Segoe UI} -size 9")
        self.NR_StartTopValue.configure(foreground="#000000")
        self.NR_StartTopValue.configure(highlightbackground="#d9d9d9")
        self.NR_StartTopValue.configure(highlightcolor="#000000")
        self.NR_StartTopValue.configure(text='''Initial top value''')

        self.NR_FinalTopValue = tk.Label(self.Frame7)
        self.NR_FinalTopValue.place(relx=0.056, rely=0.769, height=28, width=131)

        self.NR_FinalTopValue.configure(activebackground="#d9d9d9")
        self.NR_FinalTopValue.configure(activeforeground="black")
        self.NR_FinalTopValue.configure(anchor='w')
        self.NR_FinalTopValue.configure(background="#d9d9d9")
        self.NR_FinalTopValue.configure(compound='left')
        self.NR_FinalTopValue.configure(disabledforeground="#a3a3a3")
        self.NR_FinalTopValue.configure(font="-family {Segoe UI} -size 9")
        self.NR_FinalTopValue.configure(foreground="#000000")
        self.NR_FinalTopValue.configure(highlightbackground="#d9d9d9")
        self.NR_FinalTopValue.configure(highlightcolor="#000000")
        self.NR_FinalTopValue.configure(text='''Final top value''')

        self.NR_TotalTime = tk.Label(self.Frame7)
        self.NR_TotalTime.place(relx=0.056, rely=0.065, height=25, width=150)
        self.NR_TotalTime.configure(activebackground="#d9d9d9")
        self.NR_TotalTime.configure(activeforeground="black")
        self.NR_TotalTime.configure(anchor='w')
        self.NR_TotalTime.configure(background="#d9d9d9")
        self.NR_TotalTime.configure(compound='left')
        self.NR_TotalTime.configure(disabledforeground="#a3a3a3")
        self.NR_TotalTime.configure(font="-family {Segoe UI} -size 9")
        self.NR_TotalTime.configure(foreground="#000000")
        self.NR_TotalTime.configure(highlightbackground="#d9d9d9")
        self.NR_TotalTime.configure(highlightcolor="#000000")
        self.NR_TotalTime.configure(text='''Total time''')

        self.NR_TimeInHand = tk.Label(self.Frame7)
        self.NR_TimeInHand.place(relx=0.056, rely=0.115, height=25, width=130)
        self.NR_TimeInHand.configure(activebackground="#d9d9d9")
        self.NR_TimeInHand.configure(activeforeground="black")
        self.NR_TimeInHand.configure(anchor='w')
        self.NR_TimeInHand.configure(background="#d9d9d9")
        self.NR_TimeInHand.configure(compound='left')
        self.NR_TimeInHand.configure(disabledforeground="#a3a3a3")
        self.NR_TimeInHand.configure(font="-family {Segoe UI} -size 9")
        self.NR_TimeInHand.configure(foreground="#000000")
        self.NR_TimeInHand.configure(highlightbackground="#d9d9d9")
        self.NR_TimeInHand.configure(highlightcolor="#000000")
        self.NR_TimeInHand.configure(text='''Time in hand''')

        self.NR_TimeInAir = tk.Label(self.Frame7)
        self.NR_TimeInAir.place(relx=0.056, rely=0.164, height=25, width=150)
        self.NR_TimeInAir.configure(activebackground="#d9d9d9")
        self.NR_TimeInAir.configure(activeforeground="black")
        self.NR_TimeInAir.configure(anchor='w')
        self.NR_TimeInAir.configure(background="#d9d9d9")
        self.NR_TimeInAir.configure(compound='left')
        self.NR_TimeInAir.configure(disabledforeground="#a3a3a3")
        self.NR_TimeInAir.configure(font="-family {Segoe UI} -size 9")
        self.NR_TimeInAir.configure(foreground="#000000")
        self.NR_TimeInAir.configure(highlightbackground="#d9d9d9")
        self.NR_TimeInAir.configure(highlightcolor="#000000")
        self.NR_TimeInAir.configure(text='''Time in air''')

        self.NR_TimeToFirstBounce = tk.Label(self.Frame7)
        self.NR_TimeToFirstBounce.place(relx=0.056, rely=0.213, height=25
                , width=150)
        self.NR_TimeToFirstBounce.configure(activebackground="#d9d9d9")
        self.NR_TimeToFirstBounce.configure(activeforeground="black")
        self.NR_TimeToFirstBounce.configure(anchor='w')
        self.NR_TimeToFirstBounce.configure(background="#d9d9d9")
        self.NR_TimeToFirstBounce.configure(compound='left')
        self.NR_TimeToFirstBounce.configure(disabledforeground="#a3a3a3")
        self.NR_TimeToFirstBounce.configure(font="-family {Segoe UI} -size 9")
        self.NR_TimeToFirstBounce.configure(foreground="#000000")
        self.NR_TimeToFirstBounce.configure(highlightbackground="#d9d9d9")
        self.NR_TimeToFirstBounce.configure(highlightcolor="#000000")
        self.NR_TimeToFirstBounce.configure(text='''Time to first bounce''')

        self.NR_TimeInHand_var = tk.Label(self.Frame7)
        self.NR_TimeInHand_var.place(relx=0.559, rely=0.115, height=25
                , width=150)
        self.NR_TimeInHand_var.configure(activebackground="#d9d9d9")
        self.NR_TimeInHand_var.configure(activeforeground="black")
        self.NR_TimeInHand_var.configure(anchor='w')
        self.NR_TimeInHand_var.configure(background="#d9d9d9")
        self.NR_TimeInHand_var.configure(compound='left')
        self.NR_TimeInHand_var.configure(disabledforeground="#a3a3a3")
        self.NR_TimeInHand_var.configure(font="-family {Segoe UI} -size 9")
        self.NR_TimeInHand_var.configure(foreground="#000000")
        self.NR_TimeInHand_var.configure(highlightbackground="#d9d9d9")
        self.NR_TimeInHand_var.configure(highlightcolor="#000000")
        self.NR_TimeInHand_var.configure(text='''<Time in hand>''')

        self.NR_TotalTime_var = tk.Label(self.Frame7)
        self.NR_TotalTime_var.place(relx=0.559, rely=0.065, height=25, width=150)

        self.NR_TotalTime_var.configure(activebackground="#d9d9d9")
        self.NR_TotalTime_var.configure(activeforeground="black")
        self.NR_TotalTime_var.configure(anchor='w')
        self.NR_TotalTime_var.configure(background="#d9d9d9")
        self.NR_TotalTime_var.configure(compound='left')
        self.NR_TotalTime_var.configure(disabledforeground="#a3a3a3")
        self.NR_TotalTime_var.configure(font="-family {Segoe UI} -size 9")
        self.NR_TotalTime_var.configure(foreground="#000000")
        self.NR_TotalTime_var.configure(highlightbackground="#d9d9d9")
        self.NR_TotalTime_var.configure(highlightcolor="#000000")
        self.NR_TotalTime_var.configure(text='''<Total Time>''')

        self.NR_TimeInAir_var = tk.Label(self.Frame7)
        self.NR_TimeInAir_var.place(relx=0.559, rely=0.164, height=25, width=150)

        self.NR_TimeInAir_var.configure(activebackground="#d9d9d9")
        self.NR_TimeInAir_var.configure(activeforeground="black")
        self.NR_TimeInAir_var.configure(anchor='w')
        self.NR_TimeInAir_var.configure(background="#d9d9d9")
        self.NR_TimeInAir_var.configure(compound='left')
        self.NR_TimeInAir_var.configure(disabledforeground="#a3a3a3")
        self.NR_TimeInAir_var.configure(font="-family {Segoe UI} -size 9")
        self.NR_TimeInAir_var.configure(foreground="#000000")
        self.NR_TimeInAir_var.configure(highlightbackground="#d9d9d9")
        self.NR_TimeInAir_var.configure(highlightcolor="#000000")
        self.NR_TimeInAir_var.configure(text='''<Time in air>''')

        self.NR_TimeFirstBounce_var = tk.Label(self.Frame7)
        self.NR_TimeFirstBounce_var.place(relx=0.559, rely=0.213, height=25
                , width=150)
        self.NR_TimeFirstBounce_var.configure(activebackground="#d9d9d9")
        self.NR_TimeFirstBounce_var.configure(activeforeground="black")
        self.NR_TimeFirstBounce_var.configure(anchor='w')
        self.NR_TimeFirstBounce_var.configure(background="#d9d9d9")
        self.NR_TimeFirstBounce_var.configure(compound='left')
        self.NR_TimeFirstBounce_var.configure(disabledforeground="#a3a3a3")
        self.NR_TimeFirstBounce_var.configure(font="-family {Segoe UI} -size 9")
        self.NR_TimeFirstBounce_var.configure(foreground="#000000")
        self.NR_TimeFirstBounce_var.configure(highlightbackground="#d9d9d9")
        self.NR_TimeFirstBounce_var.configure(highlightcolor="#000000")
        self.NR_TimeFirstBounce_var.configure(text='''<Time to first bounce>''')

        self.NR_AvgVelOverall_var = tk.Label(self.Frame7)
        self.NR_AvgVelOverall_var.place(relx=0.559, rely=0.311, height=25
                , width=150)
        self.NR_AvgVelOverall_var.configure(activebackground="#d9d9d9")
        self.NR_AvgVelOverall_var.configure(activeforeground="black")
        self.NR_AvgVelOverall_var.configure(anchor='w')
        self.NR_AvgVelOverall_var.configure(background="#d9d9d9")
        self.NR_AvgVelOverall_var.configure(compound='left')
        self.NR_AvgVelOverall_var.configure(disabledforeground="#a3a3a3")
        self.NR_AvgVelOverall_var.configure(font="-family {Segoe UI} -size 9")
        self.NR_AvgVelOverall_var.configure(foreground="#000000")
        self.NR_AvgVelOverall_var.configure(highlightbackground="#d9d9d9")
        self.NR_AvgVelOverall_var.configure(highlightcolor="#000000")
        self.NR_AvgVelOverall_var.configure(text='''<Avg Vel Overall>''')

        self.NR_AvgVelMT_var = tk.Label(self.Frame7)
        self.NR_AvgVelMT_var.place(relx=0.559, rely=0.36, height=25, width=150)
        self.NR_AvgVelMT_var.configure(activebackground="#d9d9d9")
        self.NR_AvgVelMT_var.configure(activeforeground="black")
        self.NR_AvgVelMT_var.configure(anchor='w')
        self.NR_AvgVelMT_var.configure(background="#d9d9d9")
        self.NR_AvgVelMT_var.configure(compound='left')
        self.NR_AvgVelMT_var.configure(disabledforeground="#a3a3a3")
        self.NR_AvgVelMT_var.configure(font="-family {Segoe UI} -size 9")
        self.NR_AvgVelMT_var.configure(foreground="#000000")
        self.NR_AvgVelMT_var.configure(highlightbackground="#d9d9d9")
        self.NR_AvgVelMT_var.configure(highlightcolor="#000000")
        self.NR_AvgVelMT_var.configure(text='''<Avg Vel Mid Throw>''')

        self.NR_PeakVal_var = tk.Label(self.Frame7)
        self.NR_PeakVal_var.place(relx=0.559, rely=0.409, height=25, width=150)
        self.NR_PeakVal_var.configure(activebackground="#d9d9d9")
        self.NR_PeakVal_var.configure(activeforeground="black")
        self.NR_PeakVal_var.configure(anchor='w')
        self.NR_PeakVal_var.configure(background="#d9d9d9")
        self.NR_PeakVal_var.configure(compound='left')
        self.NR_PeakVal_var.configure(disabledforeground="#a3a3a3")
        self.NR_PeakVal_var.configure(font="-family {Segoe UI} -size 9")
        self.NR_PeakVal_var.configure(foreground="#000000")
        self.NR_PeakVal_var.configure(highlightbackground="#d9d9d9")
        self.NR_PeakVal_var.configure(highlightcolor="#000000")
        self.NR_PeakVal_var.configure(text='''<Peak Vel>''')

        self.NR_PeakAcc_var = tk.Label(self.Frame7)
        self.NR_PeakAcc_var.place(relx=0.559, rely=0.458, height=25, width=150)
        self.NR_PeakAcc_var.configure(activebackground="#d9d9d9")
        self.NR_PeakAcc_var.configure(activeforeground="black")
        self.NR_PeakAcc_var.configure(anchor='w')
        self.NR_PeakAcc_var.configure(background="#d9d9d9")
        self.NR_PeakAcc_var.configure(compound='left')
        self.NR_PeakAcc_var.configure(disabledforeground="#a3a3a3")
        self.NR_PeakAcc_var.configure(font="-family {Segoe UI} -size 9")
        self.NR_PeakAcc_var.configure(foreground="#000000")
        self.NR_PeakAcc_var.configure(highlightbackground="#d9d9d9")
        self.NR_PeakAcc_var.configure(highlightcolor="#000000")
        self.NR_PeakAcc_var.configure(text='''<Peak Acc>''')

        self.NR_AvgAngVel_var = tk.Label(self.Frame7)
        self.NR_AvgAngVel_var.place(relx=0.559, rely=0.573, height=25, width=150)

        self.NR_AvgAngVel_var.configure(activebackground="#d9d9d9")
        self.NR_AvgAngVel_var.configure(activeforeground="black")
        self.NR_AvgAngVel_var.configure(anchor='w')
        self.NR_AvgAngVel_var.configure(background="#d9d9d9")
        self.NR_AvgAngVel_var.configure(compound='left')
        self.NR_AvgAngVel_var.configure(disabledforeground="#a3a3a3")
        self.NR_AvgAngVel_var.configure(font="-family {Segoe UI} -size 9")
        self.NR_AvgAngVel_var.configure(foreground="#000000")
        self.NR_AvgAngVel_var.configure(highlightbackground="#d9d9d9")
        self.NR_AvgAngVel_var.configure(highlightcolor="#000000")
        self.NR_AvgAngVel_var.configure(text='''<Avg Ang Vel>''')

        self.NR_Rotations_var = tk.Label(self.Frame7)
        self.NR_Rotations_var.place(relx=0.559, rely=0.622, height=25, width=150)

        self.NR_Rotations_var.configure(activebackground="#d9d9d9")
        self.NR_Rotations_var.configure(activeforeground="black")
        self.NR_Rotations_var.configure(anchor='w')
        self.NR_Rotations_var.configure(background="#d9d9d9")
        self.NR_Rotations_var.configure(compound='left')
        self.NR_Rotations_var.configure(disabledforeground="#a3a3a3")
        self.NR_Rotations_var.configure(font="-family {Segoe UI} -size 9")
        self.NR_Rotations_var.configure(foreground="#000000")
        self.NR_Rotations_var.configure(highlightbackground="#d9d9d9")
        self.NR_Rotations_var.configure(highlightcolor="#000000")
        self.NR_Rotations_var.configure(text=f"{RW_TotalRotWholeThrow(self.results")

        self.NR_FinTopVal_var = tk.Label(self.Frame7)
        self.NR_FinTopVal_var.place(relx=0.559, rely=0.769, height=25, width=150)

        self.NR_FinTopVal_var.configure(activebackground="#d9d9d9")
        self.NR_FinTopVal_var.configure(activeforeground="black")
        self.NR_FinTopVal_var.configure(anchor='w')
        self.NR_FinTopVal_var.configure(background="#d9d9d9")
        self.NR_FinTopVal_var.configure(compound='left')
        self.NR_FinTopVal_var.configure(disabledforeground="#a3a3a3")
        self.NR_FinTopVal_var.configure(font="-family {Segoe UI} -size 9")
        self.NR_FinTopVal_var.configure(foreground="#000000")
        self.NR_FinTopVal_var.configure(highlightbackground="#d9d9d9")
        self.NR_FinTopVal_var.configure(highlightcolor="#000000")
        self.NR_FinTopVal_var.configure(text=f"{RW_DieEndValue(self.results)}")

        #self.NR_InitTopVal_var = tk.Label(self.Frame7)
        #self.NR_InitTopVal_var.place(relx=0.559, rely=0.72, height=25, width=150)

        #self.NR_InitTopVal_var.configure(activebackground="#d9d9d9")
        #self.NR_InitTopVal_var.configure(activeforeground="black")
        #self.NR_InitTopVal_var.configure(anchor='w')
        #self.NR_InitTopVal_var.configure(background="#d9d9d9")
        #self.NR_InitTopVal_var.configure(compound='left')
        #self.NR_InitTopVal_var.configure(disabledforeground="#a3a3a3")
        #self.NR_InitTopVal_var.configure(font="-family {Segoe UI} -size 9")
        #self.NR_InitTopVal_var.configure(foreground="#000000")
        #self.NR_InitTopVal_var.configure(highlightbackground="#d9d9d9")
        #self.NR_InitTopVal_var.configure(highlightcolor="#000000")
        #self.NR_InitTopVal_var.configure(text='''<Initial Top Value>''')

        self.NR_Title = tk.Label(self.Frame7)
        self.NR_Title.place(relx=0.022, rely=0.011, height=26, width=339)
        self.NR_Title.configure(activebackground="#d9d9d9")
        self.NR_Title.configure(activeforeground="black")
        self.NR_Title.configure(background="#d9d9d9")
        self.NR_Title.configure(compound='left')
        self.NR_Title.configure(disabledforeground="#a3a3a3")
        self.NR_Title.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.NR_Title.configure(foreground="#000000")
        self.NR_Title.configure(highlightbackground="#d9d9d9")
        self.NR_Title.configure(highlightcolor="#000000")
        self.NR_Title.configure(text='''Numerical Results''')

        self.P_CalcRotFrame = tk.Frame(self.top)
        self.P_CalcRotFrame.place(relx=0.293, rely=0.692, relheight=0.263
                , relwidth=0.689)
        self.P_CalcRotFrame.configure(relief='groove')
        self.P_CalcRotFrame.configure(borderwidth="2")
        self.P_CalcRotFrame.configure(relief="groove")
        self.P_CalcRotFrame.configure(background="#d9d9d9")
        self.P_CalcRotFrame.configure(highlightbackground="#d9d9d9")
        self.P_CalcRotFrame.configure(highlightcolor="#000000")

        self.P_MeasAccFrame = tk.Frame(self.top)
        self.P_MeasAccFrame.place(relx=0.293, rely=0.069, relheight=0.262
                , relwidth=0.689)
        self.P_MeasAccFrame.configure(relief='groove')
        self.P_MeasAccFrame.configure(borderwidth="2")
        self.P_MeasAccFrame.configure(relief="groove")
        self.P_MeasAccFrame.configure(background="#d9d9d9")
        self.P_MeasAccFrame.configure(highlightbackground="#d9d9d9")
        self.P_MeasAccFrame.configure(highlightcolor="#000000")

        self.P_AngVelFrame = tk.Frame(self.top)
        self.P_AngVelFrame.place(relx=0.293, rely=0.385, relheight=0.263
                , relwidth=0.689)
        self.P_AngVelFrame.configure(relief='groove')
        self.P_AngVelFrame.configure(borderwidth="2")
        self.P_AngVelFrame.configure(relief="groove")
        self.P_AngVelFrame.configure(background="#d9d9d9")
        self.P_AngVelFrame.configure(highlightbackground="#d9d9d9")
        self.P_AngVelFrame.configure(highlightcolor="#000000")

        self.PT_MeasuredAccel = tk.Label(self.top)
        self.PT_MeasuredAccel.place(relx=0.293, rely=0.031, height=21, width=185)

        self.PT_MeasuredAccel.configure(activebackground="#d9d9d9")
        self.PT_MeasuredAccel.configure(activeforeground="black")
        self.PT_MeasuredAccel.configure(anchor='w')
        self.PT_MeasuredAccel.configure(background="#d9d9d9")
        self.PT_MeasuredAccel.configure(compound='left')
        self.PT_MeasuredAccel.configure(disabledforeground="#a3a3a3")
        self.PT_MeasuredAccel.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.PT_MeasuredAccel.configure(foreground="#000000")
        self.PT_MeasuredAccel.configure(highlightbackground="#d9d9d9")
        self.PT_MeasuredAccel.configure(highlightcolor="#000000")
        self.PT_MeasuredAccel.configure(text='''Measured acceleration''')

        self.PT_MeasuredAngularVelocity = tk.Label(self.top)
        self.PT_MeasuredAngularVelocity.place(relx=0.293, rely=0.346, height=21
                , width=214)
        self.PT_MeasuredAngularVelocity.configure(activebackground="#d9d9d9")
        self.PT_MeasuredAngularVelocity.configure(activeforeground="black")
        self.PT_MeasuredAngularVelocity.configure(anchor='w')
        self.PT_MeasuredAngularVelocity.configure(background="#d9d9d9")
        self.PT_MeasuredAngularVelocity.configure(compound='left')
        self.PT_MeasuredAngularVelocity.configure(disabledforeground="#a3a3a3")
        self.PT_MeasuredAngularVelocity.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.PT_MeasuredAngularVelocity.configure(foreground="#000000")
        self.PT_MeasuredAngularVelocity.configure(highlightbackground="#d9d9d9")
        self.PT_MeasuredAngularVelocity.configure(highlightcolor="#000000")
        self.PT_MeasuredAngularVelocity.configure(text='''Measured angular velocity''')

        self.PT_CalculatedRotations = tk.Label(self.top)
        self.PT_CalculatedRotations.place(relx=0.293, rely=0.654, height=21
                , width=165)
        self.PT_CalculatedRotations.configure(activebackground="#d9d9d9")
        self.PT_CalculatedRotations.configure(activeforeground="black")
        self.PT_CalculatedRotations.configure(anchor='w')
        self.PT_CalculatedRotations.configure(background="#d9d9d9")
        self.PT_CalculatedRotations.configure(compound='left')
        self.PT_CalculatedRotations.configure(disabledforeground="#a3a3a3")
        self.PT_CalculatedRotations.configure(font="-family {Segoe UI} -size 12 -weight bold")
        self.PT_CalculatedRotations.configure(foreground="#000000")
        self.PT_CalculatedRotations.configure(highlightbackground="#d9d9d9")
        self.PT_CalculatedRotations.configure(highlightcolor="#000000")
        self.PT_CalculatedRotations.configure(text='''Calculated rotations''')
        
        self.plot_data(RW_PlotAccXYZ, self.P_MeasAccFrame)
        self.plot_data(RW_PlotGyrXYZ, self.P_AngVelFrame)
        self.plot_data(RW_PlotEuler, self.P_CalcRotFrame)
        
        #self.export_to_savefile()
    
    def plot_data(self, func, frame):
        fig, ax = func(self.results)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def export_to_savefile(self):
        self.filedate = iocV7_support.create_filename_date()
        self.filename = f"{self.filedate}_Results.csv"
        self.results.to_csv(self.filename)
    

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, tk.Listbox):
    '''A standard Tkinter Listbox widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
    def size_(self):
        sz = tk.Listbox.size(self)
        return sz

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
            
def start_up():
    iocV7_support.main()

if __name__ == '__main__':
    iocV7_support.main()




