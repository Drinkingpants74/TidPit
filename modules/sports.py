import sportsdataverse as sd
import PIL.ImageTk
import time
from PIL import Image
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
        self.awayTeam = "none"
        self.awayLogo = ""
        self.awayColor = ""
        self.homePoints = 0
        self.awayPoints = 0
        self.clock = "00:00"
        self.quarter = "none"
        self.date = "00/00/0000"
        self.kickoff = "1:00 pm"
        self.dbCheck = -1


def get_data_check(teamName, info):
    global cfb_df, dataCheck, id_loc
    if (info.dbCheck == -1):
        info.dbCheck = 0
        get_data(teamName, info)
    else:
        if (info.date == time.strftime("%m/%d/%y", time.localtime())) \
                and (info.kickoff <= time.strftime("%I:%M %p", time.localtime())):
            if (info.dbCheck >= 40):
                get_data(teamName, info)
        else:
            if (info.dbCheck >= 120):
                get_data(teamName, info)
                info.dbCheck = 0
            else:
                info.dbCheck += 1


def get_data(teamName, info):
    global cfb_df, dataCheck, id_loc
    cfb_df = sd.espn_nfl_schedule(week=18, season_type=2)

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

    info.homeTeam = cfb_df["home_display_name"][id_loc]
    info.homeLogo = cfb_df["home_logo"][id_loc]
    info.homeColor = "#" + cfb_df["home_color"][id_loc]
    info.homePoints = cfb_df["home_score"][id_loc]
    info.awayTeam = cfb_df["away_display_name"][id_loc]
    info.awayLogo = cfb_df["away_logo"][id_loc]
    info.awayColor = "#" + cfb_df["away_color"][id_loc]
    info.awayPoints = cfb_df["away_score"][id_loc]
    info.quarter = cfb_df["status_period"][id_loc]
    info.clock = cfb_df["status_display_clock"][id_loc]

    fix_time(info)

    print(info.homeTeam)
    print(info.homeLogo)
    print(info.homeColor)
    print(info.homePoints)
    print(info.awayTeam)
    print(info.awayLogo)
    print(info.awayColor)
    print(info.awayPoints)
    print(info.quarter)
    print(info.clock)
    print(info.date)
    print(info.kickoff)


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

        get_data_check(nflTeam, nflInfo)

        self.homeNameLBL = tk.Label(self, bg="black", fg=nflInfo.homeColor, text=nflInfo.homeTeam,
                                    font=("Helvetica Neue", fontSize), justify="center")
        self.awayNameLBL = tk.Label(self, bg="black", fg=nflInfo.awayColor, text=nflInfo.awayTeam,
                                    font=("Helvetica Neue", fontSize), justify="center")
        # self.homeLogoIMG = tk.Image(self, bg="black")
        # self.awayLogoIMG = tk.Image(self, bg="black")

        self.set_display()


    def set_display(self):
        global nflInfo
        if (nflInfo.date == time.strftime("%m/%d/%y", time.localtime())) \
                and (nflInfo.kickoff <= time.strftime("%I:%M %p", time.localtime())):
            self.set_ingame_info()
        else:
            self.set_pregame_info()

    def set_pregame_info(self):
        global nflInfo

        kickoffData = nflInfo.date + " " + nflInfo.kickoff
        kickoffLBL = tk.Label(self, bg="black", fg="white", text=kickoffData)

        self.homeNameLBL.grid(row=0, column=0)
        self.awayNameLBL.grid(row=0, column=1)
        kickoffLBL.grid(row=1, column=0, columnspan=2)


    def set_ingame_info(self):
        global gameInfo, fontSize

        homeScoreLBL = tk.Label(self, bg="black", fg=nflInfo.homeColor, text=nflInfo.homePoints,
                                font=("Helvetica Neue", fontSize))
        awayScoreLBL = tk.Label(self, bg="black", fg=nflInfo.awayColor, text=nflInfo.awayPoints)

        timeLBL = tk.Label(self, bg="black", fg="white", text=nflInfo.clock)

        self.homeNameLBL.grid(row=0, column=0)
        self.awayNameLBL.grid(row=0, column=1)
        homeScoreLBL.grid(row=1, column=0)
        awayScoreLBL.grid(row=1, column=1)
        timeLBL.grid(row=1, column=0, columnspan=2)
