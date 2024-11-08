from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import redis
import json

# Initialize FastAPI app and spaCy NLP model
app = FastAPI()
nlp = spacy.load("en_core_web_sm")

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0)


# Define the request model
class QueryRequest(BaseModel):
    query: str


@app.post("/parse_query")
async def parse_query(request: QueryRequest):
    query = request.query
    doc = nlp(query)
    intent = ""
    city = ""

    # Basic intent recognition (adjust based on actual needs)
    if "weather" in query.lower():
        intent = "get_weather"

    # Extract city name (improve with custom model for accuracy)
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geopolitical Entity (like cities)
            city = ent.text

    # Send parsed data to the Weather Agent via Redis
    if intent == "get_weather" and city:
        message = json.dumps({"intent": intent, "city": city})
        redis_client.publish("weather_requests", message)
        return {"status": "Weather request sent"}
    return {"status": "No action taken"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
