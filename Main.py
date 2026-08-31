from Core_Logic import fetch_weather


def main():

    print("=" * 40)
    print("      🌤️ WEATHER APPLICATION")
    print("=" * 40)

    while True:

        city = input(
            "\n🏙️ Enter city name (or 'exit' to quit): "
        ).strip()

        if city.lower() == "exit":
            print("\n👋 Thank you for using the Weather App!")
            break

        if not city:
            print("⚠️ Please enter a city name.")
            continue

        try:
            weather = fetch_weather(city)

            print("\n" + "=" * 40)
            print("         🌤️ WEATHER REPORT")
            print("=" * 40)

            print(f"\n📍 City        : {weather['city']}")
            print(f"🌡️ Temperature : {weather['temperature']}°C")
            print(f"🤔 Feels Like  : {weather['feels_like']}°C")
            print(f"☁️ Condition   : {weather['condition']}")
            print(f"💧 Humidity    : {weather['humidity']}%")
            print(f"💨 Wind Speed  : {weather['wind_speed']} km/h")
            print(f"🔺 High        : {weather['high']}°C")
            print(f"🔻 Low         : {weather['low']}°C")

            print("\n" + "=" * 40)

        except ValueError as error:
            print(f"\n❌ {error}")

        except Exception:
            print("\n❌ Unable to fetch weather data.")
            print("Please check your internet connection and try again.")


if __name__ == "__main__":
    main()