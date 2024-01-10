import time
import tkinter as tk

import prefs

strForm = "%I:%M %p"
textColor = prefs.textColor
BGColor = prefs.BGColor

def set_strForm():
    global strForm
    strForm = ""
    if (str(prefs.dayForm) != ""):
        strForm += str(prefs.dayForm) + "\n"
    if (str(prefs.dateForm) != ""):
        strForm += str(prefs.dateForm) + "\n"
    if (str(prefs.timeForm) != ""):
        strForm += str(prefs.timeForm)

class Clock(tk.Frame):
    def __init__(self, window):
        global textColor, BGColor
        tk.Frame.__init__(self, window)
        self.configure(bg=BGColor)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        self.lbl1 = tk.Label(self, bg=BGColor, fg=textColor, font=("Sans Serif", int(window.winfo_screenwidth() / 6), "bold"))
        self.lbl1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        set_strForm()
        self.time()

    def restart(self):
        set_strForm()
        self.time()

    def time(self):
        global strForm
        timeString = time.strftime(strForm, time.localtime())
        self.lbl1.configure(text=timeString)
        self.lbl1.after(100, self.time)