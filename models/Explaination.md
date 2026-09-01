# 🌤️ Python Weather App

A simple Python application that fetches live weather information for a city using the **Open-Meteo APIs**.

## ✨ Features

- 🏙️ Search weather using a city name
- 📍 Automatically find latitude and longitude
- 🌡️ Display current temperature
- 💨 Display wind speed
- 🌐 Fetch live weather data using APIs

---

## 🧠 Main Logic

```
Start Application
       ↓
Ask User for City
       ↓
Check Input
       ↓
Call fetch_weather(city)
       ↓
Call geocode(city)
       ↓
Get Latitude + Longitude
       ↓
Call Open-Meteo Weather API
       ↓
Get Weather JSON Data
       ↓
Extract Required Information
       ↓
Convert Weather Code to Condition
       ↓
Return Weather Dictionary
       ↓
Display Weather Report
       ↓
Search Again OR Exit
```

---

## 🧠 How It Works

The application follows a simple process:

```text
City Name
    ↓
Geocoding API
    ↓
Latitude + Longitude
    ↓
Weather API
    ↓
Current Weather Data
    ↓
Display Result
```

---

## 📦 Technologies Used

- 🐍 Python
- 🌐 Requests Library
- 📡 REST APIs
- 📦 JSON

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repository-url>
```

Move into the project folder:

```bash
cd <project-folder>
```

Install the required library:

```bash
pip install requests
```

---

## ▶️ Run the Application

```bash
python main.py
```

---

## 💻 How the Code Works

### 1️⃣ Import Requests

```python
import requests
```

The `requests` library allows Python to communicate with web APIs.

---

### 2️⃣ Get the City Name

```python
city = input("Enter your city : ")
```

The user enters a city name.

Example:

```text
Enter your city: Kolkata
```

---

### 3️⃣ Find the City's Coordinates

```python
geo = requests.get(
    "https://geocoding-api.open-meteo.com/v1/search",
    params={"name": city}
).json()
```

The **Geocoding API** searches for the city and returns geographical information.

The program extracts:

- City name
- Latitude
- Longitude
- Country

---

### 4️⃣ Extract Latitude and Longitude

```python
lat = geo["results"][0]["latitude"]
lon = geo["results"][0]["longitude"]
```

Example:

```text
Latitude  → 22.5726
Longitude → 88.3639
```

These coordinates are used to identify the location for the weather request.

---

### 5️⃣ Fetch Weather Data

```python
data = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
).json()
```

The Weather API receives the latitude and longitude and returns current weather information.

---

### 6️⃣ Extract Weather Information

#### 🌡️ Temperature

```python
temp = data["current_weather"]["temperature"]
```

#### 💨 Wind Speed

```python
wind = data["current_weather"]["windspeed"]
```

---

### 7️⃣ Display the Result

```python
print(f"\nCITY : {name}")
print(f"\nTemp : {temp}°")
print(f"\nWind speed: {wind}")
```

---

## 🖥️ Example Output

```text
Enter your city: Kolkata

CITY : Kolkata

Temp : 30°

Wind speed: 12
```

---

## 💡 Core Concept

> **City Name → Latitude & Longitude → Weather Data**

The application first converts the city name into geographical coordinates using the **Geocoding API**. It then uses those coordinates to request live weather information from the **Weather API**.

---

## 📚 Concepts Practiced

- Python
- User Input
- API Integration
- HTTP GET Requests
- JSON Data
- Python Dictionaries
- F-Strings

---

⭐ A simple project for learning how Python applications can interact with real-world APIs and process live data.