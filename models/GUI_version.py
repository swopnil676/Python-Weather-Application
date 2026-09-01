import json
import threading
import urllib.request
import urllib.parse
import tkinter as tk
from tkinter import ttk
from datetime import datetime

BG_DARK = "#0f1420"
BG_CARD = "#1a2233"
BG_CARD_HOVER = "#212b40"
ACCENT = "#4f9dff"
ACCENT_SOFT = "#2f65b8"
TEXT_MAIN = "#f2f5fa"
TEXT_SUB = "#8b95a8"
TEXT_MUTED = "#5c6478"
GOOD = "#3ddc97"
WARN = "#ffb454"
BAD = "#ff6b6b"

COUNTRIES = [
    ("India", "IN"),
    ("United Arab Emirates", "AE"),
    ("United Kingdom", "GB"),
    ("United States", "US"),
    ("Japan", "JP"),
    ("Canada", "CA"),
    ("Australia", "AU"),
]

CITY_SUGGESTIONS = {
    "IN": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata"],
    "AE": ["Dubai", "Abu Dhabi", "Sharjah"],
    "GB": ["London", "Manchester", "Birmingham"],
    "US": ["New York", "Los Angeles", "Chicago"],
    "JP": ["Tokyo", "Osaka", "Kyoto"],
    "CA": ["Toronto", "Vancouver", "Montreal"],
    "AU": ["Sydney", "Melbourne", "Brisbane"],
}

FOOTER_TEXT = "Instagram: /real.shahzaib_    |    YouTube: /real.shahzaib7"


def icon_for(description):
    desc = description.lower()
    if "thunder" in desc:
        return "⛈"
    if "snow" in desc or "sleet" in desc or "ice" in desc:
        return "❄"
    if "rain" in desc or "drizzle" in desc or "shower" in desc:
        return "🌧"
    if "fog" in desc or "mist" in desc or "haze" in desc:
        return "🌫"
    if "overcast" in desc:
        return "☁"
    if "cloud" in desc:
        return "⛅"
    if "clear" in desc or "sunny" in desc:
        return "☀"
    return "🌤"


WMO_CODES = {
    0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing Rime Fog",
    51: "Light Drizzle", 53: "Drizzle", 55: "Dense Drizzle",
    56: "Freezing Drizzle", 57: "Dense Freezing Drizzle",
    61: "Slight Rain", 63: "Rain", 65: "Heavy Rain",
    66: "Freezing Rain", 67: "Heavy Freezing Rain",
    71: "Slight Snow", 73: "Snow", 75: "Heavy Snow", 77: "Snow Grains",
    80: "Slight Rain Showers", 81: "Rain Showers", 82: "Violent Rain Showers",
    85: "Slight Snow Showers", 86: "Heavy Snow Showers",
    95: "Thunderstorm", 96: "Thunderstorm with Hail", 99: "Severe Thunderstorm with Hail",
}


def geocode(city, country_code=None):
    base = "https://geocoding-api.open-meteo.com/v1/search"
    attempts = []
    if country_code:
        attempts.append({"name": city, "country": country_code, "count": 1})
    attempts.append({"name": city, "count": 1})

    for params in attempts:
        geo_url = f"{base}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(geo_url, headers={"User-Agent": "curl/8.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        results = data.get("results")
        if results:
            top = results[0]
            label_parts = [top["name"]]
            if top.get("admin1"):
                label_parts.append(top["admin1"])
            if top.get("country"):
                label_parts.append(top["country"])
            return top["latitude"], top["longitude"], ", ".join(label_parts)
    raise ValueError(f"City not found: {city}")


