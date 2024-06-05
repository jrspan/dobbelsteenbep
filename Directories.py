import os
import sys

def add_directories_to_sys_path(directory):
    """
    Recursively add directories to sys.path starting from the given directory.
    """
    # Initialize a set to store directories that have been added
    added_directories = set()

    # Define a helper function to recursively traverse directories
    def traverse_directory(dir_path):
        nonlocal added_directories
        # Get a list of all items (files and directories) in the current directory
        items = os.listdir(dir_path)
        for item in items:
            item_path = os.path.join(dir_path, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                # If it's a directory, check if it has already been added
                if item_path not in added_directories:
                    # Add the directory to sys.path and mark it as added
                    sys.path.append(item_path)
                    added_directories.add(item_path)
                    # Recursively traverse the subdirectory
                    traverse_directory(item_path)

    # Start traversing from the initial directory
    traverse_directory(directory)
    return added_directories
    
current_directory = os.path.dirname(__file__)
test = add_directories_to_sys_path(current_directory)

for thing in test:
    print(thing)