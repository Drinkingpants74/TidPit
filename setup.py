import tkinter as tk
import setupClasses as CLASSES

window = tk.Tk()
window.title("TidPit GUI Setup")
window.minsize(height=int(window.winfo_screenheight()/2), width=int(window.winfo_screenwidth()/2))

fileNames = []

prefs = {}
frames = {}

def write_prefs(): # Write variables to Preferences.py and import necessary variables
    with open("prefs.py", "w") as file:
        for i in prefs:
            if (type(prefs[i]) is list):
                output = str(i) + " = ["
                count = len(prefs[i])
                for j in prefs[i]:
                    count -= 1
                    output += "\"" + str(j) + "\""
                    if (count != 0):
                        output += ", "
                output += "]\n"
                file.write(output)
            else:
                file.write(str(i) + " = " + "\"" + str(prefs[i]) + "\"" + "\n")


def prefs_test():
    for i in prefs:
        if (type(prefs[i]) is list):
            output = str(i) + " = ["
            count = len(prefs[i])
            for j in prefs[i]:
                count -= 1
                output += "\"" + str(j) + "\""
                if (count != 0):
                    output += ", "
            output += "]"
            print(output)
        else:
            print(str(i) + " = " + "\"" + str(prefs[i]) + "\"")


def write_output():
    # global prefs
    with open("output.py", "w") as file:
        file.write("import tkinter as tk\n")
        for i in prefs["selectedModules"]:
            if (i == "NFL"):
                file.write("from modules." + "sports" + " import " + str(i).capitalize() + "\n")
            else:
                file.write("from modules." + i + " import " + str(i).capitalize() + "\n")
        file.write("\n")


        file.write('''window = tk.Tk()
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.attributes("-fullscreen", True)
window.title("TidPit by DrinkingPants74")
window.eval('tk::PlaceWindow . center')
window.configure(bg="black")

frameList = []
currFramePos = 0
currFrame = None
''')

        file.write("\n")

        file.write('''
def loadFrame(frame):
    global currFramePos, currFrame
    if (frame != None):
        if (currFrame != None):
            currFrame.destroy()
        currFrame = frame(window)
        ''')

        file.write("\n")

        file.write('''
def showFrames():
    global currFramePos, currFrame

    loadFrame(frameList[currFramePos])
    if (currFramePos >= (len(frameList) - 1)):
        currFramePos = 0
    else:
        currFramePos += 1

    currFrame.after(30000, showFrames)
        ''')

        file.write("\n")

        for i in prefs["selectedModules"]:
            file.write("frameList.append(" + i.capitalize() + ")\n")

        file.write("\n")

        file.write("showFrames()\n")
        file.write("window.mainloop()\n")





def get_prefs():
    # Base Vars
    prefs["selectedModules"] = CLASSES.selectedModules
    prefs["fileNames"] = CLASSES.fileNames

    # Clock Vars
    # prefs["strForm"] = CLASSES.strForm
    prefs["timeForm"] = CLASSES.timeForm
    prefs["dateForm"] = CLASSES.dateForm
    prefs["dayForm"] = CLASSES.dayForm
    prefs["color"] = CLASSES.color

    # Sports Vars
    prefs["nflTeam"] = CLASSES.nflTeam
    prefs["cfbTeam"] = CLASSES.cfbTeam
    prefs["nbaTeam"] = CLASSES.nbaTeam
    prefs["nhlTeam"] = CLASSES.nhlTeam
    prefs["cbbTeam"] = CLASSES.cbbTeam
    prefs["Leagues"] = CLASSES.Leagues

    # News Vars
    prefs["newsSource"] = CLASSES.newsSource
    prefs["newsCountry"] = CLASSES.newsCountry
    prefs["newsLanguage"] = CLASSES.newsLanguage
    prefs["newsExclude"] = CLASSES.newsExclude

    prefs_test()
    write_prefs()
    write_output()
    window.destroy()


CLASSES.command = get_prefs
root = CLASSES.init(window)

window.mainloop()