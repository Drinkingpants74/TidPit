import time
import tkinter as tk
import tkinter.colorchooser

mainWindow = None
command = None
currFrame = None
setupBG = "#1f1f1f"

scaling = 1.0

selectedModules = []
fileNames = []
activeFrames = {}

# Clock Vars
strForm = "%I:%M %p"
timeForm = "%I:%M %p"
dateForm = ""
dayForm = ""
textColor = "white"
BGColor = "black"

# Sports Vars
nflTeam = "Buffalo Bills"
cfbTeam = "Georgia Bulldogs"
nbaTeam = "Houston Rockets"
nhlTeam = "Buffalo Sabres"
cbbTeam = "Duke Blue Devils"
Leagues= []

# News Vars
newsSource = "none"
newsCountry = "United States"
newsLanguage = "english"
newsExclude = []

# Weather Vars
tempForm = "fahrenheit"
windForm = "mph"
dirForm = "degrees"
location = "Dallas, TX"


def init(window):
    global mainWindow
    mainWindow = window
    switchTo(MainFrame)


def switchTo(frame):
    global currFrame
    if (frame != None):
        if (currFrame != None):
            currFrame.destroy()
        currFrame = frame(mainWindow)


def end():
    global command
    command()


def return_to_main():
    switchTo(MainFrame)


def set_teamName(name, league):
    global nflTeam, cfbTeam, nbaTeam, nhlTeam, cbbTeam, Leagues
    if (league == "NFL"):
        nflTeam = name
        selectedModules.append("NFL")
    elif (league == "CFB"):
        cfbTeam = name
        selectedModules.append("CFB")
    elif (league == "NBA"):
        selectedModules.append("NBA")
        nbaTeam = name
    elif (league == "NHL"):
        selectedModules.append("NHL")
        nhlTeam = name
    elif (league == "CBB"):
        selectedModules.append("CBB")
        cbbTeam = name

    Leagues.append(league)
    switchTo(SportsFrame)


class MainFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window, bg=setupBG)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        # self.place(relx=0.0, rely=0.0, anchor=tk.CENTER)

        self.clockButt = tk.Button(self, bg=setupBG, font=("sans-serif", 64), width=6,
                                   text="Clock", command=lambda: switchTo(ClockFrame))
        # self.clockButt.grid(row=0, column=0)
        self.clockButt.place(relx=0.17, rely=0.1, anchor=tk.CENTER)

        self.newsButt = tk.Button(self, bg=setupBG, font=("sans-serif", 64), width=6,
                                  text="News", command=lambda: switchTo(NewsFrame))
        # self.newsButt.grid(row=0, column=1)
        self.newsButt.place(relx=0.17, rely=0.3, anchor=tk.CENTER)

        self.sportsButt = tk.Button(self, bg=setupBG, font=("sans-serif", 64), width=6,
                                          text="Sports", command=lambda: switchTo(SportsFrame))
        # self.sportsButt.grid(row=0, column=2)
        self.sportsButt.place(relx=0.17, rely=0.5, anchor=tk.CENTER)

        self.weatherButt = tk.Button(self, bg=setupBG, font=("sans-serif", 64), width=6,
                                     text="Weather", command=lambda: switchTo(WeatherFrame))
        self.weatherButt.place(relx=0.17, rely=0.7, anchor=tk.CENTER)

        self.extrasButt = tk.Button(self, bg=setupBG, font=("sans-serif", 64), width=6,
                                  text="Extras", command=lambda: switchTo(OtherFrame))
        # self.extrasButt.grid(row=1, column=1)
        self.extrasButt.place(relx=0.83, rely=0.71, anchor=tk.CENTER)

        self.finishButt = tk.Button(self, bg=setupBG, font=("sans-serif", 64), width=6,
                                  text="Finish", command=end)
        # self.finishButt.grid(row=2, column=0, columnspan=3)
        self.finishButt.place(relx=0.83, rely=0.91, anchor=tk.CENTER)


class OtherFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window, bg=setupBG)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        self.fileName = tk.StringVar()

        instructions = "To Add Extra Modules (Non-Official), Enter the File Name\n"
        instructions += "as it appears in the file manager.\n"

        self.instMess = tk.Message(self, bg=setupBG, font=("sans-serif", 32),
                                   text=instructions, justify="left", width=1000)
        self.instMess.place(relx=0.0, rely=0.0, anchor="nw")

        self.fileLBL = tk.Label(self, bg=setupBG, font=("sans-serif", 32),
                                   text="File Name:")
        self.fileLBL.place(relx=0.1, rely=0.23, anchor="w")

        self.fileTB = tk.Entry(self, bg="black", font=("sans-serif", 32),
                                   textvariable=self.fileName)
        self.fileTB.place(relx=0.3, rely=0.24, anchor="w")

        self.confButt = tk.Button(self, bg=setupBG, font=("sans-serif", 32),
                                   text="Add Module", command=self.confirmClicked)
        self.confButt.place(relx=0.1, rely=0.37, anchor="w")

        self.resetButt = tk.Button(self, bg=setupBG, font=("sans-serif", 32),
                                   text="Reset List", command=self.resetClicked)
        self.resetButt.place(relx=0.4, rely=0.37, anchor="w")

        self.writeButt = tk.Button(self, bg=setupBG, font=("sans-serif", 32),
                                   text="Finish", command=return_to_main)
        self.writeButt.place(relx=0.7, rely=0.37, anchor="w")

        self.listLBL = tk.Label(self, bg=setupBG, font=("sans-serif", 32),
                                   text="Functions To Add:")
        self.listLBL.place(relx=0.35, rely=0.47, anchor="w")

        global fileNames
        fileListContents = ""
        for i in fileNames:
            fileListContents += i.capitalize() + "\n"

        self.fileList = tk.Label(self, bg=setupBG, font=("sans-serif", 32), text=fileListContents)
        self.fileList.place(relx=0.45, rely=0.6, anchor="w")

    def confirmClicked(self):
        global fileNames
        fileNames.append(str(self.fileName.get()).lower())
        self.fileTB.delete(0, tk.END)
        self.refreshFileList()

    def resetClicked(self):
        global fileNames
        self.fileTB.delete(0, tk.END)
        fileNames.clear()
        self.refreshFileList()

    def refreshFileList(self):
        global fileNames
        fileListContents = ""
        for i in fileNames:
            fileListContents += i.capitalize() + "\n"
        self.fileList.configure(text=fileListContents)


class ClockFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window, bg=setupBG)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        self.timeInstLBL = tk.Label(self, text="Select The Time Presentation")
        self.timeFormButt1 = tk.Button(self, text="12-Hour W/ AM/PM", command=lambda: self.set_timeForm("%I:%M %p"))
        self.timeFormButt2 = tk.Button(self, text="12-Hour W/o AM/PM", command=lambda: self.set_timeForm("%I:%M"))
        self.timeFormButt3 = tk.Button(self, text="24-Hour Colon", command=lambda: self.set_timeForm("%H:%M"))
        self.timeFormButt4 = tk.Button(self, text="24-Hour Dot", command=lambda: self.set_timeForm("%H.%M"))

        self.dayInstLBL = tk.Label(self, text="Select The Day of Week Presentation")
        self.dayFormButt1 = tk.Button(self, text="Full Day Name", command=lambda: self.set_dayForm("%A "))
        self.dayFormButt2 = tk.Button(self, text="Shortened Day Name",command=lambda: self.set_dayForm("%a "))
        self.dayFormButtx = tk.Button(self, text="No Day Name", command=lambda: self.set_dayForm(""))

        self.dateInstLBL = tk.Label(self, text="Select The Date Presentation")
        self.dateFormButt1 = tk.Button(self, text="Abbv. Month Day", command=lambda: self.set_dateForm("%b %d "))
        self.dateFormButt2 = tk.Button(self, text="Full Month Day", command=lambda: self.set_dateForm("%B %d "))
        self.dateFormButt3 = tk.Button(self, text="Month/Day/Abbv. Year", command=lambda: self.set_dateForm("%m/%d/%y "))
        self.dateFormButt4 = tk.Button(self, text="Day/Month/Full Year", command=lambda: self.set_dateForm("%m/%d/%Y "))
        self.dateFormButtx = tk.Button(self, text="No Date", command=lambda: self.set_dateForm(""))

        self.colorLBL = tk.Label(self, text="Choose The Clock Color")
        self.colorTextButt = tk.Button(self, text="Text Color", command=self.set_color_text)
        self.colorResetTextButt = tk.Button(self, text="Reset Text Color", command=self.reset_color_text)
        self.colorBGButt = tk.Button(self, text="BG Color", command=self.set_color_BG)
        self.colorResetBGButt = tk.Button(self, text="Reset Text Color", command=self.reset_color_BG)

        self.timeInstLBL.place(relx=0.5, rely=0.03, anchor="center")
        self.timeFormButt1.place(relx=0.2, rely=0.1, anchor="center")
        self.timeFormButt2.place(relx=0.4, rely=0.1, anchor="center")
        self.timeFormButt3.place(relx=0.6, rely=0.1, anchor="center")
        self.timeFormButt4.place(relx=0.8, rely=0.1, anchor="center")

        self.dayInstLBL.place(relx=0.5, rely=0.2, anchor="center")
        self.dayFormButt1.place(relx=0.3, rely=0.27, anchor="center")
        self.dayFormButt2.place(relx=0.5, rely=0.27, anchor="center")
        self.dayFormButtx.place(relx=0.7, rely=0.27, anchor="center")

        self.dateInstLBL.place(relx=0.5, rely=0.37, anchor="center")
        self.dateFormButt1.place(relx=0.2, rely=0.44, anchor="center")
        self.dateFormButt2.place(relx=0.4, rely=0.44, anchor="center")
        self.dateFormButt3.place(relx=0.6, rely=0.44, anchor="center")
        self.dateFormButtx.place(relx=0.8, rely=0.44, anchor="center")

        self.colorLBL.place(relx=0.5, rely=0.54, anchor="center")
        self.colorTextButt.place(relx=0.2, rely=0.61, anchor="center")
        self.colorResetTextButt.place(relx=0.4, rely=0.61, anchor="center")
        self.colorBGButt.place(relx=0.6, rely=0.61, anchor="center")
        self.colorResetBGButt.place(relx=0.8, rely=0.61, anchor="center")

        self.confButt = tk.Button(self, bg="black", text="Confirm Selection", command=self.addModule)
        self.confButt.place(relx=0.4, rely=0.7, anchor="center")
        #
        self.confButt = tk.Button(self, bg="black", text="Return", command=return_to_main)
        self.confButt.place(relx=0.6, rely=0.7, anchor="center")

        global strForm, timeForm, dateForm, dayForm, color

        self.timeLBL = tk.Label(self, bg="black", fg="white", font=("Sans Serif", int(window.winfo_screenwidth() / 25), "bold"),
                                text=time.strftime(strForm, time.localtime()))
        self.timeLBL.place(relx=0.5, rely=0.85, anchor="center")

    def update_timeLBL(self):
        global strForm, textColor, BGColor
        self.timeLBL.configure(fg=textColor, bg=BGColor, text=time.strftime(strForm, time.localtime()))

    def update_strForm(self):
        global strForm, timeForm, dateForm, dayForm
        strForm = ""
        if (str(dayForm) != ""):
            strForm += str(dayForm) + "\n"
        if (str(dateForm) != ""):
            strForm += str(dateForm) + "\n"
        if (str(timeForm) != ""):
            strForm += str(timeForm)
        # strForm = str(dayForm) + "\n" + str(dateForm) + "\n" + str(timeForm)
        self.update_timeLBL()

    def set_timeForm(self, tf):
        global strForm, timeForm, dateForm, dayForm, color
        timeForm = tf
        self.update_strForm()

    def set_dateForm(self, df):
        global strForm, timeForm, dateForm, dayForm, color
        dateForm = df
        self.update_strForm()

    def set_dayForm(self, df):
        global strForm, timeForm, dateForm, dayForm, color
        dayForm = df
        self.update_strForm()

    def set_color_text(self):
        global textColor
        colorPicker = tkinter.colorchooser.askcolor(initialcolor="white")
        textColor = colorPicker[1]
        self.update_timeLBL()

    def set_color_BG(self):
        global BGColor
        colorPicker = tkinter.colorchooser.askcolor(initialcolor="black")
        BGColor = colorPicker[1]
        self.update_timeLBL()

    def reset_color_text(self):
        global textColor
        textColor = "white"
        self.update_timeLBL()

    def reset_color_BG(self):
        global BGColor
        BGColor = "black"
        self.update_timeLBL()

    def addModule(self):
        global selectedModules
        selectedModules.append("clock")
        return_to_main()


class SportsFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure()  # bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        instructions = "Click On The League You Wish To Add a Team For:"

        self.instLBL = tk.Label(self, text=instructions)
        self.instLBL.place(relx=0.5, rely=0.03, anchor="center")

        self.nflButt = tk.Button(self, text="NFL", font=("sans-serif", 32), command=lambda: switchTo(NFLFrame))
        self.nflButt.place(relx=0.4, rely=0.12, anchor="center")
        self.cfbButt = tk.Button(self, text="CFB", font=("sans-serif", 32), command=lambda: switchTo(CFBFrame))
        self.cfbButt.place(relx=0.6, rely=0.12, anchor="center")
        self.nbaButt = tk.Button(self, text="NBA", font=("sans-serif", 32), command=lambda: switchTo(NBAFrame))
        self.nbaButt.place(relx=0.4, rely=0.25, anchor="center")
        self.cbbButt = tk.Button(self, text="CBB", font=("sans-serif", 32), command=lambda: switchTo(CBBFrame))
        self.cbbButt.place(relx=0.6, rely=0.25, anchor="center")
        self.nhlButt = tk.Button(self, text="NHL", font=("sans-serif", 32), command=lambda: switchTo(NHLFrame))
        self.nhlButt.place(relx=0.5, rely=0.38, anchor="center")

        self.exitButt = tk.Button(self, text="Confirm", font=("sans-serif", 32), command=self.addModule)
        self.exitButt.place(relx=0.4, rely=0.5, anchor="center")
        self.exitButt = tk.Button(self, text="Return", font=("sans-serif", 32), command=return_to_main)
        self.exitButt.place(relx=0.6, rely=0.5, anchor="center")

    def addModule(self):
        # global selectedModules
        # selectedModules.append("sports")
        return_to_main()


class NFLFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure()  # bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        teamNames = [
            "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
            "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
            "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
            "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
            "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
            "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants",
            "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
            "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"
        ]

        instructions = "Select Your Favorite NFL Team:"
        instLBL = tk.Label(self, text=instructions)
        instLBL.place(relx=0.5, rely=0.03, anchor="center")

        r = 1
        c = 0
        count = 0

        for i in teamNames:
            butt = tk.Button(self, text=i, font=("sans-serif", 32), command=lambda name=i: set_teamName(name, "NFL"))
            if (count >= 4):
                r += 1
                c = 0
                count = 0
            butt.grid(row=r, column=c)
            count += 1
            c += 1

        returnButt = tk.Button(self, text="Return", font=("sans-serif", 32), command=lambda: switchTo(SportsFrame))
        returnButt.place(relx=0.5, rely=0.13, anchor="center")


class NBAFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure()  # bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        teamNames =[
            "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
            "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
            "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
            "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
            "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans","New York Knicks",
            "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns"
            "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors"
            "Utah Jazz", "Washington Wizards"
        ]

        instructions = "Select Your Favorite NBA Team:"
        instLBL = tk.Label(self, text=instructions)
        instLBL.place(relx=0.5, rely=0.03, anchor="center")

        r = 1
        c = 0
        count = 0

        for i in teamNames:
            butt = tk.Button(self, text=i, font=("sans-serif", 32), command=lambda name=i: set_teamName(name, "NBA"))
            if (count >= 4):
                r += 1
                c = 0
                count = 0
            butt.grid(row=r, column=c)
            count += 1
            c += 1

        returnButt = tk.Button(self, text="Return", font=("sans-serif", 32), command=lambda: switchTo(SportsFrame))
        returnButt.place(relx=0.5, rely=0.13, anchor="center")


class NHLFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure()  # bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        teamNames =[
            "Anaheim Ducks", "Arizona Coyotes", "Boston Bruins", "Buffalo Sabres",
            "Calgary Flames", "Carolina Hurricanes", "Chicago Blackhawks", "Colorado Avalanche",
            "Columbus Blue Jackets", "Dallas Stars", "Detroit Red Wings", "Edmonton Oilers"
            "Florida Panthers", "Los Angeles Kings", "Minnesota Wild", "Montreal Canadiens"
            "Nashville Predators", "New Jersey Devils", "New York Islanders", "New York Rangers"
            "Ottawa Senators", "Philadelphia Flyers", "Pittsburgh Penguins", "San Jose Sharks"
            "Seattle Kraken", "St Louis Blues", "Tampa Bay Lightning", "Toronto Maple Leafs"
            "Vancouver Canucks", "Vegas Golden Knights", "Washington Capitals", "Winnipeg Jets"
        ]

        instructions = "Select Your Favorite NHL Team:"
        instLBL = tk.Label(self, text=instructions)
        instLBL.place(relx=0.5, rely=0.03, anchor="center")

        r = 1
        c = 0
        count = 0

        for i in teamNames:
            butt = tk.Button(self, text=i, font=("sans-serif", 32), command=lambda name=i: set_teamName(name, "NHL"))
            if (count >= 3):
                r += 1
                c = 0
                count = 0
            butt.grid(row=r, column=c)
            count += 1
            c += 1

        returnButt = tk.Button(self, text="Return", font=("sans-serif", 32), command=lambda: switchTo(SportsFrame))
        returnButt.place(relx=0.5, rely=0.13, anchor="center")


class CFBFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure()  # bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        instructions = "Enter The Full Team Name.\n"
        instructions += "EX: Duke Blue Devils"
        instLBL = tk.Label(self, font=("sans-serif", 32), text=instructions)
        instLBL.place(relx=0.5, rely=0.0, anchor="n")

        note = "Type In Your Favorite CFB Team:"
        noteLBL = tk.Label(self, font=("sans-serif", 32), text=note)
        noteLBL.place(relx=0.5, rely=0.17, anchor="n")

        self.teamName = tk.StringVar()

        teamENT = tk.Entry(self, font=("sans-serif", 32), textvariable=self.teamName)
        teamENT.place(relx=0.5, rely=0.27, anchor="n")

        teamButt = tk.Button(self, text="Set Team", font=("sans-serif", 32), command=self.send_team)
        teamButt.place(relx=0.5, rely=0.4, anchor="n")

        returnButt = tk.Button(self, text="Return", font=("sans-serif", 32), command=lambda: switchTo(SportsFrame))
        returnButt.place(relx=0.5, rely=0.55, anchor="center")

    def send_team(self):
        set_teamName(self.teamName.get().title(), "CFB")


class CBBFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure()  # bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        instructions = "Enter The Full Team Name.\n"
        instructions += "EX: Duke Blue Devils"
        instLBL = tk.Label(self, font=("sans-serif", 32), text=instructions)
        instLBL.place(relx=0.5, rely=0.0, anchor="n")

        note = "Type In Your Favorite CBB Team:"
        noteLBL = tk.Label(self, font=("sans-serif", 32), text=note)
        noteLBL.place(relx=0.5, rely=0.17, anchor="n")

        self.teamName = tk.StringVar()

        teamENT = tk.Entry(self, font=("sans-serif", 32), textvariable=self.teamName)
        teamENT.place(relx=0.5, rely=0.27, anchor="n")

        teamButt = tk.Button(self, text="Set Team", font=("sans-serif", 32), command=self.send_team)
        teamButt.place(relx=0.5, rely=0.4, anchor="n")

        returnButt = tk.Button(self, text="Return", font=("sans-serif", 32), command=lambda: switchTo(SportsFrame))
        returnButt.place(relx=0.5, rely=0.55, anchor="center")


    def send_team(self):
        set_teamName(self.teamName.get().title(), "CBB")


class NewsFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure()  # bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        self.genText = tk.StringVar()

        instructions = "The Default Location and Language are United States\nand English. "
        instructions += "To Use a Specific Source, or Exclude Sources,\nenter the Source's URL.      "
        instructions += "EX: cnn.com or foxnews.com"

        instMESS = tk.Label(self, font=("sans-serif", 32), text=instructions, justify="left")
        instMESS.place(relx=0.0, rely=0.0, anchor="nw")


        self.genENT = tk.Entry(self, font=("sans-serif", 32), bg="black", textvariable=self.genText)
        self.genENT.place(relx=0.5, rely=0.32, anchor="center")

        countryButt = tk.Button(self, font=("sans-serif", 32), text="Set Country", command=self.set_country)
        languageButt = tk.Button(self, font=("sans-serif", 32), text="Set Language", command=self.set_language)
        sourceButt = tk.Button(self, font=("sans-serif", 32), text="Set Source", command=self.set_source)
        excludeButt = tk.Button(self, font=("sans-serif", 32), text="Add Exclusion", command=self.add_exclude)
        resetExcButt = tk.Button(self, font=("sans-serif", 32), text="Reset Exclusions", command=self.reset_exclude)

        countryButt.place(relx=0.00, rely=0.45, anchor="w")
        languageButt.place(relx=0.23, rely=0.45, anchor="w")
        sourceButt.place(relx=0.5, rely=0.45, anchor="w")
        excludeButt.place(relx=0.72, rely=0.45, anchor="w")
        resetExcButt.place(relx=0.58, rely=0.55, anchor="w")

        returnButt = tk.Button(self, font=("sans-serif", 32), text="Return", command=return_to_main)
        confirmButt = tk.Button(self, font=("sans-serif", 32), text="Finish", command=self.addModule)

        returnButt.place(relx=0.1, rely=0.55, anchor="w")
        confirmButt.place(relx=0.3, rely=0.55, anchor="w")

        excLBL = tk.Label(self, font=("sans-serif", 32), text="Excluded Sources:")
        excLBL.place(relx=0.5, rely=0.65, anchor="center")

        self.excMESS = tk.Label(self, font=("sans-serif", 32))
        self.excMESS.place(relx=0.5, rely=0.75, anchor="center")



    def set_source(self):
        global newsSource
        entry = self.genText.get().lower().strip()
        if (entry != ""):
            newsSource = entry
        self.genENT.delete(0, tk.END)

    def set_country(self):
        global newsCountry
        entry = self.genText.get().lower().strip()
        if (entry != ""):
            newsCountry = entry.title()
        self.genENT.delete(0, tk.END)

    def set_language(self):
        global newsLanguage
        entry = self.genText.get().lower().strip()
        if (entry != ""):
            newsLanguage = entry
        self.genENT.delete(0, tk.END)

    def add_exclude(self):
        global newsExclude
        entry = self.genText.get().lower().strip()
        if (entry != ""):
            newsExclude.append(entry)
        self.genENT.delete(0, tk.END)
        self.update_exclude()

    def reset_exclude(self):
        global newsExclude
        newsExclude.clear()
        self.genENT.delete(0, tk.END)
        self.update_exclude()

    def update_exclude(self):
        global newsExclude
        text = ""
        for i in newsExclude:
            text += i + "\n"
        self.excMESS.configure(text=text)

    def addModule(self):
        global selectedModules
        selectedModules.append("news")
        return_to_main()


class WeatherFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure()  # bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        self.locVar = tk.StringVar()

        tempLBL = tk.Label(self, text="Choose Temperature Format:", font=("sans-serif", 32))
        self.tempButton = tk.Button(self, font=("sans-serif", 32), text="ºF", command=self.set_temps)
        tempLBL.place(relx=0.0, rely=0.1, anchor="w")
        self.tempButton.place(relx=0.5, rely=0.1, anchor="w")

        windLBL = tk.Label(self, text="Choose Wind Speed Format:", font=("sans-serif", 32))
        self.windButton = tk.Button(self, font=("sans-serif", 32), text="MPH", command=self.set_wind)
        windLBL.place(relx=0.0, rely=0.25, anchor="w")
        self.windButton.place(relx=0.55, rely=0.25, anchor="center")

        dirLBL = tk.Label(self, text="Choose Wind Direction Format:", font=("sans-serif", 32))
        self.dirButton = tk.Button(self, font=("sans-serif", 32), text="Degrees", command=self.set_dir)
        dirLBL.place(relx=0.0, rely=0.4, anchor="w")
        self.dirButton.place(relx=0.62, rely=0.4, anchor="center")

        locLBL = tk.Label(self, text="Enter a Location:", font=("sans-serif", 32))
        self.locENT = tk.Entry(self, font=("sans-serif", 32), textvariable=self.locVar)
        locLBL.place(relx=0.0, rely=0.55, anchor="w")
        self.locENT.place(relx=0.3, rely=0.56, anchor="w")

        locConfirm = tk.Button(self, font=("sans-serif", 32), text="Set Location", command=self.set_location)
        locConfirm.place(relx=0.54, rely=0.67, anchor="center")

        confirmButt = tk.Button(self, font=("sans-serif", 32), text="Confirm", command=self.add_module)
        confirmButt.place(relx=0.4, rely=0.85, anchor="center")

        returnButt = tk.Button(self, font=("sans-serif", 32), text="Return", command=return_to_main)
        returnButt.place(relx=0.6, rely=0.85, anchor="center")

    def set_temps(self):
        global tempForm
        if (tempForm == "fahrenheit"):
            tempForm = "celsius"
            self.tempButton.configure(text="ºC")
        else:
            tempForm = "fahrenheit"
            self.tempButton.configure(text="ºF")

    def set_wind(self):
        global windForm
        if (windForm == "mph"):
            windForm = "kmh"
            self.windButton.configure(text="KMH")
        else:
            windForm = "mph"
            self.windButton.configure(text="MPH")

    def set_dir(self):
        global dirForm
        if (dirForm == "degrees"):
            dirForm = "cardinal"
            self.dirButton.configure(text="Cardinal")
        else:
            dirForm = "degrees"
            self.dirButton.configure(text="Degrees")

    def set_location(self):
        global location
        location = self.locVar.get()
        self.locENT.delete(0, tk.END)

    def add_module(self):
        global selectedModules
        selectedModules.append("weather")
        return_to_main()
