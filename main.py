import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
import requests

import matplotlib.pyplot as plt

def forecast(latitude, longitude, days=7):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "forecast_days": days,
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    def CreateTemperaturePlot(dataframe: pd.DataFrame):
        plt.figure(figsize=(10, 5))
        plt.plot(dataframe['date'], dataframe['temperature_2m'], marker='o')
        plt.title(f"{days} day forecast")
        plt.xlabel('Date and Time')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    CreateTemperaturePlot(hourly_dataframe)

response = requests.get("https://ipinfo.io/json")
response.raise_for_status()
location_data = response.json()


loc = location_data["loc"].split(",")
latitude = loc[0]
longitude = loc[1]

print(f"Weather for {location_data['city']}, {location_data['country']}")

forecast(latitude, longitude, days=1)