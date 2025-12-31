# WeatherApp

A Python-based weather application that fetches and displays current weather information based on your IP location.

## Features

- Automatically detects your location using IP geolocation
- Fetches current weather data from Open-Meteo API
- Displays temperature, wind speed, wind direction, and weather conditions
- Includes weather code translations for easy understanding
- Optional: Hourly temperature forecasts using pandas

## Requirements

- Python 3.x
- requests
- openmeteo_requests (for test.py)
- pandas (for test.py)
- requests-cache (for test.py)
- retry-requests (for test.py)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AmericanSpirit38/WeatherApp.git
cd WeatherApp
```

2. Install required packages:
```bash
pip install requests openmeteo_requests pandas requests-cache retry-requests
```

## Usage

### Basic Weather Information
Run the main script to get current weather for your location:
```bash
python main.py
```

### Detailed Hourly Forecast
Run the test script for hourly temperature data:
```bash
python test.py
```

## How It Works

1. The application uses ipinfo.io to detect your current location based on your IP address
2. It then queries the Open-Meteo API (free, no API key required) for weather data
3. Weather information is displayed in a human-readable format

## APIs Used

- **ipinfo.io**: For IP-based geolocation (no API key required for basic use)
- **Open-Meteo API**: For weather forecast data (free and open-source weather API)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
