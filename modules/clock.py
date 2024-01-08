import time
import tkinter as tk

import prefs

strForm = "%I:%M %p"
color = prefs.color

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
        global color
        tk.Frame.__init__(self, window)
        self.configure(bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        self.lbl1 = tk.Label(self, bg="black", fg=color, font=("Helvetica Neue", int(window.winfo_screenwidth() / 5), "bold"))
        self.lbl1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        set_strForm()
        self.time(self.lbl1)

    def delete(self):
        self.lbl1.destroy()
        self.destroy()

    def time(self, frame):
        global strForm
        timeString = time.strftime(strForm, time.localtime())
        frame.configure(text=timeString)
        frame.after(100, self.time, frame)