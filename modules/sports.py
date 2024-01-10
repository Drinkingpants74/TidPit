import sportsdataverse as sd
import time
import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO
import tkinter as tk

import prefs

nflTeam = prefs.nflTeam
cfbTeam = prefs.cfbTeam
nbaTeam = prefs.nbaTeam
nhlTeam = prefs.nhlTeam
cbbTeam = prefs.cbbTeam
Leagues = prefs.Leagues

cfb_df = None
dataCheck = -1
id_loc = -1
fontSize = 32


class gameInfo:
    def __init__(self):
        self.homeTeam = "none"
        self.homeLogo = ""
        self.homeColor = ""
        self.homeIMG = None
        self.awayTeam = "none"
        self.awayLogo = ""
        self.awayColor = ""
        self.awayIMG = None
        self.homePoints = 0
        self.awayPoints = 0
        self.clock = "00:00"
        self.quarter = "none"
        self.date = "00/00/0000"
        self.kickoff = "1:00 pm"
        self.dbCheck = -1
        self.imgsSet = False


def get_data_check(league, teamName, info):
    global cfb_df, dataCheck, id_loc
    if (info.dbCheck == -1):
        info.dbCheck = 0
        get_data(league, teamName, info)
    else:
        dateDT = datetime.datetime.strptime(info.date, "%m/%d/%y")
        if (dateDT.date() == datetime.datetime.now().date()):
            kickoffDT = datetime.datetime.strptime(info.kickoff, "%I:%M %p")
            if (kickoffDT.time() <= datetime.datetime.now().time()):
                if (info.dbCheck >= 40):
                    get_data(league, teamName, info)
            else:
                if (info.dbCheck >= 120):
                    get_data(league, teamName, info)
                    info.dbCheck = 0
                else:
                    info.dbCheck += 1
        else:
            if (info.dbCheck >= 120):
                get_data(league, teamName, info)
                info.dbCheck = 0
            else:
                info.dbCheck += 1


def get_data(league, teamName, info):
    global cfb_df, dataCheck, id_loc
    if (league == "NFL"):
        cfb_df = sd.espn_nfl_schedule()
    elif (league == "NBA"):
        cfb_df = sd.espn_nba_schedule()
    elif (league == "NHL"):
        cfb_df = sd.espn_nhl_schedule()
    elif (league == "CFB"):
        cfb_df = sd.espn_cfb_schedule()
    elif (league == "CBB"):
        cfb_df = sd.espn_mbb_schedule()

    count = 0
    for i in cfb_df["home_display_name"]:
        if (teamName == i):
            id_loc = count
            break
        count += 1

    count = 0
    for i in cfb_df["away_display_name"]:
        if (teamName == i):
            id_loc = count
            break
        count += 1

    if (id_loc != -1):
        info.homeTeam = cfb_df["home_display_name"][id_loc]
        info.homeLogo = cfb_df["home_logo"][id_loc]
        if (cfb_df["home_color"][id_loc] == "000000"):
            info.homeColor = "#" + cfb_df["home_alternate_color"][id_loc]
        else:
            info.homeColor = "#" + cfb_df["home_color"][id_loc]
        info.homePoints = cfb_df["home_score"][id_loc]
        info.awayTeam = cfb_df["away_display_name"][id_loc]
        info.awayLogo = cfb_df["away_logo"][id_loc]
        if (cfb_df["away_color"][id_loc] == "000000"):
            info.awayColor = "#" + cfb_df["away_alternate_color"][id_loc]
        else:
            info.awayColor = "#" + cfb_df["away_color"][id_loc]
        info.awayPoints = cfb_df["away_score"][id_loc]
        info.quarter = cfb_df["status_period"][id_loc]
        info.clock = cfb_df["status_display_clock"][id_loc]
    else:
        id_loc = 0
        info.homeTeam = cfb_df["home_display_name"][id_loc]
        info.homeLogo = cfb_df["home_logo"][id_loc]
        if (cfb_df["home_color"][id_loc] == "000000"):
            info.homeColor = "#" + cfb_df["home_alternate_color"][id_loc]
        else:
            info.homeColor = "#" + cfb_df["home_color"][id_loc]
        info.homePoints = cfb_df["home_score"][id_loc]
        info.awayTeam = cfb_df["away_display_name"][id_loc]
        info.awayLogo = cfb_df["away_logo"][id_loc]
        if (cfb_df["away_color"][id_loc] == "000000"):
            info.awayColor = "#" + cfb_df["away_alternate_color"][id_loc]
        else:
            info.awayColor = "#" + cfb_df["away_color"][id_loc]
        info.awayPoints = cfb_df["away_score"][id_loc]
        info.quarter = cfb_df["status_period"][id_loc]
        info.clock = cfb_df["status_display_clock"][id_loc]

    fix_time(info)


