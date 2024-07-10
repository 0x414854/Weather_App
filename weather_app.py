import requests
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageTk

"""
This script creates a weather application using Tkinter for the GUI and the OpenWeatherMap API 
to fetch and display weather data for a given city. The weather data includes temperature, 
humidity, wind speed, and more.
"""

API_KEY = "YOUR_API_KEY"
FONT_TITLE = ("Serif Bold", 18)
FONT_NORMAL = ("Serif", 8)

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving weather data: {e}")
        return None


def update_weather():
    city = city_entry.get()
    weather_data = get_weather_data(city)

    if weather_data:
        update_labels(weather_data)
    else:
        clear_labels()
        temperature_label.config(text=f"Error: {city} not found\nPlease enter a valid city name!")


def update_labels(weather_data):
    city_name = weather_data["name"]
    country = weather_data["sys"]["country"]
    temperature = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    temp_min = weather_data["main"]["temp_min"]
    temp_max = weather_data["main"]["temp_max"]
    weather = weather_data["weather"][0]["main"]
    weather_desc = weather_data["weather"][0]["description"]
    humidity = weather_data["main"]["humidity"]
    pressure = weather_data["main"]["pressure"]
    visibility = weather_data["visibility"]
    wind_speed = weather_data["wind"]["speed"]
    deg_wind = weather_data["wind"]["deg"]
    deg_wind_direction = deg_to_direction(deg_wind)
    longitude = weather_data["coord"]["lon"]
    latitude = weather_data["coord"]["lat"]

    timezone_offset = weather_data["timezone"]
    sunrise_utc = datetime.fromtimestamp(weather_data["sys"]["sunrise"], timezone.utc)
    sunset_utc = datetime.fromtimestamp(weather_data["sys"]["sunset"], timezone.utc)
    sunrise = sunrise_utc.astimezone(timezone(timedelta(seconds=timezone_offset)))
    sunset = sunset_utc.astimezone(timezone(timedelta(seconds=timezone_offset)))

    local_time = get_local_time(timezone_offset)
    local_time_str = local_time.strftime("%H:%M:%S")

    city_name_label.config(text=f"City : {city_name}")
    country_label.config(text=f"Country : {country}")
    weather_label.config(text=f"Weather : {weather} ({weather_desc})")
    temperature_label.config(text=f"Temperature : {temperature} °C", font=FONT_TITLE)
    feels_like_label.config(text=f"Feels Like : {feels_like} °C")
    temp_min_label.config(text=f"Min Temperature : {temp_min} °C")
    temp_max_label.config(text=f"Max Temperature : {temp_max} °C")
    humidity_label.config(text=f"Humidity : {humidity} %")
    pressure_label.config(text=f"Pressure : {pressure} hPa")
    visibility_label.config(text=f"Visibility : {visibility / 1000} km")
    wind_label.config(text=f"Wind Speed : {wind_speed} km/h, {deg_wind_direction}")
    sunrise_label.config(text=f"Sunrise : {sunrise.strftime('%H:%M:%S')}")
    sunset_label.config(text=f"Sunset : {sunset.strftime('%H:%M:%S')}")
    local_time_label.config(text=f"Local Time : {local_time_str}", font=FONT_TITLE)
    coord_label.config(text=f"Coordinates : \n longitude : {longitude}, latitude : {latitude}", font=FONT_NORMAL)

    update_icon(weather_data["weather"][0]["icon"])


def update_icon(weather_icon):
    icon_url = f"http://openweathermap.org/img/w/{weather_icon}.png"
    try:
        icon_response = requests.get(icon_url, stream=True)
        icon_response.raise_for_status()
        with open("icon.png", "wb") as f:
            icon_response.raw.decode_content = True
            f.write(icon_response.content)
        icon_image = Image.open("icon.png")
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo
    except requests.RequestException as e:
        print(f"Error retrieving weather icon: {e}")


def clear_labels():
    labels = [city_name_label, country_label, weather_label, temperature_label,
              feels_like_label, temp_min_label, temp_max_label, humidity_label,
              pressure_label, visibility_label, wind_label, sunrise_label,
              sunset_label, local_time_label, coord_label]
    for label in labels:
        label.config(text="")


def get_local_time(timezone_offset):
    utc_now = datetime.utcnow()
    local_time = utc_now + timedelta(seconds=timezone_offset)
    return local_time


def deg_to_direction(deg):
    directions = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
    idx = int((deg + 22.5) / 45) % 8
    return directions[idx]


root = tk.Tk()
root.title("Weather App")
root.geometry("700x500")

city_entry = tk.Entry(root)
city_entry.grid(row=0, column=1, padx=10, pady=10)

update_button = tk.Button(root, text="Update", command=update_weather)
update_button.grid(row=0, column=2, padx=10, pady=10)

separator_1 = ttk.Separator(root, orient="horizontal")
separator_1.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10)

city_name_label = tk.Label(root)
city_name_label.grid(row=1, column=0, padx=30, pady=10)

country_label = tk.Label(root)
country_label.grid(row=1, column=1, padx=30, pady=10)

weather_label = tk.Label(root)
weather_label.grid(row=1, column=2, padx=30, pady=10)

temperature_label = tk.Label(root)
temperature_label.grid(row=3, column=1, padx=10, pady=10)

feels_like_label = tk.Label(root)
feels_like_label.grid(row=7, column=0, padx=10, pady=10)

temp_min_label = tk.Label(root)
temp_min_label.grid(row=8, column=0, padx=10, pady=10)

temp_max_label = tk.Label(root)
temp_max_label.grid(row=9, column=0, padx=10, pady=10)

humidity_label = tk.Label(root)
humidity_label.grid(row=7, column=2, padx=10, pady=10)

pressure_label = tk.Label(root)
pressure_label.grid(row=8, column=2, padx=10, pady=10)

visibility_label = tk.Label(root)
visibility_label.grid(row=9, column=2, padx=10, pady=10)

wind_label = tk.Label(root)
wind_label.grid(row=10, column=1, padx=10, pady=10)

sunrise_label = tk.Label(root)
sunrise_label.grid(row=5, column=0, padx=30, pady=10)

sunset_label = tk.Label(root)
sunset_label.grid(row=5, column=2, padx=30, pady=10)

local_time_label = tk.Label(root)
local_time_label.grid(row=6, column=1, padx=10, pady=10)

icon_label = tk.Label(root)
icon_label.grid(row=11, column=1)

coord_label = tk.Label(root)
coord_label.grid(row=12, column=2, padx=10, pady=10)

root.mainloop()