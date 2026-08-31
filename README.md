# 🌤️ Python Weather Application

A simple Python terminal-based Weather Application that fetches live weather information using the **Open-Meteo APIs**.

## 📁 Project Structure

```text
Weather_App/
│
├── main.py
└── Core_Logic.py
```

- **Core_Logic.py** → Handles API requests and weather data processing.
- **main.py** → Handles user input, application flow, and displays the weather report.

---

# 🧠 Core Application Flow

```text
User enters city
       ↓
main.py
       ↓
fetch_weather(city)
       ↓
geocode(city)
       ↓
Get Latitude + Longitude
       ↓
Weather API
       ↓
Extract Weather Data
       ↓
Return Dictionary
       ↓
main.py displays data
       ↓
User searches again or exits
```

---

# ⚙️ Core_Logic.py

This file contains the main functionality of the Weather Application.

---

## 1️⃣ Import Required Libraries

```python
import json
import urllib.request
import urllib.parse
```

### `import json`

The `json` module is used to convert JSON data received from the API into Python dictionaries.

### `import urllib.request`

This module is used to send requests to APIs.

### `import urllib.parse`

This module is used to convert parameters into URL format.

---

## 2️⃣ Weather Code Dictionary

```python
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
```

The Weather API returns a numerical weather code.

For example:

```text
0  → Clear Sky
2  → Partly Cloudy
63 → Rain
95 → Thunderstorm
```

The `WMO_CODES` dictionary converts these numerical codes into readable weather descriptions.

---

# 📍 3️⃣ The `geocode()` Function

```python
def geocode(city):
```

This function receives a city name and finds:

- Latitude
- Longitude
- City name

Example:

```text
Input: Kolkata

Output:
Latitude  → 22.5726
Longitude → 88.3639
```

---

## Base API URL

```python
base_url = "https://geocoding-api.open-meteo.com/v1/search"
```

This is the Open-Meteo Geocoding API.

It searches for geographical information about a city.

---

## Create Parameters

```python
params = {"name": city, "count": 1}
```

This sends:

```text
name  → City entered by the user
count → Return only one result
```

For example:

```text
name=Kolkata
count=1
```

---

## Create Complete URL

```python
url = f"{base_url}?{urllib.parse.urlencode(params)}"
```

`urlencode()` converts the parameters into a URL format.

Example:

```text
https://geocoding-api.open-meteo.com/v1/search?name=Kolkata&count=1
```

---

## Send API Request

```python
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())
```

### `urlopen(url)`

Sends a request to the API.

### `response.read()`

Reads the data returned by the API.

### `.decode()`

Converts the received bytes into text.

### `json.loads()`

Converts the JSON text into a Python dictionary.

The final API data is stored in:

```python
data
```

---

## Get Search Results

```python
results = data.get("results")
```

This gets the list of cities returned by the API.

---

## Check if City Exists

```python
if not results:
    raise ValueError("City not found")
```

If the API cannot find the city, the program raises an error.

Example:

```text
❌ City not found
```

---

## Select the First Result

```python
city_data = results[0]
```

The API may return multiple matching locations.

`[0]` selects the first result.

---

## Extract Location Information

```python
latitude = city_data["latitude"]
longitude = city_data["longitude"]
city_name = city_data["name"]
```

These lines extract:

```text
Latitude
Longitude
City Name
```

---

## Return Location Data

```python
return latitude, longitude, city_name
```

The function sends the location information back to the function that called it.

---

# 🌤️ 4️⃣ The `fetch_weather()` Function

```python
def fetch_weather(city):
```

This is the main weather function.

It:

1. Finds the city coordinates.
2. Calls the Weather API.
3. Extracts weather information.
4. Converts weather codes.
5. Returns clean weather data.

---

## Get City Coordinates

```python
lat, lon, city_name = geocode(city)
```

This calls:

```python
geocode(city)
```

Example:

```text
Kolkata
    ↓
Latitude → 22.5726
Longitude → 88.3639
```

---

## Create Weather API Parameters

```python
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
```

This tells the API what weather information we need.

### Current Weather

```text
temperature_2m           → Current temperature
apparent_temperature     → Feels like temperature
relative_humidity_2m     → Humidity
wind_speed_10m           → Wind speed
weather_code             → Weather condition code
```

### Daily Weather

```text
temperature_2m_max → Maximum temperature
temperature_2m_min → Minimum temperature
```

---

## Weather API URL

```python
base_url = "https://api.open-meteo.com/v1/forecast"
```

This is the Open-Meteo Weather API.

---

## Create Complete Weather URL

```python
url = f"{base_url}?{urllib.parse.urlencode(params)}"
```

This combines the API URL and parameters.

---

## Send Weather API Request

```python
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())
```

The program:

1. Sends a request.
2. Receives weather data.
3. Reads the response.
4. Converts JSON into a Python dictionary.

---

## Extract Current and Daily Weather

```python
current = data["current"]
daily = data["daily"]
```

These variables store:

```text
current → Current weather information
daily   → Daily weather information
```

---

## Get Weather Code

```python
weather_code = current["weather_code"]
```

Example:

```text
weather_code = 2
```

---

## Convert Code to Weather Condition

```python
condition = WMO_CODES.get(
    weather_code,
    "Unknown"
)
```

