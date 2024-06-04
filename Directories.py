#### NOTE: This file is only used as a test for obtaining DIRECTORY PATHS.

import sys
import os

def dir_add(directory_name: str):
    # Adds a specific directory to the current sys path
    # Only works with directories stored in same folder as this code.
    dir_path = os.path.join(os.path.dirname(__file__), directory_name)
    if not dir_path in sys.path:
        sys.path.append(dir_path)
    
if not os.path.dirname(__file__) in sys.path:
    sys.path.append(os.path.dirname(__file__))
dir_add("Project Files")
import tkinter as tk
from tkinter import ttk

class MyApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("10-Second Timer Example")
        
        self.progress = ttk.Progressbar(root, orient='horizontal', mode='determinate', maximum=100, value=0)
        self.progress.pack(padx=20, pady=20, fill='x')
        
        self.start_button = ttk.Button(root, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=10)
        
        self.reset_button = ttk.Button(root, text="Reset Timer", command=self.reset_timer)
        self.reset_button.pack(pady=10)
        
    def start_timer(self):
        self.progress['value'] = 0  # Reset progress bar value
        self.update_progress(0)  # Start updating the progress bar
    
    def update_progress(self, value):
        if value <= 100:
            self.progress['value'] = value
            self.root.after(100, self.update_progress, value + 1)  # Schedule next update after 100ms
    
    def reset_timer(self):
        self.progress['value'] = 0  # Reset progress bar value

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApplication(root)
    root.mainloop()