import colorama

print(colorama.Fore.LIGHTWHITE_EX + """ █████   ███   █████          ███████████          ███████████  
░░███   ░███  ░░███          ░█░░░███░░░█         ░░███░░░░░███ 
 ░███   ░███   ░███   ██████ ░   ░███  ░   ██████  ░███    ░███ 
 ░███   ░███   ░███  ███░░███    ░███     ███░░███ ░██████████  
 ░░███  █████  ███  ░███████     ░███    ░███████  ░███░░░░░███ 
  ░░░█████░█████░   ░███░░░      ░███    ░███░░░   ░███    ░███ 
    ░░███ ░░███     ░░██████     █████   ░░██████  █████   █████
     ░░░   ░░░       ░░░░░░     ░░░░░     ░░░░░░  ░░░░░   ░░░░░ """ + colorama.Style.RESET_ALL)

print(colorama.Fore.WHITE + "Loading imports..." + colorama.Style.RESET_ALL)
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
        plt.title(f"{days} day temperature forecast")
        plt.xlabel('Date and Time')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    CreateTemperaturePlot(hourly_dataframe)
def air_quality(latitude, longitude, days=7):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["pm10", "pm2_5", "european_aqi_pm10", "european_aqi_pm2_5"],
        "forecast_days": days
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_pm10 = hourly.Variables(0).ValuesAsNumpy()
    hourly_pm2_5 = hourly.Variables(1).ValuesAsNumpy()
    hourly_european_aqi_pm10 = hourly.Variables(2).ValuesAsNumpy()
    hourly_european_aqi_pm2_5 = hourly.Variables(3).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["pm10"] = hourly_pm10
    hourly_data["pm2_5"] = hourly_pm2_5
    hourly_data["european_aqi_pm10"] = hourly_european_aqi_pm10
    hourly_data["european_aqi_pm2_5"] = hourly_european_aqi_pm2_5

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    plt.figure(figsize=(10, 5))
    plt.plot(hourly_dataframe['date'], hourly_dataframe['european_aqi_pm10'], marker='o', label='PM10 AQI')
    plt.plot(hourly_dataframe['date'], hourly_dataframe['european_aqi_pm2_5'], marker='x', label='PM2.5 AQI')
    plt.title(f"{days} day AQI Forecast")
    plt.xlabel('Date and Time')
    plt.ylabel('European AQI')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
def wave_forecast(latitude, longitude, days=7):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://marine-api.open-meteo.com/v1/marine"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["wave_height", "wave_period"],
        "forecast_days": days
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    hourly = response.Hourly()
    hourly_wave_height = hourly.Variables(0).ValuesAsNumpy()
    hourly_wave_period = hourly.Variables(1).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}

    hourly_data["wave_height"] = hourly_wave_height
    hourly_data["wave_period"] = hourly_wave_period

    hourly_dataframe = pd.DataFrame(data=hourly_data)

    if hourly_dataframe['wave_height'].isna().any() and hourly_dataframe['wave_period'].isna().any():
        print(colorama.Fore.RED + "No wave data avalible for this location." + colorama.Style.RESET_ALL)
    else:
        plt.figure(figsize=(10, 5))
        plt.plot(hourly_dataframe['date'], hourly_dataframe['wave_height'], marker='o', label='Wave Height (m)')
        plt.plot(hourly_dataframe['date'], hourly_dataframe['wave_period'], marker='x', label='Wave Period (s)')
        plt.title(f"{days} day wave forecast")
        plt.xlabel('Date and Time')
        plt.ylabel('Values')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
def current_weather(latitude, longitude):
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
    print(colorama.Fore.LIGHTWHITE_EX + weather_codes[current["weathercode"]])
    print(f"{current['temperature']}°C")
    print(f"{current['windspeed']}km/h with {current['winddirection']}° direction")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "forecast_days": 14,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()


