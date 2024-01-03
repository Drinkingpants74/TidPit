class Clock(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self, window)
        self.configure(bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        self.lbl1 = tk.Label(self, bg="black", font=("Helvetica Neue", int(window.winfo_screenwidth() / 5), "bold"))
        self.lbl1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.time(self.lbl1)

    def delete(self):
        self.lbl1.destroy()
        self.destroy()

    def time(self, frame):
        timeString = strftime("%I:%M %p", localtime())
        frame.configure(text=timeString)
        frame.after(100, self.time, frame)