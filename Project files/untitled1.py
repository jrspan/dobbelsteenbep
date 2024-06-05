import tkinter as tk

def show_confirm_dialog():
    # Disable main window interactions
    root.attributes("-disabled", True)
    
    confirm_dialog = tk.Toplevel(root)
    confirm_dialog.title("Confirmation")
    confirm_dialog.attributes("-topmost", True)
    
    label = tk.Label(confirm_dialog, text="Are you sure you want to continue?")
    label.pack(padx=10, pady=10)
    
    yes_button = tk.Button(confirm_dialog, text="Yes", command=lambda: close_confirm_dialog(confirm_dialog))
    yes_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    no_button = tk.Button(confirm_dialog, text="No", command=lambda: cancel_confirm_dialog(confirm_dialog))
    no_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    # Wait for the dialog to be closed
    confirm_dialog.wait_window(confirm_dialog)

def close_confirm_dialog(confirm_dialog):
    # Enable main window interactions
    root.attributes("-disabled", False)
    confirm_dialog.destroy()

def cancel_confirm_dialog(confirm_dialog):
    # Enable main window interactions
    root.attributes("-disabled", False)
    confirm_dialog.destroy()

root = tk.Tk()
button = tk.Button(root, text="Show Confirmation", command=show_confirm_dialog)
button.pack(padx=10, pady=10)

root.mainloop()