def fetch_weather(city, country_code=None):
    lat, lon, resolved_name = geocode(city, country_code)

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto",
    }
    url = f"https://api.open-meteo.com/v1/forecast?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = json.loads(resp.read().decode())

    current = raw["current"]
    daily = raw["daily"]
    code = current["weather_code"]
    description = WMO_CODES.get(code, "Unknown")

    return {
        "resolved_name": resolved_name,
        "temp": round(current["temperature_2m"]),
        "feels": round(current["apparent_temperature"]),
        "condition": description,
        "icon": icon_for(description),
        "humidity": round(current["relative_humidity_2m"]),
        "wind": round(current["wind_speed_10m"]),
        "high": round(daily["temperature_2m_max"][0]),
        "low": round(daily["temperature_2m_min"][0]),
    }


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather • Static Demo")
        self.geometry("460x680")
        self.minsize(420, 640)
        self.configure(bg=BG_DARK)

        self._build_style()
        self._build_header()
        self._build_search()
        self._build_card()
        self._build_stats()
        self._build_footer()

        self.country_var.set("India")
        self._on_country_selected()
        self.city_var.set("Kolkata")
        self.search()

    def _build_style(self):
        self.option_add("*Font", "Segoeui 11")
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure(
            "Search.TCombobox",
            fieldbackground=BG_CARD,
            background=BG_CARD,
            foreground=TEXT_MAIN,
            arrowcolor=TEXT_MAIN,
            bordercolor=BG_CARD,
            lightcolor=BG_CARD,
            darkcolor=BG_CARD,
        )

    def _build_header(self):
        header = tk.Frame(self, bg=BG_DARK)
        header.pack(fill="x", padx=24, pady=(24, 8))

        tk.Label(
            header, text="Weather", bg=BG_DARK, fg=TEXT_MAIN,
            font=("Segoeui", 22, "bold")
        ).pack(anchor="w")

        self.updated_label = tk.Label(
            header, text="", bg=BG_DARK, fg=TEXT_MUTED, font=("Segoeui", 9)
        )
        self.updated_label.pack(anchor="w", pady=(2, 0))

    def _build_search(self):
        search_frame = tk.Frame(self, bg=BG_DARK)
        search_frame.pack(fill="x", padx=24, pady=(4, 16))

        country_row = tk.Frame(search_frame, bg=BG_DARK)
        country_row.pack(fill="x", pady=(0, 8))

        tk.Label(country_row, text="Country", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Segoeui", 9)).pack(anchor="w")

        self.country_var = tk.StringVar()
        self.country_box = ttk.Combobox(
            country_row,
            textvariable=self.country_var,
            values=[name for name, code in COUNTRIES],
            style="Search.TCombobox",
            state="readonly",
            font=("Segoeui", 12),
        )
        self.country_box.pack(fill="x", ipady=4, pady=(2, 0))
        self.country_box.bind("<<ComboboxSelected>>", self._on_country_selected)

        city_row = tk.Frame(search_frame, bg=BG_DARK)
        city_row.pack(fill="x")

        tk.Label(city_row, text="City", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Segoeui", 9)).pack(anchor="w")

        city_input_row = tk.Frame(city_row, bg=BG_DARK)
        city_input_row.pack(fill="x", pady=(2, 0))

        self.city_var = tk.StringVar()
        self.city_box = ttk.Combobox(
            city_input_row,
            textvariable=self.city_var,
            values=[],
            style="Search.TCombobox",
            state="disabled",
            font=("Segoeui", 12),
        )
        self.city_box.pack(side="left", fill="x", expand=True, ipady=6)
        self.city_box.bind("<Return>", lambda e: self.search())
        self.city_box.bind("<<ComboboxSelected>>", lambda e: self.search())

        go_btn = tk.Button(
            city_input_row, text="Search", bg=ACCENT, fg="#0b0f18",
            activebackground=ACCENT_SOFT, activeforeground=TEXT_MAIN,
            relief="flat", font=("Segoeui", 11, "bold"),
            padx=16, cursor="hand2", command=self.search
        )
        go_btn.pack(side="left", padx=(8, 0))

    def _on_country_selected(self, event=None):
        name = self.country_var.get()
        code = dict(COUNTRIES).get(name)
        cities = CITY_SUGGESTIONS.get(code, [])
        self.city_box.config(values=cities, state="normal")
        self.city_var.set("")
        self.city_box.focus_set()

    def _build_card(self):
        self.card = tk.Frame(self, bg=BG_CARD)
        self.card.pack(fill="x", padx=24, pady=(0, 16))

        inner = tk.Frame(self.card, bg=BG_CARD)
        inner.pack(fill="x", padx=24, pady=24)

        self.city_label = tk.Label(
            inner, text="", bg=BG_CARD, fg=TEXT_MAIN, font=("Segoeui", 16, "bold")
        )
        self.city_label.pack(anchor="w")

        self.condition_label = tk.Label(
            inner, text="", bg=BG_CARD, fg=TEXT_SUB, font=("Segoeui", 11)
        )
        self.condition_label.pack(anchor="w", pady=(2, 12))

        row = tk.Frame(inner, bg=BG_CARD)
        row.pack(fill="x")

        self.icon_label = tk.Label(
            row, text="☀", bg=BG_CARD, fg=ACCENT, font=("Segoeui", 48)
        )
        self.icon_label.pack(side="left")

        self.temp_label = tk.Label(
            row, text="", bg=BG_CARD, fg=TEXT_MAIN, font=("Segoeui", 46, "bold")
        )
        self.temp_label.pack(side="left", padx=(16, 0))

        self.feels_label = tk.Label(
            inner, text="", bg=BG_CARD, fg=TEXT_MUTED, font=("Segoeui", 10)
        )
        self.feels_label.pack(anchor="w", pady=(6, 0))

    def _build_stats(self):
        stats_frame = tk.Frame(self, bg=BG_DARK)
        stats_frame.pack(fill="x", padx=24, pady=(0, 16))
        stats_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self.stat_widgets = {}
        labels = [("High", "high", "°"), ("Low", "low", "°"),
                  ("Humidity", "humidity", "%"), ("Wind", "wind", " km/h")]

        for col, (title, key, suffix) in enumerate(labels):
            box = tk.Frame(stats_frame, bg=BG_CARD)
            box.grid(row=0, column=col, sticky="nsew", padx=4)

            tk.Label(box, text=title, bg=BG_CARD, fg=TEXT_MUTED,
                     font=("Segoeui", 9)).pack(pady=(10, 2))
            val = tk.Label(box, text="--", bg=BG_CARD, fg=TEXT_MAIN,
                            font=("Segoeui", 14, "bold"))
            val.pack(pady=(0, 10))

            self.stat_widgets[key] = (val, suffix)

    def _build_footer(self):
        footer = tk.Frame(self, bg=BG_DARK)
        footer.pack(side="bottom", fill="x", pady=(0, 16))

        tk.Label(
            footer, text=FOOTER_TEXT, bg=BG_DARK, fg=TEXT_MUTED,
            font=("Segoeui", 9)
        ).pack()

    def search(self):
        query = self.city_var.get().strip()
        country_name = self.country_var.get().strip()
        if not country_name:
            self.show_loading("")
            self.condition_label.config(text="Pick a country first")
            return
        if not query:
            return
        country_code = dict(COUNTRIES).get(country_name)
        self.show_loading(query)
        threading.Thread(
            target=self._fetch_worker, args=(query, country_code), daemon=True
        ).start()

    def _fetch_worker(self, query, country_code):
        try:
            data = fetch_weather(query, country_code)
            self.after(0, self.show_city, data)
        except Exception:
            self.after(0, self.show_not_found, query)

    def show_loading(self, query):
        self.city_label.config(text=f"Loading {query}...", fg=TEXT_MAIN)
        self.condition_label.config(text="Fetching live data from Open-Meteo")
        self.icon_label.config(text="⏳")
        self.temp_label.config(text="--")
        self.feels_label.config(text="")
        for widget, _ in self.stat_widgets.values():
            widget.config(text="--")

    def show_city(self, data):
        self.city_var.set(data["resolved_name"])
        self.city_label.config(text=data["resolved_name"], fg=TEXT_MAIN)
        self.condition_label.config(text=data["condition"])
        self.icon_label.config(text=data["icon"])
        self.temp_label.config(text=f"{data['temp']}°C")
        self.feels_label.config(text=f"Feels like {data['feels']}°C")

        for key, (widget, suffix) in self.stat_widgets.items():
            widget.config(text=f"{data[key]}{suffix}")

        now = datetime.now().strftime("%A, %d %b — %I:%M %p")
        self.updated_label.config(text=f"Last updated: {now} (live via Open-Meteo)")

    def show_not_found(self, query):
        self.city_label.config(text=f'"{query}" not found', fg=BAD)
        self.condition_label.config(text="Check spelling or your internet connection")
        self.icon_label.config(text="✕")
        self.temp_label.config(text="--")
        self.feels_label.config(text="")
        for widget, _ in self.stat_widgets.values():
            widget.config(text="--")


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()