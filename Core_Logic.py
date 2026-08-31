import json
import urllib.request
import urllib.parse


# ----------------------------------
# Weather Code Descriptions
# ----------------------------------

WMO_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Dense Drizzle",
    61: "Slight Rain",
    63: "Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    81: "Rain Showers",
    82: "Heavy Rain Showers",
    95: "Thunderstorm"
}


# ----------------------------------
# Get City Coordinates
# ----------------------------------

def geocode(city):

    base_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1}
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    results = data.get("results")
    if not results:
        raise ValueError("City not found")

    city_data = results[0]

    latitude = city_data["latitude"]
    longitude = city_data["longitude"]
    city_name = city_data["name"]

    return latitude, longitude, city_name


# ----------------------------------
# Fetch Weather
# ----------------------------------

def fetch_weather(city):

    # Step 1: Get latitude and longitude
    lat, lon, city_name = geocode(city)

    # Step 2: Weather API parameters
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": (
            "temperature_2m,"
            "apparent_temperature,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    }

    # Step 3: Create API URL
    base_url = "https://api.open-meteo.com/v1/forecast"
    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    # Step 4: Get API response
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    # Step 5: Extract current weather
    current = data["current"]
    daily = data["daily"]

    weather_code = current["weather_code"]

    condition = WMO_CODES.get(
        weather_code,
        "Unknown"
    )

    # Step 6: Return weather data
    return {
        "city": city_name,
        "temperature": round(current["temperature_2m"]),
        "feels_like": round(current["apparent_temperature"]),
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "condition": condition,
        "high": round(daily["temperature_2m_max"][0]),
        "low": round(daily["temperature_2m_min"][0])
    }
