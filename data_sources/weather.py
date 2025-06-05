# File: weather.py
import os
from dotenv import load_dotenv
import requests

# Load the API key from .env file
load_dotenv()

def get_weather(city="Houston"):
    """Get weather data using OpenWeatherMap API"""
    # Get API key from environment variables
    api_key = os.environ.get('WEATHER_API_KEY')
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"🌤️  Weather in {city}: {temp}°F, {description.title()}"
        else:
            return "🌤️  Weather: Unable to fetch (check your API key)"
    except:
        return "🌤️  Weather: Connection error"

def get_forecast(city="Houston"):
    """Get 5-day weather forecast"""
    # Get API key from environment variables
    api_key = os.environ.get('WEATHER_API_KEY')
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=imperial"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecasts = []
            for item in data['list'][:5]:
                temp = item['main']['temp']
                desc = item['weather'][0]['description']
                time = item['dt_txt']
                forecasts.append(f"{time}: {temp}°F, {desc}")
            return forecasts
        else:
            return ["Forecast unavailable"]
    except:
        return ["Forecast connection error"]