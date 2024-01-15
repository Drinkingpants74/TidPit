import openmeteo_requests
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim
import tkinter as tk
from PIL import Image, ImageTk

import prefs

BGColor = "black"
textColor = "white"

icon = None

geolocator = Nominatim(user_agent="TidPit")
location = geolocator.geocode(prefs.location)

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": location.latitude,
    "longitude": location.longitude,
    "current": ["temperature_2m", "apparent_temperature", "wind_speed_10m", "wind_direction_10m",
                "dew_point_2m", "weather_code", "precipitation_probability"],
    "temperature_unit": str(prefs.tempForm),
    "wind_speed_unit": str(prefs.windForm),
    "precipitation_unit": "inch",
    "forecast_days": 1
}
responses = openmeteo.weather_api(url, params=params)
weather = responses[0]

current = weather.Current()

current_temperature_2m = current.Variables(0).Value()
current_apparent_temperature = current.Variables(1).Value()
current_wind_speed_10m = current.Variables(2).Value()
current_wind_direction_10m = current.Variables(3).Value()
current_dew_point = current.Variables(4).Value()
current_weather_code = current.Variables(5).Value()
current_precip_chance = current.Variables(6).Value()


class Weather(tk.Frame):
    def __init__(self, window):
        global textColor, BGColor
        tk.Frame.__init__(self, window)
        self.configure(bg=BGColor)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        self.iconLBL = tk.Label(self, text="ICON", font=("Sans Serif", int(window.winfo_screenwidth() / 25)))
        self.tempLBL = tk.Label(self, font=("Sans Serif", int(window.winfo_screenwidth() / 25)))
        self.feelLBL = tk.Label(self, font=("Sans Serif", int(window.winfo_screenwidth() / 25)))
        self.cloudLBL = tk.Label(self, font=("Sans Serif", int(window.winfo_screenwidth() / 25)))
        self.precipLBL = tk.Label(self, font=("Sans Serif", int(window.winfo_screenwidth() / 25)))
        self.windSpeedLBL = tk.Label(self, font=("Sans Serif", int(window.winfo_screenwidth() / 25)))
        self.windDirLBL = tk.Label(self, font=("Sans Serif", int(window.winfo_screenwidth() / 25)))
        self.locLBL = tk.Label(self, bg="black", text=prefs.location, font=("Sans Serif", int(window.winfo_screenwidth() / 25)))

        self.iconLBL.place(relx=0.5, rely=0.05, anchor="n")
        self.locLBL.place(relx=0.5, rely=0.25, anchor="n")
        self.tempLBL.place(relx=0.25, rely=0.4, anchor="n")
        self.feelLBL.place(relx=0.5, rely=0.4, anchor="n")
        self.cloudLBL.place(relx=0.75, rely=0.4, anchor="n")
        self.precipLBL.place(relx=0.25, rely=0.55, anchor="n")
        self.windSpeedLBL.place(relx=0.5, rely=0.55, anchor="n")
        self.windDirLBL.place(relx=0.75, rely=0.55, anchor="n")

        self.set_info()

    def restart(self):
        global current_temperature_2m, current_apparent_temperature, current_wind_speed_10m,\
            current_wind_direction_10m, current_dew_point, current_weather_code, current_precip_chance
        current = weather.Current()

        current_temperature_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_wind_speed_10m = current.Variables(2).Value()
        current_wind_direction_10m = current.Variables(3).Value()
        current_dew_point = current.Variables(4).Value()
        current_weather_code = current.Variables(5).Value()
        current_precip_chance = current.Variables(6).Value()

        self.set_info()

    def set_info(self):
        global icon
        self.set_icon()

        temp = "Temperature:\n" + str(round(current_temperature_2m)) + self.set_temp()
        feels = "Feels Like:\n" + str(round(current_apparent_temperature)) + self.set_temp()
        dew = "Dew Point:\n" + str(round(current_dew_point)) + self.set_temp()
        speed = "Wind Speed:\n" + str(round(current_wind_speed_10m)) + " " + prefs.windForm.upper()
        dir = "Wind Direction:\n" + self.set_dir()
        precip = "Precipitation:\n" + str(round(current_precip_chance)) + "%"

        self.iconLBL.configure(image=icon, bg="black")
        self.tempLBL.configure(text=temp, bg="black")
        self.feelLBL.configure(text=feels, bg="black")
        self.cloudLBL.configure(text=dew, bg="black")
        self.precipLBL.configure(text=precip, bg="black")
        self.windSpeedLBL.configure(text=speed, bg="black")
        self.windDirLBL.configure(text=dir, bg="black")


    def set_temp(self):
        if (prefs.tempForm == "celsius"):
            return "ºC"
        else:
            return "ºF"

    def set_dir(self):
        if (prefs.dirForm == "cardinal"):
            if (current_wind_direction_10m > 30) and (current_wind_direction_10m < 60):
                return "NE"
            elif (current_wind_direction_10m > 60) and (current_wind_direction_10m < 120):
                return "E"
            elif (current_wind_direction_10m > 120) and (current_wind_direction_10m < 150):
                return "SE"
            elif (current_wind_direction_10m > 150) and (current_wind_direction_10m < 210):
                return "S"
            elif (current_wind_direction_10m > 210) and (current_wind_direction_10m < 240):
                return "SW"
            elif (current_wind_direction_10m > 240) and (current_wind_direction_10m < 300):
                return "W"
            elif (current_wind_direction_10m > 300) and (current_wind_direction_10m < 330):
                return "NW"
            elif (current_wind_direction_10m > 330) and (current_wind_direction_10m < 30):
                return "N"
        else:
            return str(round(current_wind_direction_10m)) + "º"


    def set_icon(self):
        global icon

        iconTemp = None
        if (current_weather_code == 0):
            iconTemp = Image.open("icons/weather/summer.png")
        elif (current_weather_code == 1) or (current_weather_code == 2):
            iconTemp = Image.open("icons/weather/partly-cloudy.png")
        elif (current_weather_code == 3):
            iconTemp = Image.open("icons/weather/clouds.png")
        elif (current_weather_code == 51) or (current_weather_code == 53) or (current_weather_code == 55):
            iconTemp = Image.open("icons/weather/light-rain.png")
        elif (current_weather_code == 61) or (current_weather_code == 63) or (current_weather_code == 65):
            iconTemp = Image.open("icons/weather/rain.png")
        elif (current_weather_code == 71) or (current_weather_code == 73):
            iconTemp = Image.open("icons/weather/light-snow.png")
        elif (current_weather_code == 75):
            iconTemp = Image.open("icons/weather/snow.png")
        elif (current_weather_code == 81) or (current_weather_code == 83) or (current_weather_code == 85):
            iconTemp = Image.open("icons/weather/rainfall.png")
        elif (current_weather_code == 85) or (current_weather_code == 86):
            iconTemp = Image.open("icons/weather/snow-storm.png")
        elif (current_weather_code == 95):
            iconTemp = Image.open("icons/weather/storm-with-heavy-rain.png")
        iconTemp = iconTemp.resize((200, 200), 5)
        icon = ImageTk.PhotoImage(iconTemp)