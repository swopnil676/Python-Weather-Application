import requests

city = input("Enter your city: ")


geo = requests.get(
    "https://geocoding-api.open-meteo.com/v1/search",
    params={"name": city}
).json()

lat = geo["results"][0]["latitude"]
lon = geo["results"][0]["longitude"]
name = geo["results"][0]["name"]


data = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
).json()

temp = data["current_weather"]["temperature"]
wind = data["current_weather"]["windspeed"]


print(f"\nCITY : {name}")
print(f"\nTemp : {temp}°")
print(f"\nWind speed: {wind}")