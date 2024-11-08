# Multi-Agent Weather Query System

This project implements a multi-agent system that processes natural language weather queries, fetches data from a weather API, and generates a user-friendly response. The system is composed of three agents that communicate via Redis: an NLP Agent, a Weather Agent, and a Response Agent.

## Project Overview

### Agents

1. **NLP Agent**: Processes natural language queries to identify the intent (e.g., "get weather") and extracts relevant entities like the city name.
2. **Weather Agent**: Receives requests from the NLP Agent to fetch weather data from the OpenWeatherMap API for the specified city.
3. **Response Agent**: Formats the weather data into a human-readable response and displays it to the user.

### Technologies Used

- **FastAPI**: API framework used by the NLP Agent for handling incoming requests.
- **Redis**: Message broker for inter-agent communication.
- **OpenWeatherMap API**: Weather data provider.
- **spaCy**: Natural language processing library for parsing user queries.

## Setup Instructions

### Prerequisites

- **Python 3.8 or higher**
- **Redis** (Make sure Redis is installed and running)
- **OpenWeatherMap API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/) to get a free API key.
- **OpenAI API Key**: (Optional) If you want to use the OpenAI API for more advanced NLP processing.

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/multi-agent-weather-system.git
   cd multi-agent-weather-system
   ```

2. **Install required Python packages**:

   ```bash
   pip install fastapi uvicorn requests redis spacy
   python -m spacy download en_core_web_sm
   ```

3. **Start Redis** (if not already running):

   - **On Ubuntu**: `sudo service redis-server start`
   - **On MacOS**: `brew services start redis`
   - Check Redis with: `redis-cli ping` (should return `PONG`)

4. **Set up the .env file**:
   - Open the `.env` file and add your OpenWeatherMap and OpenAI API keys:
     ```
     OPENWEATHERMAP_API_KEY=your-api-key
     OPENAI_API_KEY=your-api-key
     ```

## Code Overview

### 1. NLP Agent (`nlp_agent.py`)

The NLP Agent processes user queries and publishes structured messages to the `weather_requests` Redis channel.

- **Endpoint**: `/parse_query`
- **Method**: `POST`
- **Payload**: `{"query": "<your query>"}`

#### Example Usage

The NLP Agent listens for requests on `http://localhost:8001/parse_query`.

### 2. Weather Agent (`weather_agent.py`)

The Weather Agent listens for messages on the `weather_requests` channel, fetches weather data from OpenWeatherMap, and publishes the result to the `response` channel.

### 3. Response Agent (`response_agent.py`)

The Response Agent listens on the `response` channel for weather data, formats it into a user-friendly message, and prints it to the console.

## Running the System

Open three separate terminals, one for each agent, and run them in this order:

1. **Run the NLP Agent**:

   ```bash
   python nlp_agent.py
   ```

   This agent will start listening for natural language queries on port `8001`.

2. **Run the Weather Agent**:

   ```bash
   python weather_agent.py
   ```

   The Weather Agent listens to the `weather_requests` channel on Redis and fetches weather data for specified cities.

3. **Run the Response Agent**:
   ```bash
   python response_agent.py
   ```
   The Response Agent listens to the `response` channel and displays the formatted weather information.

### Testing the System

Once all agents are running, you can send a weather query via the NLP Agent using `curl`:

```bash
curl -X POST "http://127.0.0.1:8001/parse_query" -H "Content-Type: application/json" -d "{\"query\": \"What is the weather in London?\"}"
```

#### Expected Output

1. **NLP Agent** detects the intent and city, then publishes a message to `weather_requests`.
2. **Weather Agent** receives the message, retrieves the weather data, and publishes it to `response`.
3. **Response Agent** receives the weather data, formats it, and prints a response similar to:
   ```
   The current temperature in London is 18.5°C. Conditions: scattered clouds.
   ```

## Troubleshooting

- **Redis Connection Issues**: Ensure Redis is running. Check with `redis-cli ping` (should return `PONG`).
- **API Key Issues**: Verify your OpenWeatherMap API key. Without a valid key, the Weather Agent won't be able to fetch data.
- **Error Handling**: To debug, add `print` statements in each agent to confirm the flow and data handling.

## Advanced Enhancements

- **Error Handling**: Add error handling for failed API requests or missing data.
- **Multiple Channels**: Extend to handle other requests or agents by adding more Redis channels.
- **Scalability**: Consider using a task queue like Celery if the system needs to handle high loads.

## Project Structure

```
multi-agent-weather-system/
├── nlp_agent.py         # NLP Agent for query processing
├── weather_agent.py     # Weather Agent for fetching weather data
├── response_agent.py    # Response Agent for formatting responses
└── README.md            # Project documentation
```

## License

This project is licensed under the MIT License.
