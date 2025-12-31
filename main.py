import requests

response = requests.get("https://ipinfo.io/json")
response.raise_for_status()
location_data = response.json()
print(location_data)

loc = location_data["loc"].split(",")
latitude = loc[0]
longitude = loc[1]

print(f"Weather for {location_data['city']}, {location_data['country']}")

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "current_weather": True
}

weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}
response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()

current = data["current_weather"]
print(weather_codes[current["weathercode"]])
print(f"{current['temperature']}°C")
print(f"{current['windspeed']}km/h with {current['winddirection']}° direction")
print(f"Elevation: {data['elevation']}m")
print(f"Time of measurement: {current["time"].split('T')[1]}")

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "forecast_days": 14,
}
response = requests.get(url, params=params)
response.raise_for_status()
data = response.json()
print(data)