nflInfo = gameInfo()
cfbInfo = gameInfo()
nbaInfo = gameInfo()
nhlInfo = gameInfo()
cbbInfo = gameInfo()

def fix_time(info):
    temp = cfb_df["date"][id_loc]
    timeTemp = time.strptime(temp, "%Y-%m-%dT%H:%MZ")
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    timeTemp = time.mktime(timeTemp)
    timeTemp -= offset
    info.kickoff = time.strftime("%I:%M %p", time.localtime(timeTemp))
    info.date = time.strftime("%m/%d/%y", time.localtime(timeTemp))


class Nfl(tk.Frame):
    def __init__(self, window):
        global nflInfo, fontSize
        tk.Frame.__init__(self, window)
        self.configure(bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        fontSize = int(window.winfo_screenwidth() / 24)

        get_data_check("NFL", nflTeam, nflInfo)

        self.homeNameLBL = tk.Label(self, bg="black", fg=nflInfo.homeColor, text=nflInfo.homeTeam,
                                    font=("Sans Serif", fontSize), justify="center")
        self.awayNameLBL = tk.Label(self, bg="black", fg=nflInfo.awayColor, text=nflInfo.awayTeam,
                                    font=("Sans Serif", fontSize), justify="center")
        self.homeLogoIMG = tk.Label(self, bg="black", text="HOME", font=("Sans Serif", fontSize), justify="center")
        self.awayLogoIMG = tk.Label(self, bg="black", text="AWAY", font=("Sans Serif", fontSize), justify="center")

        self.set_display()

    def restart(self):
        get_data_check("NFL", nflTeam, nflInfo)
        self.set_display()

    def set_display(self):
        global nflInfo
        dateDT = datetime.datetime.strptime(nflInfo.date, "%m/%d/%y")
        if (dateDT.date() == datetime.datetime.now().date()):
            kickoffDT = datetime.datetime.strptime(nflInfo.kickoff, "%I:%M %p")
            if (kickoffDT.time() <= datetime.datetime.now().time()):
                self.set_ingame_info()
            else:
                self.set_pregame_info()
        elif (dateDT.date() < datetime.datetime.now().date()):
            self.set_ingame_info()
        else:
            self.set_pregame_info()

    def set_images(self):
        global nflInfo

        if (not nflInfo.imgsSet):
            homeLogo = requests.get(nflInfo.homeLogo)
            awayLogo = requests.get(nflInfo.awayLogo)
            homeIMG = Image.open(BytesIO(homeLogo.content))
            awayIMG = Image.open(BytesIO(awayLogo.content))
            nflInfo.homeIMG = ImageTk.PhotoImage(homeIMG)
            nflInfo.awayIMG = ImageTk.PhotoImage(awayIMG)
            nflInfo.imgsSet = True

        self.homeLogoIMG.configure(image=nflInfo.homeIMG)
        self.awayLogoIMG.configure(image=nflInfo.awayIMG)

    def set_pregame_info(self):
        global nflInfo

        kickoffData = nflInfo.date + " " + nflInfo.kickoff
        kickoffLBL = tk.Label(self, bg="black", fg="white", text=kickoffData,
                              font=("Sans Serif", fontSize), justify="center")

        self.set_images()
        self.homeLogoIMG.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
        self.homeNameLBL.place(relx=0.25, rely=0.65, anchor=tk.CENTER)
        self.awayLogoIMG.place(relx=0.75, rely=0.35, anchor=tk.CENTER)
        self.awayNameLBL.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
        kickoffLBL.place(relx=0.5, rely=0.85, anchor=tk.CENTER)


    def set_ingame_info(self):
        global nflInfo, fontSize

        homeScoreLBL = tk.Label(self, bg="black", fg=nflInfo.homeColor, text=nflInfo.homePoints,
                                font=("Sans Serif", fontSize))
        awayScoreLBL = tk.Label(self, bg="black", fg=nflInfo.awayColor, text=nflInfo.awayPoints,
                                font=("Sans Serif", fontSize))

        timeText = ""
        if (nflInfo.clock == "0:00"):
            timeText = "FINAL"
        else:
            timeText = "Quarter: " + str(nflInfo.quarter) + "\nTime: " + nflInfo.clock

        timeLBL = tk.Label(self, bg="black", fg="white", text=timeText, font=("Sans Serif", fontSize))

        self.set_images()
        self.homeLogoIMG.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
        self.homeNameLBL.place(relx=0.25, rely=0.65, anchor=tk.CENTER)
        self.awayLogoIMG.place(relx=0.75, rely=0.35, anchor=tk.CENTER)
        self.awayNameLBL.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
        homeScoreLBL.place(relx=0.25, rely=0.75, anchor=tk.CENTER)
        awayScoreLBL.place(relx=0.75, rely=0.75, anchor=tk.CENTER)
        timeLBL.place(relx=0.5, rely=0.85, anchor=tk.CENTER)


class Nba(tk.Frame):
    def __init__(self, window):
        global nbaInfo, fontSize
        tk.Frame.__init__(self, window)
        self.configure(bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        fontSize = int(window.winfo_screenwidth() / 24)

        get_data_check("NBA", nbaTeam, nbaInfo)

        self.homeNameLBL = tk.Label(self, bg="black", fg=nbaInfo.homeColor, text=nbaInfo.homeTeam,
                                    font=("Sans Serif", fontSize), justify="center")
        self.awayNameLBL = tk.Label(self, bg="black", fg=nbaInfo.awayColor, text=nbaInfo.awayTeam,
                                    font=("Sans Serif", fontSize), justify="center")
        self.homeLogoIMG = tk.Label(self, bg="black", text="HOME", font=("Sans Serif", fontSize), justify="center")
        self.awayLogoIMG = tk.Label(self, bg="black", text="AWAY", font=("Sans Serif", fontSize), justify="center")

        self.set_display()

    def restart(self):
        get_data_check("NBA", nbaTeam, nbaInfo)
        self.set_display()

    def set_display(self):
        global nbaInfo
        dateDT = datetime.datetime.strptime(nbaInfo.date, "%m/%d/%y")
        if (dateDT.date() == datetime.datetime.now().date()):
            kickoffDT = datetime.datetime.strptime(nbaInfo.kickoff, "%I:%M %p")
            if (kickoffDT.time() <= datetime.datetime.now().time()):
                self.set_ingame_info()
            else:
                self.set_pregame_info()
        elif (dateDT.date() < datetime.datetime.now().date()):
            self.set_ingame_info()
        else:
            self.set_pregame_info()

    def set_images(self):
        global nbaInfo

        if (not nbaInfo.imgsSet):
            homeLogo = requests.get(nbaInfo.homeLogo)
            awayLogo = requests.get(nbaInfo.awayLogo)
            homeIMG = Image.open(BytesIO(homeLogo.content))
            awayIMG = Image.open(BytesIO(awayLogo.content))
            nbaInfo.homeIMG = ImageTk.PhotoImage(homeIMG)
            nbaInfo.awayIMG = ImageTk.PhotoImage(awayIMG)
            nbaInfo.imgsSet = True

        self.homeLogoIMG.configure(image=nbaInfo.homeIMG)
        self.awayLogoIMG.configure(image=nbaInfo.awayIMG)

    def set_pregame_info(self):
        global nbaInfo

        kickoffData = nbaInfo.date + " " + nbaInfo.kickoff
        kickoffLBL = tk.Label(self, bg="black", fg="white", text=kickoffData,
                              font=("Sans Serif", fontSize), justify="center")

        self.set_images()
        self.homeLogoIMG.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
        self.homeNameLBL.place(relx=0.25, rely=0.65, anchor=tk.CENTER)
        self.awayLogoIMG.place(relx=0.75, rely=0.35, anchor=tk.CENTER)
        self.awayNameLBL.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
        kickoffLBL.place(relx=0.5, rely=0.85, anchor=tk.CENTER)


    def set_ingame_info(self):
        global nbaInfo, fontSize

        homeScoreLBL = tk.Label(self, bg="black", fg=nbaInfo.homeColor, text=nbaInfo.homePoints,
                                font=("Sans Serif", fontSize))
        awayScoreLBL = tk.Label(self, bg="black", fg=nbaInfo.awayColor, text=nbaInfo.awayPoints,
                                font=("Sans Serif", fontSize))

        timeText = ""
        if (nbaInfo.clock == "0:00"):
            timeText = "FINAL"
        else:
            timeText = "Quarter: " + str(nbaInfo.quarter) + "\nTime: " + nbaInfo.clock

        timeLBL = tk.Label(self, bg="black", fg="white", text=timeText, font=("Sans Serif", fontSize))

        self.set_images()
        self.homeLogoIMG.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
        self.homeNameLBL.place(relx=0.25, rely=0.65, anchor=tk.CENTER)
        self.awayLogoIMG.place(relx=0.75, rely=0.35, anchor=tk.CENTER)
        self.awayNameLBL.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
        homeScoreLBL.place(relx=0.25, rely=0.75, anchor=tk.CENTER)
        awayScoreLBL.place(relx=0.75, rely=0.75, anchor=tk.CENTER)
        timeLBL.place(relx=0.5, rely=0.85, anchor=tk.CENTER)


class Nhl(tk.Frame):
    def __init__(self, window):
        global nhlInfo, fontSize
        tk.Frame.__init__(self, window)
        self.configure(bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        fontSize = int(window.winfo_screenwidth() / 24)

        get_data_check("NHL", nhlTeam, nhlInfo)

        self.homeNameLBL = tk.Label(self, bg="black", fg=nhlInfo.homeColor, text=nhlInfo.homeTeam,
                                    font=("Sans Serif", fontSize), justify="center")
        self.awayNameLBL = tk.Label(self, bg="black", fg=nhlInfo.awayColor, text=nhlInfo.awayTeam,
                                    font=("Sans Serif", fontSize), justify="center")
        self.homeLogoIMG = tk.Label(self, bg="black", text="HOME", font=("Sans Serif", fontSize), justify="center")
        self.awayLogoIMG = tk.Label(self, bg="black", text="AWAY", font=("Sans Serif", fontSize), justify="center")

        self.set_display()

    def restart(self):
        get_data_check("NHL", nhlTeam, nhlInfo)
        self.set_display()

    def set_display(self):
        global nhlInfo
        dateDT = datetime.datetime.strptime(nhlInfo.date, "%m/%d/%y")
        if (dateDT.date() == datetime.datetime.now().date()):
            kickoffDT = datetime.datetime.strptime(nhlInfo.kickoff, "%I:%M %p")
            if (kickoffDT.time() <= datetime.datetime.now().time()):
                self.set_ingame_info()
            else:
                self.set_pregame_info()
        elif (dateDT.date() < datetime.datetime.now().date()):
            self.set_ingame_info()
        else:
            self.set_pregame_info()

    def set_images(self):
        global nhlInfo

        if (not nhlInfo.imgsSet):
            homeLogo = requests.get(nhlInfo.homeLogo)
            awayLogo = requests.get(nhlInfo.awayLogo)
            homeIMG = Image.open(BytesIO(homeLogo.content))
            awayIMG = Image.open(BytesIO(awayLogo.content))
            nhlInfo.homeIMG = ImageTk.PhotoImage(homeIMG)
            nhlInfo.awayIMG = ImageTk.PhotoImage(awayIMG)
            nhlInfo.imgsSet = True

        self.homeLogoIMG.configure(image=nhlInfo.homeIMG)
        self.awayLogoIMG.configure(image=nhlInfo.awayIMG)

    def set_pregame_info(self):
        global nhlInfo

        kickoffData = nhlInfo.date + " " + nhlInfo.kickoff
        kickoffLBL = tk.Label(self, bg="black", fg="white", text=kickoffData,
                              font=("Sans Serif", fontSize), justify="center")

        self.set_images()
        self.homeLogoIMG.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
        self.homeNameLBL.place(relx=0.25, rely=0.65, anchor=tk.CENTER)
        self.awayLogoIMG.place(relx=0.75, rely=0.35, anchor=tk.CENTER)
        self.awayNameLBL.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
        kickoffLBL.place(relx=0.5, rely=0.85, anchor=tk.CENTER)


    def set_ingame_info(self):
        global nhlInfo, fontSize

        homeScoreLBL = tk.Label(self, bg="black", fg=nhlInfo.homeColor, text=nhlInfo.homePoints,
                                font=("Sans Serif", fontSize))
        awayScoreLBL = tk.Label(self, bg="black", fg=nhlInfo.awayColor, text=nhlInfo.awayPoints,
                                font=("Sans Serif", fontSize))

        timeText = ""
        if (nhlInfo.clock == "0:00"):
            timeText = "FINAL"
        else:
            timeText = "Quarter: " + str(nhlInfo.quarter) + "\nTime: " + nhlInfo.clock

        timeLBL = tk.Label(self, bg="black", fg="white", text=timeText, font=("Sans Serif", fontSize))

        self.set_images()
        self.homeLogoIMG.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
        self.homeNameLBL.place(relx=0.25, rely=0.65, anchor=tk.CENTER)
        self.awayLogoIMG.place(relx=0.75, rely=0.35, anchor=tk.CENTER)
        self.awayNameLBL.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
        homeScoreLBL.place(relx=0.25, rely=0.75, anchor=tk.CENTER)
        awayScoreLBL.place(relx=0.75, rely=0.75, anchor=tk.CENTER)
        timeLBL.place(relx=0.5, rely=0.85, anchor=tk.CENTER)


class Cfb(tk.Frame):
    def __init__(self, window):
        global cfbInfo, fontSize
        tk.Frame.__init__(self, window)
        self.configure(bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        fontSize = int(window.winfo_screenwidth() / 24)

        get_data_check("CFB", cfbTeam, cfbInfo)

        self.homeNameLBL = tk.Label(self, bg="black", fg=cfbInfo.homeColor, text=cfbInfo.homeTeam,
                                    font=("Sans Serif", fontSize), justify="center")
        self.awayNameLBL = tk.Label(self, bg="black", fg=cfbInfo.awayColor, text=cfbInfo.awayTeam,
                                    font=("Sans Serif", fontSize), justify="center")
        self.homeLogoIMG = tk.Label(self, bg="black", text="HOME", font=("Sans Serif", fontSize), justify="center")
        self.awayLogoIMG = tk.Label(self, bg="black", text="AWAY", font=("Sans Serif", fontSize), justify="center")

        self.set_display()

    def restart(self):
        get_data_check("CFB", cfbTeam, cfbInfo)
        self.set_display()

    def set_display(self):
        global cfbInfo
        dateDT = datetime.datetime.strptime(cfbInfo.date, "%m/%d/%y")
        if (dateDT.date() == datetime.datetime.now().date()):
            kickoffDT = datetime.datetime.strptime(cfbInfo.kickoff, "%I:%M %p")
            if (kickoffDT.time() <= datetime.datetime.now().time()):
                self.set_ingame_info()
            else:
                self.set_pregame_info()
        elif (dateDT.date() < datetime.datetime.now().date()):
            self.set_ingame_info()
        else:
            self.set_pregame_info()

    def set_images(self):
        global cfbInfo

        if (not cfbInfo.imgsSet):
            homeLogo = requests.get(cfbInfo.homeLogo)
            awayLogo = requests.get(cfbInfo.awayLogo)
            homeIMG = Image.open(BytesIO(homeLogo.content))
            awayIMG = Image.open(BytesIO(awayLogo.content))
            cfbInfo.homeIMG = ImageTk.PhotoImage(homeIMG)
            cfbInfo.awayIMG = ImageTk.PhotoImage(awayIMG)
            cfbInfo.imgsSet = True

        self.homeLogoIMG.configure(image=cfbInfo.homeIMG)
        self.awayLogoIMG.configure(image=cfbInfo.awayIMG)

    def set_pregame_info(self):
        global cfbInfo

        kickoffData = cfbInfo.date + " " + cfbInfo.kickoff
        kickoffLBL = tk.Label(self, bg="black", fg="white", text=kickoffData,
                              font=("Sans Serif", fontSize), justify="center")

        self.set_images()
        self.homeLogoIMG.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
        self.homeNameLBL.place(relx=0.25, rely=0.65, anchor=tk.CENTER)
        self.awayLogoIMG.place(relx=0.75, rely=0.35, anchor=tk.CENTER)
        self.awayNameLBL.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
        kickoffLBL.place(relx=0.5, rely=0.85, anchor=tk.CENTER)


    def set_ingame_info(self):
        global cfbInfo, fontSize

        homeScoreLBL = tk.Label(self, bg="black", fg=cfbInfo.homeColor, text=cfbInfo.homePoints,
                                font=("Sans Serif", fontSize))
        awayScoreLBL = tk.Label(self, bg="black", fg=cfbInfo.awayColor, text=cfbInfo.awayPoints,
                                font=("Sans Serif", fontSize))

        timeText = ""
        if (cfbInfo.clock == "0:00"):
            timeText = "FINAL"
        else:
            timeText = "Quarter: " + str(cfbInfo.quarter) + "\nTime: " + cfbInfo.clock

        timeLBL = tk.Label(self, bg="black", fg="white", text=timeText, font=("Sans Serif", fontSize))

        self.set_images()
        self.homeLogoIMG.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
        self.homeNameLBL.place(relx=0.25, rely=0.65, anchor=tk.CENTER)
        self.awayLogoIMG.place(relx=0.75, rely=0.35, anchor=tk.CENTER)
        self.awayNameLBL.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
        homeScoreLBL.place(relx=0.25, rely=0.75, anchor=tk.CENTER)
        awayScoreLBL.place(relx=0.75, rely=0.75, anchor=tk.CENTER)
        timeLBL.place(relx=0.5, rely=0.85, anchor=tk.CENTER)


class Cbb(tk.Frame):
    def __init__(self, window):
        global cbbInfo, fontSize
        tk.Frame.__init__(self, window)
        self.configure(bg="black")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        fontSize = int(window.winfo_screenwidth() / 24)

        get_data_check("CBB", cbbTeam, cbbInfo)

        self.homeNameLBL = tk.Label(self, bg="black", fg=cbbInfo.homeColor, text=cbbInfo.homeTeam,
                                    font=("Sans Serif", fontSize), justify="center")
        self.awayNameLBL = tk.Label(self, bg="black", fg=cbbInfo.awayColor, text=cbbInfo.awayTeam,
                                    font=("Sans Serif", fontSize), justify="center")
        self.homeLogoIMG = tk.Label(self, bg="black", text="HOME", font=("Sans Serif", fontSize), justify="center")
        self.awayLogoIMG = tk.Label(self, bg="black", text="AWAY", font=("Sans Serif", fontSize), justify="center")

        self.set_display()

    def restart(self):
        get_data_check("CBB", cbbTeam, cbbInfo)
        self.set_display()

    def set_display(self):
        global cbbInfo
        dateDT = datetime.datetime.strptime(cbbInfo.date, "%m/%d/%y")
        if (dateDT.date() == datetime.datetime.now().date()):
            kickoffDT = datetime.datetime.strptime(cbbInfo.kickoff, "%I:%M %p")
            if (kickoffDT.time() <= datetime.datetime.now().time()):
                self.set_ingame_info()
            else:
                self.set_pregame_info()
        elif (dateDT.date() < datetime.datetime.now().date()):
            self.set_ingame_info()
        else:
            self.set_pregame_info()

    def set_images(self):
        global cbbInfo

        if (not cbbInfo.imgsSet):
            homeLogo = requests.get(cbbInfo.homeLogo)
            awayLogo = requests.get(cbbInfo.awayLogo)
            homeIMG = Image.open(BytesIO(homeLogo.content))
            awayIMG = Image.open(BytesIO(awayLogo.content))
            cbbInfo.homeIMG = ImageTk.PhotoImage(homeIMG)
            cbbInfo.awayIMG = ImageTk.PhotoImage(awayIMG)
            cbbInfo.imgsSet = True

        self.homeLogoIMG.configure(image=cbbInfo.homeIMG)
        self.awayLogoIMG.configure(image=cbbInfo.awayIMG)

    def set_pregame_info(self):
        global cbbInfo

        kickoffData = cbbInfo.date + " " + cbbInfo.kickoff
        kickoffLBL = tk.Label(self, bg="black", fg="white", text=kickoffData,
                              font=("Sans Serif", fontSize), justify="center")

        self.set_images()
        self.homeLogoIMG.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
        self.homeNameLBL.place(relx=0.25, rely=0.65, anchor=tk.CENTER)
        self.awayLogoIMG.place(relx=0.75, rely=0.35, anchor=tk.CENTER)
        self.awayNameLBL.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
        kickoffLBL.place(relx=0.5, rely=0.85, anchor=tk.CENTER)


    def set_ingame_info(self):
        global cbbInfo, fontSize

        homeScoreLBL = tk.Label(self, bg="black", fg=cbbInfo.homeColor, text=cbbInfo.homePoints,
                                font=("Sans Serif", fontSize))
        awayScoreLBL = tk.Label(self, bg="black", fg=cbbInfo.awayColor, text=cbbInfo.awayPoints,
                                font=("Sans Serif", fontSize))

        timeText = ""
        if (cbbInfo.clock == "0:00"):
            timeText = "FINAL"
        else:
            timeText = "Quarter: " + str(cbbInfo.quarter) + "\nTime: " + cbbInfo.clock

        timeLBL = tk.Label(self, bg="black", fg="white", text=timeText, font=("Sans Serif", fontSize))

        self.set_images()
        self.homeLogoIMG.place(relx=0.25, rely=0.35, anchor=tk.CENTER)
        self.homeNameLBL.place(relx=0.25, rely=0.65, anchor=tk.CENTER)
        self.awayLogoIMG.place(relx=0.75, rely=0.35, anchor=tk.CENTER)
        self.awayNameLBL.place(relx=0.75, rely=0.65, anchor=tk.CENTER)
        homeScoreLBL.place(relx=0.25, rely=0.75, anchor=tk.CENTER)
        awayScoreLBL.place(relx=0.75, rely=0.75, anchor=tk.CENTER)
        timeLBL.place(relx=0.5, rely=0.85, anchor=tk.CENTER)