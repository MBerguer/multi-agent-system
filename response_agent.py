import os
import redis
import json
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Redis client
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")


def format_response_with_openai(weather_data):
    city = weather_data.get("name")
    temperature = weather_data["main"]["temp"] - 273.15  # Convert Kelvin to Celsius
    description = weather_data["weather"][0]["description"]

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": (
                f"Format the following weather data into a human-readable message:\n"
                f"City: {city}\n"
                f"Temperature: {temperature:.2f}°C\n"
                f"Conditions: {description}\n"
            ),
        },
    ]

    response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages, max_tokens=50)
    response_dict = response.model_dump()  # <--- convert to dictionary
    # print(response_dict)
    response_message = response_dict["choices"][0]["message"]["content"]

    return response_message


def handle_response(message):
    weather_data = json.loads(message["data"])
    response_message = format_response_with_openai(weather_data)
    print(response_message)


# Subscribe to the response channel
pubsub = redis_client.pubsub()
pubsub.subscribe(**{"response": handle_response})

print("Response Agent is running...")
pubsub.run_in_thread(sleep_time=0.1)
