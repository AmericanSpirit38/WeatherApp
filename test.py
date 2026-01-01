import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

import matplotlib.pyplot as plt
import colorama

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

url = "https://marine-api.open-meteo.com/v1/marine"
params = {
	"latitude": 45.592222441122374,
	"longitude": 20,
	"hourly": ["wave_height", "wave_period"],
}
responses = openmeteo.weather_api(url, params=params)

response = responses[0]
print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation: {response.Elevation()} m asl")
print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

hourly = response.Hourly()
hourly_wave_height = hourly.Variables(0).ValuesAsNumpy()
hourly_wave_period = hourly.Variables(1).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["wave_height"] = hourly_wave_height
hourly_data["wave_period"] = hourly_wave_period

hourly_dataframe = pd.DataFrame(data = hourly_data)

if hourly_dataframe['wave_height'].isna().any() and hourly_dataframe['wave_period'].isna().any():
    print(colorama.Fore.RED + "No wave data avalible for this location." + colorama.Style.RESET_ALL)
else:
    plt.figure(figsize = (10, 5))
    plt.plot(hourly_dataframe['date'], hourly_dataframe['wave_height'], marker = 'o', label = 'Wave Height (m)')
    plt.plot(hourly_dataframe['date'], hourly_dataframe['wave_period'], marker = 'x', label = 'Wave Period (s)')
    plt.title("Marine Forecast")
    plt.xlabel('Date and Time')
    plt.ylabel('Values')
    plt.grid(True)
    plt.xticks(rotation = 45)
    plt.legend()
    plt.tight_layout()
    plt.show()
