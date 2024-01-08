import time
import tkinter as tk
import tkinter.colorchooser

mainWindow = None
command = None
currFrame = None

selectedModules = []
fileNames = []

# Clock Vars
strForm = "%I:%M %p"
timeForm = "%I:%M %p"
dateForm = ""
dayForm = ""
color = "white"

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
        tk.Frame.__init__(self, window)
        self.configure()#bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        # self.infoLBL = tk.Label(self, )

        self.clockButt = tk.Button(self, bg="black", text="Clock", command=lambda: switchTo(ClockFrame))
        self.clockButt.grid(row=0, column=0)
        self.newsButt = tk.Button(self, bg="black", text="News", command=lambda: switchTo(NewsFrame))
        self.newsButt.grid(row=0, column=1)
        # self.sportsButt = tk.Button(self, bg="black", text="Sports", command=lambda: switchTo(SportsFrame))
        # self.sportsButt.grid(row=1, column=0)
        # self.weatherButt = tk.Button(self, bg="black", text="Weather", command=lambda: switchTo(None))
        # self.weatherButt.grid(row=1, column=1)

        self.clockButt = tk.Button(self, bg="black", text="Extras", command=lambda: switchTo(OtherFrame))
        self.clockButt.grid(row=1, column=1)

        self.finishButt = tk.Button(self, bg="black", text="Finish", command=end)
        self.finishButt.grid(row=5, column=0, columnspan=2)


class OtherFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure()#bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        self.fileName = tk.StringVar()

        instructions = "To Add Extra Modules (Non-Official), Enter the File Name\n"
        instructions += "as it appears in the file manager.\n"

        self.instMess = tk.Message(self, text=instructions)
        self.instMess.grid(row=0, column=0, sticky="nw", columnspan=4)
        self.instMess.configure(justify="left", width=500)

        self.fileLBL = tk.Label(self, text="File Name:")
        self.fileLBL.grid(row=1, column=0, sticky="nw")

        self.fileTB = tk.Entry(self, textvariable=self.fileName)
        self.fileTB.grid(row=1, column=1)

        self.confButt = tk.Button(self, text="Add Module", command=self.confirmClicked)
        self.confButt.grid(row=2, column=0)

        self.resetButt = tk.Button(self, text="Reset List", command=self.resetClicked)
        self.resetButt.grid(row=2, column=1)

        self.writeButt = tk.Button(self, text="Finish", command=return_to_main)
        self.writeButt.grid(row=2, column=2)

        self.listLBL = tk.Label(self, text="Functions To Add:")
        self.listLBL.grid(row=3, column=0, columnspan=3, sticky="s")
        # self.listLBL.configure(justify="left")

        global fileNames
        fileListContents = ""
        for i in fileNames:
            fileListContents += i.capitalize() + "\n"

        self.fileList = tk.Label(self, text=fileListContents)
        self.fileList.grid(row=4, column=0, columnspan=3)

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
        tk.Frame.__init__(self, window)
        self.configure()#bg="black")
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
        self.colorPickButt = tk.Button(self, text="Pick Color", command=self.set_color)
        self.colorResetButt = tk.Button(self, text="Reset Color", command=self.reset_color)

        self.timeInstLBL.grid(row=0, column=0, columnspan=4)
        self.timeFormButt1.grid(row=1, column=0)
        self.timeFormButt2.grid(row=1, column=1)
        self.timeFormButt3.grid(row=1, column=2)
        self.timeFormButt4.grid(row=1, column=3)

        self.dayInstLBL.grid(row=2, column=0, columnspan=4)
        self.dayFormButt1.grid(row=3, column=0)
        self.dayFormButt2.grid(row=3, column=1)
        self.dayFormButtx.grid(row=3, column=2)

        self.dateInstLBL.grid(row=4, column=0, columnspan=4)
        self.dateFormButt1.grid(row=5, column=0)
        self.dateFormButt2.grid(row=5, column=1)
        self.dateFormButt3.grid(row=5, column=2)
        self.dateFormButtx.grid(row=5, column=3)

        self.colorLBL.grid(row=6, column=0, columnspan=4)
        self.colorPickButt.grid(row=7, column=0)
        self.colorResetButt.grid(row=7, column=1)

        self.confButt = tk.Button(self, bg="black", text="Confirm Selection", command=self.addModule)
        self.confButt.grid(row=8, column=2, columnspan=1)

        self.confButt = tk.Button(self, bg="black", text="Return", command=return_to_main)
        self.confButt.grid(row=8, column=3, columnspan=1)

        global strForm, timeForm, dateForm, dayForm, color

        self.timeLBL = tk.Label(self, bg="black", fg="white", font=("Helvetica Neue", int(window.winfo_screenwidth() / 25), "bold"),
                                text=time.strftime(strForm, time.localtime()))
        self.timeLBL.grid(row=9, column=0, columnspan=4)
        self.timeLBL.grid_rowconfigure(0, weight=1)
        self.timeLBL.grid_columnconfigure(0, weight=1)

    def update_timeLBL(self):
        global strForm, timeForm, dateForm, dayForm, color
        self.timeLBL.configure(fg=color, text=time.strftime(strForm, time.localtime()))

    def update_strForm(self):
        global strForm, timeForm, dateForm, dayForm, color
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

    def set_color(self):
        global strForm, timeForm, dateForm, dayForm, color
        colorPicker = tkinter.colorchooser.askcolor(initialcolor="white")
        color = colorPicker[1]
        self.update_timeLBL()

    def reset_color(self):
        global strForm, timeForm, dateForm, dayForm, color
        color = "white"
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
        self.grid(row=0, column=0, columnspan=2, sticky="nsew")

        instructions = "Click On The League You Wish To Add a Team For:"

        self.instLBL = tk.Label(self, text=instructions)
        self.instLBL.grid(row=0, column=0, sticky="nw")

        self.nflButt = tk.Button(self, text="NFL", command=lambda: switchTo(NFLFrame))
        self.nflButt.grid(row=1, column=0)
        self.cfbButt = tk.Button(self, text="CFB", command=lambda: switchTo(CFBFrame))
        self.cfbButt.grid(row=1, column=1)
        self.nbaButt = tk.Button(self, text="NBA", command=lambda: switchTo(NBAFrame))
        self.nbaButt.grid(row=2, column=0)
        self.nhlButt = tk.Button(self, text="NHL", command=lambda: switchTo(NHLFrame))
        self.nhlButt.grid(row=2, column=1)
        self.cbbButt = tk.Button(self, text="CBB", command=lambda: switchTo(CBBFrame))
        self.cbbButt.grid(row=3, column=0)

        self.exitButt = tk.Button(self, text="Confirm", command=self.addModule)
        self.exitButt.grid(row=4, column=0)
        self.exitButt = tk.Button(self, text="Return", command=return_to_main)
        self.exitButt.grid(row=4, column=1)

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
        instLBL.grid(row=0, column=0, columnspan=4)

        r = 1
        c = 0
        count = 0

        for i in teamNames:
            butt = tk.Button(self, text=i, command=lambda name=i: set_teamName(name, "NFL"))
            if (count >= 4):
                r += 1
                c = 0
                count = 0
            butt.grid(row=r, column=c)
            count += 1
            c += 1

        returnButt = tk.Button(self, text="Return", command=lambda: switchTo(SportsFrame))
        returnButt.grid(row=r+1, column=0, columnspan=4)


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
        instLBL.grid(row=0, column=0, columnspan=4)

        r = 1
        c = 0
        count = 0

        for i in teamNames:
            butt = tk.Button(self, text=i, command=lambda name=i: set_teamName(name, "NBA"))
            if (count >= 4):
                r += 1
                c = 0
                count = 0
            butt.grid(row=r, column=c)
            count += 1
            c += 1

        returnButt = tk.Button(self, text="Return", command=lambda: switchTo(SportsFrame))
        returnButt.grid(row=r + 1, column=0, columnspan=4)


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
        instLBL.grid(row=0, column=0, columnspan=4)

        r = 1
        c = 0
        count = 0

        for i in teamNames:
            butt = tk.Button(self, text=i, command=lambda name=i: set_teamName(name, "NHL"))
            if (count >= 4):
                r += 1
                c = 0
                count = 0
            butt.grid(row=r, column=c)
            count += 1
            c += 1

        returnButt = tk.Button(self, text="Return", command=lambda: switchTo(SportsFrame))
        returnButt.grid(row=r + 1, column=0, columnspan=4)


