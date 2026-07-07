import requests

API_KEY = "c9dc50d6c6f6814dc2e0715a4eb0f4c7"

def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    data = requests.get(url).json()

    if data.get("cod") != 200:
        return "City not found."

    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]

    return f"{city}: {temp}°C, {weather}"