def get_location():
    try:
        print(colorama.Fore.WHITE + "Getting your location from your public IP..." + colorama.Style.RESET_ALL)
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()
        location_data = response.json()

        loc = location_data["loc"].split(",")
        lat = loc[0]
        long = loc[1]
        return lat, long
    except requests.exceptions.RequestException as e:
        print(colorama.Fore.RED + f"Network error getting location: {e}" + colorama.Style.RESET_ALL)
        print(colorama.Fore.RED + "Please enter your location manually using location <latitude> <longitude>" + colorama.Style.RESET_ALL)
    except Exception as e:
        print(colorama.Fore.RED + f"Error getting location: {e}" + colorama.Style.RESET_ALL)
        print(colorama.Fore.RED + "Please enter your location manually using location <latitude> <longitude>" + colorama.Style.RESET_ALL)


latitude, longitude = get_location()
print(colorama.Fore.WHITE + "Setup finished!" + colorama.Style.RESET_ALL)

while True:
    inp = input(colorama.Fore.LIGHTWHITE_EX + "WTR> " + colorama.Style.RESET_ALL).strip().split()
    try:
        if inp[0].lower() in ["forecast", "f", "fore"]:
            try:
                days = int(inp[1])
                if days < 1 or days > 14:
                    raise ValueError
                print(colorama.Fore.WHITE + "Working..." + colorama.Style.RESET_ALL)
                forecast(latitude, longitude, days)
            except IndexError:
                print(colorama.Fore.WHITE + "Working..." + colorama.Style.RESET_ALL)
                forecast(latitude, longitude)
            except ValueError:
                print(colorama.Fore.RED + "Days must be an integer between 1 and 14." + colorama.Style.RESET_ALL)
        elif inp[0].lower() in ["exit", "quit", "q", "e"]:
            print(colorama.Fore.WHITE + "Exiting..." + colorama.Style.RESET_ALL)
            break
        elif inp[0].lower() in ["current", "c"]:
            current_weather(latitude, longitude)
        elif inp[0].lower() in ["location", "loc"]:
            if len(inp) == 3:
                try:
                    latitude = float(inp[1])
                    longitude = float(inp[2])
                    print(colorama.Fore.WHITE + f"Location set to {latitude}, {longitude}" + colorama.Style.RESET_ALL)
                except ValueError:
                    print(colorama.Fore.RED + "Invalid latitude or longitude." + colorama.Style.RESET_ALL)
            else:
                latitude, longitude = get_location()
        elif inp[0].lower() in ["airquality", "aq", "air"]:
            try:
                days = int(inp[1])
                if days < 1 or days > 14:
                    raise ValueError
                print(colorama.Fore.WHITE + "Working..." + colorama.Style.RESET_ALL)
                air_quality(latitude, longitude, days)
            except IndexError:
                print(colorama.Fore.WHITE + "Working..." + colorama.Style.RESET_ALL)
                air_quality(latitude, longitude)
            except ValueError:
                print(colorama.Fore.RED + "Days must be an integer between 1 and 14." + colorama.Style.RESET_ALL)
        elif inp[0].lower() in ["wave", "w"]:
            try:
                days = int(inp[1])
                if days < 1 or days > 14:
                    raise ValueError
                print(colorama.Fore.WHITE + "Working..." + colorama.Style.RESET_ALL)
                wave_forecast(latitude, longitude, days)
            except IndexError:
                print(colorama.Fore.WHITE + "Working..." + colorama.Style.RESET_ALL)
                wave_forecast(latitude, longitude)
            except ValueError:
                print(colorama.Fore.RED + "Days must be an integer between 1 and 14." + colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.RED + "Unknown command" + colorama.Style.RESET_ALL)

    except IndexError:
        print(colorama.Fore.RED + "Invalid input" + colorama.Style.RESET_ALL)
    except Exception as e:
        print(colorama.Fore.RED + f"An error occurred: {e}" + colorama.Style.RESET_ALL)