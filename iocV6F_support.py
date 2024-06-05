#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 8.0
#  in conjunction with Tcl version 8.6
#    Jun 04, 2024 10:26:20 AM CEST  platform: Windows NT

import os
import sys
if not os.path.dirname(__file__) in sys.path:
    sys.path.append(os.path.dirname(__file__))
    
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import iocV6F


_debug = True # False to eliminate debug printing from callback functions.

def on_destroy():
    root.destroy()
    sys.exit()

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , on_destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = iocV6F.Toplevel1(_top1)
    root.mainloop()

if __name__ == '__main__':
    iocV6F.start_up()




