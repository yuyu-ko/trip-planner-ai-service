import os
import json
from openai import OpenAI
from schemas import TripRequest, ItineraryResponse, DayPlan, Activity
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================
#  Main AI Itinerary Generator
# ============================
async def generate_itinerary(trip: TripRequest) -> ItineraryResponse:

    prompt = f"""
    You are an expert travel planning AI. Your task is to generate a strict JSON itinerary based on the user's request.

    User Request:
    - City: {trip.city}
    - Start Date: {trip.startDate}
    - End Date: {trip.endDate}
    - Budget: {trip.budgetLevel}
    - Preferences: {trip.preferences}

    Strict Rules for Generation:
    1. **Real Places**: Use REAL names of existing places as they appear on Google Maps.
    2. **Route Logic**: Group nearby attractions to minimize travel time. Do not jump across the city unnecessarily.
    3. **Daily Schedule**: Plan activities from morning (~9 AM) until evening (~8 PM).
    4. **Accommodation**: The last activity of each day MUST be the hotel/accommodation.
    5. **Dates**: You MUST calculate the correct "date" for each "dayNumber" starting from {trip.startDate}. Do NOT use the example date.
    6. **Transportation**: In the 'description' field, briefly mention how to get there from the previous location (e.g., "15 min walk", "20 min taxi"). Exception: The first activity of Day 1 does not need this.

    Output Format (JSON ONLY):
    {{
      "days": [
         {{
           "dayNumber": 1,
           "date": "YYYY-MM-DD",  <-- CALCULATE THIS BASED ON START DATE
           "activities": [
                {{
                  "time": "09:00",
                  "title": "Name of the Place",
                  "description": "Brief description of activity. (Transport: 10 mins by Metro)",
                  "location": "Google Map Address"
                }}
           ]
         }}
      ]
    }}

    IMPORTANT CONSTRAINTS:
    - Return ONLY valid JSON.
    - NO introductory text (like "Here is your itinerary...").
    - NO markdown formatting (like ```json ... ```).
    - Ensure the JSON can be parsed by Python's json.loads().
    """

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}, # 加上這行，保證 JSON 不會爛掉
        stream=True
    )

    full_text = ""

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            full_text += delta

    # full_text 現在是完整 JSON 字串
    data = json.loads(full_text)
    return ItineraryResponse(**data)
