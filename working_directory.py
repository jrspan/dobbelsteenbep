import os
def default_directory():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    
default_directory()