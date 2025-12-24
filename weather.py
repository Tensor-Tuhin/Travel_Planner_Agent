import requests
from datetime import datetime, date, timedelta

# City - Coordinates mapping
CITY_COORDINATES = {
    "delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "kolkata": (22.5726, 88.3639),
    "chennai": (13.0827, 80.2707),
    "bangalore": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "goa": (15.2993, 74.1240),
    "jaipur": (26.9124, 75.7873)
}

# HELPERS

def parse_date(value) -> date:
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format")


def validate_inputs(city: str, start_date: date, end_date: date) -> None:
    if not city:
        raise ValueError("city is required")

    if city.strip().lower() not in CITY_COORDINATES:
        raise ValueError(f"Weather data not supported for {city}")

    if start_date > end_date:
        raise ValueError("Starting date cannot be after ending date")


# WEATHER TOOL

def get_weather_forecast(city: str, start_date, end_date):
    """
    Returns day-wise weather forecast for a city.
    Returns None if forecast is not available.
    """

    # Normalize
    city = city.strip().lower()
    start_date_obj = parse_date(start_date)
    end_date_obj = parse_date(end_date)

    # SAFETY CHECKS
    today = date.today()
    max_forecast_date = today + timedelta(days=16)

    # Too far in future → NO API CALL
    if start_date_obj > max_forecast_date:
        return None

    # API does not allow same-day ranges
    if end_date_obj <= start_date_obj:
        end_date_obj = start_date_obj + timedelta(days=1)

    # Clamp end date
    if end_date_obj > max_forecast_date:
        end_date_obj = max_forecast_date

    # Validate
    validate_inputs(city, start_date_obj, end_date_obj)

    latitude, longitude = CITY_COORDINATES[city]

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max",
        "start_date": start_date_obj.isoformat(),
        "end_date": end_date_obj.isoformat(),
        "timezone": "auto"
    }

    # API CALL
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    response_json = response.json()
    daily = response_json.get("daily")

    if not isinstance(daily, dict):
        return None

    dates = daily.get("time", [])
    temps = daily.get("temperature_2m_max", [])

    return [
        {"date": d, "max_temp": t}
        for d, t in zip(dates, temps)
    ]


# LOCAL TEST

if __name__ == "__main__":
    result = get_weather_forecast(
        city="Goa",
        start_date="2025-12-19",
        end_date="2025-12-25",
    )

    if result:
        for day in result:
            print(day)
    else:
        print("Weather data not available.")