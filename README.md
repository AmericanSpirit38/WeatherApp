# WeatherApp

WeatherApp is a small interactive CLI that fetches forecasts, air quality, wave data, and current weather from the [Open-Meteo APIs](https://open-meteo.com/). It attempts to detect your location automatically from your public IP and then lets you explore different data sets with a handful of commands.

## Prerequisites

- Python 3.10 or newer
- `bash` (for running the install script)
- Internet access so the app can call the Open-Meteo and IP lookup APIs

## Installation

### Quick install (recommended)

1. Clone the repo:
   ```bash
   git clone https://github.com/AmericanSpirit38/WeatherApp
   ```
2. Change your directory to the repo:
   ```bash
   cd WeatherApp
   ```
3. Run the installer:
   ```bash
   ./install.sh
   ```
   If it fails use to make the script executable:
   ```bash
   chmod +x install.sh
   ```

The script creates a virtual environment in `.venv`, upgrades `pip`, and installs all required dependencies:

- `colorama`
- `openmeteo-requests`
- `pandas`
- `requests-cache`
- `retry-requests`
- `matplotlib`

After it finishes, activate the environment:

- macOS/Linux: `source .venv/bin/activate`
- Windows (PowerShell): `.venv\\Scripts\\Activate.ps1`
- Windows (cmd): `.venv\\Scripts\\activate`

### Manual install

If you prefer to manage dependencies yourself:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the app

Activate your virtual environment (if you created one) and run:

```bash
python main.py
```

On startup the app will try to determine your latitude/longitude from your public IP. You can also set the location manually with the `location` command.

## Commands

All commands are case-insensitive; aliases are shown in parentheses.

- `forecast [days]` (`f`, `fore`) – Show a temperature forecast plot. `days` must be 1–14; defaults to 7.
- `airquality [days]` (`aq`, `air`) – Show PM10/PM2.5 European AQI plots for the next `days` (1–14, defaults to 7).
- `wave [days]` (`w`) – Plot wave height and period forecasts for up to 14 days.
- `current` (`c`) – Print current weather, temperature, wind speed, and direction.
- `location [latitude] [longitude]` (`loc`) – Set a custom location. Without parameters, it re-detects location from your IP.
- `exit` (`quit`, `q`, `e`) – Quit the application.

## Notes and tips

- API responses are cached for one hour in `.cache.sqlite`, the SQLite database `requests-cache` creates when configured with the `.cache` cache name.
- Matplotlib opens a window for plots; ensure you are running in an environment that supports GUI windows or use a backend that fits your setup.
- Keep `days` between 1 and 14; the app will reject values outside that range.
