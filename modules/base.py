import tkinter as tk

window = tk.Tk()
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.attributes("-fullscreen", True)
window.title("TidPit by DrinkingPants74")
window.eval('tk::PlaceWindow . center')
window.configure(bg="black")


frameList = []
currFramePos = 0
currFrame = None

def loadFrame(frame):
    global currFramePos, currFrame
    if (frame != None):
        if (currFrame != None):
            currFrame.destroy()
        currFrame = frame(window)

# def showFrame():
#     global currFramePos
#
#     frame = availFrames[currFramePos]
#     frame.tkraise()
#     if (currFramePos >= (len(availFrames) - 1)):
#         currFramePos = 0
#     else:
#         currFramePos += 1
#     frame.after(30000, showFrame)
#     # frame.after(120000, showFrame)

def showFrames():
    global currFramePos, currFrame

    loadFrame(frameList[currFramePos])
    if (currFramePos >= (len(frameList) - 1)):
        currFramePos = 0
    else:
        currFramePos += 1

    currFrame.after(30000, showFrames)

window.mainloop()
