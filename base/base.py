import tkinter as tk

window = tk.Tk()
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.attributes("-fullscreen", True)
window.title("TidPit by DrinkingPants74")
window.eval('tk::PlaceWindow . center')
window.configure(bg="black")


frameList = []
availFrames = {}
currFramePos = 0

def loadFrames():
    count = 0
    for f in frameList:
        frame = f()
        availFrames[count] = frame
        count += 1
    showFrame()

def showFrame():
    global currFramePos
    frame = availFrames[currFramePos]
    frame.tkraise()
    if (currFramePos >= (len(availFrames) - 1)):
        currFramePos = 0
    else:
        currFramePos += 1
    frame.after(30000, showFrame)
    # frame.after(120000, showFrame)


loadFrames()

tk.mainloop()