class CFBFrame(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.configure()  # bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        instructions = "Enter The Full Team Name.\n"
        instructions += "EX: Duke Blue Devils"
        instLBL = tk.Label(self, text=instructions)
        instLBL.grid(row=0, column=0, columnspan=4)

        note = "Type In Your Favorite CFB Team:"
        noteLBL = tk.Label(self, text=note)
        noteLBL.grid(row=1, column=0)

        self.teamName = tk.StringVar()

        teamENT = tk.Entry(self, textvariable=self.teamName)
        teamENT.grid(row=1, column=1, columnspan=2)

        teamButt = tk.Button(self, text="Set Team", command=self.send_team)
        teamButt.grid(row=2, column=0)

        returnButt = tk.Button(self, text="Return", command=lambda: switchTo(SportsFrame))
        returnButt.grid(row=2, column=1)

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
        instLBL = tk.Label(self, text=instructions)
        instLBL.grid(row=0, column=0, columnspan=4)

        note = "Type In Your Favorite CBB Team:"
        noteLBL = tk.Label(self, text=note)
        noteLBL.grid(row=1, column=0)

        self.teamName = tk.StringVar()

        teamENT = tk.Entry(self, textvariable=self.teamName)
        teamENT.grid(row=1, column=1, columnspan=2)

        teamButt = tk.Button(self, text="Set Team", command=self.send_team)
        teamButt.grid(row=2, column=0)

        returnButt = tk.Button(self, text="Return", command=lambda: switchTo(SportsFrame))
        returnButt.grid(row=2, column=1)


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

        instructions = "The Default Location and Language are United States and English.\n"
        instructions += "To Use a Specific Source, enter the Source's URL.\nEX: cnn.com or foxnews.com\n"
        instructions += "To Exclude Sources, enter the Source's URL.\nEX: cnn.com or foxnews.com\n"

        instMESS = tk.Label(self, text=instructions, justify="left")
        instMESS.grid(row=0, column=0, columnspan=4, sticky="nw")


        self.genENT = tk.Entry(self, bg="black", textvariable=self.genText)
        self.genENT.grid(row=1, column=0, columnspan=3)

        countryButt = tk.Button(self, text="Set Country", command=self.set_country)
        languageButt = tk.Button(self, text="Set Language", command=self.set_language)
        sourceButt = tk.Button(self, text="Use Source", command=self.set_source)
        excludeButt = tk.Button(self, text="Add Exclusion", command=self.add_exclude)
        resetExcButt = tk.Button(self, text="Reset Exclusions", command=self.reset_exclude)

        countryButt.grid(row=2, column=0)
        languageButt.grid(row=2, column=1)
        sourceButt.grid(row=2, column=2)
        excludeButt.grid(row=2, column=3)
        resetExcButt.grid(row=2, column=4)

        returnButt = tk.Button(self, text="Return", command=return_to_main)
        confirmButt = tk.Button(self, text="Finish", command=self.addModule)

        returnButt.grid(row=3, column=5)
        confirmButt.grid(row=3, column=6)

        excLBL = tk.Label(self, text="Excluded Sources:")
        excLBL.grid(row=3, column=0, columnspan=4)

        self.excMESS = tk.Label(self)
        self.excMESS.grid(row=4, column=0, columnspan=4)



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