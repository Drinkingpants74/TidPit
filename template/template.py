import tkinter as tk
# Any Other Necessary Imports

# Persistent Global Vars

class TemplateName(tk.Frame):
    # Temporary Global Vars

    # Add TKInter Widgets Here, and Call Any Optional Startup Functions
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure(bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

    # Any Additional Functions
    # Note: These Functions Will NOT be Called By the Main Script.
    # Note: You Must Call Any Functions in init, and then branch out from there.