The dictionary converts:

```text
2 → Partly Cloudy
```

If the weather code does not exist in the dictionary:

```text
Unknown
```

will be returned.

---

## Return Final Weather Data

```python
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
```

The function organizes all weather information into a dictionary.

Example:

```python
{
    "city": "Kolkata",
    "temperature": 30,
    "feels_like": 34,
    "humidity": 75,
    "wind_speed": 12,
    "condition": "Partly Cloudy",
    "high": 32,
    "low": 26
}
```

This dictionary is returned to `main.py`.

---

# 🖥️ main.py

The `main.py` file controls the application and interacts with the user.

---

## 1️⃣ Import `fetch_weather`

```python
from Core_Logic import fetch_weather
```

This imports the `fetch_weather()` function from:

```text
Core_Logic.py
```

This allows `main.py` to use the weather functionality.

---

# 2️⃣ Create the Main Function

```python
def main():
```

The main application logic is placed inside the `main()` function.

---

## Print Application Header

```python
print("=" * 40)
print("      🌤️ WEATHER APPLICATION")
print("=" * 40)
```

This prints:

```text
========================================
      🌤️ WEATHER APPLICATION
========================================
```

---

# 🔄 3️⃣ Start an Infinite Loop

```python
while True:
```

The program keeps running until the user decides to exit.

This allows the user to search for multiple cities.

---

## Get City Input

```python
city = input(
    "\n🏙️ Enter city name (or 'exit' to quit): "
).strip()
```

The user enters a city name.

`.strip()` removes extra spaces.

For example:

```text
"   Kolkata   "
```

becomes:

```text
"Kolkata"
```

---

# 🚪 4️⃣ Exit Condition

```python
if city.lower() == "exit":
```

If the user types:

```text
EXIT
Exit
exit
```

all will work because `.lower()` converts the text to lowercase.

---

## Exit the Program

```python
print("\n👋 Thank you for using the Weather App!")
break
```

`break` stops the `while True` loop.

The application then closes.

---

# ⚠️ 5️⃣ Check Empty Input

```python
if not city:
    print("⚠️ Please enter a city name.")
    continue
```

If the user presses Enter without typing anything:

```text
⚠️ Please enter a city name.
```

`continue` starts the next loop iteration.

---

# 🛡️ 6️⃣ Start Error Handling

```python
try:
```

The code inside `try` may cause errors.

Using `try` prevents the application from crashing.

---

# 🌤️ 7️⃣ Fetch Weather

```python
weather = fetch_weather(city)
```

This sends the city name to `Core_Logic.py`.

The flow is:

```text
main.py
   ↓
fetch_weather(city)
   ↓
geocode(city)
   ↓
Get Coordinates
   ↓
Weather API
   ↓
Return Weather Dictionary
```

The result is stored in:

```python
weather
```

---

# 📊 8️⃣ Display Weather Report

```python
print(f"\n📍 City        : {weather['city']}")
print(f"🌡️ Temperature : {weather['temperature']}°C")
print(f"🤔 Feels Like  : {weather['feels_like']}°C")
print(f"☁️ Condition   : {weather['condition']}")
print(f"💧 Humidity    : {weather['humidity']}%")
print(f"💨 Wind Speed  : {weather['wind_speed']} km/h")
print(f"🔺 High        : {weather['high']}°C")
print(f"🔻 Low         : {weather['low']}°C")
```

The program accesses values from the weather dictionary.

For example:

```python
weather["temperature"]
```

gets the current temperature.

---

# ❌ 9️⃣ Handle City Errors

```python
except ValueError as error:
    print(f"\n❌ {error}")
```

If the city is not found:

```text
❌ City not found
```

The program displays the error instead of crashing.

---

# 🌐 🔟 Handle Other Errors

```python
except Exception:
    print("\n❌ Unable to fetch weather data.")
    print("Please check your internet connection and try again.")
```

This handles unexpected errors, such as:

- No internet connection
- API connection problems
- Server errors

---

# ▶️ 1️⃣1️⃣ Run the Main Function

```python
if __name__ == "__main__":
    main()
```

This checks whether `main.py` is being run directly.

If yes:

```python
main()
```

starts the Weather Application.

---

# 🚀 Complete Project Flow

```text
┌────────────────────────────┐
│       Start main.py        │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│      User Enters City      │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│     fetch_weather(city)    │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│       geocode(city)        │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ Geocoding API finds City   │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ Get Latitude + Longitude   │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│       Weather API          │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│   Process Weather Data     │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│ Return Weather Dictionary  │
└──────────────┬─────────────┘
               ↓
┌────────────────────────────┐
│   Display Weather Report   │
└──────────────┬─────────────┘
               ↓
        Search Again?
          ↓       ↓
         Yes      No
          ↓       ↓
      Enter City  Exit
```

# 💡 Main Concept

> **`Core_Logic.py` handles the weather API and data processing.**

> **`main.py` handles user input, program flow, and displaying results.**

## 🛠️ Concepts Used

- 🐍 Python Functions
- 🔄 While Loops
- 📦 Dictionaries
- 🌐 APIs
- 📡 HTTP Requests
- 📄 JSON
- ⚠️ Exception Handling
- 🔤 F-Strings
- 📥 User Input
- 📁 Modular Programming
