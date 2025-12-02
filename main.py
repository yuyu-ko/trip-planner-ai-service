from fastapi import FastAPI
from schemas import TripRequest, ItineraryResponse
from services.itinerary_generator import generate_itinerary

app = FastAPI(
    title="AI Trip Planner - AI Service",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"status": "alive", "message": "AI Service is running!"}

@app.post("/generate", response_model=ItineraryResponse)
async def generate(trip: TripRequest):
    itinerary = await generate_itinerary(trip)
    return itinerary

#start: uvicorn main:app --reload --port 8000