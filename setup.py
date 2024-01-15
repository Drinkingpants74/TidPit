import tkinter as tk
import setupClasses as CLASSES

window = tk.Tk()
window.title("TidPit GUI Setup")
window.minsize(height=int(window.winfo_screenheight()/2), width=int(window.winfo_screenwidth()/2))
window.configure(bg="#1f1f1f")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

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


def write_output():
    # global prefs
    with open("output.py", "w") as file:
        file.write("import tkinter as tk\n")
        for i in prefs["selectedModules"]:
            if (i == "NFL") or (i == "NBA") or (i == "NHL") or (i == "CFB") or (i == "CBB"):
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
activeFrames = []
currFramePos = 0
''')

        file.write('''
def loadFrames():
    global frameList, activeFrames
    for i in frameList:
        activeFrames.append(i(window))

    showFrames()
        

def showFrames():
    global activeFrames

    activeFrames[currFramePos].tkraise()
    activeFrames[currFramePos].restart()
    activeFrames[currFramePos].after(ms=30000, func=inc_currFramePos)


def inc_currFramePos():
    global currFramePos

    if (currFramePos >= (len(frameList) - 1)):
        currFramePos = 0
    else:
        currFramePos += 1

    showFrames()
        ''')

        file.write("\n")

        for i in prefs["selectedModules"]:
            file.write("frameList.append(" + i.capitalize() + ")\n")

        file.write("\n")

        file.write("loadFrames()\n")
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
    prefs["textColor"] = CLASSES.textColor
    prefs["BGColor"] = CLASSES.BGColor

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

    # Weather Vars
    prefs["tempForm"] = CLASSES.tempForm
    prefs["windForm"] = CLASSES.windForm
    prefs["dirForm"] = CLASSES.dirForm
    prefs["location"] = CLASSES.location

    write_prefs()
    write_output()
    window.destroy()


CLASSES.command = get_prefs
root = CLASSES.init(window)

window.mainloop()