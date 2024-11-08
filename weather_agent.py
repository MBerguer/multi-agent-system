import os
import redis
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

redis_client = redis.Redis(host="localhost", port=6379, db=0)
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    print(f"Getting weather for {city}...")
    response = requests.get(WEATHER_URL, params={"q": city, "appid": WEATHER_API_KEY})
    if response.status_code == 200:
        return response.json()
    return None


def handle_weather_request(message):
    print("Received weather request:", message)
    data = json.loads(message["data"])
    city = data.get("city")
    weather_data = get_weather(city)

    print("Weather data:", weather_data)

    # Publish weather data to the "response" channel
    if weather_data:
        redis_client.publish("response", json.dumps(weather_data))


# Subscribe to the weather_requests channel
pubsub = redis_client.pubsub()
pubsub.subscribe(**{"weather_requests": handle_weather_request})

print("Weather Agent is running...")
pubsub.run_in_thread(sleep_time=0.1)
